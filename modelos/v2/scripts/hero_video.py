# Gera o vídeo da capa do modelo A a partir das fotos do catálogo.
# Uso: python3 hero_video.py 1280 720 wide ../img/hero-wide.mp4  |  python3 hero_video.py 720 1080 tall ../img/hero-tall.mp4
# Troque a lista "codes" para usar outras peças.
import sys, subprocess, numpy as np
from PIL import Image
W,H,mode,out=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3],sys.argv[4]
codes=['1695','3745','1664','1968','3800','1272','1649','1894']
FPS=24; SEG=3.6; FADE=1.0
import os; root=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../../imagens/PROD-%s.jpg')
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
base=np.zeros((H,W,3),np.float32); base[:]=np.array([246,241,233],np.float32)
# vertical soft gradient
base*= (1-0.04*(yy/H))[...,None]
cx,cy=(W*0.71,H*0.50) if mode=='wide' else (W*0.5,H*0.40)
box=(int(H*0.66) if mode=='wide' else int(W*0.74))
def glow(intensity):
    r=np.sqrt(((xx-cx)/(box*0.75))**2+((yy-cy)/(box*0.75))**2)
    g=np.clip(1-r,0,1)**2*intensity
    col=np.array([232,190,90],np.float32)
    return g[...,None]*(col-255)*0.30   # warm tint (negative = darker toward gold)
prods=[]
for c in codes:
    im=Image.open(root%c).convert('RGB')
    # trim white border
    a=np.asarray(im).astype(np.int16); m=(a.min(axis=2)<235)
    ys,xs=np.where(m); im=im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    prods.append(im)
def render_prod(im,scale,dx):
    w,h=im.size; s=min(box/w,box/h)*scale
    im2=im.resize((max(1,int(w*s)),max(1,int(h*s))),Image.LANCZOS)
    layer=np.full((H,W,3),255,np.float32)
    x0=int(cx-im2.width/2+dx); y0=int(cy-im2.height/2)
    arr=np.asarray(im2).astype(np.float32)
    xa,ya=max(0,x0),max(0,y0); xb,yb=min(W,x0+im2.width),min(H,y0+im2.height)
    layer[ya:yb,xa:xb]=arr[ya-y0:yb-y0,xa-x0:xb-x0]
    return layer/255.0
n=len(prods); total=n*SEG; frames=int(total*FPS)
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
  '-c:v','libx264','-preset','slow','-crf','30','-pix_fmt','yuv420p','-movflags','+faststart','-an',out],stdin=subprocess.PIPE)
cache={}
for f in range(frames):
    t=f/FPS
    i=int(t//SEG); lt=t-i*SEG
    frame=base.copy()+glow(0.9+0.1*np.sin(t*1.3))
    def layer_for(k,lt):
        prog=(lt+FADE)/(SEG+FADE)
        return render_prod(prods[k%n],0.94+0.08*prog,(-12+24*prog)*(W/1280))
    L=layer_for(i,lt)
    if lt>SEG-FADE:  # crossfade to next
        a=(lt-(SEG-FADE))/FADE; a=a*a*(3-2*a)
        L2=layer_for(i+1,lt-SEG)
        L=L*(1-a)+L2*a
    out_=np.clip(frame*L,0,255).astype(np.uint8)
    p.stdin.write(out_.tobytes())
p.stdin.close(); p.wait()
