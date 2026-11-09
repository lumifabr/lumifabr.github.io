from base import *

FOOT = "<div class='foot'><span>@lumifa.br</span><span><b>lumifa.com.br</b></span></div>"

def photo(code, ext='jpg', folder='imagens'):
    return img(REPO / folder / f'{code}.{ext}')

def card(src, w, h, pad=40, bg='#fff', radius=28):
    return (f"<div style='width:{w}px;height:{h}px;background:{bg};border-radius:{radius}px;display:flex;align-items:center;justify-content:center;"
            f"box-shadow:0 30px 70px rgba(0,0,0,.35);overflow:hidden'><img src='{src}' style='max-width:{w-2*pad}px;max-height:{h-2*pad}px;object-fit:contain'></div>")

def arch(src, w, h, fit='contain', bg='#fff'):
    return (f"<div style='width:{w}px;height:{h}px;background:{bg};border-radius:{w//2}px {w//2}px 24px 24px;overflow:hidden;display:flex;align-items:center;justify-content:center;"
            f"box-shadow:0 30px 80px rgba(0,0,0,.45);border:2px solid rgba(212,175,55,.6)'><img src='{src}' style='width:{"100%" if fit=="cover" else str(w-80)+"px"};height:{"100%" if fit=="cover" else "auto"};object-fit:{fit};max-height:{h-60}px'></div>")

def swatch(c1, c2, label):
    return (f"<div style='display:flex;align-items:center;gap:30px;margin-top:46px'><div style='width:150px;height:150px;border-radius:50%;"
            f"background:radial-gradient(circle at 50% 40%, {c1} 0%, {c2} 70%);box-shadow:0 0 90px {c1}'></div>"
            f"<span style='font-size:28px;color:#cbbf9f;letter-spacing:.08em'>{label}</span></div>")

def cover(kicker, title, sub, n, visual='', title_size=104):
    body = f"""<div class='c dark'><img class='logo' src='{LOGO_DARK}'><div class='pg'>1/{n}</div>
    <div style='position:absolute;left:90px;right:90px;top:170px;bottom:150px;display:flex;flex-direction:column;justify-content:center'><div>
      <div class='kick'>{kicker}</div>
      <h1 style='font-size:{title_size}px;margin-top:34px'>{title}</h1>
      <div class='rule' style='margin:44px 0 36px'></div>
      <p style='font-size:34px;color:#ddd2bb;max-width:820px'>{sub}</p>
      {visual}
    </div></div>
    <div class='foot'><span>@lumifa.br</span><span><b>arraste →</b></span></div></div>"""
    return page(body)

def slide(i, n, label, title, text, visual='', title_size=78):
    body = f"""<div class='c dark'><img class='logo' src='{LOGO_DARK}'><div class='pg'>{i}/{n}</div>
    <div style='position:absolute;left:90px;right:90px;top:170px;bottom:150px;display:flex;flex-direction:column;justify-content:center'><div>
      <div class='serif gold' style='font-size:150px;line-height:.9;font-weight:500'>{label}</div>
      <h1 style='font-size:{title_size}px;margin-top:26px'>{title}</h1>
      <div class='rule' style='margin:40px 0 34px'></div>
      <p style='font-size:36px;color:#ddd2bb;max-width:880px'>{text}</p>
      {visual}
    </div></div>{FOOT}</div>"""
    return page(body)

def slide_photo(i, n, kicker, title, text, src):
    body = f"""<div class='c dark'><img class='logo' src='{LOGO_DARK}'><div class='pg'>{i}/{n}</div>
    <div style='position:absolute;left:90px;right:90px;top:190px;display:flex;justify-content:center'>{card(src, 900, 620)}</div>
    <div style='position:absolute;left:90px;right:90px;top:870px'>
      <div class='kick'>{kicker}</div>
      <h1 style='font-size:64px;margin-top:20px'>{title}</h1>
      <p style='font-size:31px;color:#ddd2bb;margin-top:22px'>{text}</p>
    </div>{FOOT}</div>"""
    return page(body)

def cta(i, n, title, text):
    body = f"""<div class='c dark'><img class='logo' src='{LOGO_DARK}'><div class='pg'>{i}/{n}</div>
    <div style='position:absolute;left:90px;right:90px;top:170px;bottom:150px;justify-content:center;text-align:center;display:flex;flex-direction:column;align-items:center'>
      <img src='{ICONE}' style='width:150px'>
      <h1 style='font-size:86px;margin-top:50px'>{title}</h1>
      <p style='font-size:34px;color:#ddd2bb;margin-top:34px;max-width:840px'>{text}</p>
      <div style='margin-top:60px;background:{GOLD};color:{INK};font-weight:700;font-size:30px;letter-spacing:.08em;padding:28px 50px;border-radius:999px'>PEÇA SEU ORÇAMENTO</div>
      <p style='font-size:27px;color:#cbbf9f;margin-top:26px;letter-spacing:.04em'>Fale com nossa especialista pelo WhatsApp · link na bio</p>
    </div>{FOOT}</div>"""
    return page(body)

def produto(p):
    chips = ''.join(f"<span class='chip'>{c}</span>" for c in p['chips'])
    opc = f"<span style='font-size:25px;color:#6b5d45;margin-left:22px'>{p['opcoes']}</span>" if p.get('opcoes') else ''
    body = f"""<div class='c cream'>
    <img src='{LOGO_LIGHT}' style='position:absolute;top:62px;left:90px;height:54px'>
    <div class='kick' style='position:absolute;top:80px;right:90px;color:{GOLD2};font-size:20px'>{p['selo']}</div>
    <div style='position:absolute;left:90px;right:90px;top:160px'>{card(photo(p['code']), 900, 640, pad=50, radius=30).replace('rgba(0,0,0,.35)','rgba(80,60,20,.16)')}</div>
    <div style='position:absolute;left:90px;right:90px;top:840px'>
      <div class='kick' style='color:{GOLD2}'>{p['categoria']}</div>
      <h1 style='font-size:{p.get('ts',60)}px;margin-top:16px;color:{INK}'>{p['titulo']}</h1>
      <div style='margin-top:24px'>{chips}</div>
      <div style='margin-top:8px;display:flex;align-items:center'><span class='code'>{p['code']}</span>{opc}</div>
    </div>
    <div style='position:absolute;left:0;right:0;bottom:0;height:104px;background:{INK};display:flex;align-items:center;justify-content:space-between;padding:0 90px'>
      <span style='color:{CREAM};font-size:25px;letter-spacing:.04em'>Peça seu orçamento · <b style='color:{GOLD}'>fale com nossa especialista</b></span>
      <span style='color:{GOLD};font-size:25px;font-weight:600'>lumifa.com.br</span></div></div>"""
    return page(body)

def banner():
    W = 3240
    hero = arch(photo('PROD-001'), 640, 760)
    body = f"""<div class='c' style='background:radial-gradient(ellipse 45% 70% at 50% 35%, #3d2e14 0%, #1d160e 50%, {INK} 80%)'>
    <!-- tile 1 -->
    <div style='position:absolute;left:150px;top:0;width:800px;height:1350px;display:flex;flex-direction:column;justify-content:center'>
      <div class='kick'>Bem-vindo à</div>
      <img src='{LOGO_DARK}' style='width:760px;margin-top:40px'>
      <div class='rule' style='margin:60px 0 40px'></div>
      <p style='font-size:36px;color:#ddd2bb'>Iluminação decorativa e técnica para casas, lojas e projetos.</p>
    </div>
    <!-- tile 2 -->
    <div style='position:absolute;left:1080px;width:1080px;top:150px;display:flex;flex-direction:column;align-items:center'>
      {hero}
      <h1 style='font-size:92px;text-align:center;margin-top:60px'>Luz que <i class='gold'>transforma</i><br>ambientes</h1>
    </div>
    <!-- tile 3 -->
    <div style='position:absolute;left:2280px;top:0;width:820px;height:1350px;display:flex;flex-direction:column;justify-content:center'>
      <div class='kick'>Catálogo completo</div>
      <p class='serif' style='font-size:56px;line-height:1.35;margin-top:36px'>Pendentes · Lustres<br>Arandelas · Spots<br>Painéis de LED<br>Fitas &amp; Perfis<br>Área externa</p>
      <div class='rule' style='margin:50px 0 44px'></div>
      <div style='align-self:flex-start;background:{GOLD};color:{INK};font-weight:700;font-size:28px;letter-spacing:.08em;padding:26px 44px;border-radius:999px'>PEÇA SEU ORÇAMENTO</div>
      <p style='font-size:28px;color:#cbbf9f;margin-top:28px'>lumifa.com.br · link na bio</p>
    </div></div>"""
    return page(body, W, 1350)
