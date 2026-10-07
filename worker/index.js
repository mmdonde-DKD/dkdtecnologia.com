// worker/index.js — ponto de entrada do site dkdtecnologia.com em Cloudflare Workers.
//
// As 16 páginas e todos os arquivos de assets/ são servidos direto do
// diretório estático, sem passar por este código. O Worker só é chamado
// quando nenhum arquivo corresponde à URL — /api/contato, e desde a V10.1_web
// também /api/cadastro, /api/licenca/*, /api/admin/* e /admin (worker/licencas.js).
//
// Variáveis (Settings > Variables and Secrets, tipo Secret):
//   RESEND_API_KEY    chave do provedor de e-mail transacional
//   DESTINO           ex.: comercial@dkdtecnologia.com
//   REMETENTE         ex.: site@dkdtecnologia.com (domínio verificado no provedor)
//   TURNSTILE_SECRET  chave secreta do widget Turnstile
// Binding KV (wrangler.jsonc): LEADS — namespace "dkd-leads", um registro por contato.
// Resumo diário: cron do wrangler.jsonc chama scheduled() às 23h55 de Brasília e
// manda um e-mail com os contatos do dia + CSV. Sem RESEND_API_KEY os contatos
// ficam guardados no KV e saem no primeiro resumo depois que a chave existir.
// O visitante nunca vê erro de configuração.

import { rotearLicencas } from "./licencas.js";
import { paginaAdmin } from "./admin.js";

const CAMPOS = ["nome", "empresa", "email", "telefone", "assunto",
                "modulo", "cnpjs", "mensagem", "origem"];

async function confereTurnstile(env, token, ip) {
  if (!env.TURNSTILE_SECRET) return { ok: true, motivo: "sem-turnstile" };
  if (!token) return { ok: false, motivo: "sem-token" };
  try {
    const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ secret: env.TURNSTILE_SECRET, response: token, remoteip: ip }),
    });
    const j = await r.json();
    return { ok: j.success === true, motivo: (j["error-codes"] || []).join(",") };
  } catch (e) {
    // Falha de rede na verificação não pode custar um lead: deixa passar e marca.
    return { ok: true, motivo: "verificacao-indisponivel" };
  }
}

async function guardaLead(env, dados, meta) {
  if (!env.LEADS) return false;
  const id = `lead:${new Date().toISOString()}:${crypto.randomUUID().slice(0, 8)}`;
  try {
    await env.LEADS.put(id, JSON.stringify({ ...dados, ...meta }), {
      metadata: { modulo: dados.modulo || "", origem: dados.origem || "" },
    });
    return true;
  } catch (e) {
    return false;
  }
}

async function recebeContato(request, env) {
  const url = new URL(request.url);
  const volta = (q) =>
    Response.redirect(new URL((url.searchParams.get("de") || "/contato/") + q, url).toString(), 303);

  try {
    const form = await request.formData();

    // Armadilha para robô: campo invisível preenchido = descarta em silêncio.
    if (form.get("website")) return volta("?ok=1");

    const dados = {};
    for (const c of CAMPOS) dados[c] = (form.get(c) || "").toString().slice(0, 4000);

    if (!dados.nome || !dados.email || !dados.mensagem) return volta("?erro=campos");

    const ip = request.headers.get("CF-Connecting-IP") || "";
    const t = await confereTurnstile(env, form.get("cf-turnstile-response"), ip);
    if (!t.ok) return volta("?erro=robo");

    const meta = {
      recebido_em: new Date().toISOString(),
      pais: request.headers.get("CF-IPCountry") || "",
      referrer: (form.get("referrer") || "").toString().slice(0, 500),
      turnstile: t.motivo || "ok",
    };

    const guardado = await guardaLead(env, dados, meta);

    const corpo = [
      ...CAMPOS.map((c) => `${c.toUpperCase()}: ${dados[c]}`),
      "",
      `PAÍS: ${meta.pais}`,
      `ORIGEM DO CLIQUE: ${meta.referrer}`,
      `REGISTRADO NO KV: ${guardado ? "sim" : "não"}`,
    ].join("\n");

    // Guardado no KV = recebido. O e-mail sai no resumo diário (scheduled, abaixo).
    if (guardado) return volta("?ok=1");

    // Só se o KV falhar: tenta mandar este contato na hora, para não perdê-lo.
    const enviado = await enviaEmail(env, {
      subject: `Site DKD — ${dados.origem || "contato"} — ${dados.nome}${dados.empresa ? " (" + dados.empresa + ")" : ""}`,
      text: corpo,
      reply_to: dados.email,
    });
    return volta(enviado ? "?ok=1" : "?erro=envio");
  } catch (e) {
    return volta("?erro=inesperado");
  }
}

// ------------------------------------------------------------ e-mail (Resend)
const DESTINO_PADRAO = "comercial@dkdtecnologia.com";

async function enviaEmail(env, { subject, text, reply_to, attachments }) {
  if (!env.RESEND_API_KEY || !env.REMETENTE) return false;
  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        from: env.REMETENTE,
        to: [env.DESTINO || DESTINO_PADRAO],
        subject, text,
        ...(reply_to ? { reply_to } : {}),
        ...(attachments ? { attachments } : {}),
      }),
    });
    return r.ok;
  } catch (e) {
    return false;
  }
}

// ------------------------------------------------------- resumo diário de leads
// Disparado pelo cron do wrangler.jsonc (23h55 de Brasília). Manda num e-mail só
// todos os contatos gravados desde o último resumo enviado, com um CSV anexo.
// Se o envio falhar, o marcador não avança: os contatos entram no resumo seguinte.
const MARCA_RESUMO = "meta:ultimo_resumo";
const quando = (iso) =>
  new Date(iso).toLocaleString("pt-BR", { timeZone: "America/Sao_Paulo" });
const csvCampo = (v) => '"' + String(v ?? "").replace(/"/g, '""') + '"';
const utf8b64 = (txt) => {
  const b = new TextEncoder().encode(txt);
  let bin = "";
  for (let i = 0; i < b.length; i += 0x8000) bin += String.fromCharCode(...b.subarray(i, i + 0x8000));
  return btoa(bin);
};

async function resumoDiario(env) {
  if (!env.LEADS) return "sem-kv";
  const desde = (await env.LEADS.get(MARCA_RESUMO)) || "lead:";
  const chaves = [];
  let cursor;
  do {
    const l = await env.LEADS.list({ prefix: "lead:", cursor });
    for (const k of l.keys) if (k.name > desde) chaves.push(k.name);
    cursor = l.list_complete ? undefined : l.cursor;
  } while (cursor);
  if (!chaves.length) return "nenhum-lead";
  chaves.sort();

  const leads = [];
  for (const k of chaves) {
    const v = await env.LEADS.get(k, "json");
    if (v) leads.push(v);
  }

  const hoje = new Date().toLocaleDateString("pt-BR", { timeZone: "America/Sao_Paulo" });
  const blocos = leads.map((d, i) => [
    `#${i + 1} — ${quando(d.recebido_em)} — página: ${d.origem || "-"}`,
    `Nome: ${d.nome}`,
    `Empresa: ${d.empresa || "-"}`,
    `E-mail: ${d.email}`,
    `Telefone/WhatsApp: ${d.telefone || "-"}`,
    `Interesse: ${d.modulo || "-"}${d.cnpjs ? " · CNPJs: " + d.cnpjs : ""}`,
    `Mensagem: ${d.mensagem}`,
  ].join("\n"));
  const texto = [
    `${leads.length} contato(s) registrado(s) no site dkdtecnologia.com desde o último resumo.`,
    "",
    ...blocos.flatMap((b) => [b, ""]),
    "Planilha com todos os campos em anexo (abre no Excel).",
  ].join("\n");

  const colunas = ["recebido_em", ...CAMPOS, "pais", "referrer"];
  const csv = "\uFEFF" + [colunas.join(";"),
    ...leads.map((d) => colunas.map((c) => csvCampo(c === "recebido_em" ? quando(d[c]) : d[c])).join(";"))].join("\r\n");

  const ok = await enviaEmail(env, {
    subject: `Site DKD — ${leads.length} contato(s) em ${hoje}`,
    text: texto,
    attachments: [{ filename: `contatos-site-dkd-${hoje.replace(/\//g, "-")}.csv`, content: utf8b64(csv) }],
  });
  if (ok) await env.LEADS.put(MARCA_RESUMO, chaves[chaves.length - 1]);
  return ok ? `enviado:${leads.length}` : "falha-envio";
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/api/contato") {
      if (request.method === "POST") return recebeContato(request, env);
      return new Response("Método não permitido.", {
        status: 405,
        headers: { Allow: "POST", "Content-Type": "text/plain; charset=utf-8" },
      });
    }

    // V10.1_web — cadastro, licenças (/api/cadastro, /api/licenca/*) e o painel (/admin).
    // Sem o banco LICENCAS configurado, essas rotas respondem 503 e o resto do site segue no ar.
    const lic = await rotearLicencas(request, env, url, paginaAdmin);
    if (lic) return lic;

    // Qualquer outra coisa que não bateu com um arquivo estático volta para a
    // camada de assets, que aplica o tratamento de 404 configurado.
    return env.ASSETS.fetch(request);
  },

  async scheduled(controller, env, ctx) {
    ctx.waitUntil(resumoDiario(env).then((r) => console.log("resumo diário de leads:", r)));
  },
};
