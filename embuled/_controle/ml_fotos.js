// uso: definir window.__job = {remover:true|false, fotos:[...]} antes
async function __run(job){
  const B='https://raw.githubusercontent.com/lumifabr/lumifabr.github.io/ml-fotos/embuled/';
  const sleep=ms=>new Promise(r=>setTimeout(r,ms));
  for(let i=0;i<30 && !document.querySelector('input[type=file]');i++) await sleep(500);
  const els=()=>[...document.querySelectorAll('.media-uploader__element--interactive')];
  const antes=els().map(e=>e.getAttribute('data-element-id'));
  const novos=[];
  for(const n of job.fotos){
    const b=await (await fetch(B+n)).blob();
    const dt=new DataTransfer(); dt.items.add(new File([b],n,{type:'image/jpeg'}));
    const inp=document.querySelector('input[type=file]'); const k=els().length;
    inp.files=dt.files; inp.dispatchEvent(new Event('change',{bubbles:true}));
    let id=null;
    for(let i=0;i<40;i++){await sleep(500); const e=els(); if(e.length>k){id=e[e.length-1].getAttribute('data-element-id'); if(id && /MLB/.test(id)) break;}}
    novos.push([n,id]);
  }
  if(job.remover){
    for(const id of antes){const e=els().find(x=>x.getAttribute('data-element-id')==id); const del=e&&e.querySelector('button[aria-label^="Excluir foto"]'); if(del){del.click(); await sleep(1200);}}
  }
  const final=els().map(e=>e.getAttribute('data-element-id'));
  const c=[...document.querySelectorAll('button')].find(x=>x.innerText.trim()=='Confirmar'&&!x.disabled);
  let msg='sem botão Confirmar';
  if(c && job.confirmar!==false){c.click(); await sleep(6000); msg=(document.body.innerText.match(/Salvamos as modificações[^\n]*|não foi possível[^\n]*|erro[^\n]*/i)||['?'])[0];}
  return {antes, novos, final, msg};
}
