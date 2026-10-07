# dkdtecnologia.com — site institucional

Site estático da **DKD Tecnologia e Inovação**. Sem framework e sem dependências: só Python 3 para gerar.

```
src/          a fonte — é aqui que se edita
assets/       marca, imagens e fontes próprias (entram no dist na geração)
dist/         o que o Cloudflare serve — GERADO, nunca edite à mão
ferramentas/  padroniza_portais.py — aplica a identidade DKD nos portais
CUSTOMIZAR.md o mapa numerado de tudo que dá para mudar e onde
```

16 páginas, identidade azul-noite, fontes próprias (Archivo · Inter · IBM Plex Mono), sem
nenhuma chamada a servidor de terceiros.

---

## Gerar

```bash
python3 src/build.py
```

Reescreve `dist/` e gera `DKD_Site_Institucional_previa.html` — o site inteiro num arquivo só,
para revisar sem publicar.

## Ver no navegador

```bash
python3 -m http.server 8000 --directory dist
```

Precisa ser por servidor: as páginas usam caminhos absolutos (`/assets/…`).

---

## Publicar (Cloudflare Workers + assets estáticos)

O site roda como o Worker **`dkdtecnologia-com`** (ver `wrangler.jsonc`), ligado a este
repositório pelo Workers Builds: todo `git push` na `main` publica em 1–2 minutos
(`PUBLICAR_SITE.bat` faz o push). O `dist/` já vai pronto; o Worker atende `/api/contato` e,
desde a V10.1_web, o cadastro e as licenças (seção abaixo).

`run_worker_first` no `wrangler.jsonc` manda `/api/*` e `/admin` direto para o Worker. Sem isso a
camada de assets atende primeiro as navegações do navegador e responde **405** ao envio dos
formulários (contato e cadastro) e **404** ao `/admin` — testado com o `wrangler dev` em 05/10/2026.

Variáveis do formulário (Worker → Settings → Variables and Secrets, tipo Secret):
`RESEND_API_KEY`, `DESTINO`, `REMETENTE`, `TURNSTILE_SECRET`.
Binding opcional `LEADS` (KV) — se usado, declarar em `wrangler.jsonc`, senão o deploy o remove.

O redirecionamento `www → apex` **não** funciona pelo `_redirects` em Workers: fazer por
Rules → Redirect Rules no painel do domínio.

---

## Cadastro e licenças — DKD Financial Tools AI (V10.1_web)

O módulo de Gestão Financeira passou a ser vendido também **para download**: o cliente se
cadastra em `/cadastro/`, baixa o portal e ativa com um código de 6 números que o servidor manda
ao e-mail cadastrado. Avaliação de 30 dias contados da primeira ativação.

| Rota | O quê |
|---|---|
| `POST /api/cadastro` | formulário do site → cria o cliente no D1 e manda o e-mail de boas-vindas com o download |
| `POST /api/licenca/codigo` · `/ativar` · `/renovar` | chamadas do portal (CORS aberto, JSON) |
| `/admin` e `/api/admin/*` | painel da DKD — senha `ADMIN_TOKEN`; proteja também com o Cloudflare Access |

Arquivos: `worker/licencas.js`, `worker/admin.js`, `worker/schema.sql`, `downloads/` (zip do
portal — o build só publica build de **produção**). Passo a passo completo de implantação
(D1, segredos, e-mail, Turnstile, Access, chave de produção): `GUIA_DE_IMPLANTACAO.md`, na pasta
da V10.1_web.

Segredos do Worker (tipo Secret): `LICENCA_CHAVE_PRIVADA`, `ADMIN_TOKEN`, `RESEND_API_KEY`,
`TURNSTILE_SECRET`; opcionais: `REMETENTE_LICENCAS`, `DOWNLOAD_URL`, `CODIGO_SAL`,
`AVALIACAO_DIAS`, `LIMITE_DISPOSITIVOS`. Sem o banco `LICENCAS`, as rotas respondem "em
manutenção" e o resto do site segue no ar.

---

## Regras de ouro

1. **Editar `src/` e `assets/`, nunca `dist/`.** Qualquer alteração no HTML gerado
   desaparece na próxima geração.
2. **Rodar `python3 src/build.py` antes de commitar.** O `dist/` versionado precisa
   refletir a fonte.
3. **Uma branch por rodada de mudanças.** A prévia sai automática e a produção fica
   intacta até você aprovar.

---

## Pendências conhecidas

| Onde | O quê |
|---|---|
| `src/shell.py` → `TURNSTILE_SITEKEY` | vazio — os formulários de contato e de cadastro estão sem proteção anti-robô (o cadastro manda e-mail: configure antes de divulgar) |
| `wrangler.jsonc` → `d1_databases` | comentado até o banco `dkd-licencas` ser criado — sem ele o cadastro responde "em manutenção" |
| `downloads/` | vazio até o zip de produção ser gerado no `DKD_Chaves_Licenca.html` — sem ele o download do cadastro dá 404 |
| `src/pages_b.py` → `MINUTA` | privacidade e termos publicados com aviso de minuta, até a revisão jurídica |
| Formulário de contato | sem `RESEND_API_KEY` e sem KV `LEADS`, o envio falha — configurar um dos dois |
| Caso do cliente-âncora | espaço reservado na home, sem depoimento inventado |

## Fora deste repositório

Os portais (`DKD_IA_Portal.html`, `DKD_Financial_Tools_AI_*`, `DKD_Alpha_Invest_console.html`,
`asset/`, `integrado/`) **não entram aqui**. Eles vão para projetos Pages próprios, um por
subdomínio, atrás do Cloudflare Access — conforme a nota de decisão 04. Misturar os dois faria
uma atualização de texto do site derrubar as ferramentas.
