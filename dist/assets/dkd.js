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

  // ------------------------------------------------ cadastro do teste grátis
  // Máscara e conferência do CPF/CNPJ (inclusive o CNPJ com letras, emitido
  // pela Receita desde 31/07/2026), campos da empresa só para PJ, envio único,
  // e a resposta do servidor (?ok=1 ou ?erro=...) sem tirar a pessoa da página.
  var cad = document.querySelector('[data-cadastro]');
  if(cad){
    var RASCUNHO = 'dkd_cadastro_rascunho';
    var doc = cad.querySelector('[name=documento]');
    var emp = cad.querySelector('[name=empresa]');
    var rot = cad.querySelector('[data-rotulo-doc]');
    var ajuda = cad.querySelector('[data-ajuda-doc]');
    var botao = cad.querySelector('[data-enviar]');
    var textoBotao = botao ? botao.textContent : '';
    var soAlnum = function(v){ return String(v||'').toUpperCase().replace(/[^0-9A-Z]/g,''); };
    var cpfOk = function(c){
      c = String(c||'').replace(/\D/g,'');
      if(c.length !== 11 || /^(\d)\1{10}$/.test(c)) return false;
      for(var t=9; t<11; t++){
        var s = 0; for(var i=0; i<t; i++) s += (+c[i]) * (t+1-i);
        if(((s*10) % 11) % 10 !== +c[t]) return false;
      }
      return true;
    };
    var cnpjOk = function(c){
      c = soAlnum(c);
      if(!/^[0-9A-Z]{12}\d{2}$/.test(c) || /^(.)\1{13}$/.test(c)) return false;
      var dv = function(n){
        var p = n === 12 ? [5,4,3,2,9,8,7,6,5,4,3,2] : [6,5,4,3,2,9,8,7,6,5,4,3,2], s = 0;
        for(var i=0; i<p.length; i++) s += (c.charCodeAt(i) - 48) * p[i];
        var r = s % 11; return r < 2 ? 0 : 11 - r;
      };
      return dv(12) === +c[12] && dv(13) === +c[13];
    };
    var mascara = function(v, pj){
      var d = pj ? soAlnum(v).slice(0,14) : String(v||'').replace(/\D/g,'').slice(0,11);
      var cortes = pj ? {2:'.',5:'.',8:'/',12:'-'} : {3:'.',6:'.',9:'-'}, o = '';
      for(var i=0; i<d.length; i++){ if(cortes[i]) o += cortes[i]; o += d[i]; }
      return o;
    };
    var ehPJ = function(){ var r = cad.querySelector('[name=tipo]:checked'); return !r || r.value === 'PJ'; };
    var confereDoc = function(){
      if(!doc) return true;
      var v = doc.value, pj = ehPJ(), ok = !v || (pj ? cnpjOk(v) : cpfOk(v));
      doc.setCustomValidity(ok ? '' : (pj ? 'Este CNPJ não confere. Confira os caracteres — o CNPJ novo pode ter letras.'
                                          : 'Este CPF não confere. Confira os números.'));
      return ok;
    };
    var ajustaTipo = function(){
      var pj = ehPJ();
      cad.querySelectorAll('[data-so-pj]').forEach(function(el){ el.hidden = !pj; });
      if(emp) emp.required = pj;
      if(rot) rot.textContent = pj ? 'CNPJ' : 'CPF';
      if(ajuda) ajuda.textContent = pj ? 'Aceita o CNPJ numérico e o novo CNPJ com letras.'
                                       : 'No portal, o CPF aparece mascarado.';
      if(doc){
        doc.placeholder = pj ? '00.000.000/0000-00' : '000.000.000-00';
        doc.inputMode = pj ? 'text' : 'numeric';
        doc.maxLength = pj ? 18 : 14;
        doc.value = mascara(doc.value, pj);
        confereDoc();
      }
    };
    cad.querySelectorAll('[name=tipo]').forEach(function(r){ r.addEventListener('change', ajustaTipo); });
    if(doc){
      doc.addEventListener('input', function(){ doc.value = mascara(doc.value, ehPJ()); confereDoc(); });
      doc.addEventListener('blur', function(){ if(doc.value && !confereDoc()) doc.reportValidity(); });
    }
    cad.addEventListener('submit', function(ev){
      confereDoc();
      if(!cad.checkValidity()){ ev.preventDefault(); cad.reportValidity(); return; }
      // guarda o que foi digitado só nesta aba, para refazer o formulário se o servidor devolver erro
      try{
        var g = {};
        ['nome','email','empresa','documento','telefone','cidade','uf'].forEach(function(k){
          var el = cad.querySelector('[name=' + k + ']'); if(el) g[k] = el.value; });
        g.tipo = ehPJ() ? 'PJ' : 'PF';
        sessionStorage.setItem(RASCUNHO, JSON.stringify(g));
      }catch(e){}
      if(botao){ botao.disabled = true; botao.textContent = 'Enviando…'; }
    });
    window.addEventListener('pageshow', function(){ if(botao){ botao.disabled = false; botao.textContent = textoBotao; } });
    ajustaTipo();

    var qc = new URLSearchParams(location.search);
    var caixaCad = document.querySelector('[data-aviso="cadastro"]');
    var okBloco = document.querySelector('[data-cadastro-ok]');
    var rasc = null;
    try{ rasc = JSON.parse(sessionStorage.getItem(RASCUNHO) || 'null'); }catch(e){}
    if(qc.get('ok')){
      try{ sessionStorage.removeItem(RASCUNHO); }catch(e){}
      cad.hidden = true;
      if(okBloco){ okBloco.hidden = false; okBloco.setAttribute('role','status');
                   okBloco.scrollIntoView({block:'center', behavior:'smooth'}); }
      evento('cadastro_confirmado', {pagina: location.pathname});
      history.replaceState(null, '', location.pathname + '#cadastro');
    }else if(qc.get('erro') && caixaCad){
      var M = 'comercial@dkdtecnologia.com';
      var errosCad = {
        campos: 'Faltou o nome, o e-mail ou — para empresa — a razão social. Confira e envie de novo.',
        email: 'Esse e-mail não parece válido. Confira e envie de novo.',
        documento: 'O CPF ou o CNPJ não confere. Confira os caracteres e envie de novo.',
        aceite: 'Para criar o cadastro, marque que leu e aceita os Termos de Uso e a Política de Privacidade.',
        limite: 'Muitos cadastros seguidos a partir desta conexão. Tente de novo em uma hora, ou escreva para ' + M + '.',
        robo: 'A verificação de segurança não passou. Recarregue a página e tente mais uma vez.',
        indisponivel: 'O cadastro está em manutenção agora. Tente de novo em alguns minutos, ou escreva para ' + M + '.',
        inesperado: 'Algo saiu errado no envio. Tente de novo, ou escreva para ' + M + '.'
      };
      var er = qc.get('erro');
      if(rasc){
        if(rasc.tipo){ var rb = cad.querySelector('[name=tipo][value="' + rasc.tipo + '"]'); if(rb) rb.checked = true; }
        Object.keys(rasc).forEach(function(k){
          if(k === 'tipo') return;
          var el = cad.querySelector('[name=' + k + ']'); if(el) el.value = rasc[k] || '';
        });
        ajustaTipo();
        try{ sessionStorage.removeItem(RASCUNHO); }catch(e){}
      }
      caixaCad.className = 'aviso-form aviso-form--erro';
      caixaCad.innerHTML = '<strong>O cadastro não foi concluído.</strong> ' + (errosCad[er] || errosCad.inesperado);
      caixaCad.hidden = false;
      caixaCad.setAttribute('role','alert');
      caixaCad.scrollIntoView({block:'center', behavior:'smooth'});
      history.replaceState(null, '', location.pathname + '#cadastro');
    }
  }

  // Resposta do envio, sem tirar a pessoa da página.
  var q = new URLSearchParams(location.search);
  var caixa = document.querySelector('[data-aviso]:not([data-aviso="cadastro"])');
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
