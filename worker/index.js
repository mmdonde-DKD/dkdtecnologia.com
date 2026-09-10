// worker/index.js — ponto de entrada do site dkdtecnologia.com em Cloudflare Workers.
//
// As 15 páginas e todos os arquivos de assets/ são servidos direto do
// diretório estático, sem passar por este código. O Worker só é chamado
// quando nenhum arquivo corresponde à URL — na prática, só em /api/contato.
//
// Variáveis (Settings > Variables and Secrets, tipo Secret):
//   RESEND_API_KEY    chave do provedor de e-mail transacional
//   DESTINO           ex.: contato@dkdtecnologia.com
//   REMETENTE         ex.: site@dkdtecnologia.com (domínio verificado no provedor)
//   TURNSTILE_SECRET  chave secreta do widget Turnstile
// Binding opcional (Settings > Bindings > KV namespace):
//   LEADS             guarda um registro por lead, para contar e exportar
//
// Tudo o que é opcional degrada em silêncio: sem chave de Turnstile ele não
// confere; sem KV ele não guarda; sem chave de e-mail ele avisa que falhou.
// O visitante nunca vê erro de configuração.

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

    if (!env.RESEND_API_KEY || !env.DESTINO || !env.REMETENTE) {
      // Sem e-mail configurado o lead não pode se perder: se foi para o KV,
      // vale como recebido; se não foi, o visitante precisa saber.
      return volta(guardado ? "?ok=1" : "?erro=envio");
    }

    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${env.RESEND_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: env.REMETENTE,
        to: [env.DESTINO],
        reply_to: dados.email,
        subject: `Site DKD — ${dados.origem || "contato"} — ${dados.nome}${dados.empresa ? " (" + dados.empresa + ")" : ""}`,
        text: corpo,
      }),
    });

    if (!r.ok && !guardado) return volta("?erro=envio");
    return volta("?ok=1");
  } catch (e) {
    return volta("?erro=inesperado");
  }
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

    // Qualquer outra coisa que não bateu com um arquivo estático volta para a
    // camada de assets, que aplica o tratamento de 404 configurado.
    return env.ASSETS.fetch(request);
  },
};
