// worker/licencas.js — servidor de licenças do DKD Financial Tools AI (V10.1_web)
//
// O caminho do cliente:
//   1. cadastro em dkdtecnologia.com/cadastro  → POST /api/cadastro
//      cria o cliente com 30 dias de avaliação (contados da 1ª ativação) e
//      manda o e-mail de boas-vindas com o link de download;
//   2. o portal pede o código                  → POST /api/licenca/codigo
//      o servidor confere o cadastro e o limite de computadores, e manda um
//      código de 6 dígitos ao e-mail CADASTRADO (nunca a outro);
//   3. o portal manda o código                 → POST /api/licenca/ativar
//      o servidor confere e devolve a licença ASSINADA (ECDSA P-256), presa
//      àquele computador. O portal a confere sozinho, sem rede, a cada abertura;
//   4. a cada abertura com internet            → POST /api/licenca/renovar
//      o portal busca a versão atual da licença: pagamento registrado no
//      painel estende a validade; suspensão também chega por aqui.
//
// Painel da DKD: /admin (página) e /api/admin/* (Authorization: Bearer ADMIN_TOKEN).
//
// Variáveis (Settings > Variables and Secrets):
//   LICENCA_CHAVE_PRIVADA  Secret · JWK da chave ECDSA P-256 (gerada no DKD_Chaves_Licenca.html)
//   ADMIN_TOKEN            Secret · senha longa do painel /admin
//   RESEND_API_KEY         Secret · envio de e-mail pelo Resend (o mesmo do formulário de contato)
//   REMETENTE_LICENCAS     ex.: "DKD Tecnologia e Inovação <comercial@dkdtecnologia.com>" (senão usa REMETENTE)
//   TURNSTILE_SECRET       Secret · anti-robô do formulário de cadastro
//   DOWNLOAD_URL           opcional · link do download que vai no e-mail de boas-vindas
//   AVALIACAO_DIAS         opcional · padrão 30
//   LIMITE_DISPOSITIVOS    opcional · padrão 2
// Bindings:
//   LICENCAS               D1 · banco dkd-licencas (worker/schema.sql)
//   EMAIL                  opcional · Cloudflare Email Sending — se existir, tem preferência sobre o Resend
//
// Sem LICENCAS configurado, as rotas de licença respondem 503 e o resto do site
// continua no ar — publicar este arquivo antes de criar o banco não derruba nada.

const ENC = new TextEncoder();
const DEC = new TextDecoder();
const SITE = "https://dkdtecnologia.com";
// endereço fixo: a cada versão nova o zip é trocado no site e os links dos e-mails
// antigos continuam levando à versão mais recente
const DOWNLOAD_PADRAO = SITE + "/downloads/DKD_Financial_Tools_AI_Gestao_Financeira.zip";
const CODIGO_MIN = 15;          // validade do código, em minutos
const CODIGO_TENTATIVAS = 5;

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Max-Age": "86400",
};

// ------------------------------------------------------------------ utilidades
const agoraISO = () => new Date().toISOString();
const antesISO = (min) => new Date(Date.now() - min * 60000).toISOString();
const depoisISO = (min) => new Date(Date.now() + min * 60000).toISOString();
// Brasil sem horário de verão desde 2019: UTC-3 o ano inteiro
const hojeBR = () => new Date(Date.now() - 3 * 3600000).toISOString().slice(0, 10);
function somarDias(iso, n) {
  const d = new Date(iso + "T12:00:00Z");
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
}
const soDigitos = (s) => String(s || "").replace(/\D/g, "");
// CNPJ: numérico ou alfanumérico (a Receita emite CNPJ com letras desde 31/07/2026)
const soCNPJ = (s) => String(s || "").toUpperCase().replace(/[^0-9A-Z]/g, "");
const normEmail = (e) => String(e || "").trim().toLowerCase();
const emailValido = (e) => /^[^\s@]{1,64}@[^\s@]{1,190}\.[^\s@]{2,}$/.test(e) && e.length <= 160;
const limpaTexto = (s, n) => String(s || "").replace(/[\u0000-\u001f<>]/g, " ").replace(/\s+/g, " ").trim().slice(0, n || 120);
const limpaDisp = (s) => String(s || "").toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 24);

function b64url(bytes) {
  const b = bytes instanceof Uint8Array ? bytes : new Uint8Array(bytes);
  let s = "";
  for (let i = 0; i < b.length; i++) s += String.fromCharCode(b[i]);
  return btoa(s).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}
function ub64url(s) {
  s = String(s).replace(/-/g, "+").replace(/_/g, "/");
  while (s.length % 4) s += "=";
  const bin = atob(s);
  const u = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i);
  return u;
}
async function sha256(texto) {
  return new Uint8Array(await crypto.subtle.digest("SHA-256", ENC.encode(texto)));
}
const hex = (u) => Array.from(u).map((b) => b.toString(16).padStart(2, "0")).join("");
async function iguaisSeguro(a, b) {
  const [x, y] = await Promise.all([sha256(String(a)), sha256(String(b))]);
  let d = 0;
  for (let i = 0; i < x.length; i++) d |= x[i] ^ y[i];
  return d === 0;
}

function json(obj, status, extra) {
  return new Response(JSON.stringify(obj), {
    status: status || 200,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", ...(extra || {}) },
  });
}
async function lerJson(request) {
  try {
    const t = await request.text();
    if (t.length > 20000) return {};
    return JSON.parse(t || "{}") || {};
  } catch (e) {
    return {};
  }
}

// ------------------------------------------------------------ CPF e CNPJ
function cpfValido(c) {
  c = soDigitos(c);
  if (c.length !== 11 || /^(\d)\1{10}$/.test(c)) return false;
  for (const t of [9, 10]) {
    let s = 0;
    for (let i = 0; i < t; i++) s += +c[i] * (t + 1 - i);
    const d = ((s * 10) % 11) % 10;
    if (d !== +c[t]) return false;
  }
  return true;
}
// Vale para o CNPJ numérico e para o alfanumérico (IN RFB 2.229/2024): cada
// caractere entra pelo código ASCII menos 48 — dígito continua valendo ele mesmo,
// "A" vale 17 — com os mesmos pesos e o mesmo módulo 11. Os dois dígitos
// verificadores são sempre numéricos.
function cnpjValido(c) {
  c = soCNPJ(c);
  if (!/^[0-9A-Z]{12}\d{2}$/.test(c) || /^(.)\1{13}$/.test(c)) return false;
  const v = (i) => c.charCodeAt(i) - 48;
  const calc = (n) => {
    const pesos = n === 12 ? [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2] : [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];
    const s = pesos.reduce((a, p, i) => a + v(i) * p, 0);
    const r = s % 11;
    return r < 2 ? 0 : 11 - r;
  };
  return calc(12) === +c[12] && calc(13) === +c[13];
}
const fmtCNPJ = (c) => c.replace(/^([0-9A-Z]{2})([0-9A-Z]{3})([0-9A-Z]{3})([0-9A-Z]{4})(\d{2})$/, "$1.$2.$3/$4-$5");
const mascCPF = (c) => "***." + c.slice(3, 6) + "." + c.slice(6, 9) + "-**";
function docVisivel(cli) {
  const d = soCNPJ(cli.documento);
  if (d.length === 14) return fmtCNPJ(d);
  if (/^\d{11}$/.test(d)) return mascCPF(d);
  return "";
}
function mascaraEmail(e) {
  const [u, dom] = String(e).split("@");
  if (!dom) return "";
  return (u.length <= 2 ? u[0] + "*" : u[0] + "***" + u.slice(-1)) + "@" + dom;
}

// ------------------------------------------------------------- assinatura
let _priv = null, _pub = null, _jwkLido = "";
async function chaves(env) {
  const bruto = env.LICENCA_CHAVE_PRIVADA || "";
  if (!bruto) throw new Error("sem_chave");
  if (_priv && _jwkLido === bruto) return { priv: _priv, pub: _pub };
  // aceita o JWK como foi colado no painel, inclusive com as aspas escapadas
  let jwk;
  try { jwk = JSON.parse(bruto); }
  catch (e) { jwk = JSON.parse(String(bruto).replace(/\\"/g, '"').replace(/^"|"$/g, "")); }
  if (typeof jwk === "string") jwk = JSON.parse(jwk);
  _priv = await crypto.subtle.importKey("jwk", { kty: "EC", crv: "P-256", x: jwk.x, y: jwk.y, d: jwk.d },
    { name: "ECDSA", namedCurve: "P-256" }, false, ["sign"]);
  _pub = await crypto.subtle.importKey("jwk", { kty: "EC", crv: "P-256", x: jwk.x, y: jwk.y },
    { name: "ECDSA", namedCurve: "P-256" }, true, ["verify"]);
  _jwkLido = bruto;
  return { priv: _priv, pub: _pub };
}
async function assinar(env, payload) {
  const { priv } = await chaves(env);
  const corpo = ENC.encode(JSON.stringify(payload));
  const sig = new Uint8Array(await crypto.subtle.sign({ name: "ECDSA", hash: "SHA-256" }, priv, corpo));
  return "DKD1." + b64url(corpo) + "." + b64url(sig);
}
async function lerLicenca(env, texto) {
  const p = String(texto || "").trim().split(".");
  if (p.length !== 3 || p[0] !== "DKD1") return null;
  const { pub } = await chaves(env);
  let ok = false, corpo;
  try {
    corpo = ub64url(p[1]);
    ok = await crypto.subtle.verify({ name: "ECDSA", hash: "SHA-256" }, pub, ub64url(p[2]), corpo);
  } catch (e) {
    ok = false;
  }
  if (!ok) return null;
  try {
    return JSON.parse(DEC.decode(corpo));
  } catch (e) {
    return null;
  }
}
async function chavePublicaSPKI(env) {
  const { pub } = await chaves(env);
  const spki = new Uint8Array(await crypto.subtle.exportKey("spki", pub));
  let s = "";
  for (let i = 0; i < spki.length; i++) s += String.fromCharCode(spki[i]);
  const b64 = btoa(s);
  const dig = await crypto.subtle.digest("SHA-256", spki);
  let d = "";
  const u = new Uint8Array(dig);
  for (let i = 0; i < u.length; i++) d += String.fromCharCode(u[i]);
  return { spki: b64, digital: btoa(d).slice(0, 12) };
}

async function emitir(env, cli, dispositivo) {
  const pj = cli.tipo === "PJ";
  const payload = {
    v: 2,
    modulo: "gestao-financeira",
    serie: cli.serie,
    cliente: pj && cli.empresa ? cli.empresa : cli.nome,
    doc: docVisivel(cli),
    email_h: b64url(await sha256(cli.email)),
    email_m: mascaraEmail(cli.email),
    plano: cli.plano,
    emitido_em: hojeBR(),
    expira_em: cli.validade || hojeBR(),
    dispositivo: dispositivo,
    dispositivos: cli.limite_dispositivos,
    emissor: "web",
  };
  return assinar(env, payload);
}

// ------------------------------------------------------------------ banco
const um = (env, sql, ...a) => env.LICENCAS.prepare(sql).bind(...a).first();
const todos = async (env, sql, ...a) => (await env.LICENCAS.prepare(sql).bind(...a).all()).results || [];
const roda = (env, sql, ...a) => env.LICENCAS.prepare(sql).bind(...a).run();
async function evento(env, cliente_id, tipo, detalhe, ip) {
  try {
    await roda(env, "INSERT INTO eventos (cliente_id, tipo, detalhe, ip, criado_em) VALUES (?,?,?,?,?)",
      cliente_id || null, tipo, limpaTexto(detalhe, 300), ip || "", agoraISO());
  } catch (e) { /* o registro nunca derruba a operação */ }
}
const ipDe = (request) => request.headers.get("CF-Connecting-IP") || "";

// ------------------------------------------------------------------ e-mail
async function enviarEmail(env, { para, assunto, texto, html }) {
  const remetente = env.REMETENTE_LICENCAS || env.REMETENTE || "DKD Tecnologia e Inovação <comercial@dkdtecnologia.com>";
  if (env.MODO_TESTE === "1") {
    await roda(env, "INSERT INTO emails_teste (para, assunto, texto, criado_em) VALUES (?,?,?,?)",
      para, assunto, texto, agoraISO());
    return { ok: true, via: "teste" };
  }
  try {
    if (env.EMAIL && typeof env.EMAIL.send === "function") {
      const m = /^(.*)<([^>]+)>\s*$/.exec(remetente);
      await env.EMAIL.send({
        from: m ? { email: m[2].trim(), name: m[1].trim() } : { email: remetente },
        to: { email: para }, subject: assunto, html, text: texto,
        replyTo: env.DESTINO || "comercial@dkdtecnologia.com",
      });
      return { ok: true, via: "cloudflare" };
    }
    if (env.RESEND_API_KEY) {
      const r = await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
        body: JSON.stringify({ from: remetente, to: [para], subject: assunto, text: texto, html,
          reply_to: env.DESTINO || "comercial@dkdtecnologia.com" }),
      });
      return { ok: r.ok, via: "resend", status: r.status };
    }
  } catch (e) {
    return { ok: false, via: "erro", erro: String(e && e.message || e) };
  }
  return { ok: false, via: "nenhum" };
}

const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

function moldura(titulo, corpoHtml) {
  return `<!doctype html><html lang="pt-BR"><body style="margin:0;background:#eef2f6;font-family:Segoe UI,Arial,sans-serif;color:#0f172a">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#eef2f6;padding:24px 0"><tr><td align="center">
<table role="presentation" width="560" cellpadding="0" cellspacing="0" style="max-width:560px;width:100%;background:#ffffff;border-radius:12px;overflow:hidden">
<tr><td style="background:#060e1b;padding:22px 28px;color:#e8eef5">
  <div style="font-size:18px;letter-spacing:.3px;color:#c9d1d8">DKD <b style="color:#f2f5f7">Financial Tools AI</b></div>
  <div style="font-size:11px;color:#7a8ca3;letter-spacing:.12em;text-transform:uppercase;margin-top:4px">${esc(titulo)}</div>
</td></tr>
<tr><td style="padding:26px 28px;font-size:15px;line-height:1.6">${corpoHtml}</td></tr>
<tr><td style="padding:16px 28px 22px;font-size:12px;line-height:1.5;color:#64748b;border-top:1px solid #e2e8f0">
  DKD Tecnologia e Inovação · CNPJ 59.890.881/0001-06 · Caxias do Sul/RS<br>
  comercial@dkdtecnologia.com · <a href="${SITE}" style="color:#1d6fb8">dkdtecnologia.com</a><br>
  Você recebe este e-mail porque se cadastrou no site da DKD. Dados tratados conforme a
  <a href="${SITE}/legal/privacidade/" style="color:#1d6fb8">Política de Privacidade</a>.
</td></tr></table></td></tr></table></body></html>`;
}

function emailBoasVindas(env, cli) {
  const link = env.DOWNLOAD_URL || DOWNLOAD_PADRAO;
  const dias = +(env.AVALIACAO_DIAS || 30);
  const nome = esc(String(cli.nome || "").split(" ")[0]);
  const html = moldura("Cadastro confirmado", `
  <p style="margin:0 0 14px">Olá, ${nome}!</p>
  <p style="margin:0 0 14px">Seu cadastro no <b>DKD Financial Tools AI — Módulo de Planejamento, Controle e
  Gestão Financeira</b> está feito. São <b>${dias} dias completos</b> para testar, contados a partir da ativação.</p>
  <p style="margin:22px 0"><a href="${link}" style="background:#3fa9f0;color:#03101e;text-decoration:none;font-weight:700;padding:12px 22px;border-radius:8px;display:inline-block">Baixar o portal</a></p>
  <ol style="padding-left:20px;margin:0 0 14px">
    <li>Descompacte o arquivo baixado e abra o portal — o arquivo <b>.html</b> que começa com <b>DKD_Financial_Tools_AI</b> — no Chrome ou no Edge.</li>
    <li>Na tela de ativação, informe este e-mail: <b>${esc(cli.email)}</b>.</li>
    <li>Digite o código de 6 números que vamos mandar para cá. Pronto.</li>
  </ol>
  <p style="margin:0 0 14px;color:#475569;font-size:14px">O portal roda no seu computador: os extratos e os dados
  financeiros não passam pelos servidores da DKD. A internet só é usada para ativar e renovar a licença
  e para buscar a taxa CDI pública no Banco Central.</p>
  <p style="margin:0">Série da sua licença: <b style="font-family:Consolas,monospace">${esc(cli.serie)}</b></p>`);
  const texto = `Olá, ${String(cli.nome || "").split(" ")[0]}!

Seu cadastro no DKD Financial Tools AI — Módulo de Planejamento, Controle e Gestão Financeira está feito.
São ${dias} dias completos para testar, contados a partir da ativação.

Baixe o portal: ${link}

1. Descompacte o arquivo baixado e abra o portal (o arquivo .html que começa com DKD_Financial_Tools_AI) no Chrome ou no Edge.
2. Na tela de ativação, informe este e-mail: ${cli.email}
3. Digite o código de 6 números que vamos mandar para cá.

O portal roda no seu computador: os extratos e os dados financeiros não passam pelos servidores da DKD.
A internet só é usada para ativar e renovar a licença e para buscar a taxa CDI pública no Banco Central.

Série da sua licença: ${cli.serie}

DKD Tecnologia e Inovação · comercial@dkdtecnologia.com · ${SITE}`;
  return { assunto: `Seu acesso ao DKD Financial Tools AI — ${dias} dias grátis`, html, texto };
}

function emailCodigo(cli, codigo, rotulo) {
  const c = codigo.slice(0, 3) + " " + codigo.slice(3);
  const html = moldura("Código de ativação", `
  <p style="margin:0 0 14px">Use este código para ativar o portal${rotulo ? " em <b>" + esc(rotulo) + "</b>" : ""}:</p>
  <p style="margin:18px 0;font-family:Consolas,monospace;font-size:34px;letter-spacing:.18em;font-weight:700;color:#060e1b">${c}</p>
  <p style="margin:0 0 14px;color:#475569;font-size:14px">O código vale por ${CODIGO_MIN} minutos e só funciona no computador
  que o pediu. Se não foi você, ignore este e-mail — nada é ativado sem o código.</p>`);
  const texto = `Seu código de ativação do DKD Financial Tools AI: ${c}

Vale por ${CODIGO_MIN} minutos e só funciona no computador que o pediu${rotulo ? " (" + rotulo + ")" : ""}.
Se não foi você, ignore este e-mail — nada é ativado sem o código.

DKD Tecnologia e Inovação · ${SITE}`;
  return { assunto: `Código de ativação: ${c}`, html, texto };
}

function emailChave(cli, chave, validade) {
  const html = moldura("Chave de licença", `
  <p style="margin:0 0 14px">Segue a chave de licença do seu portal, válida até <b>${validade.split("-").reverse().join("/")}</b>.</p>
  <p style="margin:0 0 8px">Abra o portal, vá em <b>Cadastro ▸ Licença e operador</b> e cole a chave no campo
  <b>Chave recebida da DKD</b>:</p>
  <p style="margin:12px 0;padding:12px;background:#f1f5f9;border-radius:8px;font-family:Consolas,monospace;font-size:12px;word-break:break-all">${esc(chave)}</p>`);
  const texto = `Chave de licença do DKD Financial Tools AI, válida até ${validade.split("-").reverse().join("/")}.

Abra o portal, vá em Cadastro > Licença e operador e cole a chave no campo "Chave recebida da DKD":

${chave}

DKD Tecnologia e Inovação · ${SITE}`;
  return { assunto: "Sua chave de licença — DKD Financial Tools AI", html, texto };
}

// ---------------------------------------------------------------- Turnstile
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
    // o cadastro dispara um e-mail para um endereço qualquer: sem conferência, não passa
    return { ok: false, motivo: "verificacao-indisponivel" };
  }
}

// ================================================================ cadastro
async function cadastro(request, env, url) {
  const volta = (q) => Response.redirect(new URL("/cadastro/" + q, url).toString(), 303);
  if (request.method !== "POST") return new Response("Método não permitido.", { status: 405, headers: { Allow: "POST" } });
  if (!env.LICENCAS) return volta("?erro=indisponivel");
  let form;
  try { form = await request.formData(); } catch (e) { return volta("?erro=campos"); }
  if (form.get("website")) return volta("?ok=1");                 // armadilha para robô

  const ip = ipDe(request);
  const d = {
    nome: limpaTexto(form.get("nome"), 120),
    empresa: limpaTexto(form.get("empresa"), 160),
    tipo: form.get("tipo") === "PJ" ? "PJ" : "PF",
    documento: form.get("tipo") === "PJ" ? soCNPJ(form.get("documento")).slice(0, 14)
                                         : soDigitos(form.get("documento")).slice(0, 11),
    email: normEmail(form.get("email")),
    telefone: soDigitos(form.get("telefone")).slice(0, 13),
    cidade: limpaTexto(form.get("cidade"), 80),
    uf: limpaTexto(form.get("uf"), 2).toUpperCase(),
    origem: limpaTexto(form.get("origem") || "site", 40),
  };
  if (d.nome.length < 3 || !d.email) return volta("?erro=campos");
  if (!emailValido(d.email)) return volta("?erro=email");
  if (d.tipo === "PJ" ? !cnpjValido(d.documento) : !cpfValido(d.documento)) return volta("?erro=documento");
  if (d.tipo === "PJ" && d.empresa.length < 3) return volta("?erro=campos");
  if (!form.get("aceite")) return volta("?erro=aceite");

  const n = await um(env, "SELECT COUNT(*) AS n FROM eventos WHERE ip = ? AND tipo = 'cadastro' AND criado_em > ?",
    ip, antesISO(60));
  if (ip && n && n.n >= 5) return volta("?erro=limite");

  const t = await confereTurnstile(env, form.get("cf-turnstile-response"), ip);
  if (!t.ok) return volta("?erro=robo");

  const ja = await um(env, "SELECT * FROM clientes WHERE email = ?", d.email);
  if (ja) {
    // não revela o cadastro de ninguém e não deixa sobrescrever os dados de outra pessoa:
    // só manda de novo o e-mail de boas-vindas, no máximo uma vez a cada 10 minutos
    const rec = await um(env, "SELECT COUNT(*) AS n FROM eventos WHERE cliente_id = ? AND tipo = 'email' AND detalhe LIKE 'boas-vindas%' AND criado_em > ?",
      ja.id, antesISO(10));
    if (!rec || !rec.n) {
      const m = emailBoasVindas(env, ja);
      const r = await enviarEmail(env, { para: ja.email, ...m });
      await evento(env, ja.id, "email", "boas-vindas (cadastro repetido) · " + r.via + (r.ok ? "" : " · FALHOU"), ip);
    }
    await evento(env, ja.id, "cadastro", "cadastro repetido", ip);
    return volta("?ok=1");
  }

  const agora = agoraISO();
  const limite = +(env.LIMITE_DISPOSITIVOS || 2);
  const ins = await roda(env,
    `INSERT INTO clientes (email, nome, empresa, tipo, documento, telefone, cidade, uf, origem,
       plano, status, validade, limite_dispositivos, aceite_em, ip_cadastro, criado_em, atualizado_em)
     VALUES (?,?,?,?,?,?,?,?,?, 'avaliacao','ativo', NULL, ?, ?, ?, ?, ?)`,
    d.email, d.nome, d.empresa || null, d.tipo, d.documento, d.telefone || null, d.cidade || null, d.uf || null,
    d.origem, limite, agora, ip, agora, agora);
  const id = ins.meta && ins.meta.last_row_id;
  const serie = "DKD-GF-" + hojeBR().slice(0, 4) + "-" + String(id).padStart(4, "0");
  await roda(env, "UPDATE clientes SET serie = ? WHERE id = ?", serie, id);
  await evento(env, id, "cadastro", (d.tipo === "PJ" ? "PJ " : "PF ") + (d.cidade || "") + (d.uf ? "/" + d.uf : "") + " · turnstile " + t.motivo, ip);

  const cli = await um(env, "SELECT * FROM clientes WHERE id = ?", id);
  const m = emailBoasVindas(env, cli);
  const r = await enviarEmail(env, { para: cli.email, ...m });
  await evento(env, id, "email", "boas-vindas · " + r.via + (r.ok ? "" : " · FALHOU"), ip);

  // avisa a DKD de cada cadastro novo, pelo mesmo canal do formulário de contato
  if (env.DESTINO && env.MODO_TESTE !== "1") {
    await enviarEmail(env, {
      para: env.DESTINO,
      assunto: `Novo cadastro — Gestão Financeira — ${cli.empresa || cli.nome}`,
      texto: `Série: ${serie}\nNome: ${cli.nome}\nEmpresa: ${cli.empresa || "—"}\nTipo: ${cli.tipo}\nDocumento: ${docVisivel(cli)}\nE-mail: ${cli.email}\nTelefone: ${cli.telefone || "—"}\nCidade: ${cli.cidade || "—"}/${cli.uf || "—"}\nOrigem: ${cli.origem}`,
      html: moldura("Novo cadastro", `<p>Série <b>${esc(serie)}</b> — ${esc(cli.empresa || cli.nome)} (${esc(cli.tipo)})<br>${esc(cli.email)} · ${esc(cli.cidade || "")}${cli.uf ? "/" + esc(cli.uf) : ""}</p>`),
    });
  }
  return volta("?ok=1");
}

// ============================================================ código e ativação
async function buscaCliente(env, email) {
  return um(env, "SELECT * FROM clientes WHERE email = ?", email);
}
function recusaStatus(cli) {
  if (cli.status === "suspenso") return json({ ok: false, erro: "suspenso" }, 403, CORS);
  if (cli.status === "cancelado") return json({ ok: false, erro: "cancelado" }, 403, CORS);
  return null;
}
async function confereVaga(env, cli, dispositivo) {
  const conhecido = await um(env, "SELECT * FROM dispositivos WHERE cliente_id = ? AND dispositivo = ?", cli.id, dispositivo);
  if (conhecido && conhecido.ativo) return { ok: true, conhecido };
  const n = await um(env, "SELECT COUNT(*) AS n FROM dispositivos WHERE cliente_id = ? AND ativo = 1", cli.id);
  const ativos = (n && n.n) || 0;
  if (ativos >= cli.limite_dispositivos) return { ok: false, ativos };
  return { ok: true, conhecido };
}
function gerarCodigo() {
  const u = new Uint32Array(1);
  do { crypto.getRandomValues(u); } while (u[0] >= 4294000000);   // sem viés
  return String(u[0] % 1000000).padStart(6, "0");
}
const hashCodigo = async (env, cliId, disp, codigo) =>
  hex(await sha256(`${cliId}:${disp}:${codigo}:${env.CODIGO_SAL || "dkd-v10"}`));

async function pedirCodigo(env, corpo, ip) {
  const email = normEmail(corpo.email);
  const disp = limpaDisp(corpo.dispositivo);
  const rotulo = limpaTexto(corpo.rotulo, 60);
  if (!emailValido(email)) return json({ ok: false, erro: "email_invalido" }, 400, CORS);
  if (disp.length < 8) return json({ ok: false, erro: "dispositivo_invalido" }, 400, CORS);

  const porIp = await um(env, "SELECT COUNT(*) AS n FROM codigos WHERE ip = ? AND criado_em > ?", ip, antesISO(60));
  if (ip && porIp && porIp.n >= 20) return json({ ok: false, erro: "muitas_tentativas" }, 429, CORS);

  const cli = await buscaCliente(env, email);
  if (!cli) {
    await evento(env, null, "recusa", "código pedido para e-mail não cadastrado", ip);
    return json({ ok: false, erro: "nao_cadastrado" }, 404, CORS);
  }
  const st = recusaStatus(cli);
  if (st) { await evento(env, cli.id, "recusa", "código pedido com licença " + cli.status, ip); return st; }

  const vaga = await confereVaga(env, cli, disp);
  if (!vaga.ok) {
    await evento(env, cli.id, "recusa", "limite de computadores (" + vaga.ativos + "/" + cli.limite_dispositivos + ") · " + rotulo, ip);
    return json({ ok: false, erro: "limite_dispositivos", limite: cli.limite_dispositivos, ativos: vaga.ativos }, 403, CORS);
  }

  const hora = await um(env, "SELECT COUNT(*) AS n FROM codigos WHERE cliente_id = ? AND criado_em > ?", cli.id, antesISO(60));
  if (hora && hora.n >= 5) return json({ ok: false, erro: "muitas_tentativas" }, 429, CORS);

  const codigo = gerarCodigo();
  await roda(env, "UPDATE codigos SET usado = 1 WHERE cliente_id = ? AND dispositivo = ? AND usado = 0", cli.id, disp);
  await roda(env, "INSERT INTO codigos (cliente_id, dispositivo, codigo_hash, expira_em, ip, criado_em) VALUES (?,?,?,?,?,?)",
    cli.id, disp, await hashCodigo(env, cli.id, disp, codigo), depoisISO(CODIGO_MIN), ip, agoraISO());

  const m = emailCodigo(cli, codigo, rotulo);
  const r = await enviarEmail(env, { para: cli.email, ...m });
  await evento(env, cli.id, "codigo", rotulo + " · " + r.via + (r.ok ? "" : " · FALHOU"), ip);
  if (!r.ok) return json({ ok: false, erro: "envio_falhou" }, 502, CORS);
  return json({ ok: true, para: mascaraEmail(cli.email), validade_min: CODIGO_MIN }, 200, CORS);
}

async function ativar(env, corpo, ip) {
  const email = normEmail(corpo.email);
  const disp = limpaDisp(corpo.dispositivo);
  const rotulo = limpaTexto(corpo.rotulo, 60);
  const versao = limpaTexto(corpo.versao, 60);
  const codigo = soDigitos(corpo.codigo);
  if (!emailValido(email)) return json({ ok: false, erro: "email_invalido" }, 400, CORS);
  if (disp.length < 8) return json({ ok: false, erro: "dispositivo_invalido" }, 400, CORS);
  if (codigo.length !== 6) return json({ ok: false, erro: "codigo_formato" }, 400, CORS);

  const cli = await buscaCliente(env, email);
  if (!cli) return json({ ok: false, erro: "nao_cadastrado" }, 404, CORS);
  const st = recusaStatus(cli);
  if (st) return st;

  const c = await um(env, "SELECT * FROM codigos WHERE cliente_id = ? AND dispositivo = ? AND usado = 0 ORDER BY id DESC LIMIT 1",
    cli.id, disp);
  if (!c) return json({ ok: false, erro: "sem_codigo" }, 400, CORS);
  if (c.expira_em < agoraISO() || c.tentativas >= CODIGO_TENTATIVAS) {
    await roda(env, "UPDATE codigos SET usado = 1 WHERE id = ?", c.id);
    return json({ ok: false, erro: "codigo_expirado" }, 400, CORS);
  }
  const certo = await iguaisSeguro(c.codigo_hash, await hashCodigo(env, cli.id, disp, codigo));
  if (!certo) {
    const tent = c.tentativas + 1;
    await roda(env, "UPDATE codigos SET tentativas = ?, usado = ? WHERE id = ?", tent, tent >= CODIGO_TENTATIVAS ? 1 : 0, c.id);
    await evento(env, cli.id, "codigo_errado", rotulo, ip);
    return json({ ok: false, erro: "codigo_invalido", restam: Math.max(0, CODIGO_TENTATIVAS - tent) }, 400, CORS);
  }
  await roda(env, "UPDATE codigos SET usado = 1 WHERE id = ?", c.id);

  const vaga = await confereVaga(env, cli, disp);
  if (!vaga.ok) return json({ ok: false, erro: "limite_dispositivos", limite: cli.limite_dispositivos, ativos: vaga.ativos }, 403, CORS);
  const agora = agoraISO();
  if (vaga.conhecido) {
    await roda(env, "UPDATE dispositivos SET ativo = 1, rotulo = ?, versao = ?, ultimo_contato = ? WHERE id = ?",
      rotulo, versao, agora, vaga.conhecido.id);
  } else {
    await roda(env, "INSERT INTO dispositivos (cliente_id, dispositivo, rotulo, versao, ativo, primeira_ativacao, ultimo_contato) VALUES (?,?,?,?,1,?,?)",
      cli.id, disp, rotulo, versao, agora, agora);
  }

  // a avaliação começa a contar na primeira ativação, não no cadastro
  if (cli.plano === "avaliacao" && !cli.validade) {
    // 30 dias inteiros depois do dia da ativação: ativou em 05/10, usa até 04/11
    cli.validade = somarDias(hojeBR(), +(env.AVALIACAO_DIAS || 30));
    await roda(env, "UPDATE clientes SET validade = ?, atualizado_em = ? WHERE id = ?", cli.validade, agora, cli.id);
  }
  const licenca = await emitir(env, cli, disp);
  await evento(env, cli.id, "ativacao", rotulo + " · " + disp + " · até " + cli.validade, ip);
  return json({ ok: true, licenca, agora: hojeBR(), plano: cli.plano, expira_em: cli.validade }, 200, CORS);
}

async function renovar(env, corpo, ip) {
  const d = await lerLicenca(env, corpo.licenca);
  if (!d) return json({ ok: false, erro: "licenca_invalida" }, 400, CORS);
  const disp = limpaDisp(corpo.dispositivo);
  if (d.dispositivo !== "*" && d.dispositivo !== disp) return json({ ok: false, erro: "dispositivo_invalido" }, 400, CORS);
  const cli = await um(env, "SELECT * FROM clientes WHERE serie = ?", d.serie);
  if (!cli) return json({ ok: false, erro: "nao_encontrado" }, 404, CORS);
  const st = recusaStatus(cli);
  if (st) { await evento(env, cli.id, "recusa", "renovação com licença " + cli.status, ip); return st; }
  if (d.dispositivo !== "*") {
    const dv = await um(env, "SELECT * FROM dispositivos WHERE cliente_id = ? AND dispositivo = ?", cli.id, disp);
    if (!dv || !dv.ativo) {
      await evento(env, cli.id, "recusa", "renovação de computador removido · " + disp, ip);
      return json({ ok: false, erro: "dispositivo_removido" }, 403, CORS);
    }
    await roda(env, "UPDATE dispositivos SET ultimo_contato = ?, versao = ? WHERE id = ?",
      agoraISO(), limpaTexto(corpo.versao, 60), dv.id);
  }
  const licenca = await emitir(env, cli, d.dispositivo);
  const mudou = d.expira_em !== cli.validade || d.plano !== cli.plano;
  await evento(env, cli.id, "renovacao", (mudou ? "MUDOU para " + cli.plano + " até " + cli.validade : "sem mudança") + " · " + d.dispositivo, ip);
  return json({ ok: true, licenca, agora: hojeBR(), mudou }, 200, CORS);
}

// ================================================================== painel
async function autorizado(request, env) {
  if (!env.ADMIN_TOKEN || env.ADMIN_TOKEN.length < 16) return false;
  const h = request.headers.get("Authorization") || "";
  const t = h.startsWith("Bearer ") ? h.slice(7) : "";
  return t ? iguaisSeguro(t, env.ADMIN_TOKEN) : false;
}

async function admin(request, env, url) {
  if (!env.ADMIN_TOKEN) return json({ ok: false, erro: "admin_desligado" }, 503);
  if (!(await autorizado(request, env))) return json({ ok: false, erro: "nao_autorizado" }, 401);
  if (!env.LICENCAS) return json({ ok: false, erro: "servico_indisponivel" }, 503);
  const p = url.pathname.replace(/^\/api\/admin\//, "");
  const ip = ipDe(request);
  const corpo = request.method === "POST" ? await lerJson(request) : {};

  if (p === "clientes" && request.method === "GET") {
    const termo = limpaTexto(url.searchParams.get("q"), 80);
    const q = "%" + termo.toLowerCase() + "%";
    const qd = soCNPJ(termo);
    const lista = await todos(env, `
      SELECT c.*, (SELECT COUNT(*) FROM dispositivos d WHERE d.cliente_id = c.id AND d.ativo = 1) AS ativos,
             (SELECT MAX(ultimo_contato) FROM dispositivos d WHERE d.cliente_id = c.id) AS ultimo_contato,
             (SELECT COUNT(*) FROM clientes c2 WHERE c2.documento = c.documento AND c2.id <> c.id
                AND IFNULL(c.documento,'') <> '') AS mesmo_doc
        FROM clientes c
       WHERE lower(c.email) LIKE ? OR lower(c.nome) LIKE ? OR lower(IFNULL(c.empresa,'')) LIKE ?
             OR c.documento LIKE ? OR lower(IFNULL(c.serie,'')) LIKE ?
       ORDER BY c.id DESC LIMIT 500`, q, q, q, qd ? "%" + qd + "%" : q, q);
    const tot = await um(env, `SELECT COUNT(*) AS n,
        SUM(CASE WHEN plano = 'avaliacao' THEN 1 ELSE 0 END) AS avaliacao,
        SUM(CASE WHEN plano <> 'avaliacao' AND status = 'ativo' THEN 1 ELSE 0 END) AS pagantes,
        SUM(CASE WHEN status <> 'ativo' THEN 1 ELSE 0 END) AS inativos FROM clientes`);
    return json({ ok: true, clientes: lista, totais: tot, hoje: hojeBR() });
  }
  if (p === "cliente" && request.method === "GET") {
    const id = +url.searchParams.get("id");
    const cli = await um(env, "SELECT * FROM clientes WHERE id = ?", id);
    if (!cli) return json({ ok: false, erro: "nao_encontrado" }, 404);
    const disp = await todos(env, "SELECT * FROM dispositivos WHERE cliente_id = ? ORDER BY ativo DESC, ultimo_contato DESC", id);
    const evt = await todos(env, "SELECT * FROM eventos WHERE cliente_id = ? ORDER BY id DESC LIMIT 60", id);
    return json({ ok: true, cliente: cli, dispositivos: disp, eventos: evt });
  }
  if (p === "cliente" && request.method === "POST") {
    const id = +corpo.id;
    const cli = await um(env, "SELECT * FROM clientes WHERE id = ?", id);
    if (!cli) return json({ ok: false, erro: "nao_encontrado" }, 404);
    const campos = {};
    if (corpo.plano != null) campos.plano = limpaTexto(corpo.plano, 30) || cli.plano;
    if (corpo.validade != null) {
      if (corpo.validade && !/^\d{4}-\d{2}-\d{2}$/.test(corpo.validade)) return json({ ok: false, erro: "validade" }, 400);
      campos.validade = corpo.validade || null;
    }
    if (corpo.status != null) {
      if (["ativo", "suspenso", "cancelado"].indexOf(corpo.status) < 0) return json({ ok: false, erro: "status" }, 400);
      campos.status = corpo.status;
    }
    if (corpo.limite_dispositivos != null) campos.limite_dispositivos = Math.max(1, Math.min(20, +corpo.limite_dispositivos || 1));
    for (const k of ["nome", "empresa", "cidade", "obs"]) if (corpo[k] != null) campos[k] = limpaTexto(corpo[k], k === "obs" ? 1000 : 160);
    if (corpo.uf != null) campos.uf = limpaTexto(corpo.uf, 2).toUpperCase();
    if (corpo.telefone != null) campos.telefone = soDigitos(corpo.telefone).slice(0, 13);
    if (corpo.tipo != null) campos.tipo = corpo.tipo === "PJ" ? "PJ" : "PF";
    if (corpo.documento != null) {
      const dd = soCNPJ(corpo.documento);
      if (dd && !((/^\d{11}$/.test(dd) && cpfValido(dd)) || cnpjValido(dd))) return json({ ok: false, erro: "documento" }, 400);
      campos.documento = dd;
    }
    const ks = Object.keys(campos);
    if (!ks.length) return json({ ok: false, erro: "nada" }, 400);
    await roda(env, "UPDATE clientes SET " + ks.map((k) => k + " = ?").join(", ") + ", atualizado_em = ? WHERE id = ?",
      ...ks.map((k) => campos[k]), agoraISO(), id);
    await evento(env, id, "admin", "alterou " + ks.map((k) => k + "=" + campos[k]).join(" · "), ip);
    return json({ ok: true, cliente: await um(env, "SELECT * FROM clientes WHERE id = ?", id) });
  }
  if (p === "dispositivo" && request.method === "POST") {
    const r = await roda(env, "UPDATE dispositivos SET ativo = ? WHERE cliente_id = ? AND dispositivo = ?",
      corpo.ativo ? 1 : 0, +corpo.cliente_id, limpaDisp(corpo.dispositivo));
    await evento(env, +corpo.cliente_id, "admin", (corpo.ativo ? "reativou" : "removeu") + " o computador " + limpaDisp(corpo.dispositivo), ip);
    return json({ ok: true, alterados: (r.meta && r.meta.changes) || 0 });
  }
  if (p === "chave" && request.method === "POST") {
    const cli = await um(env, "SELECT * FROM clientes WHERE id = ?", +corpo.cliente_id);
    if (!cli) return json({ ok: false, erro: "nao_encontrado" }, 404);
    const disp = corpo.dispositivo === "*" ? "*" : limpaDisp(corpo.dispositivo);
    if (disp !== "*" && disp.length < 8) return json({ ok: false, erro: "dispositivo_invalido" }, 400);
    if (!cli.validade) return json({ ok: false, erro: "sem_validade" }, 400);
    const chave = await emitir(env, cli, disp);
    if (disp !== "*") {
      const agora = agoraISO();
      await roda(env, `INSERT INTO dispositivos (cliente_id, dispositivo, rotulo, ativo, primeira_ativacao, ultimo_contato)
                       VALUES (?,?,?,1,?,?) ON CONFLICT(cliente_id, dispositivo) DO UPDATE SET ativo = 1`,
        cli.id, disp, "chave manual", agora, agora);
    }
    let envio = null;
    if (corpo.enviar) {
      const m = emailChave(cli, chave, cli.validade);
      envio = await enviarEmail(env, { para: cli.email, ...m });
    }
    await evento(env, cli.id, "admin", "emitiu chave manual para " + disp + (envio ? " · e-mail " + envio.via + (envio.ok ? "" : " FALHOU") : ""), ip);
    return json({ ok: true, chave, enviado: envio ? envio.ok : false });
  }
  if (p === "reenviar" && request.method === "POST") {
    const cli = await um(env, "SELECT * FROM clientes WHERE id = ?", +corpo.cliente_id);
    if (!cli) return json({ ok: false, erro: "nao_encontrado" }, 404);
    const m = emailBoasVindas(env, cli);
    const r = await enviarEmail(env, { para: cli.email, ...m });
    await evento(env, cli.id, "email", "boas-vindas (reenvio pelo painel) · " + r.via + (r.ok ? "" : " · FALHOU"), ip);
    return json({ ok: r.ok, via: r.via });
  }
  if (p === "eventos" && request.method === "GET") {
    const lista = await todos(env, `SELECT e.*, c.email FROM eventos e LEFT JOIN clientes c ON c.id = e.cliente_id
                                     ORDER BY e.id DESC LIMIT ?`, Math.min(500, +(url.searchParams.get("limite") || 200)));
    return json({ ok: true, eventos: lista });
  }
  if (p === "chave-publica" && request.method === "GET") {
    try { return json({ ok: true, ...(await chavePublicaSPKI(env)) }); }
    catch (e) { return json({ ok: false, erro: "sem_chave" }, 503); }
  }
  if (p === "emails-teste" && request.method === "GET" && env.MODO_TESTE === "1") {
    return json({ ok: true, emails: await todos(env, "SELECT * FROM emails_teste ORDER BY id DESC LIMIT 50") });
  }
  return json({ ok: false, erro: "rota" }, 404);
}

// =================================================================== rotas
export async function rotearLicencas(request, env, url, paginaAdmin) {
  const p = url.pathname;
  if (p === "/api/cadastro") return cadastro(request, env, url);
  if (p.startsWith("/api/licenca/")) {
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });
    if (request.method !== "POST") return json({ ok: false, erro: "metodo" }, 405, CORS);
    if (!env.LICENCAS || !env.LICENCA_CHAVE_PRIVADA) return json({ ok: false, erro: "servico_indisponivel" }, 503, CORS);
    const corpo = await lerJson(request);
    const ip = ipDe(request);
    try {
      if (p === "/api/licenca/codigo") return await pedirCodigo(env, corpo, ip);
      if (p === "/api/licenca/ativar") return await ativar(env, corpo, ip);
      if (p === "/api/licenca/renovar") return await renovar(env, corpo, ip);
    } catch (e) {
      return json({ ok: false, erro: "interno" }, 500, CORS);
    }
    return json({ ok: false, erro: "rota" }, 404, CORS);
  }
  if (p === "/admin" || p === "/admin/") return paginaAdmin();
  if (p.startsWith("/api/admin/")) {
    try { return await admin(request, env, url); }
    catch (e) { return json({ ok: false, erro: "interno", detalhe: String(e && e.message || e) }, 500); }
  }
  return null;
}

// para os testes
export const _interno = { cpfValido, cnpjValido, docVisivel, mascaraEmail, somarDias, hojeBR, fmtCNPJ, soCNPJ };
