# DKD Tecnologia e Inovação — site institucional e portais

**Atualizado em 09/09/2026.** Identidade única no site e nos cinco portais, e
uma página **Portais** no site que abre cada um deles.

---

## 1. Como abrir para a reunião

### Jeito recomendado — `ABRIR_APRESENTACAO.bat`

Clique duas vezes. Ele sobe um servidor local nesta pasta e abre o site sozinho
no navegador. Uma janela preta fica aberta enquanto a apresentação roda; feche-a
no fim.

**Por que este é o jeito certo:** servido por HTTP, *tudo* funciona — inclusive
o Asset Intelligence e o Portal Integrado, que são aplicações React e não
carregam por clique duplo no arquivo. Nada é publicado na internet: o servidor
escuta só em `127.0.0.1`, a sua própria máquina.

### Jeito simples — `DKD_Site_Institucional_previa.html`

Clique duas vezes no arquivo. O site inteiro abre do disco, sem internet.
Funciona igual, com uma ressalva: o Asset e o Portal Integrado abrem só o
cabeçalho, sem conteúdo.

> **Não mova o `.html` sozinho para outro lugar.** Ele e a pasta `portais/`
> precisam ficar lado a lado — é assim que os botões acham cada portal. Se
> precisar levar a apresentação para outra máquina, leve a pasta inteira.

### Roteiro sugerido, 8 minutos

1. **Início** — a proposta e os quatro módulos.
2. **Módulos** → um módulo. A cor do cabeçalho e da página muda junto.
3. **Portais** — a tela nova, com os cinco portais lado a lado.
4. **"Abrir o portal ↗"** — o portal de verdade abre em outra aba, com o mesmo
   cabeçalho DKD. É este o momento que vende.
5. **Preços** — tabela aberta, sem "agende uma demonstração".

---

## 2. A página Portais

Nova no menu, entre **Módulos** e **Preços**. Cinco cartões, cada um na cor do
seu módulo, com o botão **"Abrir o portal ↗"**. Os mesmos botões aparecem
também na home, na tabela de Módulos, em cada página de módulo e na tela
**Minhas ferramentas** (o "Entrar ↗" do cabeçalho leva até ela).

No **site publicado**, esses botões apontam para os subdomínios
(`atc.`, `gestao.`, `alpha.`, `asset.dkdtecnologia.com`), com o Cloudflare
Access na frente. É o mesmo código: quem troca o endereço é o build.

### O que cada portal precisa

| Portal | Clique duplo no `.html` | Com o `.bat` | Com o servidor Node do projeto |
|---|---|---|---|
| Fiscal e Tributária | **completo** | completo | — |
| Planejamento e Gestão Financeira | **completo** | completo | — |
| Alpha Invest AI | tela sim, cotações não | tela sim, cotações não | completo |
| Asset Intelligence AI | só o cabeçalho | **tela completa**, sem dados | completo |
| Portal Integrado | só o cabeçalho | **tela completa**, sem dados | completo |

Os três de investimento buscam dados no `server.js` de cada projeto. Para a
demonstração com dados reais, rode antes o `_run_alpha.bat`, o `start.bat` do
Asset e o do Portal Integrado.

**Na frente do cliente, clique com segurança nos dois primeiros.**

---

## 3. O que tem na pasta

```
ABRIR_APRESENTACAO.bat              o jeito recomendado de abrir
DKD_Site_Institucional_previa.html  o site inteiro num arquivo só
LEIA-ME.md                          este arquivo
portais/
  DKD_IA_Portal.html                            Fiscal e Tributária
  DKD_Financial_Tools_AI_V43_1_ZERADA_...html   Planejamento e Gestão Financeira
  DKD_Alpha_Invest_console.html                 Alpha Invest AI
  asset/index.html        (+ assets)            Asset Intelligence AI
  integrado/index.html    (+ assets)            Portal Integrado
site/                               pacote para publicar no Cloudflare Pages
ferramentas/                        script de padronização e código-fonte
```

O Asset e o Portal Integrado vieram com os arquivos de apoio deles
(`dkd-ui.css`, `dkd-ui.js`, `hub.js` e o *bundle* React), cada um na sua
subpasta, com os caminhos ajustados de absolutos para relativos — é o que
faz os dois abrirem daqui.

**Os arquivos originais dos projetos não foram alterados.** Estas são cópias.

---

## 4. O que mudou nos portais

Cada um ganhou **só o cabeçalho e a padronização visual**: a faixa de
identidade DKD fixa no topo — emblema, DKD, nome do módulo, jargão e a cor do
módulo —, o ícone da guia e o título padronizados, com o cabeçalho do próprio
portal grudando logo abaixo da faixa. A marca antiga foi escondida por CSS,
**sem sair do DOM**, para não quebrar o JavaScript que se apoia nela (o selo de
licença do portal financeiro, por exemplo, continua aparecendo).

**Nenhuma linha da lógica foi tocada.** Os cinco foram abertos no navegador:
zero erro de JavaScript.

No portal financeiro, a tela do cofre esconde tudo menos ela mesma. Abri uma
exceção **só para a faixa da marca**, que não carrega dado nenhum — assim a
primeira tela que o cliente vê já é DKD. O resto da blindagem segue igual.

### Quando sair uma versão nova de um portal

```
cd ferramentas
python padroniza_portais.py "portal_novo.html" "..\portais\portal_novo.html" gestao
```

O último argumento é `gestao`, `alpha`, `asset`, `fiscal` ou `hub`. Rodar duas
vezes no mesmo arquivo não duplica nada. Se você renomear um arquivo de portal,
ajuste o dicionário `PORTAIS` em `src/shell.py` (dentro de
`ferramentas/fonte_do_site.zip`) e rode `python src/build.py` — os links do site
acompanham.

---

## 5. Identidade

| Item | Agora |
|---|---|
| Cor da marca | azul-noite metálico com prata, do emblema DKD IA |
| Tipografia | **Archivo 700/800** nos títulos, **Inter** no texto, **IBM Plex Mono** em números e rótulos |
| Logotipo | emblema DKD IA + wordmark prata + jargão |
| Jargão | **Tecnologia que impulsiona na busca pelo novo** |
| Ícone da guia | emblema DKD, igual no site e nos cinco portais |
| Fontes | servidas pelo próprio domínio — abre igual sem internet |

Cor por módulo — a página inteira assume a cor do módulo em que se está:

| Módulo | Cor | Código |
|---|---|---|
| Planejamento, Controle e Gestão Financeira | verde esmeralda | `#2FCB92` |
| Alpha Invest AI | verde-azulado | `#25C0B4` |
| Asset Intelligence AI | azul ciano | `#3FB0E8` |
| Análise, Simulação e Inteligência Fiscal e Tributária | azul royal | `#5B95F5` |

### Nomes padronizados

Fonte única: `src/shell.py`, dicionário `MODULOS`.

- `DKD Financial Tools AI — Módulo de Planejamento, Controle e Gestão Financeira`
- `DKD Financial Tools AI — Módulo Alpha Invest AI`
- `DKD Financial Tools AI — Módulo Asset Intelligence AI`
- `DKD Financial Tools AI — Módulo de Análise, Simulação e Inteligência Fiscal e Tributária`

**Três decisões que continuam esperando a sua confirmação:**

1. Publiquei **"Módulo de Planejamento, Controle e Gestão Financeira"**; você
   havia escrito "Módulo de Gestão de Planejamento, Controle e Gestão
   Financeira" — o "Gestão de" na frente repetia o "Gestão" do fim.
2. Mantive **"Asset Intelligence AI"** no lugar de "Asset Investment AI", que é
   o nome já usado no portal e na pasta do projeto.
3. Substituí **"DKD TaxVision Analytics"** pelo nome padronizado do módulo
   fiscal. Se TaxVision for sub-marca a manter, ela volta como segunda linha.

### Seção "Quem está por trás"

Escrita a partir da sua trajetória. **Leia antes de mostrar** — é sobre você.

### Preços

Mesmos valores já aprovados, sem o aviso de rascunho interno: Fiscal
R$ 690 / 1.890 / 4.900 por faixa de CNPJs; Gestão R$ 149 / 279 / 690;
Alpha R$ 79 (avançado 149); Asset R$ 99 (avançado 189); Alpha + Asset R$ 199.

---

## 6. Publicar o site — pasta `site/`

**Workers & Pages → Create → Pages → Upload assets**, sobe a pasta `site/`
inteira, e depois **Custom domains** com `dkdtecnologia.com`.

- O formulário de contato precisa das variáveis `RESEND_API_KEY`, `DESTINO` e
  `REMETENTE` no painel. Sem elas, apague o `<form>` de `contato/index.html`.
- As minutas de privacidade e termos continuam com aviso de rascunho visível.
  **Não tire antes da revisão do advogado.**
- O aviso de CVM no rodapé e nas páginas de investimento **não pode sair**.
- A contagem regressiva está fixada em **30/09/2026**; depois disso troque a
  data em `site/assets/dkd.js` para o próximo marco.
- Os botões dos portais só respondem depois que cada portal estiver no ar como
  projeto Pages próprio, com o Access na frente.

---

## 7. Mexer no visual depois

Tudo que é identidade está no topo de `src/theme.py`, no bloco
`IDENTIDADE DKD`. Trocou lá, rodou `python src/build.py`, e site e prévia saem
atualizados juntos. O código-fonte está em `ferramentas/fonte_do_site.zip`.
