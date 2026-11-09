"""Trilha animada original (120 BPM) — gerada por síntese, sem direitos de terceiros."""
import numpy as np, sys, wave
SR=44100; BPM=120; BEAT=60/BPM
def env(n, a=0.005, d=0.2):
    t=np.arange(n)/SR; return np.minimum(1,t/a)*np.exp(-t/d)
def kick():
    n=int(.35*SR); t=np.arange(n)/SR; f=50+90*np.exp(-t*30)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)*0.9
def clap():
    n=int(.25*SR); x=np.random.randn(n); x=np.convolve(x,np.ones(6)/6,'same')
    return x*env(n,.001,.07)*0.35
def hat(open_=False):
    n=int((.18 if open_ else .05)*SR); x=np.random.randn(n); x=x-np.convolve(x,np.ones(3)/3,'same')
    return x*env(n,.001,.06 if open_ else .015)*0.25
def saw(f,n):
    t=np.arange(n)/SR; return 2*((t*f)%1)-1
def lp(x,a): 
    y=np.zeros_like(x); s=0
    for i,v in enumerate(x): s+=a*(v-s); y[i]=s
    return y
def note(m): return 440*2**((m-69)/12)
def render(dur, seed=1, prog=None, out='trilha.wav'):
    np.random.seed(seed)
    N=int(dur*SR); mix=np.zeros(N+SR)
    prog = prog or [[57,60,64],[53,57,60],[48,52,55],[55,59,62]]   # Am F C G
    bass = [45,41,36,43]
    beats=int(dur/BEAT)+1
    def add(x,pos,g=1):
        i=int(pos*SR); j=min(len(mix),i+len(x)); mix[i:j]+=x[:j-i]*g
    for b in range(beats):
        t=b*BEAT; bar=b//4; ch=prog[bar%4]
        if b>=2: add(kick(),t)
        if b%2==1 and b>=4: add(clap(),t)
        for k in range(2):
            add(hat(k==1), t+k*BEAT/2, 1 if k==1 else .7)
        if b>=4:
            for k in (0,1): add(hat(),t+BEAT/4+k*BEAT/2,.5)
        # baixo em colcheias, com sidechain implícito (entra no contratempo)
        n=int(BEAT/2*SR); bs=lp(saw(note(bass[bar%4]),n),.08)*env(n,.005,.18)*0.45
        add(bs,t+BEAT/2)
        # stabs de acorde no contratempo
        n=int(.22*SR); st=sum(lp(saw(note(m),n),.15) for m in ch)/3*env(n,.003,.09)*0.42
        add(st,t+BEAT/2)
        # arpejo pluck em semicolcheias
        if b>=8:
            for k in range(4):
                m=ch[(b*4+k)%3]+12; n=int(.15*SR)
                add(np.sin(2*np.pi*note(m)*np.arange(n)/SR)*env(n,.002,.05)*0.16, t+k*BEAT/4)
    # pad suave
    t=np.arange(N)/SR; pad=np.zeros(N)
    for bar in range(int(dur/(4*BEAT))+1):
        i=int(bar*4*BEAT*SR); j=min(N,int((bar+1)*4*BEAT*SR))
        for m in prog[bar%4]: pad[i:j]+=np.sin(2*np.pi*note(m)*t[i:j])*0.05
    mix[:N]+=pad
    x=np.tanh(mix[:N]*1.4)*0.8
    fi=int(.3*SR); fo=int(1.2*SR)
    x[:fi]*=np.linspace(0,1,fi); x[-fo:]*=np.linspace(1,0,fo)
    x=(x/np.max(np.abs(x))*0.89*32767).astype(np.int16)
    st=np.stack([x,x],1)
    with wave.open(out,'w') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
if __name__=='__main__':
    render(float(sys.argv[1]), int(sys.argv[2]) if len(sys.argv)>2 else 1, out=sys.argv[3] if len(sys.argv)>3 else 'trilha.wav')
