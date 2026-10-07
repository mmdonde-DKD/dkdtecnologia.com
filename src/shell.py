# -*- coding: utf-8 -*-
"""Casca comum: <head>, barra superior e rodapé do site da DKD.

Tudo que se repete em toda página está aqui. Os nomes dos módulos saem de
MODULOS — um único lugar — para que site, portais e material comercial
falem exatamente a mesma coisa.
"""

from theme import FONTS_LINK, marca, JARGAO

SITE = "https://dkdtecnologia.com"
APP = "https://app.dkdtecnologia.com"

# --------------------------------------------------------------- identidade
RAZAO = "DKD Tecnologia e Inovação"
MARCA = "DKD Tecnologia e Inovação"
CNPJ = "59.890.881/0001-06"
CIDADE = "Caxias do Sul / RS"
EMAIL = "comercial@dkdtecnologia.com"
# único e-mail publicado no site (decisão de 07/10/2026), inclusive para LGPD
EMAIL_DPO = EMAIL
# ------------------------------------------------- o que você preenche
# WhatsApp comercial, só dígitos, com 55 e DDD. Enquanto ficar como está,
# o botão flutuante simplesmente não aparece — nada quebra na tela.
WHATSAPP = "5554999135507"
WHATS_MSG = "Olá! Vim pelo site da DKD e queria entender melhor os módulos."

# Chave pública do widget Turnstile (Cloudflare → Turnstile → Add widget).
# Vazia = o site funciona igual, só sem a proteção anti-robô no formulário.
TURNSTILE_SITEKEY = ""

SUITE = "DKD Financial Tools AI"

# Download do módulo de Gestão Financeira (versão para o computador do cliente).
# Endereço fixo: a cada versão nova troca-se o zip em downloads/, e os links dos
# e-mails de boas-vindas já enviados continuam levando à versão mais recente.
# O build só publica o zip se ele vier carimbado com a chave de PRODUÇÃO.
DOWNLOAD_GESTAO = "/downloads/DKD_Financial_Tools_AI_Gestao_Financeira.zip"

# ------------------------------------------------------------------ módulos
# chave: (nome curto, nome completo, cor/tema, rota, resumo de uma linha, linha do cabeçalho)
MODULOS = {
    "gestao": (
        "Gestão Financeira",
        f"{SUITE} — Módulo de Planejamento, Controle e Gestão Financeira",
        "gestao",
        "/produtos/gestao-financeira/",
        "Planejamento, controle e gestão financeira de CPF e CNPJ no mesmo painel.",
        "Módulo · Planejamento e Gestão Financeira",
    ),
    "alpha": (
        "Alpha Invest AI",
        f"{SUITE} — Módulo Alpha Invest AI",
        "alpha",
        "/produtos/alpha-invest/",
        "Triagem e comparação de ativos pelos critérios que você define.",
        "Módulo · Alpha Invest AI",
    ),
    "asset": (
        "Asset Intelligence AI",
        f"{SUITE} — Módulo Asset Intelligence AI",
        "asset",
        "/produtos/asset-intelligence/",
        "Acompanhamento de carteira, concentração, proventos e eventos societários.",
        "Módulo · Asset Intelligence AI",
    ),
    "fiscal": (
        "Fiscal e Tributária",
        f"{SUITE} — Módulo de Análise, Simulação e Inteligência Fiscal e Tributária",
        "fiscal",
        "/produtos/fiscal-tributaria/",
        "Comparação de regimes sobre o SPED real, com o dispositivo citado no parecer.",
        "Módulo · Inteligência Fiscal e Tributária",
    ),
}

# ordem de apresentação em menus, rodapé e listagens
ORDEM = ["gestao", "alpha", "asset", "fiscal"]

# ------------------------------------------------------------------ portais
# Onde cada portal abre. O corpo das páginas usa a marca __PORTAL_<CHAVE>__ e o
# build troca conforme o destino:
#   · prévia de arquivo único → o arquivo do portal AO LADO dela, na mesma
#                               pasta, para o link nunca depender de subpasta;
#   · site publicado          → subdomínio com o Cloudflare Access na frente.
PORTAIS = {
    "gestao": ("10_DKD_Portal_Gestao_Financeira.html",
               "https://gestao.dkdtecnologia.com"),
    "alpha":  ("11a_DKD_Portal_Alpha_Invest.html",
               "https://alpha.dkdtecnologia.com"),
    "asset":  ("11b_DKD_Portal_Asset_Intelligence.html",
               "https://asset.dkdtecnologia.com"),
    "hub":    ("11c_DKD_Portal_Integrado.html",
               APP),
    "fiscal": ("12_DKD_Portal_Fiscal_Tributaria.html",
               "https://atc.dkdtecnologia.com"),
}


def portal(chave: str) -> str:
    """Marca que o build troca pelo endereço certo do portal."""
    return "__PORTAL_%s__" % chave.upper()


def whats_link(msg: str = "") -> str:
    """Link do WhatsApp com a mensagem já escrita. Vazio se não configurado."""
    if "X" in WHATSAPP:
        return ""
    from urllib.parse import quote
    return f"https://wa.me/{WHATSAPP}?text={quote(msg or WHATS_MSG)}"


def whats_flutuante() -> str:
    """Botão fixo no canto. Só existe se o número estiver preenchido."""
    href = whats_link()
    if not href:
        return ""
    return f"""<a class="zap" href="{href}" target="_blank" rel="noopener"
   data-lead="whatsapp" aria-label="Falar com a DKD no WhatsApp">
  <svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true" fill="currentColor">
    <path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.46 1.32 4.96L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91C21.96 6.45 17.5 2 12.04 2m0 18.15h-.01a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.22 8.22 0 0 1-1.26-4.38c0-4.54 3.7-8.23 8.25-8.23a8.23 8.23 0 0 1 0 16.47m4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.24-.64.8-.78.97-.15.16-.29.18-.54.06-.25-.13-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.38.11-.5.11-.11.25-.29.37-.44.13-.15.17-.25.25-.42.09-.16.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.4-.42-.56-.43h-.47c-.17 0-.43.06-.66.31-.22.25-.87.85-.87 2.07s.89 2.4 1.02 2.56c.12.17 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.47-.07 1.47-.6 1.68-1.18.2-.58.2-1.08.14-1.18-.06-.11-.22-.17-.47-.29"/>
  </svg>
  <span>Falar no WhatsApp</span>
</a>"""


def turnstile() -> str:
    """Widget anti-robô. Sem chave configurada, não renderiza nada."""
    if not TURNSTILE_SITEKEY:
        return ""
    return (f'<div class="cf-turnstile" data-sitekey="{TURNSTILE_SITEKEY}" '
            'data-theme="dark" data-language="pt-br" style="margin:4px 0"></div>')


def turnstile_script() -> str:
    if not TURNSTILE_SITEKEY:
        return ""
    return ('<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" '
            'async defer></script>')

# rota → chave do módulo, para colorir a página e nomear o cabeçalho
ROTA_MOD = {m[3]: k for k, m in MODULOS.items()}
ROTA_MOD["/cadastro/"] = "gestao"     # o teste grátis é do módulo de Gestão Financeira

NAV = [
    ("Módulos", "/produtos/"),
    ("Portais", "/portais/"),
    ("Consultoria", "/consultoria/"),
    ("Segurança", "/seguranca/"),
    ("Sobre", "/sobre/"),
    ("Contato", "/contato/"),
]

AVISO_CVM = (
    f"A {MARCA} não é consultora de valores mobiliários nem analista de valores "
    "mobiliários registrada na CVM. Os módulos DKD Alpha Invest AI e DKD Asset Intelligence AI "
    "são ferramentas de triagem, comparação e acompanhamento operadas pelo próprio usuário, "
    "segundo critérios que ele define. Nada do que produzem constitui recomendação, "
    "oferta ou sugestão de compra ou venda de ativos. A decisão de investir é exclusiva do investidor."
)

AVISO_FISCAL = (
    "As análises fiscais e tributárias são insumo técnico para decisão profissional. "
    "A responsabilidade pela decisão tributária e pelo parecer assinado é do contador ou "
    "responsável técnico habilitado do cliente."
)


# ------------------------------------------------------------------ topo
def topbar(active: str, spa: bool = False, sub: str = "") -> str:
    """Cabeçalho padrão. `sub` troca a linha de assinatura pelo nome do módulo."""
    def href(u):
        return ("#" + u.rstrip("/") if u != "/" else "#/") if spa else u
    links = "".join(
        '<a href="{h}"{cur}>{t}</a>'.format(
            h=href(u), t=t, cur=' aria-current="page"' if u == active else ""
        )
        for t, u in NAV
    )
    return f"""<a class="sr-only" href="#conteudo">Pular para o conteúdo</a>
<header class="topbar">
  <div class="topbar-in">
    <a class="marca-link" href="{href('/')}" aria-label="{MARCA} — início">{marca(sub)}</a>
    <button class="burger" aria-label="Abrir menu" aria-expanded="false"><span></span><span></span><span></span></button>
    <nav class="nav" aria-label="Principal">
      {links}
      <div class="nav-actions">
        <a class="signin" href="{APP}">Entrar<span aria-hidden="true">↗</span></a>
        <a class="btn btn--sm btn--solid" href="{href('/diagnostico/')}" data-lead="cta-topo">Diagnóstico gratuito</a>
      </div>
    </nav>
  </div>
</header>"""


# ------------------------------------------------------------------ rodapé
def footer(spa: bool = False) -> str:
    def href(u):
        return ("#" + u.rstrip("/") if u != "/" else "#/") if spa else u
    mods = "".join(
        f'<li><a href="{href(MODULOS[k][3])}">{MODULOS[k][0]}</a></li>' for k in ORDEM
    )
    return f"""<footer class="footer">
  <div class="container">
    <div class="foot-grid">
      <div>
        {marca(classe="marca--foot")}
        <p class="tiny" style="margin-top:16px;max-width:36ch">Plataformas de análise financeira, fiscal e de investimentos, e consultoria em
        processos de gestão comercial e financeira com o uso de IA.</p>
      </div>
      <div>
        <h4>Módulos {SUITE}</h4>
        <ul>{mods}</ul>
      </div>
      <div>
        <h4>Empresa</h4>
        <ul>
          <li><a href="{href('/sobre/')}">Sobre a DKD</a></li>
          <li><a href="{href('/seguranca/')}">Segurança e LGPD</a></li>
          <li><a href="{href('/consultoria/')}">Consultoria com IA</a></li>
          <li><a href="{href('/diagnostico/')}">Diagnóstico gratuito</a></li>
          <li><a href="{href('/contato/')}">Contato</a></li>
        </ul>
      </div>
      <div>
        <h4>Acesso</h4>
        <ul>
          <li><a href="{APP}">Entrar no portal</a></li>
          <li><a href="{href('/legal/privacidade/')}">Privacidade</a></li>
          <li><a href="{href('/legal/termos/')}">Termos de uso</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-legal">
      <p><strong>{RAZAO}</strong> · CNPJ {CNPJ} · {CIDADE} · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p>{AVISO_CVM}</p>
      <p>{AVISO_FISCAL}</p>
      <p>© 2026 {RAZAO}. Todos os direitos reservados. DKD™ e {SUITE}™ são marcas da {RAZAO}.</p>
    </div>
  </div>
</footer>"""


# -------------------------------------------------------------------- head
HEAD_TPL = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="{razao}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{marca_nome}">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{site}/assets/dkd-og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{site}/assets/dkd-og.jpg">
<meta name="theme-color" content="#030913">
<meta name="color-scheme" content="dark">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/assets/favicon-64.png" sizes="64x64" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
{fonts}
<link rel="stylesheet" href="/assets/dkd.css">
</head>
<body{mod}>
{topbar}
<main id="conteudo">
{body}
</main>
{footer}
{zap}
{turnstile}
<script src="/assets/dkd.js" defer></script>
</body>
</html>
"""


def page(title, desc, path, body, active=None):
    canonical = SITE + path
    chave = ROTA_MOD.get(path)
    mod = f' data-mod="{MODULOS[chave][2]}"' if chave else ""
    sub = MODULOS[chave][5] if chave else JARGAO
    return HEAD_TPL.format(
        title=title,
        desc=desc,
        canonical=canonical,
        site=SITE,
        razao=RAZAO,
        marca_nome=MARCA,
        fonts=FONTS_LINK,
        mod=mod,
        topbar=topbar(active or path, sub=sub),
        body=body,
        footer=footer(),
        zap=whats_flutuante(),
        turnstile=turnstile_script(),
    )


# ---------------------------------------------------------------- formulário
def formulario(origem: str, botao: str, msg_placeholder: str, compacto: bool = False) -> str:
    """Formulário de lead. `origem` identifica de qual página veio, e viaja
    junto no e-mail, no registro do lead e no evento de conversão."""
    opcoes = "".join(
        f'<option value="{MODULOS[k][0]}">{MODULOS[k][0]}</option>' for k in ORDEM
    )
    extra = "" if compacto else f"""
        <div class="two">
          <div class="field"><label for="tel-{origem}">Telefone ou WhatsApp</label>
            <input id="tel-{origem}" name="telefone" autocomplete="tel"></div>
          <div class="field"><label for="cnpjs-{origem}">CNPJs na carteira</label>
            <input id="cnpjs-{origem}" name="cnpjs" inputmode="numeric" placeholder="ex.: 120"></div>
        </div>"""
    return f"""<form class="form" method="POST" action="/api/contato?de=/{origem}/"
      data-lead-form="{origem}">
        <input type="hidden" name="origem" value="{origem}">
        <input type="hidden" name="referrer" value="" data-referrer>
        <div class="two">
          <div class="field"><label for="nome-{origem}">Nome</label>
            <input id="nome-{origem}" name="nome" required autocomplete="name"></div>
          <div class="field"><label for="emp-{origem}">Empresa</label>
            <input id="emp-{origem}" name="empresa" autocomplete="organization"></div>
        </div>
        <div class="two">
          <div class="field"><label for="mail-{origem}">E-mail</label>
            <input id="mail-{origem}" name="email" type="email" required autocomplete="email"></div>
          <div class="field"><label for="mod-{origem}">Módulo de interesse</label>
            <select id="mod-{origem}" name="modulo">{opcoes}
              <option value="Mais de um módulo">Mais de um módulo</option>
              <option value="Consultoria e soluções customizadas com IA">Consultoria e soluções customizadas com IA</option>
              <option value="Ainda não sei">Ainda não sei</option>
            </select></div>
        </div>{extra}
        <div class="field"><label for="msg-{origem}">Mensagem</label>
          <textarea id="msg-{origem}" name="mensagem" required placeholder="{msg_placeholder}"></textarea></div>
        <div aria-hidden="true" style="position:absolute;left:-9999px">
          <label for="hp-{origem}">Não preencha</label>
          <input id="hp-{origem}" name="website" tabindex="-1" autocomplete="off"></div>
        {turnstile()}
        <div class="field" style="display:flex;gap:10px;align-items:flex-start">
          <input id="ok-{origem}" name="consentimento" type="checkbox" required style="width:auto;margin-top:6px">
          <label for="ok-{origem}" style="text-transform:none;letter-spacing:0;font-family:var(--font-body);font-size:.86rem;color:var(--txt-2)">
            Autorizo a DKD a usar estes dados para responder ao meu contato, conforme a
            <a href="/legal/privacidade/">Política de Privacidade</a>.</label>
        </div>
        <div><button class="btn btn--solid" type="submit">{botao}</button></div>
      </form>
      <div class="aviso-form" data-aviso hidden></div>"""
