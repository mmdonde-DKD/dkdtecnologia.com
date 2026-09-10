# -*- coding: utf-8 -*-
"""Gera o site estático da DKD (dist/) e a prévia navegável de arquivo único."""

import base64
import io
import json
import os
import re
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI) if os.path.basename(AQUI) == "src" else AQUI
sys.path.insert(0, AQUI)

from theme import CSS, JS, FONTS_LINK, JARGAO
import shell
from shell import page, topbar, footer, SITE, SUITE, MODULOS, ROTA_MOD, PORTAIS
import pages_a as A
import pages_b as B


def liga_portais(html, local: bool):
    """Troca as marcas __PORTAL_X__ pelo endereço certo do portal.

    `local=True` aponta para o arquivo do portal ao lado da prévia — é assim que
    a demonstração roda direto do disco. `local=False` aponta para o subdomínio
    com o Cloudflare Access na frente, que é o site publicado.
    """
    for chave, (arquivo, url) in PORTAIS.items():
        html = html.replace("__PORTAL_%s__" % chave.upper(), arquivo if local else url)
    if local:
        # sem servidor no ar, "Entrar no portal" leva à área logada de exemplo,
        # que é de onde a demonstração abre cada portal de verdade
        html = html.replace('href="%s"' % shell.APP, 'href="#/app-preview"')
    return html

OUT = os.path.join(RAIZ, "dist")
ATIVOS = os.path.join(RAIZ, "assets")
PREVIA = os.path.join(RAIZ, "DKD_Site_Institucional_previa.html")

# imagens copiadas para dist/assets
IMAGENS = [
    "dkd-emblema.png",
    "dkd-emblema-88.png",
    "dkd-marca.jpg",
    "dkd-hero.jpg",
    "dkd-og.jpg",
    "favicon-32.png",
    "favicon-64.png",
    "apple-touch-icon.png",
]

M = MODULOS
PAGES = [
    # (caminho, título, descrição, corpo, entra_no_sitemap)
    ("/", "DKD Tecnologia e Inovação — análise financeira, fiscal e de investimentos",
     "Quatro módulos de análise para contador, empresário e investidor. Motor determinístico, IA que cita a fonte e dossiê de evidência exportável.",
     A.HOME, True),
    ("/produtos/", f"Módulos {SUITE} — DKD Tecnologia e Inovação",
     "Planejamento e Gestão Financeira, Alpha Invest AI, Asset Intelligence AI e Análise, Simulação e Inteligência Fiscal e Tributária. Quatro módulos, um acesso.",
     A.PRODUTOS, True),
    (M["fiscal"][3], f'{M["fiscal"][1]} — DKD Tecnologia e Inovação',
     "Compare Simples puro, híbrido, Presumido e Real sobre o SPED real, veja a carteira inteira numa tela e exporte o parecer com o dispositivo citado.",
     A.FISCAL, True),
    (M["gestao"][3], f'{M["gestao"][1]} — DKD Tecnologia e Inovação',
     "Extratos de pessoa física e jurídica classificados no mesmo painel, fronteira entre empresa e dono, e projeção de caixa de 30, 60 e 90 dias.",
     A.GESTAO, True),
    (M["alpha"][3], f'{M["alpha"][1]} — DKD Tecnologia e Inovação',
     "Ferramenta de triagem e comparação de ativos operada por você, com a fonte de cada número. Não emite recomendação de investimento.",
     A.ALPHA, True),
    (M["asset"][3], f'{M["asset"][1]} — DKD Tecnologia e Inovação',
     "Concentração recalculada, proventos, eventos societários e alertas nos limites que você define. Não emite recomendação de investimento.",
     A.ASSET, True),
    ("/diagnostico/", "Diagnóstico gratuito de regime tributário — DKD Tecnologia e Inovação",
     "Envie o SPED de até três CNPJs e receba em dois dias úteis o comparativo entre Simples puro, híbrido, Presumido e Real, com o dispositivo legal citado. Sem cartão.",
     B.DIAGNOSTICO, True),
    ("/portais/", f"Portais {SUITE} — DKD Tecnologia e Inovação",
     "Acesso aos cinco portais da DKD: Fiscal e Tributária, Planejamento e Gestão Financeira, Alpha Invest AI, Asset Intelligence AI e o Portal Integrado.",
     B.PORTAIS_PAGE, True),
    ("/precos/", f"Preços {SUITE} — DKD Tecnologia e Inovação",
     "Tabela pública dos quatro módulos, adicionais e condições de contratação. Sem “agende uma demonstração”.",
     B.PRECOS, True),
    ("/seguranca/", "Segurança, privacidade e LGPD — DKD Tecnologia e Inovação",
     "Papéis de controlador e operador, onde o dado fica, controle de acesso, medidas do artigo 46 e o que a DKD garante e não garante.",
     B.SEGURANCA, True),
    ("/sobre/", "Sobre a DKD Tecnologia e Inovação",
     "Ferramentas de análise para quem precisa responder por número diante de outra pessoa. Como a DKD constrói e o que a DKD não é.",
     B.SOBRE, True),
    ("/contato/", "Contato — DKD Tecnologia e Inovação",
     "Fale com quem construiu a ferramenta. Resposta em até um dia útil.",
     B.CONTATO, True),
    ("/legal/privacidade/", "Política de Privacidade — DKD Tecnologia e Inovação",
     "Como a DKD trata dados pessoais, em quais papéis, por quanto tempo e com quem compartilha.",
     B.PRIVACIDADE, True),
    ("/legal/termos/", "Termos de Uso — DKD Tecnologia e Inovação",
     "Licença de uso, natureza do resultado, obrigações, propriedade intelectual e limitação de responsabilidade.",
     B.TERMOS, True),
    ("/app-preview/", "Prévia do portal — DKD Tecnologia e Inovação",
     "Prévia interna da área logada. Não indexar.",
     B.APP_HUB, False),
]

NAV_PATHS = {u for _, u in shell.NAV}


def active_for(path):
    """Qual item de menu deve aparecer marcado nesta página."""
    if path in NAV_PATHS:
        return path
    if path.startswith("/produtos/"):
        return "/produtos/"
    return path


# Favicon vetorial: emblema DKD simplificado (octógono de IA sobre azul-noite).
FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<defs><linearGradient id="p" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#F7FAFC"/><stop offset=".55" stop-color="#C9D1D8"/><stop offset="1" stop-color="#8E9AA4"/>
</linearGradient></defs>
<rect width="64" height="64" rx="12" fill="#030913"/>
<circle cx="32" cy="32" r="25" fill="#08172E" stroke="url(#p)" stroke-width="3"/>
<path d="M22 24h20l6 6v8l-6 6H22l-6-6v-8z" fill="#0C2540" stroke="url(#p)" stroke-width="2.4"/>
<text x="32" y="39" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif"
      font-size="17" font-weight="700" fill="url(#p)">IA</text>
</svg>"""

# Cabeçalhos de segurança aplicados pelo Cloudflare Pages a todas as respostas.
#
# A CSP abre exceção para exatamente três coisas, e nada além:
#   challenges.cloudflare.com    → widget Turnstile (script e iframe)
#   static.cloudflareinsights.com → beacon do Web Analytics
#   'self' em connect-src        → o beacon manda os dados para /cdn-cgi/rum,
#                                   no seu próprio domínio, e o Zaraz roda em
#                                   /cdn-cgi/zaraz/ — os dois são same-origin
#
# Se você ligar alguma ferramenta de terceiro no Zaraz (um pixel, um chat),
# ela vai precisar do host dela liberado aqui — e aí passa a valer a pena
# reler esta linha inteira antes de publicar.
HEADERS = """/*
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=(), payment=(), usb=(), interest-cohort=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  Cross-Origin-Opener-Policy: same-origin
  X-Robots-Tag: index, follow
  Content-Security-Policy: default-src 'self'; script-src 'self' https://challenges.cloudflare.com https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self' data:; connect-src 'self' https://cloudflareinsights.com; frame-src https://challenges.cloudflare.com; form-action 'self'; frame-ancestors 'self'; base-uri 'self'; object-src 'none'; upgrade-insecure-requests

/app-preview/*
  X-Robots-Tag: noindex, nofollow

/assets/*
  Cache-Control: public, max-age=31536000, immutable
"""

REDIRECTS = """# apex é canônico; www redireciona
https://www.dkdtecnologia.com/*  https://dkdtecnologia.com/:splat  301

# atalhos e nomes antigos
/atc                    /produtos/fiscal-tributaria/  301
/produtos/atc           /produtos/fiscal-tributaria/  301
/fiscal                 /produtos/fiscal-tributaria/  301
/gestao                 /produtos/gestao-financeira/  301
/alpha                  /produtos/alpha-invest/       301
/asset                  /produtos/asset-intelligence/ 301
/privacidade            /legal/privacidade/           301
/termos                 /legal/termos/                301
/entrar                 https://app.dkdtecnologia.com 302
"""

ROBOTS = f"""User-agent: *
Allow: /
Disallow: /app-preview/

Sitemap: {SITE}/sitemap.xml
"""

FUNCTION_CONTATO = r"""// functions/api/contato.js — Cloudflare Pages Function
//
// Recebe os formulários do site (/contato/ e /diagnostico/), confere o
// Turnstile, envia por e-mail e guarda o lead. Tudo o que é opcional
// degrada em silêncio: sem a chave do Turnstile ele não confere; sem o KV
// ele não guarda; sem a chave de e-mail ele avisa que falhou. O visitante
// nunca vê erro de configuração.
//
// Variáveis (Settings > Variables and Secrets, tipo Secret):
//   RESEND_API_KEY    chave do provedor de e-mail transacional
//   DESTINO           ex.: contato@dkdtecnologia.com
//   REMETENTE         ex.: site@dkdtecnologia.com (domínio verificado no provedor)
//   TURNSTILE_SECRET  chave secreta do widget Turnstile
// Binding opcional (Settings > Bindings > KV namespace):
//   LEADS             guarda um registro por lead, para você contar e exportar

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

export async function onRequestPost({ request, env }) {
  const url = new URL(request.url);
  const volta = (q) => Response.redirect(new URL((url.searchParams.get("de") || "/contato/") + q, url), 303);

  try {
    const form = await request.formData();

    // Armadilha para robô: campo invisível preenchido = descarta em silêncio.
    if (form.get("website")) return volta("?ok=1");

    const dados = {};
    for (const c of CAMPOS) dados[c] = (form.get(c) || "").toString().slice(0, 4000);

    if (!dados.nome || !dados.email || !dados.mensagem) {
      return volta("?erro=campos");
    }

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
"""


def write(path, content):
    full = os.path.join(OUT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def build_static():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    write("assets/dkd.css", CSS.strip() + "\n")
    write("assets/dkd.js", JS.strip() + "\n")
    write("assets/favicon.svg", FAVICON)
    write("_headers", HEADERS)
    write("_redirects", REDIRECTS)
    write("robots.txt", ROBOTS)
    write("functions/api/contato.js", FUNCTION_CONTATO)
    # Em Workers com assets, tudo que está no diretório é servido publicamente.
    # O .assetsignore mantém a Pages Function fora do ar — ela só existe aqui
    # para o caso de o site voltar a ser publicado como Cloudflare Pages.
    write(".assetsignore", "functions/\n")

    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    for img in IMAGENS:
        shutil.copy(os.path.join(ATIVOS, img), os.path.join(OUT, "assets", img))

    shutil.copy(os.path.join(ATIVOS, "fonts.css"), os.path.join(OUT, "assets", "fonts.css"))
    destino_fontes = os.path.join(OUT, "assets", "fonts")
    if os.path.isdir(destino_fontes):
        shutil.rmtree(destino_fontes)
    shutil.copytree(os.path.join(ATIVOS, "fonts"), destino_fontes)

    urls = []
    for path, title, desc, body, in_map in PAGES:
        html = liga_portais(page(title, desc, path, body, active=active_for(path)), local=False)
        if not in_map:
            html = html.replace("<head>", '<head>\n<meta name="robots" content="noindex,nofollow">', 1)
        target = "index.html" if path == "/" else path.strip("/") + "/index.html"
        write(target, html)
        if in_map:
            urls.append(SITE + path)

    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        prio = "1.0" if u.rstrip("/") == SITE else ("0.8" if "/produtos/" in u or "/precos" in u else "0.5")
        sitemap.append(f"  <url><loc>{u}</loc><changefreq>weekly</changefreq><priority>{prio}</priority></url>")
    sitemap.append("</urlset>")
    write("sitemap.xml", "\n".join(sitemap) + "\n")
    return urls


# ------------------------------------------------------------------ prévia
LINK_RE = re.compile(r'href="(/[^"#]*)"')


def data_uri(nome):
    caminho = os.path.join(ATIVOS, nome)
    mime = "image/png" if nome.endswith(".png") else "image/jpeg"
    with open(caminho, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode("ascii")


def to_spa(html):
    def sub(m):
        u = m.group(1)
        if u.startswith("/assets/"):
            return m.group(0)
        return 'href="#{}"'.format("/" if u == "/" else u.rstrip("/"))
    out = LINK_RE.sub(sub, html)
    out = out.replace('<form class="form" method="POST" action="/api/contato">',
                      '<form class="form" onsubmit="return false">')
    return out


SPA_JS = r"""
(function(){
  var titulos = __TITULOS__, subs = __SUBS__, mods = __MODS__;
  var jargao = __JARGAO__;
  function rota(){ var h=location.hash.replace(/^#/,''); return h||'/'; }
  function mostrar(){
    var r=rota(), achou=false;
    document.querySelectorAll('[data-route]').forEach(function(s){
      var on = s.getAttribute('data-route')===r;
      s.hidden=!on; if(on) achou=true;
    });
    if(!achou){ var p=document.querySelector('[data-route="/"]'); if(p) p.hidden=false; r='/'; }
    document.title = titulos[r] || 'DKD Tecnologia e Inovação';
    // cabeçalho acompanha o módulo: cor e linha de assinatura
    document.body.setAttribute('data-mod', mods[r] || '');
    var sub=document.querySelector('.topbar .marca-sub');
    if(sub) sub.textContent = subs[r] || jargao;
    document.querySelectorAll('.nav a').forEach(function(a){
      var h=a.getAttribute('href')||'';
      if(h.charAt(0)==='#'){
        if(h.slice(1)===r) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current');
      }
    });
    var n=document.querySelector('.nav'); if(n) n.classList.remove('open');
    window.scrollTo(0,0);
  }
  window.addEventListener('hashchange',mostrar);
  mostrar();
})();
"""

PREVIA_HEAD = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>DKD Tecnologia e Inovação — site institucional</title>
<meta name="theme-color" content="#030913">
<meta name="color-scheme" content="dark">
<link rel="icon" href="__FAVICON__">
{fonts}
<style>
{css}
.route[hidden]{{display:none}}
</style>
</head>
<body>
{topbar}
<main id="conteudo">
{rotas}
</main>
{footer}
{zap}
<script>
{js}
</script>
<script>
{spa}
</script>
</body>
</html>
"""


def build_spa():
    blocos, titulos, subs, mods = [], {}, {}, {}
    for path, title, desc, body, _ in PAGES:
        r = "/" if path == "/" else path.rstrip("/")
        titulos[r] = title
        chave = ROTA_MOD.get(path)
        mods[r] = MODULOS[chave][2] if chave else ""
        subs[r] = MODULOS[chave][5] if chave else JARGAO
        blocos.append(
            '<div class="route" data-route="{r}" hidden>\n{b}\n</div>'.format(r=r, b=to_spa(body))
        )

    fontes_embutidas = "<style>\n" + io.open(
        os.path.join(ATIVOS, "fonts-embed.css"), encoding="utf-8").read() + "</style>"

    doc = PREVIA_HEAD.format(
        fonts=fontes_embutidas,
        css=CSS.strip(),
        topbar=to_spa(topbar("/", spa=True)),
        rotas="\n".join(blocos),
        footer=to_spa(footer(spa=True)),
        zap=shell.whats_flutuante(),
        js=JS.strip(),
        spa=(SPA_JS.replace("__TITULOS__", json.dumps(titulos, ensure_ascii=False))
                   .replace("__SUBS__", json.dumps(subs, ensure_ascii=False))
                   .replace("__MODS__", json.dumps(mods, ensure_ascii=False))
                   .replace("__JARGAO__", json.dumps(JARGAO, ensure_ascii=False))),
    )

    # arquivo único: toda imagem vira data URI para abrir direto do disco
    favicon_uri = "data:image/svg+xml;base64," + base64.b64encode(FAVICON.encode("utf-8")).decode("ascii")
    doc = doc.replace("__FAVICON__", favicon_uri)
    for img in IMAGENS:
        doc = doc.replace("/assets/" + img, data_uri(img))
    doc = liga_portais(doc, local=True)

    with open(PREVIA, "w", encoding="utf-8") as f:
        f.write(doc)
    return doc


if __name__ == "__main__":
    urls = build_static()
    build_spa()
    n = sum(len(files) for _, _, files in os.walk(OUT))
    print("páginas no sitemap:", len(urls))
    print("arquivos em dist/:", n)
    print("prévia:", os.path.getsize(PREVIA), "bytes")
