from layouts import *
OUT = Path('/home/claude/work/reel1'); OUT.mkdir(exist_ok=True)
def bg(inner, cream=False):
    cls = 'c cream' if cream else 'c dark'
    st = "" if cream else f"style='background:radial-gradient(ellipse 90% 50% at 50% 35%, #3d2e14 0%, #1d160e 50%, {INK} 80%)'"
    return page(f"<div class='{cls}' {st}>{inner}</div>", 1080, 1920)
hook = bg(f"""<img src='{LOGO_DARK}' style='position:absolute;top:260px;left:50%;transform:translateX(-50%);height:70px'>
<div style='position:absolute;left:90px;right:90px;top:560px;text-align:center'>
<div class='kick'>Sala de jantar</div>
<h1 style='font-size:132px;margin-top:40px'><span class='gold'>3 pendentes</span><br>que transformam<br>a sua mesa</h1>
<div class='rule' style='margin:60px auto 0'></div>
<p style='font-size:38px;color:#ddd2bb;margin-top:50px'>Qual é o seu favorito? 1, 2 ou 3?</p></div>""")
def prod(n, code, nome, info):
    return bg(f"""<img src='{LOGO_LIGHT}' style='position:absolute;top:240px;left:90px;height:60px'>
<div class='serif' style='position:absolute;top:210px;right:90px;font-size:120px;color:{GOLD2};line-height:1'>{n}</div>
<div style='position:absolute;left:70px;right:70px;top:400px'>{card(photo(code), 940, 860, pad=50, radius=34).replace('rgba(0,0,0,.35)','rgba(80,60,20,.18)')}</div>
<div style='position:absolute;left:90px;right:90px;top:1310px'>
<h1 style='font-size:76px;color:{INK}'>{nome}</h1>
<p style='font-size:34px;color:#5a4d38;margin-top:18px'>{info}</p>
<div style='margin-top:26px'><span class='code'>{code}</span></div></div>""", cream=True)
cta_ = bg(f"""<div style='position:absolute;left:90px;right:90px;top:480px;text-align:center;display:flex;flex-direction:column;align-items:center'>
<img src='{ICONE}' style='width:200px'>
<h1 style='font-size:110px;margin-top:70px'>Qual combina<br>com a sua casa?</h1>
<p style='font-size:38px;color:#ddd2bb;margin-top:40px'>Comenta o número aqui embaixo 👇</p>
<div style='margin-top:70px;background:{GOLD};color:{INK};font-weight:700;font-size:36px;letter-spacing:.08em;padding:32px 60px;border-radius:999px'>PEÇA SEU ORÇAMENTO</div>
<p style='font-size:32px;color:#cbbf9f;margin-top:34px'>lumifa.com.br · link na bio</p></div>""")
scenes = [hook,
  prod('1','PROD-001','Pendente Acrilux Brisa','Leve como uma pétala · dourado · LED 13W'),
  prod('2','PROD-1722','Pendente Silicone LED','Ondas de luz · 80 cm · branco ou dourado'),
  prod('3','PROD-1587','Pendente Cristal ⌀12cm','Lindo em dupla ou trio · dourado ou cromado'),
  cta_]
with Renderer() as r:
    for i,s in enumerate(scenes): r.render(s, OUT/f's{i}.jpg', 1080, 1920)
