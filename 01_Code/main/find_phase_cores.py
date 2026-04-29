import numpy as np
from sympy import primerange
import sys

print("=== PHASE-KERN SCANNER v2.1 - FIXED ===")

data = np.loadtxt('01_Daten/gamma_1000000.txt')
N = len(data)
spacings = np.diff(data)
z_scores = (spacings - np.mean(spacings)) / np.std(spacings)

# FFT der Z-Scores
fft = np.fft.rfft(z_scores)
freqs = np.fft.rfftfreq(N, d=1.0)
phases = np.angle(fft)
amps = np.abs(fft)

print(f"FFT Länge: {len(fft)}, Max Freq: {freqs[-1]:.6f}")

primes = list(primerange(2, 1000))
print(f"Teste {len(primes)} Primzahlen...")

# Mappe Primzahl p auf Phase bei Frequenz 1/p
def get_phase(p):
    target_freq = 1.0 / p
    idx = np.argmin(np.abs(freqs - target_freq))
    # Sicherheitscheck
    idx = min(idx, len(phases)-1)
    return phases[idx], amps[idx]

phase_map = {p: get_phase(p) for p in primes}

# Finde Paare mit kleiner Phasendifferenz
threshold_deg = 2.0 # 2 Grad für ersten Scan
results = []

for i, p1 in enumerate(primes):
    phase1, amp1 = phase_map[p1]
    for p2 in primes[i+1:]:
        phase2, amp2 = phase_map[p2]
        # Phasendifferenz in Grad, kleinster Winkel
        delta = np.angle(np.exp(1j*(phase1 - phase2)))
        delta_deg = abs(np.degrees(delta))
        if delta_deg < threshold_deg and amp1 > 20 and amp2 > 20: # Nur starke Peaks
            results.append((p1, p2, p2-p1, delta_deg, amp1, amp2))

results.sort(key=lambda x: x[3])

print(f"\n=== TOP 40 PHASE-GEKOPPELTE PAARE (Δφ < {threshold_deg}°) ===")
print("P1 P2 Gap Δφ° Amp1 Amp2")
print("-" * 60)
for p1, p2, gap, delta, a1, a2 in results[:40]:
    mark = ""
    if (p1==137 and p2==607) or (p1==607 and p2==137):
        mark = "← KADEN 607-137"
    if p1==23 or p2==23:
        mark += " ← 23"
    print(f"{p1:4d} {p2:4d} {gap:4d} {delta:5.3f} {a1:6.1f} {a2:6.1f} {mark}")

# Check 607-137-23 explizit
p607_ph, p607_amp = phase_map[607]
p137_ph, p137_amp = phase_map[137]
p23_ph, p23_amp = phase_map[23]

d_607_137 = np.degrees(np.angle(np.exp(1j*(p607_ph - p137_ph))))
d_137_23 = np.degrees(np.angle(np.exp(1j*(p137_ph - p23_ph))))

print(f"\n=== KADEN TRIPLETT CHECK - FFT PHASE ===")
print(f"607: φ = {np.degrees(p607_ph):7.3f}° | Amp = {p607_amp:.1f}")
print(f"137: φ = {np.degrees(p137_ph):7.3f}° | Amp = {p137_amp:.1f} | Δφ = {d_607_137:.3f}°")
print(f" 23: φ = {np.degrees(p23_ph):7.3f}° | Amp = {p23_amp:.1f} | Δφ = {d_137_23:.3f}°")

# Suche Tripletts in den Ergebnissen
print(f"\n=== TRIPLETT-KANDIDATEN AUS TOP-LISTE ===")
triplet_count = 0
for i, (p1, p2, g1, d1, a1, a2) in enumerate(results):
    for p3, p4, g2, d2, a3, a4 in results[i+1:i+50]:
        if p2 == p3: # Kette p1-p2-p4
            triplet_count += 1
            print(f"{triplet_count}. {p1}-{p2}-{p4} | Gaps: {g1},{g2} | Δφ: {d1:.2f}°,{d2:.2f}° | Amp: {a1:.0f},{a2:.0f},{a4:.0f}")
            if triplet_count >= 20: break
    if triplet_count >= 20: break

if triplet_count == 0:
    print("Keine Tripletts in Top-Liste. Threshold erhöhen?")

print("\n=== FERTIG ===")
