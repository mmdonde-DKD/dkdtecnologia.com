// worker/admin.js — painel de licenças da DKD, servido em /admin pelo próprio Worker.
//
// A página não guarda segredo nenhum: tudo o que ela faz passa pela API
// /api/admin/*, que exige o ADMIN_TOKEN no cabeçalho. Mesmo assim, coloque
// /admin* e /api/admin/* atrás do Cloudflare Access (Zero Trust → Access →
// Applications), liberado só para o seu e-mail — é a segunda tranca.

const HTML = String.raw`<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Licenças · DKD Financial Tools AI</title>
<style>
:root{--bg:#060e1b;--bg2:#08131f;--sf:#0b1a2e;--sf2:#0e2138;--ln:#1e3550;--ln2:#2b4a6b;--tx:#e8eef5;--tx2:#a9b7c6;--tx3:#7a8ca3;
  --az:#3fa9f0;--ok:#34d399;--wa:#fbbf24;--cr:#f87171;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);font:14px/1.5 "Segoe UI",system-ui,sans-serif}
header{display:flex;align-items:center;gap:16px;padding:14px 22px;background:var(--bg2);border-bottom:1px solid var(--ln);position:sticky;top:0;z-index:5}
header .m{font-size:17px;color:#c9d1d8}header .m b{color:#f2f5f7}header .s{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--tx3)}
main{padding:20px 22px;max-width:1500px;margin:0 auto}
.kp{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:16px}
.kp div{background:var(--sf);border:1px solid var(--ln);border-radius:10px;padding:12px 14px}.kp b{display:block;font-size:24px}.kp span{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--tx3)}
input,select,textarea{background:#050d18;border:1px solid var(--ln2);color:var(--tx);border-radius:8px;padding:8px 10px;font:inherit}
input:focus,select:focus,textarea:focus{outline:2px solid var(--az);outline-offset:1px}
button{background:var(--sf2);color:var(--tx);border:1px solid var(--ln2);border-radius:8px;padding:8px 14px;font:inherit;font-weight:600;cursor:pointer}
button:hover{border-color:var(--az)}button.pri{background:var(--az);color:#03101e;border-color:var(--az)}button.ghost{background:none}
button.xs{padding:3px 9px;font-size:12px}button:disabled{opacity:.5;cursor:default}
table{width:100%;border-collapse:collapse;font-size:13px}th{text-align:left;font-size:11px;letter-spacing:.07em;text-transform:uppercase;color:var(--tx3);font-weight:600;padding:8px;border-bottom:1px solid var(--ln)}
td{padding:8px;border-bottom:1px solid #12233a;vertical-align:top}tbody tr{cursor:pointer}tbody tr:hover{background:#0c1d32}
.mono{font-family:ui-monospace,Consolas,monospace;font-size:12.5px}.hint{color:var(--tx3);font-size:12px}
.pill{display:inline-block;padding:1px 8px;border-radius:99px;font-size:11.5px;font-weight:600;border:1px solid}
.p-ok{color:var(--ok);border-color:rgba(52,211,153,.4)}.p-wa{color:var(--wa);border-color:rgba(251,191,36,.4)}.p-cr{color:var(--cr);border-color:rgba(248,113,113,.4)}.p-az{color:var(--az);border-color:rgba(63,169,240,.4)}
.lay{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(360px,1fr);gap:16px;align-items:start}
.card{background:var(--sf);border:1px solid var(--ln);border-radius:12px;padding:16px}
.card h2{font-size:15px;margin:0 0 10px}.card h3{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--tx3);margin:18px 0 8px}
.fl{display:grid;grid-template-columns:1fr 1fr;gap:10px}.fl label{display:block;font-size:11px;letter-spacing:.07em;text-transform:uppercase;color:var(--tx3);margin-bottom:4px}
.fl input,.fl select{width:100%}.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
#login{max-width:420px;margin:12vh auto}#login .card{padding:26px}
.msg{min-height:18px;font-size:13px;margin:8px 0}.msg.e{color:var(--cr)}.msg.o{color:var(--ok)}
textarea.chave{width:100%;font:12px/1.5 ui-monospace,Consolas,monospace}
@media (max-width:1000px){.lay{grid-template-columns:1fr}.kp{grid-template-columns:repeat(2,1fr)}}
</style></head><body>
<header><div><div class="m">DKD <b>Financial Tools AI</b></div><div class="s">Painel de licenças</div></div>
<div style="flex:1"></div><span class="hint" id="dig"></span><button class="ghost xs" id="sair" hidden>Sair</button></header>

<div id="login"><div class="card"><h2>Entrar no painel</h2>
<p class="hint">Use o ADMIN_TOKEN configurado no Worker. Ele fica só nesta aba do navegador.</p>
<input id="tok" type="password" autocomplete="off" style="width:100%" placeholder="ADMIN_TOKEN">
<div class="msg e" id="lmsg"></div><button class="pri" id="entrar">Entrar</button></div></div>

<main id="app" hidden>
  <div class="kp"><div><span>Clientes</span><b id="k1">—</b></div><div><span>Em avaliação</span><b id="k2">—</b></div>
    <div><span>Pagantes</span><b id="k3">—</b></div><div><span>Suspensos ou cancelados</span><b id="k4">—</b></div></div>
  <div class="lay">
    <div class="card">
      <div class="row" style="margin-bottom:10px"><input id="q" placeholder="Buscar por nome, e-mail, documento ou série" style="flex:1">
        <button id="buscar">Buscar</button></div>
      <div style="overflow:auto"><table><thead><tr><th>Série</th><th>Cliente</th><th>Plano</th><th>Validade</th><th>PCs</th><th>Último contato</th></tr></thead>
      <tbody id="lista"></tbody></table></div>
    </div>
    <div class="card" id="det"><p class="hint">Escolha um cliente na lista.</p></div>
  </div>
</main>

<script>
(function(){
  var T = sessionStorage.getItem('dkd_admin') || '';
  var HOJE = '';
  function $(id){ return document.getElementById(id); }
  function e(s){ return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];}); }
  function br(d){ return d ? String(d).slice(0,10).split('-').reverse().join('/') : '—'; }
  function dias(a,b){ return Math.round((Date.parse(b+'T12:00:00Z')-Date.parse(a+'T12:00:00Z'))/864e5); }
  function soma(iso,n){ var d=new Date(iso+'T12:00:00Z'); d.setUTCDate(d.getUTCDate()+n); return d.toISOString().slice(0,10); }
  function api(met, rota, corpo){
    return fetch('/api/admin/'+rota, {method:met, headers:{'Authorization':'Bearer '+T,'Content-Type':'application/json'},
      body: corpo ? JSON.stringify(corpo) : undefined}).then(function(r){ return r.json().then(function(j){ j._st=r.status; return j; }); });
  }
  function pillValidade(c){
    if(c.status!=='ativo') return '<span class="pill p-cr">'+e(c.status)+'</span>';
    if(!c.validade) return '<span class="pill p-az">não ativou</span>';
    var d = dias(HOJE, c.validade);
    var cls = d < 0 ? 'p-cr' : d <= 7 ? 'p-wa' : 'p-ok';
    return br(c.validade)+' <span class="pill '+cls+'">'+(d<0?'venceu':d+' d')+'</span>';
  }
  function carregar(){
    api('GET','clientes?q='+encodeURIComponent($('q').value||'')).then(function(j){
      if(j._st===401){ sair(); $('lmsg').textContent='Token recusado.'; return; }
      if(!j.ok){ $('lista').innerHTML='<tr><td colspan="6" class="hint">'+e(j.erro)+'</td></tr>'; return; }
      HOJE = j.hoje;
      var t=j.totais||{}; $('k1').textContent=t.n||0; $('k2').textContent=t.avaliacao||0; $('k3').textContent=t.pagantes||0; $('k4').textContent=t.inativos||0;
      $('lista').innerHTML = j.clientes.map(function(c){
        var rep = c.mesmo_doc ? ' <span class="pill p-wa" title="Outro cadastro usa o mesmo CPF/CNPJ — confira se não é a mesma pessoa repetindo a avaliação">mesmo doc. ×'+(c.mesmo_doc+1)+'</span>' : '';
        return '<tr data-id="'+c.id+'"><td class="mono">'+e(c.serie)+'</td><td><b>'+e(c.empresa||c.nome)+'</b>'+rep+'<div class="hint">'+e(c.email)+'</div></td>'+
          '<td>'+e(c.plano)+'</td><td>'+pillValidade(c)+'</td><td>'+c.ativos+' / '+c.limite_dispositivos+'</td><td class="hint">'+br(c.ultimo_contato)+'</td></tr>';
      }).join('') || '<tr><td colspan="6" class="hint">Nenhum cliente.</td></tr>';
      Array.prototype.forEach.call(document.querySelectorAll('#lista tr[data-id]'), function(tr){ tr.onclick=function(){ detalhe(+tr.dataset.id); }; });
    });
  }
  function detalhe(id){
    api('GET','cliente?id='+id).then(function(j){
      if(!j.ok){ $('det').innerHTML='<p class="msg e">'+e(j.erro)+'</p>'; return; }
      var c=j.cliente, planos=['avaliacao','mensal','trimestral','semestral','anual','cortesia','parceiro'];
      if(planos.indexOf(c.plano)<0) planos.push(c.plano);
      $('det').innerHTML =
        '<h2>'+e(c.empresa||c.nome)+'</h2><div class="hint mono">'+e(c.serie)+' · '+e(c.email)+' · '+e(c.tipo)+' '+e(c.documento)+'</div>'+
        '<div class="hint">'+e(c.telefone||'')+' · '+e(c.cidade||'')+(c.uf?'/'+e(c.uf):'')+' · cadastro '+br(c.criado_em)+' · origem '+e(c.origem||'')+'</div>'+
        '<h3>Licença</h3><div class="fl">'+
        '<div><label>Plano</label><select id="fPlano">'+planos.map(function(p){return '<option'+(p===c.plano?' selected':'')+'>'+p+'</option>';}).join('')+'</select></div>'+
        '<div><label>Status</label><select id="fSt">'+['ativo','suspenso','cancelado'].map(function(s){return '<option'+(s===c.status?' selected':'')+'>'+s+'</option>';}).join('')+'</select></div>'+
        '<div><label>Válida até</label><input type="date" id="fVal" value="'+e(c.validade||'')+'"></div>'+
        '<div><label>Computadores</label><input type="number" min="1" max="20" id="fLim" value="'+c.limite_dispositivos+'"></div></div>'+
        '<div class="row" style="margin-top:8px"><span class="hint">Estender a partir de hoje ou da validade:</span>'+
        [30,90,180,365].map(function(n){return '<button class="xs" data-ext="'+n+'">+'+n+' d</button>';}).join('')+'</div>'+
        '<div style="margin-top:10px"><label class="hint">Observação interna</label><textarea id="fObs" rows="2" style="width:100%">'+e(c.obs||'')+'</textarea></div>'+
        '<div class="row" style="margin-top:8px"><button class="pri" id="salvar">Salvar</button><span class="msg" id="smsg"></span></div>'+
        '<h3>Computadores ('+j.dispositivos.filter(function(d){return d.ativo;}).length+' ativos)</h3>'+
        (j.dispositivos.map(function(d){
          return '<div class="row" style="justify-content:space-between;border-bottom:1px solid #12233a;padding:6px 0"><div><span class="mono">'+e(d.dispositivo.match(/.{1,4}/g).join('-'))+'</span> '+
            (d.ativo?'<span class="pill p-ok">ativo</span>':'<span class="pill p-cr">removido</span>')+'<div class="hint">'+e(d.rotulo||'')+' · '+e(d.versao||'')+' · último contato '+br(d.ultimo_contato)+'</div></div>'+
            '<button class="xs" data-disp="'+e(d.dispositivo)+'" data-at="'+(d.ativo?0:1)+'">'+(d.ativo?'Remover':'Reativar')+'</button></div>';
        }).join('') || '<p class="hint">Ainda não ativou em nenhum computador.</p>')+
        '<h3>Ações</h3><div class="row"><button id="reenv">Reenviar boas-vindas</button></div>'+
        '<div style="margin-top:10px"><label class="hint">Chave manual (cliente sem internet): identificador do computador, ou * para qualquer um</label>'+
        '<div class="row"><input id="kDisp" placeholder="ABCD-EFGH-JKLM ou *" style="flex:1"><label class="hint"><input type="checkbox" id="kMail"> enviar por e-mail</label><button id="kGerar">Emitir chave</button></div>'+
        '<textarea class="chave" id="kOut" rows="3" readonly hidden></textarea></div>'+
        '<h3>Eventos</h3><div style="max-height:260px;overflow:auto">'+j.eventos.map(function(v){
          return '<div style="font-size:12.5px;border-bottom:1px solid #12233a;padding:4px 0"><span class="hint">'+br(v.criado_em)+' '+e(String(v.criado_em).slice(11,16))+'</span> <b>'+e(v.tipo)+'</b> '+e(v.detalhe||'')+'</div>';
        }).join('')+'</div>';
      Array.prototype.forEach.call(document.querySelectorAll('[data-ext]'), function(b){ b.onclick=function(){
        var base = $('fVal').value && $('fVal').value > HOJE ? $('fVal').value : HOJE;
        $('fVal').value = soma(base, +b.dataset.ext); }; });
      $('salvar').onclick=function(){
        api('POST','cliente',{id:c.id, plano:$('fPlano').value, status:$('fSt').value, validade:$('fVal').value,
          limite_dispositivos:+$('fLim').value, obs:$('fObs').value}).then(function(r){
          $('smsg').className='msg '+(r.ok?'o':'e'); $('smsg').textContent = r.ok ? 'Salvo. O portal do cliente recebe na próxima abertura com internet.' : ('Erro: '+r.erro);
          carregar(); });
      };
      Array.prototype.forEach.call(document.querySelectorAll('[data-disp]'), function(b){ b.onclick=function(){
        api('POST','dispositivo',{cliente_id:c.id, dispositivo:b.dataset.disp, ativo:+b.dataset.at}).then(function(){ detalhe(c.id); carregar(); }); }; });
      $('reenv').onclick=function(){ api('POST','reenviar',{cliente_id:c.id}).then(function(r){ alertar(r.ok?'E-mail reenviado ('+r.via+').':'Falhou: '+(r.erro||r.via)); detalhe(c.id); }); };
      $('kGerar').onclick=function(){
        var d=$('kDisp').value.trim(); if(d!=='*') d=d.replace(/[^A-Za-z0-9]/g,'').toUpperCase();
        api('POST','chave',{cliente_id:c.id, dispositivo:d, enviar:$('kMail').checked}).then(function(r){
          var o=$('kOut'); o.hidden=false; o.value = r.ok ? r.chave : ('Erro: '+r.erro); if(r.ok){ o.select(); } });
      };
    });
  }
  function alertar(t){ var m=$('smsg'); if(m){ m.className='msg o'; m.textContent=t; } }
  function sair(){ T=''; sessionStorage.removeItem('dkd_admin'); $('app').hidden=true; $('login').hidden=false; $('sair').hidden=true; }
  function entrar(){
    T = $('tok').value.trim() || T;
    api('GET','clientes?q=').then(function(j){
      if(j._st===401 || !j.ok){ $('lmsg').textContent = j.erro==='admin_desligado' ? 'ADMIN_TOKEN não configurado no Worker.' : 'Token recusado.'; return; }
      sessionStorage.setItem('dkd_admin', T);
      $('login').hidden=true; $('app').hidden=false; $('sair').hidden=false;
      carregar();
      api('GET','chave-publica').then(function(k){ if(k.ok) $('dig').textContent='emissor · digital '+k.digital; });
    });
  }
  $('entrar').onclick=entrar; $('tok').onkeydown=function(ev){ if(ev.key==='Enter') entrar(); };
  $('buscar').onclick=carregar; $('q').onkeydown=function(ev){ if(ev.key==='Enter') carregar(); };
  $('sair').onclick=sair;
  if(T) entrar();
})();
</script></body></html>`;

export function paginaAdmin() {
  return new Response(HTML, {
    headers: {
      "Content-Type": "text/html; charset=utf-8",
      "Cache-Control": "no-store",
      "X-Robots-Tag": "noindex, nofollow",
      "X-Frame-Options": "DENY",
      "Referrer-Policy": "no-referrer",
      "Content-Security-Policy": "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; img-src data:; base-uri 'none'; form-action 'none'; frame-ancestors 'none'",
    },
  });
}
