"""Trilhas animadas originais geradas por síntese (sem direitos de terceiros).
Cada `estilo` muda andamento, harmonia, ritmo e timbres, para nenhum Reel repetir música."""
import numpy as np, wave
SR = 44100

PROGS = {
 'Am-F-C-G': ([[57,60,64],[53,57,60],[48,52,55],[55,59,62]], [45,41,36,43]),
 'C-G-Am-F': ([[48,52,55],[55,59,62],[57,60,64],[53,57,60]], [36,43,45,41]),
 'Dm-Bb-F-C': ([[50,53,57],[46,50,53],[53,57,60],[48,52,55]], [38,34,41,36]),
 'Em-C-G-D': ([[52,55,59],[48,52,55],[55,59,62],[50,54,57]], [40,36,43,38]),
 'F-G-Em-Am': ([[53,57,60],[55,59,62],[52,55,59],[57,60,64]], [41,43,40,45]),
 'Cmaj7-Am7-Dm7-G7': ([[48,52,55,59],[57,60,64,67],[50,53,57,60],[55,59,62,65]], [36,45,38,43]),
 'Gm-Eb-Bb-F': ([[55,58,62],[51,55,58],[58,62,65],[53,57,60]], [43,39,46,41]),
 'Bm-G-D-A': ([[59,62,66],[55,59,62],[50,54,57],[57,61,64]], [47,43,38,45]),
 'Fmaj7-Em7-Dm7-Cmaj7': ([[53,57,60,64],[52,55,59,62],[50,53,57,60],[48,52,55,59]], [41,40,38,36]),
}

def _env(n, a=.005, d=.2):
    t = np.arange(n)/SR; return np.minimum(1, t/a)*np.exp(-t/d)
def _lp(x, a):
    # passa-baixa de 1 polo, vetorizado
    from scipy.signal import lfilter
    return lfilter([a], [1, a-1], x)
def _saw(f, n): t = np.arange(n)/SR; return 2*((t*f) % 1)-1
def _sq(f, n): t = np.arange(n)/SR; return np.sign(np.sin(2*np.pi*f*t))
def _note(m): return 440*2**((m-69)/12)
def _kick(soft=False):
    n = int(.35*SR); t = np.arange(n)/SR; f = 48+(70 if soft else 100)*np.exp(-t*30)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*(11 if soft else 8))*(.7 if soft else .95)
def _snare(clap=True):
    n = int(.25*SR); x = np.random.randn(n); x = np.convolve(x, np.ones(6)/6, 'same')
    body = 0 if clap else np.sin(2*np.pi*190*np.arange(n)/SR)*_env(n, .001, .05)*.5
    return (x*_env(n, .001, .07 if clap else .12))*.35+body*.3
def _hat(open_=False):
    n = int((.2 if open_ else .05)*SR); x = np.random.randn(n); x = x-np.convolve(x, np.ones(3)/3, 'same')
    return x*_env(n, .001, .07 if open_ else .015)*.22

def estilo(i):
    """Estilo determinístico e diferente para cada número i."""
    keys = list(PROGS)
    bpms = [118, 124, 104, 112, 128, 98, 120, 110, 126, 108, 116, 122, 100, 114, 130, 106, 119, 125]
    grooves = ['house', 'pop', 'chill', 'disco', 'house', 'chill', 'pop', 'disco', 'house']
    leads = ['pluck', 'bell', 'square', 'saw', 'pluck', 'bell', 'square']
    return dict(bpm=bpms[i % len(bpms)], prog=keys[(i*4+1) % len(keys)], groove=grooves[i % len(grooves)],
                lead=leads[(i*3) % len(leads)], transp=[0, 2, -3, 5, -2, 3, -5, 1][i % 8], arp=[0, 1, 2, 3][(i*5) % 4], seed=100+i)

def render(dur, est, out):
    np.random.seed(est['seed'])
    bpm = est['bpm']; B = 60/bpm; tr = est['transp']
    chords, bass = PROGS[est['prog']]
    chords = [[m+tr for m in c] for c in chords]; bass = [b+tr for b in bass]
    g = est['groove']
    N = int(dur*SR); mix = np.zeros(N+2*SR)
    def add(x, pos, k=1.):
        i = int(pos*SR)
        if i >= len(mix): return
        j = min(len(mix), i+len(x)); mix[i:j] += x[:j-i]*k
    beats = int(dur/B)+1
    for b in range(beats):
        t = b*B; bar = b//4; ch = chords[bar % 4]; bn = bass[bar % 4]
        intro = b < 2
        # bateria
        if not intro:
            if g in ('house', 'disco'): add(_kick(), t)
            elif g == 'pop':
                if b % 4 in (0, 2) or (b % 8 == 7): add(_kick(), t + (B/2 if b % 8 == 7 else 0))
            else:
                if b % 4 in (0, 2): add(_kick(True), t)
        if b % 2 == 1 and b >= 4: add(_snare(g != 'chill'), t, .8 if g == 'chill' else 1)
        hats = {'house': [(B/2, True)], 'disco': [(0, False), (B/2, True)], 'pop': [(0, False), (B/2, False)],
                'chill': [(B/2, False)]}[g]
        for off, op in hats: add(_hat(op), t+off, .9)
        if b >= 4 and g in ('house', 'pop'):
            for k in (1, 3): add(_hat(), t+k*B/4, .45)
        # baixo
        n = int(B/2*SR)
        if g == 'disco':
            for k, oc in ((0, 0), (1, 12)): add(_lp(_saw(_note(bn+oc), n), .1)*_env(n, .004, .12)*.42, t+k*B/2)
        elif g == 'chill':
            if b % 2 == 0: m = int(B*1.6*SR); add(np.sin(2*np.pi*_note(bn)*np.arange(m)/SR)*_env(m, .01, .5)*.5, t)
        else:
            add(_lp(_saw(_note(bn), n), .07)*_env(n, .005, .16)*.45, t+B/2)
            if g == 'pop' and b % 2 == 0: add(_lp(_saw(_note(bn), n), .07)*_env(n, .005, .16)*.35, t)
        # acordes
        if g in ('house', 'disco'):
            n = int(.22*SR); st = sum(_lp(_saw(_note(m), n), .14) for m in ch)/len(ch)*_env(n, .003, .09)*.42
            add(st, t+B/2)
        elif g == 'pop' and b % 2 == 0:
            n = int(B*2*SR); st = sum(_lp(_saw(_note(m), n), .05) for m in ch)/len(ch)*_env(n, .02, .6)*.3
            add(st, t)
        # melodia/arpejo
        if b >= 8 or (g == 'chill' and b >= 4):
            pat = [[0, 1, 2, 1], [0, 2, 1, 2], [2, 1, 0, 1], [0, 1, 2, 3]][est['arp']]
            steps = 4 if g != 'chill' else 2
            for k in range(steps):
                idx = pat[(b*steps+k) % 4] % len(ch); m = ch[idx]+12; n = int(.18*SR)
                lead = est['lead']; tt = np.arange(n)/SR
                if lead == 'bell': x = (np.sin(2*np.pi*_note(m)*tt)+.4*np.sin(2*np.pi*_note(m)*2.01*tt))*_env(n, .002, .09)*.14
                elif lead == 'square': x = _lp(_sq(_note(m), n), .2)*_env(n, .002, .05)*.08
                elif lead == 'saw': x = _lp(_saw(_note(m), n), .12)*_env(n, .002, .06)*.12
                else: x = np.sin(2*np.pi*_note(m)*tt)*_env(n, .002, .05)*.17
                add(x, t+k*B/steps)
    # pad
    tt = np.arange(N)/SR; pad = np.zeros(N)
    for bar in range(int(dur/(4*B))+1):
        i = int(bar*4*B*SR); j = min(N, int((bar+1)*4*B*SR))
        if i >= N: break
        for m in chords[bar % 4]: pad[i:j] += np.sin(2*np.pi*_note(m)*tt[i:j])*(.06 if g == 'chill' else .04)
    mix[:N] += pad
    x = np.tanh(mix[:N]*1.3)*.8
    fi = int(.25*SR); fo = int(1.0*SR)
    x[:fi] *= np.linspace(0, 1, fi); x[-fo:] *= np.linspace(1, 0, fo)
    x = (x/np.max(np.abs(x))*.85*32767).astype(np.int16)
    with wave.open(out, 'w') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.stack([x, x], 1).tobytes())
