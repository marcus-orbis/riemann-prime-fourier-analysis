import numpy as np
from sympy import primerange
import sys

print("=== SYMMETRIE-KERN SCANNER v1.1 ===")
print("Suche nach gekoppelten Primzahl-Paaren wie 607-137...")

# Lade Daten
try:
    data = np.loadtxt('01_Daten/gamma_1000000.txt')
except:
    print("FEHLER: 01_Daten/gamma_1000000.txt nicht gefunden!")
    sys.exit(1)

N = len(data)
print(f"Geladen: N = {N} Nullstellen, t_max = {data[-1]:.1f}")

# Z-Scores der Abstände
spacings = np.diff(data)
z_scores = (spacings - np.mean(spacings)) / np.std(spacings)

# Primzahlen bis 3000 scannen
primes = list(primerange(2, 3000))
print(f"Teste {len(primes)} Primzahlen von 2 bis 3000...")

# Mappe Primzahl p auf Z-Score bei Position p
def get_zscore(p):
    idx = int(p * N / data[-1])
    if 0 <= idx < N-1:
        return z_scores[idx]
    return 0

zscore_map = {p: get_zscore(p) for p in primes}

# Finde Paare mit kleiner Z-Score Differenz
threshold = 0.5
results = []

for i, p1 in enumerate(primes):
    for p2 in primes[i+1:i+100]:
        delta = abs(zscore_map[p1] - zscore_map[p2]) # FIXED
        if delta < threshold:
            gap = p2 - p1
            results.append((p1, p2, gap, delta, zscore_map[p1], zscore_map[p2]))

results.sort(key=lambda x: x[3])

print(f"\n=== TOP 40 GEKOPPELTE PAARE (ΔZ < {threshold}) ===")
print("P1 P2 Gap ΔZ Z1 Z2")
print("-" * 55)
for p1, p2, gap, delta, z1, z2 in results[:40]:
    mark = "← KADEN" if (p1==137 and p2==607) or (p1==607 and p2==137) else ""
    print(f"{p1:4d} {p2:4d} {gap:4d} {delta:.3f} {z1:6.2f} {z2:6.2f} {mark}")

# Suche Tripletts
print("\n=== KANDIDATEN FÜR NEUE TRIPLETTS ===")
triplet_count = 0
for i, (p1, p2, g1, d1, z1, z2) in enumerate(results):
    for p3, p4, g2, d2, z3, z4 in results[i+1:i+30]:
        if p2 == p3 and abs(g1 - g2) < 100:
            triplet_count += 1
            print(f"{triplet_count}. {p1} - {p2} - {p4} | Gaps: {g1}, {g2} | ΔZ: {d1:.3f}, {d2:.3f}")

if triplet_count == 0:
    print("Keine klaren Tripletts gefunden. Erhöhe Threshold oder Bereich.")

# Check 607-137-23
p607, p137, p23 = zscore_map[607], zscore_map[137], zscore_map[23]
print(f"\n=== KADEN TRIPLETT CHECK ===")
print(f"607: Z = {p607:.3f}")
print(f"137: Z = {p137:.3f} | ΔZ zu 607: {abs(p607-p137):.3f}")
print(f" 23: Z = {p23:.3f} | ΔZ zu 137: {abs(p137-p23):.3f}")

print("\n=== FERTIG ===")
