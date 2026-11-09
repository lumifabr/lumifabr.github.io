"""Monta um Reel 1080x1920 a partir de cenas HTML + trilha animada."""
import subprocess, shutil, os
from pathlib import Path
from layouts import *
from musica import render as musica, estilo

def bg(inner, cream=False):
    cls = 'c cream' if cream else 'c dark'
    st = "" if cream else f"style='background:radial-gradient(ellipse 90% 50% at 50% 35%, #3d2e14 0%, #1d160e 50%, {INK} 80%)'"
    return page(f"<div class='{cls}' {st}>{inner}</div>", 1080, 1920)

def hook(kicker, titulo, sub, size=128):
    return bg(f"""<img src='{LOGO_DARK}' style='position:absolute;top:260px;left:50%;transform:translateX(-50%);height:70px'>
<div style='position:absolute;left:90px;right:90px;top:520px;text-align:center'>
<div class='kick'>{kicker}</div><h1 style='font-size:{size}px;margin-top:40px'>{titulo}</h1>
<div class='rule' style='margin:60px auto 0'></div><p style='font-size:40px;color:#ddd2bb;margin-top:50px'>{sub}</p></div>""")

def prod(n, code, nome, info, ts=76):
    return bg(f"""<img src='{LOGO_LIGHT}' style='position:absolute;top:240px;left:90px;height:60px'>
<div class='serif' style='position:absolute;top:210px;right:90px;font-size:120px;color:{GOLD2};line-height:1'>{n}</div>
<div style='position:absolute;left:70px;right:70px;top:400px'>{card(photo(code), 940, 860, pad=50, radius=34).replace('rgba(0,0,0,.35)','rgba(80,60,20,.18)')}</div>
<div style='position:absolute;left:90px;right:90px;top:1310px'><h1 style='font-size:{ts}px;color:{INK}'>{nome}</h1>
<p style='font-size:34px;color:#5a4d38;margin-top:18px'>{info}</p><div style='margin-top:26px'><span class='code'>{code}</span></div></div>""", cream=True)

def tip(n, titulo, texto, total=None):
    num = f"<div class='serif gold' style='font-size:200px;line-height:.9'>{n}</div>" if n else ''
    return bg(f"""<img src='{LOGO_DARK}' style='position:absolute;top:250px;left:90px;height:62px'>
<div style='position:absolute;left:90px;right:90px;top:520px'>{num}
<h1 style='font-size:96px;margin-top:30px'>{titulo}</h1><div class='rule' style='margin:50px 0 44px'></div>
<p style='font-size:44px;color:#ddd2bb;line-height:1.45'>{texto}</p></div>""")

def fim(titulo='Qual combina<br>com a sua casa?', sub='Comenta o número aqui embaixo 👇'):
    return bg(f"""<div style='position:absolute;left:90px;right:90px;top:480px;text-align:center;display:flex;flex-direction:column;align-items:center'>
<img src='{ICONE}' style='width:200px'><h1 style='font-size:104px;margin-top:70px'>{titulo}</h1>
<p style='font-size:38px;color:#ddd2bb;margin-top:40px'>{sub}</p>
<div style='margin-top:70px;background:{GOLD};color:{INK};font-weight:700;font-size:36px;letter-spacing:.08em;padding:32px 60px;border-radius:999px'>PEÇA SEU ORÇAMENTO</div>
<p style='font-size:32px;color:#cbbf9f;margin-top:34px'>lumifa.com.br · link na bio</p></div>""")

def build(scenes, out, r, est, work='/home/claude/work/_reel'):
    """scenes: lista de (html, tempos). A duração de cada cena é medida em tempos da música, então os cortes caem na batida."""
    B = 60/est['bpm']
    w = Path(work); shutil.rmtree(w, ignore_errors=True); w.mkdir(parents=True)
    lst = []
    for i, (h, d) in enumerate(scenes):
        png = r.render(h, w/f's{i}.jpg', 1080, 1920)
        n = round(d*B*30); fo = n/30-0.2
        tmp = w/f'tmp{i}.mp4'; fin = w/f'v{i}.mp4'
        subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(png),'-vf',
          f"scale=2160:3840,zoompan=z='1+0.05*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1080x1920:fps=30,fade=t=in:st=0:d=0.15,fade=t=out:st={fo}:d=0.2,format=yuv420p",
          '-frames:v',str(n),'-c:v','libx264','-crf','18','-preset','veryfast','-pix_fmt','yuv420p',str(tmp)], check=True)
        os.rename(tmp, fin); lst.append(f"file '{fin}'")
    (w/'list.txt').write_text('\n'.join(lst))
    subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(w/'list.txt'),'-c','copy',str(w/'video.mp4')], check=True)
    dur = sum(round(d*B*30) for _, d in scenes)/30
    musica(dur, est, str(w/'trilha.wav'))
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(w/'video.mp4'),'-i',str(w/'trilha.wav'),'-map','0:v','-map','1:a',
      '-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',str(out)], check=True)
    shutil.copy(w/'s0.jpg', out.with_name(out.stem+'-capa.jpg'))
    return out
