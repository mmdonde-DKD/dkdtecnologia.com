# -*- coding: utf-8 -*-
"""Home, hub de módulos e as quatro fichas de produto."""

from shell import APP, AVISO_CVM

# --------------------------------------------------------------- diagrama
HERO_SVG = """<figure style="margin:0">
<svg class="dgm" viewBox="0 0 440 252" role="img" aria-label="Um único acesso por PIN de e-mail passa pela camada de licença da DKD, que controla papéis, prazo de contrato e registro, e libera os quatro módulos: Fiscal e Tributária, Gestão Financeira, Alpha Invest AI e Asset Intelligence AI.">
  <defs><marker id="a" viewBox="0 0 9 7" refX="8.5" refY="3.5" markerWidth="8" markerHeight="7" orient="auto">
    <polygon points="0,0 9,3.5 0,7" fill="currentColor"/></marker></defs>
  <rect class="b" x="130" y="6" width="180" height="42"/>
  <text class="t" x="220" y="26" text-anchor="middle">Um acesso</text>
  <text class="s" x="220" y="41" text-anchor="middle">PIN enviado para o seu e-mail</text>
  <line class="ln" x1="220" y1="48" x2="220" y2="64" marker-end="url(#a)"/>
  <rect class="b-key" x="12" y="70" width="416" height="54"/>
  <text class="t" x="220" y="92" text-anchor="middle">Camada de licença e acesso DKD</text>
  <text class="s" x="220" y="110" text-anchor="middle">papéis · prazo do contrato · registro de cada emissão</text>
  <line class="ln" x1="220" y1="124" x2="220" y2="142"/>
  <line class="ln" x1="61" y1="142" x2="379" y2="142"/>
  <line class="ln" x1="61" y1="142" x2="61" y2="170" marker-end="url(#a)"/>
  <line class="ln" x1="167" y1="142" x2="167" y2="170" marker-end="url(#a)"/>
  <line class="ln" x1="273" y1="142" x2="273" y2="170" marker-end="url(#a)"/>
  <line class="ln" x1="379" y1="142" x2="379" y2="170" marker-end="url(#a)"/>
  <rect class="b" x="12" y="174" width="98" height="62"/>
  <text class="s" x="61" y="200" text-anchor="middle">Fiscal e</text>
  <text class="s" x="61" y="215" text-anchor="middle">Tributária</text>
  <rect class="b" x="118" y="174" width="98" height="62"/>
  <text class="s" x="167" y="200" text-anchor="middle">Gestão</text>
  <text class="s" x="167" y="215" text-anchor="middle">Financeira</text>
  <rect class="b" x="224" y="174" width="98" height="62"/>
  <text class="s" x="273" y="200" text-anchor="middle">Alpha</text>
  <text class="s" x="273" y="215" text-anchor="middle">Invest AI</text>
  <rect class="b" x="330" y="174" width="98" height="62"/>
  <text class="s" x="379" y="200" text-anchor="middle">Asset</text>
  <text class="s" x="379" y="215" text-anchor="middle">Intelligence AI</text>
</svg>
<figcaption class="tiny" style="margin-top:12px">Um acesso, quatro módulos. A camada de licença controla quem entra, o que cada papel enxerga e até quando o contrato vale.</figcaption>
</figure>"""

URGENCIA = """<section class="urgency">
  <div class="container urgency-in">
    <div class="count" data-count>
      <div><b data-d>—</b><span>dias</span></div>
      <div><b data-h>—</b><span>horas</span></div>
      <div><b data-m>—</b><span>min</span></div>
    </div>
    <p><strong>O prazo de opção pelo regime híbrido do Simples foi prorrogado até 30 de outubro de 2026</strong>, com efeito em 1º de janeiro de 2027. Detalhes no <a href="https://www8.receita.fazenda.gov.br/simplesnacional/" target="_blank" rel="noopener">Portal do Simples Nacional</a>.
    O módulo Fiscal e Tributária compara Simples puro, Simples híbrido, Lucro Presumido e Lucro Real sobre os dados reais de cada CNPJ da carteira.</p>
    <a class="btn btn--solid" href="/produtos/fiscal-tributaria/">Ver o módulo Fiscal</a>
  </div>
</section>"""

# ------------------------------------------------------------------ HOME
HOME = f"""
<section class="band band--hero band--surface">
  <div class="container hero-grid hero">
    <div>
      <p class="eyebrow">DKD Financial Tools AI</p>
      <h1>Análise que chega com a fonte anexada.</h1>
      <p class="lead">Quatro módulos para quem responde por número: o contador que precisa decidir regime antes do prazo,
      o empresário que precisa enxergar o próprio caixa, e o investidor que precisa comparar ativos pelos critérios dele.
      O cálculo roda em motor determinístico. A IA lê, classifica e redige — e cita o dispositivo. Nada sai sem o dossiê que sustenta.</p>
      <div class="btn-row">
        <a class="btn btn--solid" href="/produtos/">Ver os quatro módulos</a>
        <a class="btn btn--quiet" href="{APP}">Entrar no portal</a>
      </div>
    </div>
    <div>{HERO_SVG}</div>
  </div>
</section>

<section class="assinatura">
  <div class="container"><p>Tecnologia que impulsiona na busca pelo novo</p></div>
</section>

{URGENCIA}

<section class="band band--wash band--tight">
  <div class="container hero-grid" style="align-items:center;gap:36px">
    <div>
      <p class="eyebrow">Antes de decidir qualquer coisa</p>
      <h2 style="margin-bottom:12px">Teste com os seus próprios clientes, de graça.</h2>
      <p class="lead" style="margin-bottom:0">Mande o SPED de até três CNPJs da sua carteira. Em dois dias úteis
      volta o comparativo dos quatro regimes sobre os números reais deles, com o dispositivo citado.
      Sem cartão, sem ligação de vendedor.</p>
    </div>
    <div style="justify-self:start">
      <a class="btn btn--solid" href="/diagnostico/" data-lead="diagnostico-home">Pedir o diagnóstico gratuito</a>
    </div>
  </div>
</section>


<section class="band">
  <div class="container">
    <p class="eyebrow">Escolha por onde entrar</p>
    <h2>Três perfis, quatro ferramentas</h2>
    <p class="sec-intro lead">Você não precisa entender a nossa taxonomia de produto. Diga quem você é e nós mostramos o que resolve a sua semana.</p>
    <div class="grid g3" style="background:transparent;border:0;gap:18px">
      <a class="door" href="/produtos/fiscal-tributaria/">
        <span class="who">Escritório de contabilidade</span>
        <h3>Decidir o regime de 300 clientes sem abrir 300 planilhas</h3>
        <p class="small">Suba o SPED, veja a carteira inteira numa tela, descubra quais clientes perdem margem em 2027 e gere o parecer com o artigo da lei anexado.</p>
        <span class="go">Módulo Fiscal e Tributária →</span>
      </a>
      <a class="door" href="/produtos/gestao-financeira/">
        <span class="who">Micro e pequeno empresário</span>
        <h3>Separar o que é seu do que é da empresa e enxergar o caixa</h3>
        <p class="small">Extratos de CPF e CNPJ lidos e classificados, pró-labore e retiradas isolados, e a projeção de caixa dos próximos 90 dias com o que já está contratado.</p>
        <span class="go">Módulo Gestão Financeira →</span>
      </a>
      <a class="door" href="/produtos/alpha-invest/">
        <span class="who">Investidor pessoa física</span>
        <h3>Filtrar e acompanhar ativos pelos seus próprios critérios</h3>
        <p class="small">Você define os filtros; a ferramenta varre, compara e monitora. Sem carteira pronta, sem palpite, sem recomendação — a decisão continua sendo sua.</p>
        <span class="go">Alpha Invest e Asset Intelligence →</span>
      </a>
    </div>
  </div>
</section>

<section class="band band--surface">
  <div class="container">
    <p class="eyebrow">DKD Financial Tools AI</p>
    <h2>Os quatro módulos</h2>
    <p class="sec-intro lead">Cada um resolve um problema inteiro sozinho. Juntos, dividem o mesmo acesso, o mesmo padrão de evidência e a mesma conta.</p>
    <div class="grid g2" style="background:transparent;border:0;gap:18px">

      <article class="mod mod--fiscal">
        <span class="chip chip--live">DKD Financial Tools AI · Disponível</span>
        <h3>Análise, Simulação e Inteligência Fiscal e Tributária</h3>
        <p class="tagline small">A carteira inteira do escritório numa tela, com o parecer pronto para o CRC assinar.</p>
        <ul class="ticks small">
          <li>Compara Simples puro, híbrido, Presumido e Real sobre o SPED real</li>
          <li>Mostra quanto crédito de IBS/CBS você transfere ao cliente PJ</li>
          <li>Classificação de CST e cClassTrib com fila de exceção priorizada por risco em reais</li>
        </ul>
        <div class="foot btn-row" style="margin-top:0"><a class="btn btn--sm" href="/produtos/fiscal-tributaria/">Conhecer o módulo</a><a class="btn btn--sm btn--quiet" href="__PORTAL_FISCAL__" target="_blank" rel="noopener">Abrir o portal<span aria-hidden="true">&#8599;</span></a></div>
      </article>

      <article class="mod mod--gestao">
        <span class="chip chip--live">DKD Financial Tools AI · Disponível</span>
        <h3>Planejamento, Controle e Gestão Financeira</h3>
        <p class="tagline small">Para quem é o dono, o financeiro e o caixa da empresa ao mesmo tempo.</p>
        <ul class="ticks small">
          <li>Leitura de extratos e faturas de pessoa física e jurídica no mesmo painel</li>
          <li>Classificação automática com regras que você ajusta uma vez</li>
          <li>Projeção de caixa de 30, 60 e 90 dias a partir do que já está contratado</li>
        </ul>
        <div class="foot btn-row" style="margin-top:0"><a class="btn btn--sm" href="/produtos/gestao-financeira/">Conhecer o módulo</a><a class="btn btn--sm btn--quiet" href="__PORTAL_GESTAO__" target="_blank" rel="noopener">Abrir o portal<span aria-hidden="true">&#8599;</span></a></div>
      </article>

      <article class="mod mod--alpha">
        <span class="chip chip--live">DKD Financial Tools AI · Disponível</span>
        <h3>Alpha Invest AI</h3>
        <p class="tagline small">Triagem e comparação de ativos segundo os critérios que você define.</p>
        <ul class="ticks small">
          <li>Filtros próprios sobre dados públicos de mercado e de fatos relevantes</li>
          <li>Comparação lado a lado com o histórico e a fonte de cada número</li>
          <li>Ferramenta operada por você — não emite recomendação de compra ou venda</li>
        </ul>
        <div class="foot btn-row" style="margin-top:0"><a class="btn btn--sm" href="/produtos/alpha-invest/">Conhecer o módulo</a><a class="btn btn--sm btn--quiet" href="__PORTAL_ALPHA__" target="_blank" rel="noopener">Abrir o portal<span aria-hidden="true">&#8599;</span></a></div>
      </article>

      <article class="mod mod--asset">
        <span class="chip chip--live">DKD Financial Tools AI · Disponível</span>
        <h3>Asset Intelligence AI</h3>
        <p class="tagline small">Acompanhamento da carteira que você já tem, sem planilha manual.</p>
        <ul class="ticks small">
          <li>Concentração por ativo, setor e emissor, com o número recalculado a cada aporte</li>
          <li>Proventos, eventos societários e comunicados lidos e resumidos com link para a fonte</li>
          <li>Alertas segundo os limites que você mesmo definiu</li>
        </ul>
        <div class="foot btn-row" style="margin-top:0"><a class="btn btn--sm" href="/produtos/asset-intelligence/">Conhecer o módulo</a><a class="btn btn--sm btn--quiet" href="__PORTAL_ASSET__" target="_blank" rel="noopener">Abrir o portal<span aria-hidden="true">&#8599;</span></a></div>
      </article>

    </div>
  </div>
</section>

<section class="band">
  <div class="container">
    <p class="eyebrow">Como a DKD constrói</p>
    <h2>Três regras que não são negociáveis</h2>
    <p class="sec-intro lead">Elas valem nos quatro módulos e são a razão de um profissional conseguir assinar embaixo do que a ferramenta produz.</p>
    <div class="grid g3">
      <div>
        <h3>O motor calcula. A IA explica.</h3>
        <p class="small">Todo cálculo roda em motor determinístico versionado por vigência — o mesmo dado produz o mesmo número hoje e daqui a três anos, numa fiscalização.
        O modelo de linguagem lê documento, classifica o ambíguo e redige. <strong>Fazer conta é proibido para ele</strong>: alucinação numérica é o risco fatal em produto financeiro, e foi eliminado por arquitetura, não por promessa.</p>
      </div>
      <div>
        <h3>Sem citação, não vai para a tela.</h3>
        <p class="small">Toda afirmação normativa carrega norma, dispositivo e link oficial. Um verificador secundário confere se o trecho citado sustenta a frase;
        se não sustentar, a resposta é marcada como não verificada. Abaixo do limiar de confiança a ferramenta se cala e abre uma tarefa de revisão humana, em vez de chutar.</p>
      </div>
      <div>
        <h3>Todo entregável vira dossiê.</h3>
        <p class="small">Cada análise gera um artefato imutável e exportável: os arquivos processados com hash, a versão do motor, a data-base do corpus,
        a cadeia de premissa → dispositivo → cálculo → resultado, os itens em que a ferramenta se absteve, e quem revisou e aprovou.
        Não é relatório bonito — é prova.</p>
      </div>
    </div>
  </div>
</section>

<section class="band">
  <div class="container">
    <p class="eyebrow eyebrow--mute">Prova de campo</p>
    <h2>O primeiro caso entra aqui.</h2>
    <p class="sec-intro lead">A DKD não publica depoimento inventado nem número de cliente que não existe —
    numa venda para contador, uma prova falsa some com a credibilidade no primeiro telefonema.
    Este espaço fica reservado ao primeiro escritório que autorizar o próprio nome.</p>
    <div class="grid g3" style="margin-top:8px">
      <div>
        <h3>O que vai aparecer</h3>
        <p class="small">Tamanho da carteira, o que o escritório fazia antes, quanto tempo levava, e o que mudou —
        com número conferível e o nome de quem autorizou.</p>
      </div>
      <div>
        <h3>O que não vai</h3>
        <p class="small">Nenhum dado de cliente final, nenhuma métrica que não dê para verificar, e nenhuma frase
        que o escritório não tenha escrito com as próprias palavras.</p>
      </div>
      <div>
        <h3>Quer ser o primeiro?</h3>
        <p class="small">O escritório-âncora entra em condição especial de primeiro ano e participa das decisões de
        produto. <a href="/contato/">Fale com a DKD</a>.</p>
      </div>
    </div>
  </div>
</section>

<section class="band band--surface">
  <div class="container">
    <p class="eyebrow">Segurança e conformidade</p>
    <h2>O que o comprador pergunta antes de assinar</h2>
    <p class="sec-intro lead">Escritório de contabilidade faz <i>due diligence</i>. Estas respostas já estão prontas.</p>
    <dl class="kpis">
      <div><dt>Onde o dado fica</dt><dd>Brasil</dd><small>Infraestrutura e modelos em região brasileira. Sem transferência internacional a documentar.</small></div>
      <div><dt>Retenção pelo modelo</dt><dd>Zero</dd><small>O provedor de IA não retém o conteúdo enviado para treinamento nem para inspeção.</small></div>
      <div><dt>Acesso</dt><dd>PIN + prazo</dd><small>Entrada por código de uso único, papéis distintos, sessão com prazo e revogação imediata.</small></div>
      <div><dt>Antes de entregar</dt><dd>Revisão humana</dd><small>Nada chega ao cliente final sem aprovação nominal de um responsável identificado.</small></div>
    </dl>
    <div class="btn-row"><a class="btn" href="/seguranca/">Ver a página de segurança e LGPD</a></div>
  </div>
</section>

<section class="band">
  <div class="container">
    <div class="hero-grid">
      <div>
        <p class="eyebrow">Consultoria e soluções customizadas com IA</p>
        <h2>Além das plataformas: o processo desenhado para o seu negócio.</h2>
        <p class="lead">Da inteligência de mercado à revisão das estratégias comerciais e financeiras, a DKD
        constrói com a sua equipe as ferramentas que transformam dado em decisão — e decisão em resultado.</p>
        <div class="btn-row">
          <a class="btn btn--solid" href="/consultoria/">Conhecer a consultoria</a>
          <a class="btn btn--quiet" href="__WHATSAPP__" target="_blank" rel="noopener" data-lead="whatsapp-home-consultoria">Conversar no WhatsApp</a>
        </div>
      </div>
      <div class="card card--pad">
        <p class="eyebrow eyebrow--mute">Proposta sob medida</p>
        <p class="small">Cada operação tem a sua carteira, o seu volume e o seu momento. Por isso a DKD apresenta
        <strong>proposta comercial personalizada</strong>, montada a partir de uma conversa sobre o seu cenário.</p>
        <p class="tiny">Fale com a DKD pelo WhatsApp ou pelo e-mail comercial@dkdtecnologia.com.</p>
      </div>
    </div>
  </div>
</section>

<section class="band band--wash band--tight">
  <div class="container" style="text-align:center">
    <h2>Comece pelo módulo que resolve a sua semana.</h2>
    <p class="lead" style="margin:0 auto 6px">Converse com a DKD pelo WhatsApp ou por e-mail e receba uma proposta para o seu cenário.</p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn btn--solid" href="/produtos/">Ver os módulos</a>
      <a class="btn btn--quiet" href="/contato/">Falar com a DKD</a>
    </div>
  </div>
</section>
"""

# ----------------------------------------------------------- HUB PRODUTOS
PRODUTOS = f"""
<section class="band band--hero band--surface">
  <div class="container">
    <p class="eyebrow">DKD Financial Tools AI</p>
    <h1>Quatro módulos, um acesso.</h1>
    <p class="lead" style="margin-top:18px">Cada módulo é contratado separadamente e resolve um problema inteiro sozinho.
    O que eles dividem é o portal de entrada, o padrão de evidência e a fatura.</p>
  </div>
</section>

<section class="band">
  <div class="container">
    <div class="tablewrap">
      <table>
        <caption>Se você está em dúvida sobre por onde começar, escolha pela primeira coluna.</caption>
        <thead><tr><th>Se o seu problema é…</th><th>O módulo é</th><th>E o entregável é</th><th>Portal</th></tr></thead>
        <tbody>
          <tr>
            <th scope="row">“Meus clientes estão perguntando sobre a reforma e eu não sei responder com segurança”</th>
            <td><a href="/produtos/fiscal-tributaria/">Fiscal e Tributária</a></td>
            <td>Comparativo de regimes por CNPJ, painel da carteira e parecer com dispositivo citado</td>
            <td><a href="__PORTAL_FISCAL__" target="_blank" rel="noopener">Abrir&#8599;</a></td>
          </tr>
          <tr>
            <th scope="row">“Não sei quanto sobra, quanto é meu e quanto é da empresa”</th>
            <td><a href="/produtos/gestao-financeira/">Gestão Financeira CPF e CNPJ</a></td>
            <td>Painel de caixa com PF e PJ separados e projeção de 30, 60 e 90 dias</td>
            <td><a href="__PORTAL_GESTAO__" target="_blank" rel="noopener">Abrir&#8599;</a></td>
          </tr>
          <tr>
            <th scope="row">“Perco horas comparando ativos em abas e planilhas”</th>
            <td><a href="/produtos/alpha-invest/">Alpha Invest AI</a></td>
            <td>Triagem e comparação segundo os seus filtros, com a fonte de cada número</td>
            <td><a href="__PORTAL_ALPHA__" target="_blank" rel="noopener">Abrir&#8599;</a></td>
          </tr>
          <tr>
            <th scope="row">“Tenho a carteira montada e não acompanho o que muda nela”</th>
            <td><a href="/produtos/asset-intelligence/">Asset Intelligence AI</a></td>
            <td>Concentração, proventos, eventos e alertas nos limites que você definiu</td>
            <td><a href="__PORTAL_ASSET__" target="_blank" rel="noopener">Abrir&#8599;</a></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="band band--surface">
  <div class="container">
    <h2>O que todos têm em comum</h2>
    <div class="grid g3" style="margin-top:26px">
      <div><h3>Motor determinístico</h3><p class="small">Cálculo versionado por vigência, reproduzível e testado. O mesmo dado devolve o mesmo número anos depois.</p></div>
      <div><h3>Fonte em toda afirmação</h3><p class="small">Norma, dispositivo, link — ou o dado de mercado com origem e data. Sem lastro, não vai para a tela.</p></div>
      <div><h3>Dossiê exportável</h3><p class="small">Hash dos arquivos, versão do motor, cadeia de raciocínio e quem aprovou. Prova, não relatório.</p></div>
    </div>
    <div class="btn-row"><a class="btn btn--solid" href="/contato/">Falar com a DKD</a><a class="btn btn--quiet" href="__WHATSAPP__" target="_blank" rel="noopener" data-lead="whatsapp-produtos">Conversar no WhatsApp</a></div>
  </div>
</section>
"""

# ------------------------------------------------------------- ATC (fiscal)
FISCAL = """
<section class="band band--hero band--surface">
  <div class="container hero-grid">
    <div>
      <p class="eyebrow">DKD Financial Tools AI · Módulo de Análise, Simulação e Inteligência Fiscal e Tributária</p>
      <h1>A carteira inteira numa tela — com o artigo da lei anexado.</h1>
      <p class="lead" style="margin-top:18px">Todo mundo compara regime por CNPJ. Nenhum concorrente responde
      <em>“dos meus 300 clientes, quais 40 perdem margem em 2027 e quanto de honorário isso representa”.</em>
      É essa pergunta que este módulo responde.</p>
      <div class="btn-row">
        <a class="btn btn--solid" href="/contato/">Agendar conversa técnica</a>
        <a class="btn btn--portal" href="__PORTAL_FISCAL__" target="_blank" rel="noopener">Abrir o portal<span aria-hidden="true">&#8599;</span></a>
        <a class="btn btn--quiet" href="__WHATSAPP__" target="_blank" rel="noopener" data-lead="whatsapp-hero">Conversar no WhatsApp</a>
      
      </div>
    </div>
    <div class="card card--pad">
      <p class="eyebrow eyebrow--warn">Prazo em vigor</p>
      <h3>30 de outubro de 2026</h3>
      <p class="small">Prazo prorrogado para a opção pelo regime híbrido do Simples Nacional, com efeito em
      1º de janeiro de 2027. Detalhes no <a href="https://www8.receita.fazenda.gov.br/simplesnacional/" target="_blank" rel="noopener">Portal do Simples Nacional</a>.</p>
      <p class="small" style="margin-bottom:0"><strong>1º de janeiro de 2027:</strong> o Simples entra em todos os modelos,
      a CBS passa a ser cobrada integralmente, PIS e COFINS acabam e o IPI vai a zero.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="container">
    <p class="eyebrow">O problema</p>
    <h2>A decisão tem data marcada e não tem substituto</h2>
    <p class="lead sec-intro">Pesquisa com 633 empresas contábeis mostrou que <strong>61% ainda não mapearam o impacto da reforma nos clientes</strong>.
    Outra, com 149 respondentes, que <strong>68% já foram procurados por clientes mas só 5% têm estratégia estruturada</strong>.
    A demanda existe, o prazo corre, e a oferta está partida em dois extremos: calculadora gratuita que exige digitação manual,
    e ferramenta de R$ 18 mil a R$ 30 mil por ano desenhada para departamento fiscal de indústria.</p>
    <div class="note note--brand">
      <span class="tag">Onde a DKD entra</span>
      <p>O escritório com 80 a 400 CNPJs na carteira não tem produto desenhado para ele. Este módulo ocupa exatamente esse vão:
      lê o SPED que já existe, raciocina sobre a carteira inteira e entrega o parecer que o escritório revende como consultoria.</p>
    </div>
  </div>
</section>

<section class="band band--surface">
  <div class="container">
    <p class="eyebrow">O que o módulo faz</p>
    <h2>Da ingestão ao parecer assinado</h2>
    <div class="grid g2" style="margin-top:28px">
      <div>
        <h3>Ingestão sem digitação</h3>
        <p class="small">Upload direto de EFD ICMS/IPI, EFD-Contribuições, ECD, ECF, XML de NF-e, NFC-e, CT-e e NFS-e,
        PGDAS-D, balancete e cadastro de itens. Arrasta e solta e funciona no primeiro dia — sem projeto de implantação.</p>
      </div>
      <div>
        <h3>Comparador dos quatro regimes</h3>
        <p class="small">Simples puro, Simples híbrido, Lucro Presumido e Lucro Real sobre os números reais do cliente —
        incluindo o efeito de segunda ordem que decide a competitividade B2B: <strong>quanto crédito você transfere ao seu cliente pessoa jurídica</strong>.</p>
      </div>
      <div>
        <h3>Painel da carteira</h3>
        <p class="small">A visão que ninguém entrega: os clientes ordenados por risco em reais, quais migram de regime,
        quais perdem margem em 2027 e quanto de honorário de consultoria essa lista representa para o escritório.</p>
      </div>
      <div>
        <h3>Classificação de CST e cClassTrib</h3>
        <p class="small">Cadastro de itens classificado em lote, com fila de exceção priorizada por impacto financeiro —
        o analista revisa os 40 itens que valem 80% do risco, não 4.000 em ordem alfabética.</p>
      </div>
      <div>
        <h3>Auditoria de documentos fiscais</h3>
        <p class="small">Nota autorizada e não escriturada, item sem NCM ou com NCM inválido, CFOP incompatível com o CST informado,
        campos de IBS e CBS ausentes desde 3 de agosto de 2026, e fornecedor que não gera crédito integral.</p>
      </div>
      <div>
        <h3>Copiloto fiscal com citação</h3>
        <p class="small">Pergunta em linguagem natural sobre o CNPJ aberto, resposta curta com norma, dispositivo e link oficial.
        Filtro de vigência rígido: analisar 2029 com norma de 2033 é o erro silencioso mais caro possível, e ele é bloqueado na origem.</p>
      </div>
    </div>
  </div>
</section>

<section class="band">
  <div class="container">
    <p class="eyebrow">Como funciona</p>
    <h2>Três passos até o entregável</h2>
    <div class="grid g3" style="margin-top:26px">
      <div><p class="eyebrow eyebrow--mute">Passo 1</p><h3>Suba o arquivo</h3><p class="small">Um SPED basta para o primeiro comparativo. Em menos de dez minutos você vê o resultado do primeiro CNPJ.</p></div>
      <div><p class="eyebrow eyebrow--mute">Passo 2</p><h3>Revise o que a ferramenta separou</h3><p class="small">Os itens em que ela se absteve chegam numa fila ordenada por valor em risco. Você decide, e a decisão vira caso de teste.</p></div>
      <div><p class="eyebrow eyebrow--mute">Passo 3</p><h3>Exporte o dossiê</h3><p class="small">Parecer técnico com premissas, dispositivos citados, versão do motor e espaço para a aprovação nominal do contador com CRC.</p></div>
    </div>
  </div>
</section>

<section class="band band--surface">
  <div class="container">
    <h2>Para quem é — e para quem ainda não é</h2>
    <div class="grid g2" style="margin-top:26px">
      <div>
        <h3>É para você se…</h3>
        <ul class="ticks small">
          <li>Tem de 80 a 400 CNPJs na carteira, com pelo menos 30% em Lucro Presumido ou Real</li>
          <li>Já usa software contábil em nuvem e quer uma camada de análise em cima dele</li>
          <li>Quer vender consultoria de reforma, não só escrita fiscal</li>
          <li>Precisa defender por escrito a recomendação que assinou</li>
        </ul>
      </div>
      <div>
        <h3>Ainda não é para você se…</h3>
        <ul class="plain small">
          <li>Sua carteira é só MEI e Simples puro, sem clientes que vendem para pessoa jurídica</li>
          <li>Você é a empresa final e não tem contador — o parecer precisa de responsável técnico habilitado</li>
          <li>Você procura uma calculadora gratuita de resposta única, sem leitura de arquivo</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="band">
  <div class="container">
    <h2>Perguntas que sempre aparecem</h2>
    <div style="margin-top:20px;border-top:1px solid var(--rule)">
      <details><summary>A IA calcula o imposto?</summary><div class="ans">Não, e isso é decisão de projeto. O cálculo roda em motor determinístico versionado por vigência; o modelo de linguagem lê documento, classifica o ambíguo, explica e redige. Quando precisa de um número, ele chama a ferramenta de cálculo e transcreve o retorno — números gerados pelo modelo são descartados.</div></details>
      <details><summary>O que acontece quando a norma muda?</summary><div class="ans">Há um acompanhamento diário do Diário Oficial, do portal do CGIBS e do Portal da NF-e. O compromisso é refletir a norma publicada no corpus em até três dias úteis, e qualquer análise feita sob norma anterior recebe alerta na tela. A alíquota de referência é parâmetro configurável — nunca constante no código.</div></details>
      <details><summary>Quem assina o parecer?</summary><div class="ans">O contador responsável, com CRC. A ferramenta produz insumo técnico com a cadeia de evidência anexada; a decisão tributária e a assinatura são do profissional habilitado. Isso está escrito no contrato e é a razão de o dossiê existir.</div></details>
      <details><summary>Meus dados ficam onde?</summary><div class="ans">Em infraestrutura no Brasil, com o provedor de modelos configurado para não reter o conteúdo enviado. Se a sua política interna exigir que o SPED não saia da máquina do escritório, existe a modalidade local licenciada — fale com a DKD.</div></details>
      <details><summary>Integra com o meu sistema contábil?</summary><div class="ans">O upload direto funciona com qualquer sistema, desde o primeiro dia. Integrações diretas com softwares contábeis são contratadas por módulo — fale com a DKD sobre o seu sistema.</div></details>
    </div>
    <div class="btn-row"><a class="btn btn--solid" href="/contato/">Solicitar proposta</a><a class="btn btn--quiet" href="__WHATSAPP__" target="_blank" rel="noopener" data-lead="whatsapp-fiscal-rodape">Conversar no WhatsApp</a></div>
  </div>
</section>
"""

# ------------------------------------------------------ GESTÃO FINANCEIRA
GESTAO = """
<section class="band band--hero band--surface">
  <div class="container hero-grid">
    <div>
      <p class="eyebrow">DKD Financial Tools AI · Módulo de Planejamento, Controle e Gestão Financeira</p>
      <h1>Quanto sobrou, quanto é seu, e o que vem pela frente.</h1>
      <p class="lead" style="margin-top:18px">Feito para quem é dono, financeiro e caixa da empresa ao mesmo tempo.
      Você sobe os extratos da pessoa física e da jurídica, a ferramenta classifica, separa o que é retirada do que é despesa da empresa,
      e mostra o caixa dos próximos noventa dias com o que já está contratado.</p>
      <div class="btn-row">
        <a class="btn btn--solid" href="/contato/" data-lead="gestao-contato">Falar com a DKD</a>
        <a class="btn btn--portal" href="__PORTAL_GESTAO__" target="_blank" rel="noopener">Abrir o portal<span aria-hidden="true">&#8599;</span></a>
        <a class="btn btn--quiet" href="__WHATSAPP__" target="_blank" rel="noopener" data-lead="whatsapp-hero">Conversar no WhatsApp</a>
      </div>
      <p class="tiny" style="margin-top:14px">Os extratos são processados no seu computador e não passam pelos servidores da DKD.</p>
    </div>
    <div class="card card--pad">
      <p class="eyebrow eyebrow--mute">O sintoma</p>
      <p class="small">“Tem dinheiro na conta, então está tudo bem.” É o erro mais caro do pequeno negócio:
      confundir <strong>saldo</strong> com <strong>resultado</strong>, e confundir o caixa da empresa com o bolso do dono.</p>
      <p class="small" style="margin-bottom:0">Quando a conta é uma só, a empresa financia o padrão de vida sem que ninguém perceba —
      até o mês em que o imposto e o fornecedor caem juntos.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="container">
    <p class="eyebrow">O que o módulo faz</p>
    <h2>Do extrato bruto à decisão da semana</h2>
    <div class="grid g2" style="margin-top:28px">
      <div>
        <h3>Leitura dos extratos</h3>
        <p class="small">Extratos em PDF do Bradesco, Banco do Brasil, Itaú e Safra, faturas de cartão do Bradesco e do Banco do Brasil,
        e planilhas XLSX, XLS e CSV de qualquer banco — contas de pessoa física e de pessoa jurídica no mesmo painel.
        Lançamentos duplicados e transferências entre contas próprias são identificados e não contam duas vezes.</p>
      </div>
      <div>
        <h3>Classificação que você ensina uma vez</h3>
        <p class="small">A ferramenta propõe a categoria, você corrige, e a correção vira regra. Da segunda vez em diante,
        aquele fornecedor já entra classificado — sem macro, sem planilha paralela.</p>
      </div>
      <div>
        <h3>Fronteira entre PF e PJ</h3>
        <p class="small">Pró-labore, distribuição de lucro e retirada informal ficam separados das despesas da operação.
        O resultado da empresa aparece limpo, e o quanto o dono retirou aparece explícito.</p>
      </div>
      <div>
        <h3>Fluxo de caixa previsto, orçado e realizado</h3>
        <p class="small">O orçamento do ano por categoria, a projeção dos meses à frente e o realizado lado a lado, mês a mês —
        para ver cedo o mês em que o caixa aperta, e o quanto o realizado se afastou do que foi planejado.</p>
      </div>
      <div>
        <h3>Pendências e auditoria do fechamento</h3>
        <p class="small">Lançamento sem categoria vai para a fila de pendências. Saldo que não bate com o extrato, transferência
        sem a contrapartida e extrato importado em dobro aparecem na auditoria do mês, critério por critério — antes de o número ir para alguém.</p>
      </div>
      <div>
        <h3>Investimentos e relatório do mês</h3>
        <p class="small">A carteira por produto, com a rentabilidade medida e a comparação com o CDI; e o relatório gerencial
        do mês em XLSX e PDF, com os lançamentos classificados por titular, banco e categoria — o que encurta a conversa de fechamento.</p>
      </div>
    </div>
    <div class="note" style="margin-top:32px">
      <span class="tag">Limite honesto</span>
      <p>Este módulo organiza, projeta e mostra. Ele não substitui o seu contador, não faz escrituração fiscal e não emite obrigação acessória.
      O objetivo é você chegar na reunião de fechamento sabendo o que perguntar.</p>
    </div>
  </div>
</section>

<section class="band band--surface">
  <div class="container">
    <h2>Para quem é</h2>
    <div class="grid g3" style="margin-top:26px">
      <div><h3>Micro e pequeno empresário</h3><p class="small">Faturamento de até alguns milhões por ano, conta de pessoa física e jurídica misturadas, sem departamento financeiro.</p></div>
      <div><h3>Profissional autônomo com CNPJ</h3><p class="small">Médico, advogado, engenheiro, consultor — quem emite nota pela empresa e vive do que retira dela.</p></div>
      <div><h3>Escritório que atende esse perfil</h3><p class="small">O contador usa como camada de organização antes do fechamento e devolve ao cliente um painel que ele entende sozinho.</p></div>
    </div>
    <div class="btn-row"><a class="btn btn--solid" href="/contato/" data-lead="gestao-contato-rodape">Solicitar proposta</a><a class="btn btn--quiet" href="__WHATSAPP__" target="_blank" rel="noopener" data-lead="whatsapp-gestao-rodape">Conversar no WhatsApp</a></div>
  </div>
</section>
"""

# ------------------------------------------------------------ ALPHA INVEST
DISCLAIMER_CVM = f"""<div class="note note--warn">
  <span class="tag">Aviso obrigatório</span>
  <p>{AVISO_CVM}</p>
</div>"""

ALPHA = f"""
<section class="band band--hero band--surface">
  <div class="container hero-grid">
    <div>
      <p class="eyebrow">DKD Financial Tools AI · Módulo Alpha Invest AI</p>
      <h1>Seus critérios, aplicados a tudo — em segundos.</h1>
      <p class="lead" style="margin-top:18px">Você define o que importa: liquidez mínima, faixa de vacância, histórico de distribuição,
      segmento, alavancagem, o que for. A ferramenta varre a base, aplica os seus filtros e devolve a comparação com a fonte de cada número.
      <strong>Quem escolhe continua sendo você.</strong></p>
      <div class="btn-row">
        <a class="btn btn--solid" href="/contato/">Falar com a DKD</a>
        <a class="btn btn--portal" href="__PORTAL_ALPHA__" target="_blank" rel="noopener">Abrir o portal<span aria-hidden="true">&#8599;</span></a>
        <a class="btn btn--quiet" href="__WHATSAPP__" target="_blank" rel="noopener" data-lead="whatsapp-hero">Conversar no WhatsApp</a>
      
      </div>
    </div>
    <div class="card card--pad">
      <p class="eyebrow eyebrow--mute">O que muda</p>
      <p class="small">A triagem que consome um sábado inteiro entre abas, sites de dados e uma planilha que ninguém mais entende
      passa a levar minutos — e fica registrada, com os critérios explícitos e reaplicáveis no mês seguinte.</p>
      <p class="small" style="margin-bottom:0">Sem carteira pronta. Sem “os melhores da semana”. Sem palpite.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="container">
    {DISCLAIMER_CVM}
    <p class="eyebrow">O que o módulo faz</p>
    <h2>Triagem, comparação e memória de critério</h2>
    <div class="grid g2" style="margin-top:28px">
      <div>
        <h3>Filtros que são seus</h3>
        <p class="small">Você monta o conjunto de critérios uma vez e ele fica salvo. Reaplicar no mês seguinte é um clique,
        e a ferramenta mostra o que entrou e o que saiu da lista desde a última execução.</p>
      </div>
      <div>
        <h3>Comparação lado a lado</h3>
        <p class="small">Os ativos que passaram no seu filtro, na mesma tela, com o histórico do indicador e o link para a origem pública de cada número —
        relatório do administrador, comunicado, demonstração financeira.</p>
      </div>
      <div>
        <h3>Leitura de documento</h3>
        <p class="small">Relatórios gerenciais, comunicados e fatos relevantes lidos e resumidos, com a citação do trecho que sustenta o resumo.
        Se o documento não sustentar a frase, ela é marcada como não verificada.</p>
      </div>
      <div>
        <h3>Nenhum número inventado</h3>
        <p class="small">O mesmo princípio dos outros módulos: indicador é calculado por motor determinístico a partir do dado de origem,
        com data e fonte carimbadas. O modelo de linguagem lê e explica — não faz conta.</p>
      </div>
    </div>
  </div>
</section>

<section class="band band--surface">
  <div class="container">
    <h2>O que este módulo deliberadamente não faz</h2>
    <p class="sec-intro lead">Esta lista é uma escolha de produto e de conformidade — e vale a pena ler antes de contratar.</p>
    <div class="grid g3" style="margin-top:8px">
      <div><h3>Não recomenda ativo</h3><p class="small">Não existe lista de “melhores”, ranking de compra, nota de recomendação nem carteira sugerida. A ferramenta ordena pelo critério que <em>você</em> escolheu.</p></div>
      <div><h3>Não avalia o seu perfil</h3><p class="small">Não há suitability, nem adequação de perfil, nem orientação personalizada — atividades privativas de quem tem registro na CVM.</p></div>
      <div><h3>Não executa ordem</h3><p class="small">Nenhuma integração com corretora para comprar ou vender. A execução acontece onde você já opera, por sua decisão.</p></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="container">
    <h2>Perguntas frequentes</h2>
    <div style="margin-top:20px;border-top:1px solid var(--rule)">
      <details><summary>Vocês dizem o que eu devo comprar?</summary><div class="ans">Não. A DKD não é consultora nem analista de valores mobiliários registrada na CVM, e a ferramenta não emite recomendação. Ela aplica os critérios que você definiu e mostra o resultado com a fonte de cada dado. A decisão e a responsabilidade por ela são inteiramente suas.</div></details>
      <details><summary>De onde vêm os dados?</summary><div class="ans">De fontes públicas de mercado e dos documentos divulgados pelos próprios emissores e administradores. Cada número exibido carrega a origem e a data de referência, para você conseguir conferir.</div></details>
      <details><summary>Os dados são em tempo real?</summary><div class="ans">Os dados de mercado têm defasagem inerente à fonte pública utilizada, e essa defasagem aparece na tela junto com o número. A ferramenta é de análise e triagem — não é plataforma de negociação.</div></details>
      <details><summary>Posso exportar o que a ferramenta produz?</summary><div class="ans">Sim, com os critérios aplicados, as fontes e a data-base registrados no próprio arquivo — para você reproduzir a análise depois e entender por que a lista era aquela naquele dia.</div></details>
    </div>
    <div class="btn-row"><a class="btn btn--solid" href="/contato/">Solicitar proposta</a><a class="btn btn--quiet" href="/produtos/asset-intelligence/">Ver o Asset Intelligence</a></div>
  </div>
</section>
"""

# ------------------------------------------------------- ASSET INTELLIGENCE
ASSET = f"""
<section class="band band--hero band--surface">
  <div class="container hero-grid">
    <div>
      <p class="eyebrow">DKD Financial Tools AI · Módulo Asset Intelligence AI</p>
      <h1>A carteira que você já tem, sob observação.</h1>
      <p class="lead" style="margin-top:18px">Montar a carteira é o começo. O trabalho de verdade é perceber o que mudou nela:
      a concentração que cresceu sem você notar, o provento que caiu, o comunicado que ninguém leu.
      Este módulo acompanha e avisa — <strong>nos limites que você mesmo definiu</strong>.</p>
      <div class="btn-row">
        <a class="btn btn--solid" href="/contato/">Falar com a DKD</a>
        <a class="btn btn--portal" href="__PORTAL_ASSET__" target="_blank" rel="noopener">Abrir o portal<span aria-hidden="true">&#8599;</span></a>
        <a class="btn btn--quiet" href="__WHATSAPP__" target="_blank" rel="noopener" data-lead="whatsapp-hero">Conversar no WhatsApp</a>
      
      </div>
    </div>
    <div class="card card--pad">
      <p class="eyebrow eyebrow--mute">O ponto cego</p>
      <p class="small">A maior parte do risco de uma carteira de pessoa física não vem da escolha inicial.
      Vem da <strong>concentração que se acumula sem intenção</strong> — aportes repetidos no que é familiar,
      até um único emissor ou setor responder por metade do patrimônio.</p>
      <p class="small" style="margin-bottom:0">É um número simples. Quase ninguém o recalcula todo mês.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="container">
    {DISCLAIMER_CVM}
    <p class="eyebrow">O que o módulo faz</p>
    <h2>Acompanhamento com critério explícito</h2>
    <div class="grid g2" style="margin-top:28px">
      <div>
        <h3>Concentração recalculada</h3>
        <p class="small">Por ativo, por segmento, por emissor e por administrador, atualizada a cada aporte.
        Mostra a distância entre onde a carteira está e os limites que você declarou querer respeitar.</p>
      </div>
      <div>
        <h3>Proventos e eventos</h3>
        <p class="small">Distribuições recebidas e anunciadas, amortizações, desdobramentos, emissões e subscrições,
        organizados por data, com o documento de origem ao lado.</p>
      </div>
      <div>
        <h3>Comunicados lidos e resumidos</h3>
        <p class="small">Fatos relevantes e relatórios dos ativos que você tem, resumidos em linguagem direta,
        sempre com o trecho citado e o link do documento oficial.</p>
      </div>
      <div>
        <h3>Alertas que você configura</h3>
        <p class="small">Limite de concentração ultrapassado, queda de distribuição em relação à média,
        evento societário com prazo de decisão e vencimento próximo. O alerta informa — não instrui.</p>
      </div>
      <div>
        <h3>Histórico auditável</h3>
        <p class="small">A carteira em qualquer data passada, com os preços e critérios daquele momento —
        para você entender a decisão que tomou com a informação que tinha, e não com a de hoje.</p>
      </div>
      <div>
        <h3>Relatório do período</h3>
        <p class="small">Exportável, com aportes, proventos, variação de composição e as fontes carimbadas.
        Serve para a sua conferência e para a conversa com o seu contador na declaração anual.</p>
      </div>
    </div>
  </div>
</section>

<section class="band band--surface">
  <div class="container">
    <h2>Alpha Invest ou Asset Intelligence?</h2>
    <div class="tablewrap" style="margin-top:24px">
      <table>
        <caption>Os dois módulos são independentes e se complementam: um olha para fora da carteira, o outro para dentro.</caption>
        <thead><tr><th>&nbsp;</th><th>Alpha Invest AI</th><th>Asset Intelligence AI</th></tr></thead>
        <tbody>
          <tr><th scope="row">Pergunta que responde</th><td>“O que passa nos meus critérios?”</td><td>“O que mudou no que eu já tenho?”</td></tr>
          <tr><th scope="row">Universo</th><td>Todos os ativos da base</td><td>Só a sua carteira</td></tr>
          <tr><th scope="row">Momento de uso</th><td>Quando você vai aportar</td><td>Toda semana, sem você pedir</td></tr>
          <tr><th scope="row">Saída principal</th><td>Lista comparada com fontes</td><td>Alertas, concentração e eventos</td></tr>
          <tr><th scope="row">Recomenda ativo?</th><td>Não</td><td>Não</td></tr>
        </tbody>
      </table>
    </div>
    <div class="btn-row"><a class="btn btn--solid" href="/contato/">Solicitar proposta</a><a class="btn btn--quiet" href="/produtos/alpha-invest/">Ver o Alpha Invest</a></div>
  </div>
</section>
"""
