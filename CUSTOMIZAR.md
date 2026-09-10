# Mapa de customização — dkdtecnologia.com

**Atualizado em 10/09/2026**, depois da rodada que trouxe a identidade azul-noite, as fontes
próprias, a página de Portais e a oferta de diagnóstico gratuito.

Este documento existe para você pedir uma mudança sem precisar descrevê-la: cite o número,
mande o texto novo, e eu edito a fonte e reconstruo.

---

## 1 · Identidade — `src/theme.py`, bloco `IDENTIDADE DKD TECNOLOGIA E INOVAÇÃO`

O site é **escuro por definição** — não há tema claro. As cores estão todas pintadas
explicitamente, então ele se comporta igual em qualquer navegador.

| # | O quê | Variável | Hoje |
|---|---|---|---|
| 1.1 | Fundo institucional | `--void` `--bg` `--bg-2` | `#030913` · `#060E1B` · `#08131F` |
| 1.2 | Superfícies e linhas | `--surface*` `--line*` | azul-noite metálico |
| 1.3 | Texto | `--txt` `--txt-2` `--txt-3` | `#EDF3F9` → `#7A8CA3` |
| 1.4 | Prata da marca | `--prata-1/2/3` | `#F2F5F7` → `#8E9AA4` |
| 1.5 | Azul institucional | `--dkd` `--dkd-2` `--dkd-dim` | `#3FA9F0` |
| 1.6 | Cor de cada módulo | `--m-gestao` `--m-alpha` `--m-asset` `--m-fiscal` | verde esmeralda → azul royal |
| 1.7 | Sinalização | `--ok` `--warn` `--crit` | verde · âmbar · vermelho |
| 1.8 | Tipografia | `--font-display` `--font-body` `--font-mono` | Archivo · Inter · IBM Plex Mono |
| 1.9 | Arquivos de fonte | `assets/fonts/*.woff2` + `assets/fonts.css` | 11 faces próprias, sem Google Fonts |
| 1.10 | Logotipo e emblema | `assets/dkd-emblema*.png`, `dkd-marca.jpg` | aplicados |
| 1.11 | Ícones da guia | `assets/favicon-32/64.png`, `apple-touch-icon.png` | aplicados |
| 1.12 | Imagem de compartilhamento | `assets/dkd-og.jpg` | aplicada |

> **Cuidado com `assets/fonts.css`.** Ele é copiado literalmente para `dist/`. Se as chaves
> `{ }` forem duplicadas (`{{ }}`), o navegador descarta todas as regras `@font-face` em
> silêncio e o site volta para a fonte do sistema. Foi exatamente o que aconteceu na versão
> anterior. Depois de mexer nele, confira no navegador: `document.fonts.size` tem que ser 11.

---

## 2 · Empresa, menu e rodapé — `src/shell.py`

| # | O quê | Variável | Estado |
|---|---|---|---|
| 2.1 | Razão social | `RAZAO` | DKD Tecnologia e Inovação Ltda |
| 2.2 | Marca curta | `MARCA` | DKD Tecnologia e Inovação |
| 2.3 | CNPJ | `CNPJ` | 59.890.881/0001-06 |
| 2.4 | Cidade | `CIDADE` | Caxias do Sul / RS |
| 2.5 | E-mail comercial | `EMAIL` | contato@dkdtecnologia.com |
| 2.6 | E-mail do encarregado | `EMAIL_DPO` | privacidade@dkdtecnologia.com |
| 2.7 | **WhatsApp** | `WHATSAPP` | ⚠ ainda `55XXXXXXXXXXX` |
| 2.8 | Mensagem inicial do WhatsApp | `WHATS_MSG` | escrita |
| 2.9 | **Chave do Turnstile** | `TURNSTILE_SITEKEY` | ⚠ vazia |
| 2.10 | Nome da suíte | `SUITE` | DKD Financial Tools AI |
| 2.11 | Itens do menu | `NAV` | Módulos · Portais · Preços · Segurança · Sobre · Contato |
| 2.12 | Botões do topo | `topbar()` | Entrar · Diagnóstico gratuito |
| 2.13 | Rodapé | `footer()` | colunas, avisos CVM e fiscal |

---

## 3 · Página inicial — `src/pages_a.py`, `HOME`

| # | Seção |
|---|---|
| 3.1 | Manchete e subtítulo |
| 3.2 | Botões do topo da home |
| 3.3 | Diagrama do acesso (`HERO_SVG`) |
| 3.4 | Faixa do jargão — "tecnologia que impulsiona na busca pelo novo" |
| 3.5 | Faixa de urgência da reforma e a data da contagem (`URGENCIA`) |
| 3.6 | Oferta do diagnóstico gratuito |
| 3.7 | Portas por perfil |
| 3.8 | Cards dos quatro módulos |
| 3.9 | "Três regras não negociáveis" |
| 3.10 | Faixa de segurança |
| 3.11 | Preço e prova de retorno |
| 3.12 | Chamada final |

**Reservado:** o caso do cliente-âncora entra depois de 3.8, quando a firma autorizar.

---

## 4 · Módulos e portais — `src/pages_a.py` e `src/pages_b.py`

| # | Página | Variável |
|---|---|---|
| 4.1 | Fiscal e Tributária | `FISCAL` |
| 4.2 | Gestão Financeira CPF e CNPJ | `GESTAO` |
| 4.3 | Alpha Invest AI | `ALPHA` |
| 4.4 | Asset Intelligence AI | `ASSET` |
| 4.5 | Hub dos quatro | `PRODUTOS` |
| 4.6 | **Portais** (vitrine das ferramentas) | `PORTAIS_PAGE` |
| 4.7 | **Diagnóstico gratuito** | `DIAGNOSTICO` |
| 4.8 | Aviso da CVM nas páginas de investimento | `DISCLAIMER_CVM` — mantenha |

---

## 5 · Preços — `src/pages_b.py`, `PRECOS`

| # | O quê |
|---|---|
| 5.1 | Planos do módulo Fiscal |
| 5.2 | Planos de Gestão, Alpha e Asset |
| 5.3 | Tabela de adicionais |
| 5.4 | Perguntas sobre cobrança |
| 5.5 | Reajuste e desconto anual |

---

## 6 · Apoio e legal — `src/pages_b.py`

| # | Página | Variável | Observação |
|---|---|---|---|
| 6.1 | Segurança e LGPD | `SEGURANCA` | encurta a due diligence do comprador |
| 6.2 | Sobre a DKD | `SOBRE` | |
| 6.3 | Contato | `CONTATO` | formulário + canais diretos |
| 6.4 | Privacidade | `PRIVACIDADE` | ⚠ minuta |
| 6.5 | Termos de uso | `TERMOS` | ⚠ minuta |
| 6.6 | Aviso de minuta | `MINUTA` | remova quando o advogado aprovar |
| 6.7 | Prévia da área logada | `APP_HUB` | vai para `app.`, não para o site público |

---

## 7 · Estrutura e operação — `src/build.py`

| # | O quê |
|---|---|
| 7.1 | Adicionar, remover ou reordenar páginas — lista `PAGES` |
| 7.2 | Título e descrição que aparecem no Google |
| 7.3 | Endereços curtos e redirecionamentos — `_redirects` |
| 7.4 | Regras para robôs — `robots.txt` |
| 7.5 | Cabeçalhos de segurança e CSP — `_headers` |
| 7.6 | Envio do formulário — `functions/api/contato.js` |
| 7.7 | Prévia de arquivo único — usa `assets/fonts-embed.css` |

---

## 8 · Portais — `ferramentas/padroniza_portais.py`

Aplica a identidade DKD no cabeçalho e na guia do navegador de cada portal: troca o ícone,
padroniza o título como «Módulo — DKD Financial Tools AI», injeta a faixa de identidade com a
cor do módulo e esconde por CSS a marca antiga sem remover nada do DOM.

```bash
python3 ferramentas/padroniza_portais.py                    # usa o mapa PORTAIS do script
python3 ferramentas/padroniza_portais.py entrada.html saida.html gestao
```

Rode de novo a cada versão nova de portal. Os arquivos dos portais ficam fora deste
repositório — cada um vai para o seu próprio projeto no Cloudflare, atrás do Access.

---

## 9 · Como pedir para ser rápido

- **Cite o número.** `"3.1: trocar a manchete para X"` vale mais que três parágrafos.
- **Mande o texto pronto** quando tiver opinião formada.
- **Para o resto, descreva o efeito, não a solução.** *"a home demora demais para chegar no
  preço"* leva mais longe que *"tira a terceira seção"*.
- **Junte tudo num lote.** Dez mudanças custam o mesmo que uma.
- **Diga o que não pode mudar** — frases travadas por motivo comercial ou jurídico.
