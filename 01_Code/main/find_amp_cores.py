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

print(f"FFT: {len(fft)} bins, Freq-Range: {freqs[0]:.6f} bis {freqs[-1]:.6f}")

primes = list(primerange(2, 1000))

def get_amp_phase(p):
    target_freq = 1.0 / p
    # Nur wenn Frequenz im FFT-Bereich liegt
    if target_freq > freqs[-1]:
        return 0, 0 # Zu hohe Frequenz, nicht auflösbar
    idx = np.argmin(np.abs(freqs - target_freq))
    idx = min(idx, len(amps)-1) # FIX: Clamp auf gültigen Bereich
    return amps[idx], phases[idx]

# Teste 607-137 mit Amplituden-Ratio wie in v1.0
amp_607, ph_607 = get_amp_phase(607)
amp_137, ph_137 = get_amp_phase(137)
amp_23, ph_23 = get_amp_phase(23)

ratio = amp_607 / amp_137 if amp_137 > 0 else 0
delta_phase_deg = np.degrees(np.angle(np.exp(1j*(ph_607 - ph_137))))

print(f"\n=== KADEN v1.0 REPRODUKTION ===")
print(f"607: Amp={amp_607:.2f}, φ={np.degrees(ph_607):.3f}°")
print(f"137: Amp={amp_137:.2f}, φ={np.degrees(ph_137):.3f}°")
print(f" 23: Amp={amp_23:.2f}, φ={np.degrees(ph_23):.3f}°")
print(f"Ratio 607/137: {ratio:.4f}")
print(f"Δφ 607-137: {delta_phase_deg:.4f}°")

# Suche andere Paare mit ähnlichem Ratio
target_ratio = ratio
print(f"\n=== SUCHE PAARE MIT RATIO ≈ {target_ratio:.3f} ± 0.2 ===")
print("P1 P2 Ratio Δφ° Amp1 Amp2")
print("-" * 55)

results = []
for i, p1 in enumerate(primes):
    a1, ph1 = get_amp_phase(p1)
    if a1 < 50: continue # Skip schwache Peaks
    for p2 in primes[i+1:i+100]:
        a2, ph2 = get_amp_phase(p2)
        if a2 < 50: continue
        r = a1 / a2 if a2 > 0 else 0
        d = np.degrees(np.angle(np.exp(1j*(ph1 - ph2))))
        if abs(r - target_ratio) < 0.2 and abs(d) < 3.0:
            results.append((p1, p2, r, d, a1, a2))
            print(f"{p1:4d} {p2:4d} {r:5.3f} {d:5.2f} {a1:6.1f} {a2:6.1f}")

if len(results) == 0:
    print("Keine Paare mit ähnlicher Ratio gefunden. Kaden-Kern ist einzigartig.")

print(f"\nGefunden: {len(results)} Paare")
print("=== FERTIG ===")
