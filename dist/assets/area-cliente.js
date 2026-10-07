fetch('/api/eu').then(function(r){return r.ok?r.json():null}).then(function(j){
  if(j&&j.email){var el=document.querySelector('[data-quem]');if(el)el.textContent=', '+j.email;}
}).catch(function(){});
