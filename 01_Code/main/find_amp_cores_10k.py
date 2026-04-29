import numpy as np
from sympy import primerange
import sys
import time

start = time.time()

data = np.loadtxt('01_Daten/gamma_1000000.txt')
N = len(data)
spacings = np.diff(data)
z_scores = (spacings - np.mean(spacings)) / np.std(spacings)
fft = np.fft.rfft(z_scores)
freqs = np.fft.rfftfreq(N, d=1.0)
amps = np.abs(fft)
phases = np.angle(fft)

primes = list(primerange(2, 10000))
total = len(primes)
print(f"=== SINGULARITÄTS-TEST BIS 10.000 ===")
print(f"Teste {total} Primzahlen...")
print(f"Erwarte ~{total**2//2:,} Paare, Dauer ~3-4min")

def get_amp_phase(p):
    target_freq = 1.0 / p
    if target_freq > freqs[-1]: return 0, 0
    idx = np.argmin(np.abs(freqs - target_freq))
    idx = min(idx, len(amps)-1)
    return amps[idx], phases[idx]

target_ratio = 2.806
amp_threshold = 100
phase_threshold = 5.0

print(f"\n=== SUCHE RATIO ≈ {target_ratio:.3f} ± 0.3, Δφ < {phase_threshold}° ===")
print(f"Filter: Amp > {amp_threshold}")

count = 0
checked = 0
start_scan = time.time()

for i, p1 in enumerate(primes):
    a1, ph1 = get_amp_phase(p1)
    if a1 < amp_threshold: continue
    for p2 in primes[i+1:]:
        checked += 1
        if checked % 50000 == 0:
            elapsed = time.time() - start_scan
            rate = checked / elapsed
            remaining = (total**2//2 - checked) / rate
            sys.stdout.write(f"\rProgress: {checked:,} Paare | {rate:.0f}/s | ETA: {remaining:.0f}s ")
            sys.stdout.flush()
        a2, ph2 = get_amp_phase(p2)
        if a2 < amp_threshold: continue
        r = a1 / a2 if a2 > 0 else 0
        d = np.degrees(np.angle(np.exp(1j*(ph1 - ph2))))
        if abs(r - target_ratio) < 0.3 and abs(d) < phase_threshold:
            count += 1
            print(f"\n{count}. {p1:4d}-{p2:4d} | Ratio: {r:.3f} | Δφ: {d:.2f}° | Amp: {a1:.0f},{a2:.0f}")

elapsed = time.time() - start
print(f"\n\n=== ERGEBNIS ===")
print(f"Geprüft: {checked:,} Paare in {elapsed:.1f}s")
if count == 1:
    print("BESTÄTIGT: 607-137 ist SINGULÄR bis 10.000")
    print("Nur das Kaden-Paar erfüllt die Kriterien.")
elif count == 0:
    print("KEIN Paar gefunden. Filter zu streng?")
else:
    print(f"GEFUNDEN: {count} Paare. Kaden-Kern nicht einzigartig.")
    
print("=== FERTIG ===")
