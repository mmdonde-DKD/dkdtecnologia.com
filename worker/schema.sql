-- =====================================================================
-- DKD Financial Tools AI — servidor de licenças (Cloudflare D1)
--
-- Banco: dkd-licencas   ·   binding no Worker: LICENCAS
-- Aplicar uma vez, pelo painel (D1 → dkd-licencas → Console → colar e
-- executar) ou pela linha de comando:
--   npx wrangler d1 execute dkd-licencas --remote --file=worker/schema.sql
--
-- LGPD: guarda o mínimo para emitir e controlar a licença — identificação
-- do cliente (base legal: execução de contrato), os computadores ativados e
-- o registro dos eventos. Nenhum dado financeiro do cliente passa por aqui.
-- =====================================================================

CREATE TABLE IF NOT EXISTS clientes (
  id                   INTEGER PRIMARY KEY AUTOINCREMENT,
  email                TEXT NOT NULL UNIQUE,          -- sempre minúsculo
  nome                 TEXT NOT NULL,
  empresa              TEXT,                          -- razão social, quando PJ
  tipo                 TEXT NOT NULL DEFAULT 'PF',    -- PF | PJ
  documento            TEXT,                          -- CPF: 11 dígitos · CNPJ: 14 caracteres, numérico ou alfanumérico
  telefone             TEXT,
  cidade               TEXT,
  uf                   TEXT,
  origem               TEXT,                          -- de onde veio o cadastro
  plano                TEXT NOT NULL DEFAULT 'avaliacao',
  status               TEXT NOT NULL DEFAULT 'ativo', -- ativo | suspenso | cancelado
  validade             TEXT,                          -- AAAA-MM-DD; nula até a 1ª ativação da avaliação
  limite_dispositivos  INTEGER NOT NULL DEFAULT 2,
  serie                TEXT UNIQUE,                   -- DKD-GF-2026-0001
  aceite_em            TEXT,                          -- aceite dos Termos e da Política de Privacidade
  ip_cadastro          TEXT,
  obs                  TEXT,
  criado_em            TEXT NOT NULL,
  atualizado_em        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dispositivos (
  id                 INTEGER PRIMARY KEY AUTOINCREMENT,
  cliente_id         INTEGER NOT NULL REFERENCES clientes(id),
  dispositivo        TEXT NOT NULL,                   -- identificador gerado pelo portal
  rotulo             TEXT,                            -- "Windows · Chrome"
  versao             TEXT,
  ativo              INTEGER NOT NULL DEFAULT 1,
  primeira_ativacao  TEXT NOT NULL,
  ultimo_contato     TEXT NOT NULL,
  UNIQUE (cliente_id, dispositivo)
);

CREATE TABLE IF NOT EXISTS codigos (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  cliente_id   INTEGER NOT NULL REFERENCES clientes(id),
  dispositivo  TEXT NOT NULL,
  codigo_hash  TEXT NOT NULL,                         -- SHA-256, nunca o código em claro
  expira_em    TEXT NOT NULL,                         -- ISO 8601
  tentativas   INTEGER NOT NULL DEFAULT 0,
  usado        INTEGER NOT NULL DEFAULT 0,
  ip           TEXT,
  criado_em    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS eventos (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  cliente_id  INTEGER,
  tipo        TEXT NOT NULL,   -- cadastro | codigo | ativacao | renovacao | recusa | codigo_errado | admin | email
  detalhe     TEXT,
  ip          TEXT,
  criado_em   TEXT NOT NULL
);

-- só existe para os testes locais (MODO_TESTE=1): o e-mail é gravado aqui em vez de enviado
CREATE TABLE IF NOT EXISTS emails_teste (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  para       TEXT NOT NULL,
  assunto    TEXT NOT NULL,
  texto      TEXT,
  criado_em  TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_disp_cliente    ON dispositivos (cliente_id);
CREATE INDEX IF NOT EXISTS idx_cod_cliente     ON codigos (cliente_id, criado_em);
CREATE INDEX IF NOT EXISTS idx_cod_ip          ON codigos (ip, criado_em);
CREATE INDEX IF NOT EXISTS idx_evt_cliente     ON eventos (cliente_id, criado_em);
CREATE INDEX IF NOT EXISTS idx_evt_ip_tipo     ON eventos (ip, tipo, criado_em);
