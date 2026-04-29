import numpy as np
from sympy import primerange

data = np.loadtxt('01_Daten/gamma_1000000.txt')
N = len(data)
spacings = np.diff(data)
z_scores = (spacings - np.mean(spacings)) / np.std(spacings)
fft = np.fft.rfft(z_scores)
freqs = np.fft.rfftfreq(N, d=1.0)
amps = np.abs(fft)
phases = np.angle(fft)

def get(p):
    idx = np.argmin(np.abs(freqs - 1.0/p))
    return amps[idx], phases[idx]

a23, p23 = get(23)
a607, p607 = get(607)
a137, p137 = get(137)

def show(n1,a1,ph1, n2,a2,ph2):
    r = max(a1/a2, a2/a1)
    d = np.degrees(np.angle(np.exp(1j*(ph1-ph2))))
    print(f"{n1:3d}-{n2:3d} | Ratio: {r:.3f} | Δφ: {d:5.2f}° | Amp: {a1:.0f},{a2:.0f}")

print("=== 23er-TRIPLETT CHECK ===")
show(607,a607,p607, 137,a137,p137)
show(607,a607,p607, 23,a23,p23)
show(137,a137,p137, 23,a23,p23)
