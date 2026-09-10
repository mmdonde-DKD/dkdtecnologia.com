# -*- coding: utf-8 -*-
"""Aplica a identidade DKD ao cabeçalho e à guia do navegador dos portais.

O que faz em cada arquivo HTML de portal:
  1. troca o ícone da guia do navegador pelo emblema DKD;
  2. padroniza o <title> no formato «Módulo — DKD Financial Tools AI»;
  3. injeta a faixa de identidade DKD no topo da página (emblema, DKD,
     nome do módulo, jargão e a cor do módulo);
  4. neutraliza a marca antiga do próprio portal, sem remover nada do DOM —
     só esconde por CSS, para não quebrar o JavaScript que se apoia nela.

Nada da lógica do portal é tocado. Para uma versão nova do portal, basta
rodar este script de novo apontando para o arquivo novo.

    python padroniza_portais.py                 # usa o mapa PORTAIS abaixo
    python padroniza_portais.py entrada.html saida.html gestao
"""

import base64
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- identidade
SUITE = "DKD Financial Tools AI"
JARGAO = "Tecnologia que impulsiona na busca pelo novo"
EMPRESA = "DKD Tecnologia e Inovação"

# módulo → (rótulo do cabeçalho, título da guia, cor)
MODULOS = {
    "gestao": ("Módulo · Planejamento e Gestão Financeira",
               "Planejamento, Controle e Gestão Financeira", "#2FCB92"),
    "alpha":  ("Módulo · Alpha Invest AI",
               "Alpha Invest AI", "#25C0B4"),
    "asset":  ("Módulo · Asset Intelligence AI",
               "Asset Intelligence AI", "#3FB0E8"),
    "fiscal": ("Módulo · Inteligência Fiscal e Tributária",
               "Análise, Simulação e Inteligência Fiscal e Tributária", "#5B95F5"),
    "hub":    ("Portal integrado", "Portal Integrado", "#3FA9F0"),
}


def b64(caminho):
    with open(caminho, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


EMBLEMA = "data:image/png;base64," + b64(os.path.join(AQUI, "..", "assets", "dkd-emblema-88.png"))
FAVICON = "data:image/png;base64," + b64(os.path.join(AQUI, "..", "assets", "favicon-64.png"))
TOQUE = "data:image/png;base64," + b64(os.path.join(AQUI, "..", "assets", "apple-touch-icon.png"))
FONTES = io.open(os.path.join(AQUI, "fontes_cabecalho.css"), encoding="utf-8").read()

CSS = """
/* ====== Identidade DKD — faixa padrão de cabeçalho (gerada) ============== */
:root{--dkd-h:74px}
@media (max-width:680px){:root{--dkd-h:112px}}
%(fontes)s
.dkd-idbar{
  position:sticky;top:0;z-index:9600;--dkd-h:74px;
  background:linear-gradient(180deg,#060E1B,#030913);
  border-bottom:1px solid #1A2C46;font-family:"Archivo","Segoe UI",system-ui,sans-serif
}
.dkd-idbar::before{content:"";display:block;height:3px;background:var(--dkd-mod,#3FA9F0)}
.dkd-idbar-in{
  display:flex;align-items:center;gap:16px;max-width:1600px;margin:0 auto;
  padding:11px 22px;flex-wrap:wrap
}
.dkd-idbar-emb{width:44px;height:44px;flex:0 0 44px;display:block;
  filter:drop-shadow(0 2px 7px rgba(0,0,0,.65))}
.dkd-idbar-txt{display:flex;flex-direction:column;min-width:0;line-height:1.15}
.dkd-idbar-nome{
  font-size:26px;font-weight:800;letter-spacing:.055em;line-height:1.08;white-space:nowrap;
  background:linear-gradient(180deg,#F7FAFC 0%%,#D2DCE4 42%%,#93A1AD 72%%,#C4CED8 100%%);
  -webkit-background-clip:text;background-clip:text;color:transparent
}
.dkd-idbar-nome sup{font-size:.36em;font-weight:600;letter-spacing:0;position:relative;top:-.9em}
.dkd-idbar-sub{
  font-family:"IBM Plex Mono",ui-monospace,Consolas,monospace;font-size:10px;line-height:1.4;
  color:#7A8CA3;letter-spacing:.185em;text-transform:uppercase;white-space:nowrap;margin-top:5px
}
.dkd-idbar-suite{
  margin-left:auto;font-family:"IBM Plex Mono",ui-monospace,Consolas,monospace;font-size:10.5px;
  letter-spacing:.16em;text-transform:uppercase;color:var(--dkd-mod,#3FA9F0);font-weight:500;
  border:1px solid var(--dkd-mod,#3FA9F0);border-radius:999px;padding:5px 12px;white-space:nowrap
}
.dkd-idbar-jargao{
  font-family:"IBM Plex Mono",ui-monospace,Consolas,monospace;font-size:10px;letter-spacing:.2em;
  text-transform:uppercase;color:#5D6E85;white-space:nowrap;
  padding-left:18px;border-left:1px solid #1A2C46;margin-left:2px
}
@media (max-width:1080px){.dkd-idbar-jargao{display:none}}
@media (max-width:680px){
  .dkd-idbar-suite{margin-left:0;order:3;width:100%%;text-align:center}
  .dkd-idbar-nome{font-size:22px}
}
@media print{.dkd-idbar{display:none}}

/* ---- marca antiga do portal: escondida por CSS, mantida no DOM --------- */
%(neutraliza)s
"""

BARRA = """<div class="dkd-idbar" id="dkd-idbar" style="--dkd-mod:%(cor)s">
  <div class="dkd-idbar-in">
    <img class="dkd-idbar-emb" src="%(emblema)s" alt="" aria-hidden="true">
    <span class="dkd-idbar-txt">
      <span class="dkd-idbar-nome">DKD<sup>&#8482;</sup></span>
      <span class="dkd-idbar-sub">%(rotulo)s</span>
    </span>
    <span class="dkd-idbar-jargao">%(jargao)s</span>
    <span class="dkd-idbar-suite">%(suite)s</span>
  </div>
</div>
"""

# Cada portal tem a sua própria marca antiga. Escondemos só o que duplica.
NEUTRALIZA = {
    # portal fiscal — header.topbar > .brand · o topo fixo desce para abaixo da faixa
    "fiscal": ".brand > img{display:none}\n.brand-name{display:none}\n"
              ".brand-sub{font-size:12.5px;letter-spacing:.04em;color:#a8b4bd;text-transform:none}\n"
              "header.topbar{padding-top:8px}\n"
              ".topo-fixo{top:var(--dkd-h)}",
    # portal de gestão financeira — #top > .r1 > #marca · idem, e o cofre abre abaixo
    "gestao": "#marca > img{display:none}\n#marca .nome{display:none}\n"
              "#marca .sub2{font-size:12.5px;color:#cbd5e1;font-weight:600}\n"
              "#marca{gap:0}\n"
              "#top{top:var(--dkd-h)}\n"
              "#cofre{align-items:flex-start;padding-top:calc(var(--dkd-h) + 26px)}\n"
              "#splash{padding-top:var(--dkd-h)}\n"
              "/* a tela do cofre esconde tudo menos ela; a faixa da marca, que\n"
              "   não carrega dado nenhum, volta para o cliente ver de quem é o portal */\n"
              "html body.cf-lock > #dkd-idbar.dkd-idbar{display:block !important}",
    # console Alpha Invest e Asset Intelligence — .topbar > .topbar-left > .logo
    "alpha":  ".topbar .logo > i{display:none}\n"
              ".topbar .logo{font-size:13px;color:#cbd5e1;font-weight:600}\n"
              ".topbar{top:var(--dkd-h)}",
    "asset":  ".topbar .logo > i{display:none}\n"
              ".topbar .logo{font-size:13px;color:#cbd5e1;font-weight:600}\n"
              ".topbar{top:var(--dkd-h)}",
    "hub":    ".topbar .logo > i{display:none}\n"
              ".topbar .logo{font-size:13px;color:#cbd5e1;font-weight:600}\n"
              ".topbar{top:var(--dkd-h)}",
}


def titulo_padrao(mod):
    rotulo, titulo, _ = MODULOS[mod]
    if mod == "hub":
        return f"{SUITE} — Portal Integrado | {EMPRESA}"
    return f"{SUITE} — {titulo} | {EMPRESA}"


def _limites(html):
    """Onde termina o <head> de verdade e onde começa o <body> de verdade.

    Os portais trazem bibliotecas embutidas (SheetJS, por exemplo) que carregam
    '</head>' e '<title>' dentro de textos de JavaScript. Mexer no primeiro que
    aparecer quebra a biblioteca — e o portal junto. A âncora confiável é a tag
    <body> em início de linha; o </head> que vale é o último antes dela.
    """
    m = re.search(r"^<body[^>]*>", html, re.M) or re.search(r"^[ \t]*<body[^>]*>", html, re.M)
    if not m:
        raise SystemExit("não achei a tag <body> em início de linha — arquivo fora do padrão")
    fim_head = html.rfind("</head>", 0, m.start())
    if fim_head < 0:
        raise SystemExit("não achei o </head> que fecha o cabeçalho real")
    return fim_head, m.end()


def padroniza(html, mod):
    rotulo, _, cor = MODULOS[mod]

    # limpa uma padronização anterior antes de tudo, para poder rodar de novo
    html = re.sub(r'<style id="dkd-identidade">.*?</style>\n?', "", html, flags=re.S)
    html = re.sub(r'<div class="dkd-idbar"[^>]*>.*?\n</div>\n', "", html, flags=re.S)

    fim_head, _ = _limites(html)
    head, resto = html[:fim_head], html[fim_head:]

    # 1. título da guia — só dentro do cabeçalho real
    head, n = re.subn(r"<title>.*?</title>", "<title>%s</title>" % titulo_padrao(mod),
                      head, count=1, flags=re.S)
    if not n:
        head = head.replace("<head>", "<head>\n<title>%s</title>" % titulo_padrao(mod), 1)

    # 2. ícone da guia — fora os antigos, entra o emblema DKD
    head = re.sub(r'\s*<link[^>]*rel="(?:shortcut )?icon"[^>]*>', "", head)
    head = re.sub(r'\s*<link[^>]*rel="apple-touch-icon"[^>]*>', "", head)
    head = re.sub(r'\s*<meta[^>]*name="theme-color"[^>]*>', "", head)
    icones = ('\n<link rel="icon" type="image/png" href="%s">'
              '\n<link rel="apple-touch-icon" href="%s">'
              '\n<meta name="theme-color" content="#030913">' % (FAVICON, TOQUE))
    head = re.sub(r"(<meta charset=[^>]*>)", lambda g: g.group(1) + icones,
                  head, count=1, flags=re.I)

    html = head + resto

    # 3. estilo da faixa — logo antes do <body>, e não dentro do <head>.
    #    Alguns portais têm blocos <style> soltos DEPOIS do </head>; entrando
    #    aqui, a identidade DKD é sempre a última palavra sobre o cabeçalho.
    estilo = "<style id=\"dkd-identidade\">\n" + (CSS % {
        "fontes": FONTES,
        "neutraliza": NEUTRALIZA.get(mod, ""),
    }) + "\n</style>\n"
    m = re.search(r"^<body[^>]*>", html, re.M) or re.search(r"^[ \t]*<body[^>]*>", html, re.M)
    html = html[:m.start()] + estilo + html[m.start():]

    # 4. a faixa em si, como primeiro elemento do corpo real
    _, ini_body = _limites(html)
    barra = BARRA % {"cor": cor, "emblema": EMBLEMA, "rotulo": rotulo,
                     "jargao": JARGAO, "suite": SUITE}
    return html[:ini_body] + "\n" + barra + html[ini_body:]


def roda(entrada, saida, mod):
    html = io.open(entrada, encoding="utf-8", errors="strict").read()
    novo = padroniza(html, mod)
    os.makedirs(os.path.dirname(saida) or ".", exist_ok=True)
    io.open(saida, "w", encoding="utf-8").write(novo)
    print("%-46s %8.0f KB → %s" % (mod, os.path.getsize(saida) / 1024, os.path.basename(saida)))


if __name__ == "__main__":
    if len(sys.argv) == 4:
        roda(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        raise SystemExit("uso: padroniza_portais.py <entrada.html> <saida.html> "
                         "<gestao|alpha|asset|fiscal|hub>")
