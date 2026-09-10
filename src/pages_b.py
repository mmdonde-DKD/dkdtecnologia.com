# -*- coding: utf-8 -*-
"""Preços, segurança, sobre, contato, legal e a prévia da área logada."""

from shell import APP, EMAIL, EMAIL_DPO, RAZAO, CNPJ, CIDADE, AVISO_CVM, formulario, whats_link

# ------------------------------------------------------------------ PREÇOS
# TODO PREÇO: os valores do módulo Fiscal vêm do Plano de Comercialização
# aprovado (doc 01). Os valores dos outros três módulos são PROPOSTA e
# precisam da sua validação — veja LEIA-ME.md, item 1.
PRECOS = """
<section class="band band--hero band--surface">
  <div class="container">
    <p class="eyebrow">Preços</p>
    <h1>Tabela aberta. Sem “agende uma demonstração”.</h1>
    <p class="lead" style="margin-top:18px">Todos os planos são por assinatura, com desconto de 15% no pagamento anual antecipado.
    Reajuste anual por IPCA mais 4 pontos percentuais, escrito em contrato desde o primeiro dia — aumento previsto é aceito; aumento surpresa é motivo de troca de fornecedor.</p>
  </div>
</section>

<section class="band">
  <div class="container">
    <!-- ================= REVISAR ANTES DE PUBLICAR =====================
         Remova o bloco .todo abaixo depois de validar os preços dos
         módulos Gestão Financeira, Alpha Invest e Asset Intelligence.
         Os preços do módulo Fiscal vêm do doc 01 e já estão aprovados.
         ================================================================ -->

    <p class="eyebrow">DKD Financial Tools AI · Módulo de Análise, Simulação e Inteligência Fiscal e Tributária</p>
    <h2>Por faixa de CNPJs sob gestão</h2>
    <p class="sec-intro lead">A métrica de cobrança acompanha a unidade econômica do escritório e cresce junto com a carteira.
    Você varre os trezentos clientes — não só os que já reclamaram.</p>
    <div class="plans">
      <div class="plan">
        <span class="chip">Diagnóstico</span>
        <div class="price">R$ 0</div><div class="per">teste de 14 dias · sem cartão</div>
        <ul><li>3 CNPJs</li><li>1 usuário</li><li>100 créditos de análise</li><li>Comparador de regimes</li><li>Copiloto limitado</li></ul>
        <div class="foot"><a class="btn btn--sm" href="/contato/">Começar</a></div>
      </div>
      <div class="plan">
        <span class="chip">Essencial</span>
        <div class="price">R$ 690</div><div class="per">por mês, no plano anual · R$ 810 mês a mês</div>
        <ul><li>Até 25 CNPJs</li><li>3 usuários</li><li>500 créditos por mês</li><li>Painel de carteira</li><li>Dossiê exportável</li><li>Suporte por e-mail em 24 h úteis</li></ul>
        <div class="foot"><a class="btn btn--sm" href="/contato/">Contratar</a></div>
      </div>
      <div class="plan plan--pick">
        <span class="chip chip--live">Profissional</span>
        <div class="price">R$ 1.890</div><div class="per">por mês, no plano anual · R$ 2.220 mês a mês</div>
        <ul><li>Até 100 CNPJs</li><li>10 usuários</li><li>2.500 créditos por mês</li><li>Auditoria de documentos fiscais</li><li>Simulador de split payment</li><li>1 integração com sistema contábil</li></ul>
        <div class="foot"><a class="btn btn--sm btn--solid" href="/contato/">Contratar</a></div>
      </div>
      <div class="plan">
        <span class="chip">Corporate</span>
        <div class="price">R$ 4.900</div><div class="per">por mês, no plano anual · R$ 5.760 mês a mês</div>
        <ul><li>Até 400 CNPJs</li><li>30 usuários</li><li>10.000 créditos por mês</li><li>Conciliação da apuração assistida</li><li>3 integrações · API · white-label</li><li>Gerente de sucesso dedicado</li></ul>
        <div class="foot"><a class="btn btn--sm" href="/contato/">Falar com a DKD</a></div>
      </div>
    </div>
    <p class="tiny" style="margin-top:14px">Acima de 400 CNPJs, o plano Rede/Enterprise começa em R$ 9.800 por mês com SLA contratual.
    Implantação única: R$ 1.500 no Essencial, R$ 4.500 no Profissional, R$ 12.000 no Corporate.
    Prova de conceito de 30 dias sobre 20 CNPJs reais: R$ 4.900, abatidos do primeiro ano se houver contratação.</p>
  </div>
</section>

<section class="band band--surface">
  <div class="container">
    <p class="eyebrow">Demais módulos</p>
    <h2>Planejamento e Gestão Financeira, Alpha Invest AI e Asset Intelligence AI</h2>
    <div class="plans" style="grid-template-columns:repeat(3,minmax(0,1fr))">
      <div class="plan">
        <span class="chip">Planejamento e Gestão Financeira · CPF e CNPJ</span>
        <div class="price">R$ 149</div><div class="per">por mês · 1 CNPJ e 1 CPF</div>
        <ul><li>Extratos e faturas ilimitados</li><li>Classificação com regras próprias</li><li>Projeção de 30, 60 e 90 dias</li><li>Pacote para o contador</li></ul>
        <p class="tiny" style="margin-top:12px">Completo, até 3 CNPJs: R$ 279/mês. Versão para escritório, até 20 clientes: R$ 690/mês.</p>
        <div class="foot"><a class="btn btn--sm" href="/contato/">Contratar</a></div>
      </div>
      <div class="plan">
        <span class="chip">Alpha Invest AI</span>
        <div class="price">R$ 79</div><div class="per">por mês · uso pessoal</div>
        <ul><li>Filtros salvos e reaplicáveis</li><li>Comparação com fonte por número</li><li>Leitura de relatórios e comunicados</li><li>Exportação com critérios registrados</li></ul>
        <p class="tiny" style="margin-top:12px">Avançado, com histórico estendido e mais filtros simultâneos: R$ 149/mês.</p>
        <div class="foot"><a class="btn btn--sm" href="/contato/">Contratar</a></div>
      </div>
      <div class="plan">
        <span class="chip">Asset Intelligence AI</span>
        <div class="price">R$ 99</div><div class="per">por mês · uso pessoal</div>
        <ul><li>Concentração recalculada a cada aporte</li><li>Proventos e eventos societários</li><li>Alertas nos seus limites</li><li>Relatório do período</li></ul>
        <p class="tiny" style="margin-top:12px">Avançado, com histórico auditável completo: R$ 189/mês. Alpha e Asset juntos: R$ 199/mês.</p>
        <div class="foot"><a class="btn btn--sm" href="/contato/">Contratar</a></div>
      </div>
    </div>
  </div>
</section>

<section class="band">
  <div class="container">
    <h2>Adicionais do módulo Fiscal e Tributário</h2>
    <div class="tablewrap" style="margin-top:22px">
      <table>
        <caption>Contratáveis a qualquer momento, com cobrança proporcional ao ciclo vigente.</caption>
        <thead><tr><th>Item</th><th class="n">Preço</th></tr></thead>
        <tbody>
          <tr><th scope="row">Bloco de 1.000 créditos extras</th><td class="n">R$ 240</td></tr>
          <tr><th scope="row">Usuário adicional</th><td class="n">R$ 90 / mês</td></tr>
          <tr><th scope="row">CNPJ acima da faixa — Essencial / Profissional / Corporate</th><td class="n">R$ 24 · 18 · 12 / CNPJ / mês</td></tr>
          <tr><th scope="row">White-label nos relatórios do escritório</th><td class="n">R$ 490 / mês</td></tr>
          <tr><th scope="row">API REST e webhooks</th><td class="n">R$ 890 / mês</td></tr>
          <tr><th scope="row">Integração adicional com ERP ou sistema contábil</th><td class="n">R$ 390 / mês</td></tr>
          <tr><th scope="row">Treinamento e certificação DKD (turma de 10)</th><td class="n">R$ 1.200</td></tr>
          <tr><th scope="row">Modalidade local licenciada — o dado não sai da sua máquina</th><td class="n">prêmio de 20% a 30%</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="band band--surface">
  <div class="container">
    <h2>Perguntas sobre cobrança</h2>
    <div style="margin-top:20px;border-top:1px solid var(--rule)">
      <details><summary>Como funcionam os créditos de análise?</summary><div class="ans">Cada plano inclui um volume mensal de créditos, consumidos por classificação, leitura de documento e consulta ao copiloto. Há alerta automático ao atingir 80% do saldo e teto contratual — sem fatura surpresa. Créditos extras são vendidos em blocos com validade de 12 meses.</div></details>
      <details><summary>Posso cancelar quando quiser?</summary><div class="ans">No plano mês a mês, sim, com efeito ao fim do ciclo vigente. No plano anual antecipado, o compromisso é de 12 meses — que é o que sustenta o desconto de 15%. Ao encerrar, você continua com todos os dossiês já exportados.</div></details>
      <details><summary>Qual é a forma de pagamento?</summary><div class="ans">Cartão de crédito com recorrência automática, ou PIX e boleto no plano anual. A nota fiscal de serviço é emitida a cada cobrança confirmada.</div></details>
      <details><summary>E se eu precisar de algo que não está na tabela?</summary><div class="ans">Customizações são contratadas por bolsa de horas — 40, 100 ou 200 horas com desconto progressivo. A propriedade intelectual do que for construído permanece com a DKD, e se o item virar produto em até 12 meses você recebe crédito de 50% do valor pago em mensalidades.</div></details>
    </div>
  </div>
</section>
"""

# --------------------------------------------------------------- SEGURANÇA
SEGURANCA = f"""
<section class="band band--hero band--surface">
  <div class="container">
    <p class="eyebrow">Segurança, privacidade e LGPD</p>
    <h1>As respostas que o seu jurídico vai pedir.</h1>
    <p class="lead" style="margin-top:18px">Esta página existe para encurtar a sua <i>due diligence</i>.
    Se faltar alguma coisa aqui, escreva para <a href="mailto:{EMAIL_DPO}">{EMAIL_DPO}</a> e nós respondemos por escrito.</p>
  </div>
</section>

<section class="band">
  <div class="container">
    <p class="eyebrow">Papéis</p>
    <h2>Quem é controlador e quem é operador</h2>
    <div class="grid g2" style="margin-top:24px">
      <div>
        <h3>Você é o controlador</h3>
        <p class="small">Sobre os dados dos seus clientes que você processa na plataforma. Você decide a finalidade e o tratamento;
        a DKD executa dentro do que o contrato autoriza, e nada além disso.</p>
      </div>
      <div>
        <h3>A DKD é operadora</h3>
        <p class="small">Ao tratar esses dados por sua conta e ordem. Simultaneamente, a DKD é controladora dos dados
        dos próprios usuários da plataforma — cadastro, acesso e faturamento. Os dois papéis são formalizados em instrumentos distintos.</p>
      </div>
    </div>
  </div>
</section>

<section class="band band--surface">
  <div class="container">
    <p class="eyebrow">Infraestrutura</p>
    <h2>Onde o dado fica e quem consegue vê-lo</h2>
    <dl class="kpis" style="margin-bottom:28px">
      <div><dt>Hospedagem</dt><dd>Brasil</dd><small>Aplicação, banco e arquivos em região brasileira.</small></div>
      <div><dt>Modelos de IA</dt><dd>Região BR</dd><small>Inferência em região brasileira, sem transferência internacional a documentar.</small></div>
      <div><dt>Retenção pelo provedor</dt><dd>Zero</dd><small>Conteúdo enviado não é retido para treinamento nem para inspeção humana.</small></div>
      <div><dt>Criptografia</dt><dd>Em trânsito e repouso</dd><small>TLS na borda e criptografia dos arquivos armazenados.</small></div>
    </dl>
    <div class="grid g2">
      <div>
        <h3>Isolamento entre clientes</h3>
        <p class="small">Cada escritório é um inquilino isolado, com o identificador obrigatório em toda consulta e segurança em nível de linha no banco.
        O isolamento é testado automaticamente a cada publicação — vazamento entre inquilinos concorrentes é risco existencial, não incidente.</p>
      </div>
      <div>
        <h3>Controle de acesso</h3>
        <p class="small">Entrada por código de uso único enviado ao seu e-mail, com validade curta. Papéis distintos por usuário,
        sessão com prazo alinhado ao contrato, registro de autenticação e revogação imediata ao encerrar o vínculo — sem esperar senha expirar.</p>
      </div>
      <div>
        <h3>Mascaramento</h3>
        <p class="small">CPF é mascarado nas telas e nos registros. CNPJ é pseudonimizado quando não é necessário ao raciocínio da análise.</p>
      </div>
      <div>
        <h3>Registro e retenção</h3>
        <p class="small">Registros de acesso e de operação mantidos pelo prazo contratado, exportáveis a pedido do controlador.</p>
      </div>
    </div>
  </div>
</section>

<section class="band">
  <div class="container">
    <p class="eyebrow">Programa de privacidade</p>
    <h2>As medidas do artigo 46 da LGPD</h2>
    <div class="grid g2" style="margin-top:24px">
      <div><h3>Inventário de dados pessoais</h3><p class="small">Mapa do que é coletado, para quê, por quanto tempo e com quem é compartilhado.</p></div>
      <div><h3>Encarregado designado</h3><p class="small">Contato publicado e monitorado: <a href="mailto:{EMAIL_DPO}">{EMAIL_DPO}</a>.</p></div>
      <div><h3>Controles de acesso</h3><p class="small">Segundo fator obrigatório nos perfis administrativos e registros retidos por, no mínimo, seis meses.</p></div>
      <div><h3>Plano de resposta a incidentes</h3><p class="small">Procedimento escrito, com simulação anual e comunicação ao controlador dentro do prazo contratual.</p></div>
      <div><h3>Contratos com fornecedores</h3><p class="small">Acordo de tratamento de dados assinado com cada subprocessador, com lista disponível a pedido.</p></div>
      <div><h3>Teste de intrusão</h3><p class="small">Realizado por terceiro independente, com sumário executivo disponível sob acordo de confidencialidade.</p></div>
    </div>
  </div>
</section>

<section class="band band--surface">
  <div class="container">
    <p class="eyebrow">Compromissos e limites</p>
    <h2>O que a DKD garante — e o que não garante</h2>
    <div class="grid g2" style="margin-top:24px">
      <div>
        <h3>Garantimos</h3>
        <ul class="ticks small">
          <li>Disponibilidade contratada, com crédito de serviço em caso de descumprimento</li>
          <li>Rastreabilidade da fonte legal em cada afirmação normativa</li>
          <li>Atualização do corpus normativo em até três dias úteis após a publicação oficial</li>
          <li>Revisão humana identificada antes de qualquer entrega ao cliente final</li>
          <li>Devolução e eliminação dos dados ao término do contrato, no prazo acordado</li>
        </ul>
      </div>
      <div>
        <h3>Não garantimos</h3>
        <ul class="plain small">
          <li><strong>Percentual de acerto da classificação por IA.</strong> Nenhum fornecedor sério garante, e quem garante deveria ser questionado. Garantimos o processo: abstenção abaixo do limiar, fila de revisão e evidência anexada.</li>
          <li><strong>A decisão tributária do cliente.</strong> A análise é insumo técnico. Quem assina é o profissional habilitado, com registro no conselho.</li>
          <li><strong>Resultado de investimento.</strong> Os módulos de investimento são ferramentas operadas pelo usuário e não emitem recomendação.</li>
        </ul>
      </div>
    </div>
    <div class="note note--brand" style="margin-top:30px">
      <span class="tag">Se a sua política proíbe dado em nuvem</span>
      <p>Existe a modalidade local licenciada: o programa roda na máquina do escritório e os arquivos fiscais nunca saem dela.
      Nessa modalidade a DKD deixa de ser operadora dos dados dos seus clientes. O acesso é liberado por chave de ativação assinada,
      com prazo definido em contrato e renovação periódica — que é também o canal pelo qual a atualização normativa chega até você.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="container">
    <h2>Documentos disponíveis</h2>
    <p class="lead sec-intro">Enviamos sob solicitação, por e-mail, em até dois dias úteis.</p>
    <div class="grid g3">
      <div><h3>Contrato-quadro e ordem de serviço</h3><p class="small">Modelo em uso, com anexo por plano contratado.</p></div>
      <div><h3>Acordo de tratamento de dados</h3><p class="small">Objeto, finalidade, duração, medidas, subprocessadores, devolução e eliminação.</p></div>
      <div><h3>Questionário de segurança respondido</h3><p class="small">Formato padrão de mercado, atualizado a cada revisão do programa.</p></div>
    </div>
    <div class="btn-row"><a class="btn btn--solid" href="mailto:{EMAIL_DPO}">Solicitar os documentos</a></div>
  </div>
</section>
"""

# ------------------------------------------------------------------- SOBRE
SOBRE = f"""
<section class="band band--hero band--surface">
  <div class="container">
    <p class="eyebrow">Sobre a DKD</p>
    <h1>Ferramenta boa é a que você consegue defender depois.</h1>
    <p class="lead" style="margin-top:18px">A DKD Tecnologia constrói ferramentas de análise financeira, fiscal e de investimentos
    para quem precisa responder por número diante de outra pessoa: um cliente, um sócio, um fiscal, ou você mesmo daqui a dois anos.</p>
  </div>
</section>

<section class="band">
  <div class="container">
    <div class="hero-grid">
      <div>
        <p class="eyebrow">A tese</p>
        <h2>O mercado entrega resposta. Falta a prova.</h2>
        <p>Ferramenta financeira com inteligência artificial não é escassa. O que é escasso é a que entrega,
        junto com o número, a cadeia inteira que levou até ele: qual arquivo entrou, qual regra foi aplicada,
        qual dispositivo a sustenta, em que versão do motor, com qual data-base, e quem revisou.</p>
        <p>Sem isso, quem assina embaixo está apostando na reputação de um fornecedor.
        Com isso, está apoiado em evidência que sobrevive a uma auditoria — e essa diferença é o produto inteiro.</p>
      </div>
      <div class="card card--pad">
        <p class="eyebrow eyebrow--mute">O que a DKD não é</p>
        <ul class="plain small" style="margin-bottom:0">
          <li>Não é escritório de contabilidade — não fazemos escrituração nem assinamos parecer fiscal.</li>
          <li>Não é consultoria nem análise de valores mobiliários registrada na CVM — não recomendamos ativos.</li>
          <li>Não é instituição financeira — não custodiamos, não intermediamos e não executamos ordens.</li>
          <li>Não é software house — construímos produto, e customização é exceção contratada, não modelo de negócio.</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="band band--surface">
  <div class="container">
    <p class="eyebrow">Como trabalhamos</p>
    <h2>Quatro decisões que atravessam tudo</h2>
    <div class="grid g2" style="margin-top:26px">
      <div><h3>Cálculo separado da linguagem</h3><p class="small">Motor determinístico para número, modelo de linguagem para texto. A fronteira entre os dois não é negociável em nenhum módulo.</p></div>
      <div><h3>Dois motores independentes, testados um contra o outro</h3><p class="small">As regras críticas são implementadas duas vezes, em tecnologias diferentes, e comparadas automaticamente. Divergência bloqueia a publicação.</p></div>
      <div><h3>Vigência é dado, não constante</h3><p class="small">Toda regra carrega o período em que vale. Nenhuma alíquota é escrita no código — o que muda por lei muda por configuração.</p></div>
      <div><h3>Correção de usuário vira teste, não treino</h3><p class="small">Quando você corrige a ferramenta, aquilo entra no conjunto de casos de teste. Nunca ajustamos o modelo automaticamente com a correção de um cliente — seria propagar o erro de um para todos.</p></div>
    </div>
  </div>
</section>

<section class="band band--surface">
  <div class="container">
    <p class="eyebrow">Antes de fechar</p>
    <h2>As cinco perguntas que sempre aparecem</h2>
    <div style="margin-top:24px;border-top:1px solid var(--line)">
      <details><summary>Vocês são uma empresa pequena. E se a DKD fechar?</summary><div class="ans">Pergunta justa, e a
      resposta está no contrato: em caso de encerramento da operação, você recebe o código do módulo contratado em
      modalidade local licenciada, sem custo adicional, e todos os dossiês exportados continuam seus — eles são
      arquivos, não uma tela que some. Nenhuma análise que você já entregou ao seu cliente depende de nós continuarmos
      existindo.</div></details>
      <details><summary>Meus dados ficam na mão de vocês?</summary><div class="ans">A DKD é operadora, não controladora:
      o dado é do seu escritório e sai quando você mandar. Infraestrutura e modelos em região brasileira, sem
      transferência internacional a documentar, e o provedor de IA não retém o conteúdo para treinamento nem inspeção.
      Existe ainda a modalidade local licenciada, em que o dado não sai da sua máquina.</div></details>
      <details><summary>A IA pode errar uma conta e eu assinar embaixo?</summary><div class="ans">Não, por arquitetura.
      Todo cálculo roda em motor determinístico versionado; o modelo de linguagem lê documento, classifica o ambíguo e
      redige — <strong>fazer conta é proibido para ele</strong>. Abaixo do limiar de confiança a ferramenta se cala e
      abre tarefa de revisão humana em vez de chutar. E nada chega ao cliente final sem aprovação nominal de um
      responsável identificado.</div></details>
      <details><summary>Quanto tempo até eu ver valor?</summary><div class="ans">O diagnóstico gratuito devolve o
      primeiro comparativo em dois dias úteis, sobre os seus próprios CNPJs. Na contratação, a carteira inteira entra
      em uma a duas semanas, conforme o volume e a qualidade dos arquivos. Não há projeto de implantação de seis
      meses.</div></details>
      <details><summary>Preciso trocar o meu sistema contábil?</summary><div class="ans">Não. A DKD lê o que os seus
      sistemas já produzem — SPED, extratos, faturas. Integração com ERP ou sistema contábil existe como adicional,
      para quem quiser automatizar a entrada, mas nunca foi requisito para começar.</div></details>
    </div>
    <div class="btn-row"><a class="btn btn--solid" href="/diagnostico/">Pedir o diagnóstico gratuito</a>
    <a class="btn btn--quiet" href="/contato/">Falar com a DKD</a></div>
  </div>
</section>

<section class="band">
  <div class="container">
    <h2>Quem está por trás</h2>
    <div class="hero-grid" style="align-items:start">
      <div>
        <p class="lead" style="max-width:60ch">A DKD nasceu de vinte e cinco anos dentro da indústria — chão de fábrica,
        engenharia de qualidade, engenharia de aplicação, gestão comercial e direção executiva em multinacionais de componentes
        hidráulicos e sistemas de movimentação. Maicol Dondé, fundador, passou esse tempo do lado de quem precisa justificar um
        número: para o cliente, para a matriz, para o auditor.</p>
        <p>A formação puxa para o mesmo lado. Engenharia de Produção na graduação, mestrado em Engenharia Mecânica com
        dissertação sobre redes neurais aplicadas à predição de dados industriais, MBA na FGV, Lean Six Sigma Black Belt e a
        certificação CQE da ASQ. A DKD Tecnologia e Inovação foi constituída em março de 2025 para levar esse método —
        medir, testar, provar — às ferramentas de análise financeira, fiscal e de investimentos.</p>
        <p>É uma empresa pequena e isso é dito na cara: você fala com quem construiu a ferramenta, em português, inglês,
        espanhol ou italiano, e a resposta não passa por três níveis de atendimento.</p>
      </div>
      <div class="card card--pad">
        <p class="eyebrow eyebrow--mute">Trajetória</p>
        <ul class="plain small" style="margin-bottom:0">
          <li>25+ anos entre operações, qualidade, engenharia de aplicação e liderança executiva</li>
          <li>Passagens por Eaton Corporation, Weber-Hydraulik, Interpump Hydraulics e Hidromas</li>
          <li>Engenharia de Produção · Mestrado em Engenharia Mecânica (IA aplicada a dados industriais)</li>
          <li>MBA FGV · Lean Six Sigma Black Belt · CQE ASQ</li>
          <li>Atendimento em português, inglês, espanhol e italiano</li>
        </ul>
      </div>
    </div>
    <dl class="kpis" style="margin-top:28px">
      <div><dt>Razão social</dt><dd style="font-size:1.05rem">{RAZAO}</dd><small>CNPJ {CNPJ}</small></div>
      <div><dt>Sede</dt><dd style="font-size:1.05rem">{CIDADE}</dd><small>Atendimento em todo o Brasil</small></div>
      <div><dt>Contato comercial</dt><dd style="font-size:1.05rem"><a href="mailto:{EMAIL}">{EMAIL}</a></dd><small>Resposta em até um dia útil</small></div>
      <div><dt>Encarregado de dados</dt><dd style="font-size:1.05rem"><a href="mailto:{EMAIL_DPO}">{EMAIL_DPO}</a></dd><small>Titulares e controladores</small></div>
    </dl>
  </div>
</section>
"""

# ----------------------------------------------------------------- CONTATO
CONTATO = f"""
<section class="band band--hero band--surface">
  <div class="container">
    <p class="eyebrow">Contato</p>
    <h1>Fale com quem construiu a ferramenta.</h1>
    <p class="lead" style="margin-top:18px">A DKD é uma equipe pequena. Quem responde entende do produto e da norma —
    não há triagem por script nem fila de qualificação.</p>
  </div>
</section>

<section class="band">
  <div class="container hero-grid">
    <div>
      <h2>Escreva para a gente</h2>
      {formulario("contato", "Enviar mensagem", "Quantos CNPJs tem a carteira, qual sistema você usa hoje, e o que precisa resolver.")}
      <p class="tiny" style="margin-top:14px">Se o formulário falhar por qualquer motivo, escreva direto para
      <a href="mailto:{EMAIL}">{EMAIL}</a> — a caixa é monitorada todos os dias úteis.</p>
    </div>

    <div>
      <div class="card card--pad" style="margin-bottom:18px">
        <p class="eyebrow eyebrow--mute">Canais diretos</p>
        <ul class="plain small" style="margin-bottom:0">
          <li>Comercial e suporte: <a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>Privacidade e LGPD: <a href="mailto:{EMAIL_DPO}">{EMAIL_DPO}</a></li>
          <li>Já é cliente? Entre direto no <a href="{APP}">portal</a>.</li>
        </ul>
      </div>
      <div class="card card--pad">
        <p class="eyebrow eyebrow--mute">O que acontece depois</p>
        <ul class="plain small" style="margin-bottom:0">
          <li><strong>Em 1 dia útil</strong> — respondemos com o material do módulo e duas ou três perguntas objetivas.</li>
          <li><strong>Em 3 a 5 dias</strong> — conversa técnica de 45 minutos, com a ferramenta aberta sobre um caso parecido com o seu.</li>
          <li><strong>Se fizer sentido</strong> — teste de 14 dias no módulo Fiscal, ou prova de conceito paga sobre os seus próprios dados.</li>
        </ul>
      </div>
    </div>
  </div>
</section>
"""

# ------------------------------------------------------------------- LEGAL
MINUTA = """<div class="todo"><b>Minuta</b> — texto-base preparado para revisão do advogado da DKD.
Não publique como definitivo sem essa revisão. Remova este aviso quando o documento estiver aprovado.</div>"""

PRIVACIDADE = f"""
<section class="band band--hero band--surface">
  <div class="container">
    <p class="eyebrow">Legal</p>
    <h1>Política de Privacidade</h1>
    <p class="lead" style="margin-top:18px">Última atualização: 9 de setembro de 2026. Aplica-se ao site dkdtecnologia.com e aos módulos DKD Financial Tools.</p>
  </div>
</section>
<section class="band">
  <div class="container">
    {MINUTA}
    <h2>1. Quem trata os seus dados</h2>
    <p>{RAZAO}, CNPJ {CNPJ}, com sede em {CIDADE}. Encarregado pelo tratamento de dados pessoais: <a href="mailto:{EMAIL_DPO}">{EMAIL_DPO}</a>.</p>

    <h2>2. Os dois papéis da DKD</h2>
    <p>A DKD é <strong>controladora</strong> dos dados de quem visita o site e de quem usa a plataforma: cadastro, credenciais, registros de acesso e dados de faturamento.
    A DKD é <strong>operadora</strong> dos dados que o cliente carrega na plataforma sobre terceiros — arquivos fiscais, extratos e cadastros — tratando-os por conta e ordem do cliente,
    que é o controlador desses dados.</p>

    <h2>3. Dados coletados e finalidade</h2>
    <div class="tablewrap" style="margin:18px 0 24px">
      <table>
        <thead><tr><th>Dado</th><th>Finalidade</th><th>Base legal</th></tr></thead>
        <tbody>
          <tr><th scope="row">Nome, e-mail, telefone e empresa</th><td>Responder contato, executar e administrar o contrato</td><td>Execução de contrato e procedimentos preliminares</td></tr>
          <tr><th scope="row">Credenciais e registros de acesso</th><td>Autenticar, controlar permissões e manter trilha de auditoria</td><td>Cumprimento de obrigação legal e legítimo interesse em segurança</td></tr>
          <tr><th scope="row">Dados de faturamento</th><td>Cobrar e emitir documento fiscal</td><td>Execução de contrato e obrigação legal</td></tr>
          <tr><th scope="row">Arquivos carregados pelo cliente</th><td>Executar a análise contratada</td><td>Execução de contrato, na qualidade de operadora</td></tr>
          <tr><th scope="row">Dados de navegação essenciais</th><td>Manter a sessão e a segurança do site</td><td>Legítimo interesse</td></tr>
        </tbody>
      </table>
    </div>

    <h2>4. Compartilhamento</h2>
    <p>Os dados são compartilhados apenas com subprocessadores necessários à prestação — infraestrutura, provedor de modelos de inteligência artificial,
    meio de pagamento e envio de mensagens — todos vinculados por acordo de tratamento de dados. A lista atualizada é fornecida sob solicitação.
    A DKD não vende dados pessoais e não os utiliza para publicidade de terceiros.</p>

    <h2>5. Inteligência artificial</h2>
    <p>O conteúdo enviado aos modelos de linguagem é processado em região brasileira e o provedor está configurado para não retê-lo,
    nem para treinamento, nem para inspeção humana. Dados pessoais são mascarados sempre que não forem necessários ao processamento.</p>

    <h2>6. Retenção e eliminação</h2>
    <p>Dados de conta e registros de acesso são mantidos enquanto durar o contrato e pelo prazo legal aplicável após o encerramento.
    Arquivos carregados pelo cliente são devolvidos e eliminados conforme o prazo previsto em contrato, mediante confirmação por escrito.</p>

    <h2>7. Direitos do titular</h2>
    <p>Você pode solicitar confirmação de tratamento, acesso, correção, anonimização, portabilidade, informação sobre compartilhamento e revogação de consentimento,
    escrevendo para <a href="mailto:{EMAIL_DPO}">{EMAIL_DPO}</a>. Respondemos em até 15 dias.
    Quando o pedido se referir a dados em que a DKD atua como operadora, ele é encaminhado ao controlador responsável, e você é informado disso.</p>

    <h2>8. Incidentes</h2>
    <p>Há plano de resposta a incidentes escrito, com comunicação ao controlador e, quando cabível, à Autoridade Nacional de Proteção de Dados e aos titulares afetados,
    nos prazos e na forma da legislação.</p>

    <h2>9. Alterações</h2>
    <p>Mudanças relevantes nesta política são comunicadas por e-mail aos clientes ativos com pelo menos 30 dias de antecedência.</p>
  </div>
</section>
"""

TERMOS = f"""
<section class="band band--hero band--surface">
  <div class="container">
    <p class="eyebrow">Legal</p>
    <h1>Termos de Uso</h1>
    <p class="lead" style="margin-top:18px">Última atualização: 9 de setembro de 2026. Aplicam-se ao site e aos módulos DKD Financial Tools.</p>
  </div>
</section>
<section class="band">
  <div class="container">
    {MINUTA}
    <h2>1. Objeto</h2>
    <p>Estes termos regem o acesso ao site e o uso dos módulos da DKD Financial Tools, complementados pelo contrato específico firmado com cada cliente,
    que prevalece em caso de divergência.</p>

    <h2>2. Licença de uso</h2>
    <p>A contratação concede licença de uso pessoal, intransferível e não exclusiva, limitada ao número de usuários, ao volume e ao prazo contratados.
    É vedado compartilhar credenciais, revender o acesso, disponibilizar o programa a terceiros não licenciados, ou realizar engenharia reversa,
    descompilação ou extração das bases de regras e tabelas. O descumprimento autoriza suspensão imediata do acesso e a penalidade prevista em contrato.</p>

    <h2>3. Natureza do resultado</h2>
    <p>Os relatórios, pareceres, classificações e análises produzidos são <strong>insumo técnico</strong>.
    A decisão tributária, contábil, financeira ou de investimento, bem como a assinatura de qualquer peça, cabe ao usuário ou ao profissional habilitado por ele designado.
    A DKD não responde por decisões tomadas com base nos resultados.</p>

    <h2>4. Módulos de investimento</h2>
    <p>{AVISO_CVM}</p>

    <h2>5. Obrigações do cliente</h2>
    <ul class="plain">
      <li>Garantir que possui base legal para tratar os dados que carrega na plataforma.</li>
      <li>Manter a confidencialidade das credenciais e comunicar imediatamente qualquer uso indevido.</li>
      <li>Revisar os resultados antes de utilizá-los perante terceiros.</li>
      <li>Não utilizar a plataforma para finalidade ilícita ou fora do escopo contratado.</li>
    </ul>

    <h2>6. Disponibilidade e suporte</h2>
    <p>A disponibilidade contratada, os canais e os prazos de suporte constam do plano contratado. Manutenções programadas são avisadas com antecedência.
    Não há garantia de operação ininterrupta durante eventos fora do controle razoável da DKD.</p>

    <h2>7. Propriedade intelectual</h2>
    <p>O programa, as bases de regras, as tabelas, a marca e a documentação pertencem à DKD.
    Os dados carregados e os relatórios gerados a partir deles pertencem ao cliente, que pode exportá-los a qualquer momento durante a vigência.</p>

    <h2>8. Vigência, reajuste e rescisão</h2>
    <p>A vigência, o reajuste anual e as condições de rescisão são os definidos no contrato e na tabela de preços publicada.
    Encerrado o contrato, o acesso é revogado e os dados são devolvidos e eliminados no prazo acordado.</p>

    <h2>9. Limitação de responsabilidade</h2>
    <p>Ressalvadas as hipóteses de dolo e as vedações legais, a responsabilidade da DKD limita-se ao valor pago pelo cliente nos 12 meses anteriores ao evento.</p>

    <h2>10. Foro</h2>
    <p>Fica eleito o foro da comarca de Caxias do Sul, Rio Grande do Sul, com renúncia a qualquer outro.</p>
  </div>
</section>
"""

# ---------------------------------------------------------- ÁREA LOGADA
APP_HUB = f"""
<section class="band band--hero band--surface">
  <div class="container">
    <div class="todo"><b>Prévia</b> — esta é a tela que vai atrás do portão de acesso, em
    <code>app.dkdtecnologia.com</code>. Nesta prévia os dados são de exemplo. Não publique este arquivo no site público.</div>
    <p class="eyebrow">Portal DKD</p>
    <h1>Minhas ferramentas</h1>
    <p class="lead" style="margin-top:16px">Escritório Exemplo Contabilidade · <span class="mono">CNPJ 12.345.678/0001-90</span> ·
    perfil <strong>Administrador do escritório</strong></p>
  </div>
</section>

<section class="band">
  <div class="container">
    <div class="tools">
      <article class="tool">
        <span class="state">Licença ativa</span>
        <h3>Análise, Simulação e Inteligência Fiscal e Tributária</h3>
        <p class="small">Comparador de regimes, painel da carteira, classificação e dossiê.</p>
        <a class="btn btn--sm btn--solid" href="__PORTAL_FISCAL__" target="_blank" rel="noopener" style="align-self:flex-start">Abrir módulo</a>
        <div class="meta"><span>plano Profissional</span><span>62 / 100 CNPJs</span><span>motor 2026.08.1</span><span>corpus 2026-08-24</span><span>vence 31/10/2026</span></div>
      </article>

      <article class="tool">
        <span class="state state--warn">Vence em 9 dias</span>
        <h3>Gestão Financeira CPF e CNPJ</h3>
        <p class="small">Extratos classificados, fronteira entre pessoa física e jurídica, projeção de caixa.</p>
        <a class="btn btn--sm btn--solid" href="__PORTAL_GESTAO__" target="_blank" rel="noopener" style="align-self:flex-start">Abrir módulo</a>
        <div class="meta"><span>plano Completo</span><span>3 CNPJs</span><span>motor 2026.08.1</span><span>vence 04/09/2026</span></div>
      </article>

      <article class="tool tool--off">
        <span class="state state--off">Não contratado</span>
        <h3>DKD Alpha Invest AI</h3>
        <p class="small">Triagem e comparação de ativos segundo os seus critérios.</p>
        <a class="btn btn--sm" href="https://dkdtecnologia.com/produtos/alpha-invest/" style="align-self:flex-start">Conhecer</a><a class="btn btn--sm btn--quiet" href="__PORTAL_ALPHA__" target="_blank" rel="noopener" style="align-self:flex-start;margin-top:8px">Abrir o portal<span aria-hidden="true">&#8599;</span></a>
        <div class="meta"><span>disponível para contratação</span></div>
      </article>

      <article class="tool tool--off">
        <span class="state state--off">Não contratado</span>
        <h3>DKD Asset Intelligence AI</h3>
        <p class="small">Acompanhamento da carteira, concentração, proventos e eventos.</p>
        <a class="btn btn--sm" href="https://dkdtecnologia.com/produtos/asset-intelligence/" style="align-self:flex-start">Conhecer</a><a class="btn btn--sm btn--quiet" href="__PORTAL_ASSET__" target="_blank" rel="noopener" style="align-self:flex-start;margin-top:8px">Abrir o portal<span aria-hidden="true">&#8599;</span></a>
        <div class="meta"><span>disponível para contratação</span></div>
      </article>

      <article class="tool">
        <span class="state">Licença ativa</span>
        <h3>Portal Integrado</h3>
        <p class="small">Hub dos módulos de investimento: alterna entre Alpha Invest, Asset Intelligence e Investors Profile sem sair da tela.</p>
        <a class="btn btn--sm btn--solid" href="__PORTAL_HUB__" target="_blank" rel="noopener" style="align-self:flex-start">Abrir o portal</a>
        <div class="meta"><span>três módulos ligados</span><span>um acesso só</span></div>
      </article>
    </div>

    <div class="note note--warn" style="margin-top:30px">
      <span class="tag">Renovação</span>
      <p>O módulo Gestão Financeira vence em <strong>4 de setembro de 2026</strong>. A renovação é automática no cartão cadastrado.
      Para alterar plano, faixa ou forma de pagamento, escreva para <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    </div>
  </div>
</section>

<section class="band band--surface">
  <div class="container">
    <h2>Usuários do escritório</h2>
    <div class="tablewrap" style="margin-top:22px">
      <table>
        <caption>Somente o administrador do escritório enxerga e altera esta lista.</caption>
        <thead><tr><th>Usuário</th><th>Papel</th><th>Módulos</th><th>Último acesso</th></tr></thead>
        <tbody>
          <tr><th scope="row">maria@exemplo.com.br</th><td>Administrador do escritório</td><td>Todos os contratados</td><td class="n">hoje, 09:12</td></tr>
          <tr><th scope="row">joao@exemplo.com.br</th><td>Analista</td><td>Fiscal e Tributária</td><td class="n">ontem, 17:40</td></tr>
          <tr><th scope="row">cliente@outraempresa.com.br</th><td>Consulta</td><td>Fiscal — somente leitura</td><td class="n">22/08, 11:05</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>
"""


# ---------------------------------------------------------------- PORTAIS
def _cartao(chave, nome, papel, resumo, itens, alvo, chip):
    lis = "".join("<li>%s</li>" % i for i in itens)
    return f"""
      <article class="mod mod--{chave}">
        <span class="chip chip--live">{chip}</span>
        <h3>{nome}</h3>
        <p class="tagline small">{papel}</p>
        <p class="small">{resumo}</p>
        <ul class="ticks small">{lis}</ul>
        <div class="foot">
          <a class="btn btn--portal" href="{alvo}" target="_blank" rel="noopener">Abrir o portal<span aria-hidden="true">&#8599;</span></a>
        </div>
      </article>"""


PORTAIS_PAGE = f"""
<section class="band band--hero band--surface">
  <div class="container">
    <p class="eyebrow">Acesso aos portais</p>
    <h1>Os cinco portais da DKD, num lugar só.</h1>
    <p class="lead" style="margin-top:18px">Cada módulo roda no seu próprio portal, com o mesmo cabeçalho, o mesmo padrão de
    evidência e a mesma camada de licença. Abra qualquer um daqui.</p>
  </div>
</section>

<section class="band">
  <div class="container">
    <div class="grid g2" style="background:transparent;border:0;gap:18px">
{_cartao("fiscal", "Análise, Simulação e Inteligência Fiscal e Tributária",
         "Para o escritório de contabilidade",
         "A carteira inteira numa tela, comparação de regimes sobre o SPED real e o parecer com o dispositivo citado.",
         ["Simples puro, híbrido, Presumido e Real lado a lado",
          "Classificação de CST e cClassTrib com fila de exceção",
          "Dossiê exportável com hash, versão do motor e data-base"],
         "__PORTAL_FISCAL__", "Disponível")}
{_cartao("gestao", "Planejamento, Controle e Gestão Financeira",
         "Para o dono do negócio",
         "Extratos de pessoa física e jurídica no mesmo painel, a fronteira entre empresa e dono, e o caixa dos próximos 90 dias.",
         ["Leitura e classificação de extratos e faturas",
          "Projeção de caixa de 30, 60 e 90 dias",
          "Base criptografada, com PIN e senha mestra"],
         "__PORTAL_GESTAO__", "Disponível")}
{_cartao("alpha", "Alpha Invest AI",
         "Para o investidor pessoa física",
         "Triagem e comparação de ativos da B3 pelos critérios que você define, com a fonte de cada número.",
         ["Filtros próprios, salvos e reaplicáveis",
          "Comparação com histórico e origem do dado",
          "Ferramenta operada por você — não recomenda ativo"],
         "__PORTAL_ALPHA__", "Disponível")}
{_cartao("asset", "Asset Intelligence AI",
         "Para quem já tem carteira montada",
         "Concentração recalculada a cada aporte, proventos, eventos societários e alertas nos limites que você definiu.",
         ["Concentração por ativo, setor e emissor",
          "Proventos e comunicados resumidos com link para a fonte",
          "Ferramenta operada por você — não recomenda ativo"],
         "__PORTAL_ASSET__", "Disponível")}
    </div>

    <article class="mod" style="margin-top:18px;--mod-c:var(--dkd)">
      <span class="chip chip--live">Hub</span>
      <h3>Portal Integrado</h3>
      <p class="tagline small">O caminho curto entre os módulos de investimento</p>
      <p class="small">Alterna entre Alpha Invest, Asset Intelligence e Investors Profile sem sair da tela, com um acesso só.</p>
      <div class="foot">
        <a class="btn btn--portal" href="__PORTAL_HUB__" target="_blank" rel="noopener">Abrir o portal<span aria-hidden="true">&#8599;</span></a>
      </div>
    </article>
  </div>
</section>

<section class="band band--surface">
  <div class="container">
    <div class="note note--brand">
      <span class="tag">Como o acesso funciona</span>
      <p>A entrada é por código de uso único enviado ao seu e-mail, com papéis distintos, sessão com prazo e revogação
      imediata. Cada portal é um projeto independente: a atualização de um não derruba os outros, e cada um tem a sua
      própria política de acesso.</p>
      <p style="margin-bottom:0"><a href="/seguranca/">Ver a página de segurança e LGPD</a></p>
    </div>
  </div>
</section>
"""


# ----------------------------------------------------------- DIAGNÓSTICO
DIAGNOSTICO = f"""
<section class="band band--hero band--surface" data-mod="fiscal">
  <div class="container hero-grid">
    <div>
      <p class="eyebrow">Diagnóstico gratuito · sem cartão</p>
      <h1>Descubra quais clientes seus perdem margem em 2027.</h1>
      <p class="lead" style="margin-top:20px">Você manda o SPED de até <strong>três CNPJs</strong> da sua carteira.
      A DKD devolve, em até dois dias úteis, o comparativo entre Simples puro, Simples híbrido, Lucro Presumido e
      Lucro Real sobre os números reais deles — com o dispositivo legal citado em cada linha.</p>
      <p class="lead">Sem compromisso de contratar. O documento é seu, com ou sem negócio.</p>
      <div class="btn-row">
        <a class="btn btn--solid" href="#pedir">Pedir o diagnóstico</a>
        <a class="btn btn--quiet" href="/produtos/fiscal-tributaria/">Ver o módulo por trás disso</a>
      </div>
    </div>
    <div class="card card--pad">
      <p class="eyebrow eyebrow--warn">Por que agora</p>
      <p class="small">A opção pelo regime híbrido do Simples <strong>fecha em 30 de setembro de 2026</strong>
      (Resolução CGSN nº 190/2026). O efeito começa em 1º de janeiro de 2027 e é irretratável depois disso.</p>
      <p class="small" style="margin-bottom:0">Quem responder ao cliente depois do prazo vai responder por uma decisão
      que já não dá para desfazer.</p>
    </div>
  </div>
</section>

<section class="band" data-mod="fiscal">
  <div class="container">
    <p class="eyebrow">Como funciona</p>
    <h2>Três passos, dois dias úteis</h2>
    <div class="grid g3" style="margin-top:34px">
      <div>
        <h3>1 · Você pede</h3>
        <p class="small">Preenche o formulário abaixo. Nada de arquivo por aqui — respondemos com um link de envio
        seguro, com prazo e uso único, para você mandar o SPED sem passar por e-mail comum.</p>
      </div>
      <div>
        <h3>2 · O motor roda</h3>
        <p class="small">Os quatro regimes são calculados sobre os dados reais de cada CNPJ, por motor determinístico
        versionado por vigência. A IA lê, classifica o que é ambíguo e redige — <strong>ela não faz conta</strong>.</p>
      </div>
      <div>
        <h3>3 · Você recebe o dossiê</h3>
        <p class="small">Comparativo por CNPJ, quanto de crédito de IBS/CBS você transfere ao cliente PJ, o que muda
        no seu honorário, e o dispositivo legal de cada afirmação. Em PDF, pronto para levar ao cliente.</p>
      </div>
    </div>
  </div>
</section>

<section class="band band--surface" data-mod="fiscal">
  <div class="container">
    <div class="hero-grid" style="align-items:start">
      <div>
        <p class="eyebrow">O que você leva</p>
        <h2>É o mesmo entregável que o escritório cobra de R$ 4.500 a R$ 14.000.</h2>
        <ul class="ticks">
          <li>Comparativo dos quatro regimes por CNPJ, com o número e a origem dele</li>
          <li>O ponto de virada: a partir de que faturamento o regime deixa de compensar</li>
          <li>Crédito de IBS/CBS transferido ao cliente PJ — o argumento que segura cliente B2B</li>
          <li>Riscos de classificação de CST e cClassTrib, ordenados por valor em reais</li>
          <li>Dossiê com hash dos arquivos, versão do motor e data-base do corpus normativo</li>
        </ul>
        <p class="tiny">Faixa de honorário observada no mercado em 2026. O que a DKD entrega no diagnóstico é o
        mesmo artefato — a diferença é que aqui ele sai de graça, para você ver a ferramenta trabalhando.</p>
      </div>
      <div class="card card--pad">
        <p class="eyebrow eyebrow--mute">O que a DKD ganha com isso</p>
        <p class="small">Nada, na primeira rodada. É custo de máquina e de revisão humana.</p>
        <p class="small">A aposta é simples e está dita na cara: quem vê o comparativo pronto sobre os próprios
        clientes entende em cinco minutos o que levaria uma semana de planilha. Se a ferramenta não impressionar
        aí, ela não merece a sua assinatura.</p>
        <p class="small" style="margin-bottom:0">Não há ligação de vendedor depois. Você recebe o dossiê e decide.</p>
      </div>
    </div>
  </div>
</section>

<section class="band" data-mod="fiscal" id="pedir">
  <div class="container">
    <div class="hero-grid" style="align-items:start">
      <div>
        <p class="eyebrow">Pedir o diagnóstico</p>
        <h2>Leva um minuto.</h2>
        <p class="sec-intro">Quanto mais você contar sobre a carteira, mais útil o comparativo volta.
        Se preferir, chame no WhatsApp — o pedido vale igual.</p>
        {formulario("diagnostico", "Pedir o diagnóstico gratuito",
                    "Qual o ramo dos clientes que você quer testar, e o que te preocupa na reforma.")}
      </div>
      <div>
        <div class="note note--brand">
          <span class="tag">O que acontece com o seu arquivo</span>
          <p class="small">O SPED é processado para produzir o seu diagnóstico e mais nada. <strong>Não treina
          modelo, não vira base de dados nossa e não é compartilhado.</strong></p>
          <p class="small">O arquivo e o resultado são apagados em até 30 dias, ou antes se você pedir —
          basta um e-mail para <a href="mailto:{EMAIL_DPO}">{EMAIL_DPO}</a>.</p>
          <p class="small" style="margin-bottom:0">Nesta etapa a DKD é <strong>operadora</strong>; o controlador
          dos dados continua sendo o seu escritório. <a href="/seguranca/">Ver a página de segurança</a>.</p>
        </div>
        <div class="card card--pad">
          <p class="eyebrow eyebrow--mute">Quem já pode pedir</p>
          <ul class="plain small" style="margin-bottom:0">
            <li>Escritório de contabilidade com carteira de qualquer tamanho</li>
            <li>Empresa que quer testar o próprio regime antes de decidir</li>
            <li>Consultor tributário avaliando a ferramenta para os clientes dele</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="band band--surface" data-mod="fiscal">
  <div class="container">
    <h2>Perguntas que todo escritório faz antes de mandar o arquivo</h2>
    <div style="margin-top:24px;border-top:1px solid var(--line)">
      <details><summary>Vocês vão ligar tentando vender?</summary><div class="ans">Não. Você recebe o dossiê por
      e-mail e um resumo do que ele mostra. Se quiser conversar, responde. Se não responder, não insistimos —
      e o material continua seu.</div></details>
      <details><summary>Preciso mandar o SPED inteiro?</summary><div class="ans">O EFD-Contribuições e o EFD-ICMS/IPI
      do período que você quiser testar. Se só tiver alguns meses, dá para trabalhar com isso — o comparativo sai
      com a ressalva de amostra escrita no próprio documento.</div></details>
      <details><summary>E se eu não quiser mandar dado de cliente?</summary><div class="ans">Use o CNPJ do seu próprio
      escritório, ou peça a um cliente com quem você tenha abertura. O diagnóstico funciona igual — o que muda é
      quanto ele conversa com a sua carteira de verdade.</div></details>
      <details><summary>O comparativo tem validade técnica?</summary><div class="ans">Ele é insumo técnico para a sua
      decisão profissional, com a fonte de cada afirmação. A responsabilidade pelo parecer assinado e pela decisão
      tributária continua sendo do contador ou responsável técnico habilitado — a DKD não assina parecer.</div></details>
      <details><summary>Quanto tempo demora mesmo?</summary><div class="ans">Dois dias úteis a partir do momento em que
      o arquivo chega. Se a fila estiver maior que isso numa semana de pico, avisamos no mesmo dia com o prazo real.</div></details>
    </div>
  </div>
</section>

<section class="band band--wash band--tight" data-mod="fiscal">
  <div class="container" style="text-align:center">
    <h2>O prazo de 30 de setembro não se move.</h2>
    <p class="lead" style="margin:0 auto 6px">Um diagnóstico agora vale mais do que uma boa ferramenta em novembro.</p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn btn--solid" href="#pedir">Pedir o diagnóstico</a>
      <a class="btn btn--quiet" href="/precos/">Ver os preços</a>
    </div>
  </div>
</section>
"""
