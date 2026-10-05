(function(){
  var b=document.querySelector('.burger'),n=document.querySelector('.nav');
  if(b&&n){b.addEventListener('click',function(){
    var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});}

  // Contagem regressiva para o fim da janela de opção pelo regime híbrido.
  // TODO: revisar a data quando a janela de setembro/2026 se encerrar.
  var alvo=new Date('2026-09-30T23:59:59-03:00');
  document.querySelectorAll('[data-count]').forEach(function(el){
    function tick(){
      var d=alvo-new Date();
      if(d<0){el.innerHTML='<p class="mono">A janela de 30/09/2026 encerrou. Fale com a DKD sobre os próximos marcos.</p>';return;}
      var dias=Math.floor(d/864e5),h=Math.floor(d/36e5)%24,m=Math.floor(d/6e4)%60;
      el.querySelector('[data-d]').textContent=dias;
      el.querySelector('[data-h]').textContent=('0'+h).slice(-2);
      el.querySelector('[data-m]').textContent=('0'+m).slice(-2);
    }
    tick();setInterval(tick,30000);
  });

  // ------------------------------------------------------------- eventos
  // Manda o evento para o Zaraz quando ele existir. Sem Zaraz configurado,
  // não acontece nada — nenhum erro no console, nenhuma tela quebrada.
  function evento(nome, dados){
    try{ if(window.zaraz && typeof zaraz.track==='function') zaraz.track(nome, dados||{}); }catch(e){}
  }

  // De onde a pessoa veio, para viajar junto com o lead.
  document.querySelectorAll('[data-referrer]').forEach(function(i){
    i.value = document.referrer || 'direto';
  });

  // Cliques que valem dinheiro: WhatsApp, CTA do topo, abrir portal.
  document.addEventListener('click', function(e){
    var a = e.target.closest && e.target.closest('a');
    if(!a) return;
    var marca = a.getAttribute('data-lead');
    if(marca) evento('cta_clique', {onde: marca, pagina: location.pathname});
    if(a.classList.contains('btn--portal') || /portais\//.test(a.getAttribute('href')||''))
      evento('portal_aberto', {pagina: location.pathname});
  }, true);

  // Formulário: quando começa a preencher e quando envia.
  document.querySelectorAll('[data-lead-form]').forEach(function(f){
    var origem = f.getAttribute('data-lead-form'), comecou = false;
    f.addEventListener('input', function(){
      if(comecou) return; comecou = true;
      evento('formulario_iniciado', {origem: origem});
    });
    f.addEventListener('submit', function(){
      var m = f.querySelector('[name=modulo]');
      evento('lead_enviado', {origem: origem, modulo: m ? m.value : ''});
    });
  });

  // Resposta do envio, sem tirar a pessoa da página.
  var q = new URLSearchParams(location.search);
  var caixa = document.querySelector('[data-aviso]');
  if(caixa && (q.get('ok') || q.get('erro'))){
    var erros = {
      campos: 'Faltou preencher nome, e-mail ou mensagem. Confira e envie de novo.',
      robo: 'A verificação de segurança não passou. Recarregue a página e tente mais uma vez.',
      envio: 'O envio falhou do nosso lado. Escreva direto para comercial@dkdtecnologia.com — respondemos igual.',
      inesperado: 'Algo saiu errado no envio. Escreva direto para comercial@dkdtecnologia.com.'
    };
    var e = q.get('erro');
    caixa.className = 'aviso-form ' + (e ? 'aviso-form--erro' : 'aviso-form--ok');
    caixa.innerHTML = e
      ? '<strong>Não deu para enviar.</strong> ' + (erros[e] || erros.inesperado)
      : '<strong>Recebido.</strong> Respondemos em até um dia útil, no e-mail que você informou.';
    caixa.hidden = false;
    caixa.setAttribute('role','status');
    caixa.scrollIntoView({block:'center', behavior:'smooth'});
    if(!e) evento('lead_confirmado', {pagina: location.pathname});
    history.replaceState(null, '', location.pathname + location.hash);
  }
})();
