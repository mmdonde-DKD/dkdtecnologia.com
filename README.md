# dkdtecnologia.com — site institucional

Site estático da **DKD Tecnologia e Inovação**. Sem framework e sem dependências: só Python 3 para gerar.

```
src/          a fonte — é aqui que se edita
assets/       marca, imagens e fontes próprias (entram no dist na geração)
dist/         o que o Cloudflare serve — GERADO, nunca edite à mão
ferramentas/  padroniza_portais.py — aplica a identidade DKD nos portais
CUSTOMIZAR.md o mapa numerado de tudo que dá para mudar e onde
```

15 páginas, identidade azul-noite, fontes próprias (Archivo · Inter · IBM Plex Mono), sem
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
(`PUBLICAR_SITE.bat` faz o push). O `dist/` já vai pronto; o Worker só atende `/api/contato`.

Variáveis do formulário (Worker → Settings → Variables and Secrets, tipo Secret):
`RESEND_API_KEY`, `DESTINO`, `REMETENTE`, `TURNSTILE_SECRET`.
Binding opcional `LEADS` (KV) — se usado, declarar em `wrangler.jsonc`, senão o deploy o remove.

O redirecionamento `www → apex` **não** funciona pelo `_redirects` em Workers: fazer por
Rules → Redirect Rules no painel do domínio.

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
| `src/shell.py` → `TURNSTILE_SITEKEY` | vazio — o formulário de contato está sem proteção anti-robô |
| `src/pages_b.py` → `MINUTA` | privacidade e termos publicados com aviso de minuta, até a revisão jurídica |
| Formulário de contato | sem `RESEND_API_KEY` e sem KV `LEADS`, o envio falha — configurar um dos dois |
| Caso do cliente-âncora | espaço reservado na home, sem depoimento inventado |

## Fora deste repositório

Os portais (`DKD_IA_Portal.html`, `DKD_Financial_Tools_AI_*`, `DKD_Alpha_Invest_console.html`,
`asset/`, `integrado/`) **não entram aqui**. Eles vão para projetos Pages próprios, um por
subdomínio, atrás do Cloudflare Access — conforme a nota de decisão 04. Misturar os dois faria
uma atualização de texto do site derrubar as ferramentas.
