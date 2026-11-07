window.__ctl3 = {res:{}, i:0, running:false};
if(!window.__wk){const blob=new Blob(["onmessage=e=>setTimeout(()=>postMessage(e.data),e.data.ms)"]);window.__wk=new Worker(URL.createObjectURL(blob));window.__wkcb={};window.__wkid=0;__wk.onmessage=e=>{const f=__wkcb[e.data.id];delete __wkcb[e.data.id];f&&f();};}
(async()=>{
 const C=window.__ctl3; if(C.running) return; C.running=true;
 const B='https://raw.githubusercontent.com/lumifabr/lumifabr.github.io/ml-fotos/embuled/';
 const jobs=await (await fetch(B+'_controle/jobs_v2.json?t='+Date.now())).json();
 C.total=jobs.length;
 let done={}; try{done=JSON.parse(localStorage.getItem('lumifa_emb_done')||'{}')}catch(e){}
 const sleep=ms=>new Promise(r=>{const id=++window.__wkid;__wkcb[id]=r;__wk.postMessage({id,ms});});
 for(const job of jobs){
  if(C.stop) break;
  const key=job.mlb; if((done[key]==='ok' && !job.force)||done[key]==='okc'){C.res[key]='ok';C.i++;continue;}
  C.cur=job.c;
  let f=document.getElementById('__rob'); if(f) f.remove();
  f=document.createElement('iframe'); f.id='__rob'; f.style.cssText='position:fixed;right:0;bottom:0;width:900px;height:700px;z-index:99999;background:#fff';
  f.src='https://www.mercadolivre.com.br/syi/core/modify?itemId='+job.mlb; document.body.appendChild(f);
  let st='erro';
  try{
   let d=null;
   for(let i=0;i<60;i++){await sleep(1000); try{d=f.contentDocument; if(d && d.querySelector('.media-uploader__element--interactive, input[type=file][multiple]')) break;}catch(e){}}
   await sleep(2000);
   const W=f.contentWindow; d=f.contentDocument;
   const els=()=>[...d.querySelectorAll('.media-uploader__element--interactive')];
   const inp=()=>[...d.querySelectorAll('input[type=file]')].find(i=>i.multiple)||d.querySelector('input[type=file]');
   if(!inp()) throw 'sem campo de fotos';
   const antes=els().map(e=>e.getAttribute('data-element-id'));
   let falhas=0;
   const up=async n=>{const b=await (await fetch(B+n)).blob(); const dt=new W.DataTransfer(); dt.items.add(new W.File([b],n,{type:'image/jpeg'}));
     const k=els().length; const I=inp(); I.files=dt.files; I.dispatchEvent(new W.Event('change',{bubbles:true}));
     let ok=false; for(let i=0;i<40;i++){await sleep(500); const e=els(); if(e.length>k){const id=e[e.length-1].getAttribute('data-element-id'); if(id&&/MLB/.test(id)){ok=true;break;}}}
     if(!ok) falhas++;};
   const fs=[...job.fotos];
   if(job.remover){ await up(fs.shift()); for(const id of antes){const e=els().find(x=>x.getAttribute('data-element-id')==id); const del=e&&e.querySelector('button[aria-label^="Excluir foto"]'); if(del){del.click(); await sleep(1200);}} }
   for(const n of fs) await up(n);
   if(falhas) throw 'upload falhou '+falhas;
   const c=[...d.querySelectorAll('button')].find(x=>x.innerText.trim()=='Confirmar'&&!x.disabled);
   if(!c) throw 'sem Confirmar';
   c.click();
   let msg=''; for(let i=0;i<20;i++){await sleep(1000); msg=(d.body.innerText.match(/Salvamos as modificações|não foi possível[^\n]*|Ocorreu um erro[^\n]*/i)||[''])[0]; if(msg) break;}
   st=/Salvamos/.test(msg)?'ok':('?'+msg.slice(0,60));
  }catch(e){st='erro: '+e}
  C.res[key]=st; C.i++;
  if(st==='ok'){done[key]=job.force?'okc':'ok'; try{localStorage.setItem('lumifa_emb_done',JSON.stringify(done))}catch(e){}}
 }
 C.running=false; C.end=true;
 const f=document.getElementById('__rob'); if(f) f.remove();
})(); 'iniciado'
