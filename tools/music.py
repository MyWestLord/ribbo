"""RIBBO soundtrack: a 19-second, 120 BPM house loop synthesised from scratch with numpy.
Writes music.wav to the current directory."""
import numpy as np, wave
from scipy.signal import butter, lfilter
rng = np.random.default_rng(7)
sr = 44100; beat = 0.5; dur = 19.0; n = int(sr * dur)
mix = np.zeros(n); pad_bus = np.zeros(n); bass_bus = np.zeros(n)
def put(buf, sig, t0, g=1.0):
    i = int(t0 * sr); j = min(n, i + len(sig))
    if 0 <= i < n: buf[i:j] += g * sig[:j - i]
def lp(x, fc, order=2):
    b, a = butter(order, min(fc, sr * 0.45) / (sr / 2)); return lfilter(b, a, x)
def bp(x, lo, hi):
    b, a = butter(2, [lo / (sr / 2), hi / (sr / 2)], btype='band'); return lfilter(b, a, x)
def hp(x, fc):
    b, a = butter(2, fc / (sr / 2), btype='high'); return lfilter(b, a, x)
def kick():
    L = int(0.45 * sr); tt = np.arange(L) / sr
    f = 46 + 120 * np.exp(-tt * 30); ph = 2 * np.pi * np.cumsum(f) / sr
    s = np.sin(ph) * np.exp(-tt * 7) + 0.3 * rng.standard_normal(L) * np.exp(-tt * 400)
    return np.tanh(1.8 * s) * 0.95
def hat(L=0.045, dec=80, g=0.16):
    L = int(L * sr); tt = np.arange(L) / sr
    return hp(rng.standard_normal(L), 7000) * np.exp(-tt * dec) * g
def clap():
    L = int(0.3 * sr); tt = np.arange(L) / sr; nz = bp(rng.standard_normal(L), 900, 4000)
    env = sum((tt >= d) * np.exp(-np.clip(tt - d, 0, None) * k) for d, k in [(0, 150), (0.012, 150), (0.024, 14)])
    return nz * env * 0.55
def saw(f, L, det=0.0):
    tt = np.arange(L) / sr; return 2 * ((tt * f * (1 + det)) % 1) - 1
def bass(f):
    L = int(0.22 * sr); tt = np.arange(L) / sr
    s = saw(f, L) + 0.6 * saw(f, L, 0.007) + 0.8 * np.sin(2 * np.pi * f * tt)
    s = lp(s, 900) * np.minimum(1, tt / 0.004) * np.exp(-tt * 9)
    return s * 0.42
def chord(fs, L, cutoff=2200, g=0.11):
    s = sum(saw(f, L, d) for f in fs for d in (-0.006, 0, 0.006))
    tt = np.arange(L) / sr
    return lp(s, cutoff) * np.minimum(1, tt / 0.02) * g
def pluck(f):
    L = int(0.2 * sr); tt = np.arange(L) / sr
    s = np.sign(np.sin(2 * np.pi * f * tt)) * 0.6 + saw(f * 2, L) * 0.3
    return lp(s, 3500) * np.exp(-tt * 16) * 0.16
def crash(g=0.35):
    L = int(1.6 * sr); tt = np.arange(L) / sr
    return hp(rng.standard_normal(L), 5000) * np.exp(-tt * 2.6) * g

roots = [110.0, 87.31, 130.81, 98.0]
chords = [[220, 261.63, 329.63], [174.61, 220, 261.63], [261.63, 329.63, 392.0], [196.0, 246.94, 293.66]]
gap = lambda t: 11.0 <= t < 12.0
kicks = []
for k in range(36):
    t = k * beat
    if gap(t): continue
    put(mix, kick(), t); kicks.append(t)
for k in range(36):
    t = k * beat + 0.25
    if not gap(t): put(mix, hat(0.12, 22, 0.13), t)
    if t >= 8 and not gap(t):
        for s16 in (0.125, 0.375):
            put(mix, hat(), k * beat + s16, 0.55)
    if t >= 4 and k % 2 == 1 and not gap(k * beat): put(mix, clap(), k * beat)
for k in range(36):
    t = k * beat + 0.25
    if t < 2 or gap(t) or t >= 18: continue
    bar = int(t // 2) % 4
    put(bass_bus, bass(roots[bar]), t)
    if 12 <= t < 16:
        put(bass_bus, bass(roots[bar] * 2), t + 0.125, 0.35)
for bar in range(9):
    t0 = bar * 2.0
    if t0 < 8: continue
    L = int((1.0 if bar == 5 else 2.0) * sr)
    if bar == 5: put(pad_bus, chord(chords[bar % 4], L), t0 + 0.0)
    else: put(pad_bus, chord(chords[bar % 4], L, 2600 if 6 <= bar <= 7 else 1500), t0)
arp_steps = [0, 1, 2, 1, 2, 0, 2, 1]
for s in range(32):
    t = 12 + s * 0.125
    fs = chords[int(t // 2) % 4]
    put(pad_bus, pluck(fs[arp_steps[s % 8]] * 2), t, 0.9)
# build-up: clap roll + noise riser into the drop
for k, t in enumerate(np.concatenate([11 + np.arange(4) * 0.125, 11.5 + np.arange(8) * 0.0625])):
    put(mix, clap(), t, 0.25 + 0.5 * k / 12)
L = int(1.6 * sr); tt = np.arange(L) / sr
nz = rng.standard_normal(L); riser = np.zeros(L)
for seg in range(16):
    a, b = seg * L // 16, (seg + 1) * L // 16
    fc = 400 * (2 ** (seg / 3.2))
    riser[a:b] = bp(nz, fc, min(fc * 1.8, 18000))[a:b]
put(mix, riser * (tt / tt[-1]) ** 2 * 0.5, 10.4)
put(mix, crash(0.4), 12.0); put(mix, crash(0.22), 16.0); put(mix, crash(0.35), 18.0)
# final hit
put(mix, kick(), 18.0)
L = int(1.0 * sr); tt = np.arange(L) / sr
put(pad_bus, chord([220, 261.63, 329.63, 440], L, 3000, 0.14) * np.exp(-tt * 3.5), 18.0)
put(bass_bus, lp(saw(55, L) + np.sin(2 * np.pi * 55 * tt), 500) * np.exp(-tt * 3) * 0.5, 18.0)
# sidechain pump
tgrid = np.arange(n) / sr; sc = np.ones(n)
for kt in kicks:
    i = int(kt * sr); seg = tgrid[i:i + int(0.5 * sr)] - kt
    sc[i:i + len(seg)] = np.minimum(sc[i:i + len(seg)], 1 - 0.65 * np.exp(-seg * 9))
out = mix + (pad_bus + bass_bus) * sc
# simple stereo: delay echo on pad for width
dl = int(0.1875 * sr)
left = out + 0.18 * np.concatenate([np.zeros(dl), pad_bus[:-dl]])
right = out + 0.18 * np.concatenate([np.zeros(dl * 2), pad_bus[:-dl * 2]])
st = np.stack([left, right], 1)
st = np.tanh(st * 1.1)
st /= np.abs(st).max() / 0.92
fade = np.clip((dur - tgrid) / 0.5, 0, 1)[:, None]
st *= fade
with wave.open('music.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
print('ok', st.shape)
