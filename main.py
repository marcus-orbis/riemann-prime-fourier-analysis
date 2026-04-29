import numpy as np
from sympy import primerange
from tqdm import tqdm

def normalized_spacings(gamma):
    """Compute δ_k = (γ_{k+1} - γ_k) * log(γ_k/2π) / 2π"""
    diff = np.diff(gamma)
    log_term = np.log(gamma[:-1] / (2*np.pi)) / (2*np.pi)
    return diff * log_term

def prime_fourier_components(delta, N=10**6, p_max=10**4):
    """Extract A(p) and φ(p) for primes p < p_max"""
    delta = delta - np.mean(delta) # remove mean
    fft = np.fft.fft(delta)
    
    primes = list(primerange(2, p_max))
    results = {}
    
    for p in tqdm(primes, desc="Computing Fourier components"):
        m_p = int(round((N-1) / p))
        A_p = np.abs(fft[m_p])
        phi_p = np.angle(fft[m_p], deg=True)
        results[p] = {'A': A_p, 'phi': phi_p}
    
    return results

def find_pairs(components, ratio_range, min_A, max_dphi):
    """Exhaustive search for pairs matching thresholds"""
    primes = list(components.keys())
    pairs = []
    
    for i, p1 in enumerate(tqdm(primes, desc="Searching pairs")):
        for p2 in primes[i+1:]:
            A1, phi1 = components[p1]['A'], components[p1]['phi']
            A2, phi2 = components[p2]['A'], components[p2]['phi']
            
            ratio = A1 / A2 if A2 > 0 else np.inf
            dphi = np.abs(phi1 - phi2)
            dphi = min(dphi, 360 - dphi) # wrap to [0, 180]
            
            if (ratio_range[0] <= ratio <= ratio_range[1] and
                min(A1, A2) > min_A and
                dphi < max_dphi):
                pairs.append((p1, p2, ratio, dphi))
    
    return pairs

if __name__ == "__main__":
    print("Prime-Indexed Fourier Analysis of Riemann Zero Spacings")
    print("=" * 60)
    print("Load zeros from LMFDB or Odlyzko and uncomment below to run")
    print()
    
    # zeros = np.loadtxt('zeros_1e6.txt') # one zero per line
    # delta = normalized_spacings(zeros)
    # comps = prime_fourier_components(delta, N=10**6, p_max=10**4)
    # 
    # # Cluster at ~2.51
    # pairs_251 = find_pairs(comps, [2.50, 2.54], 4000, 0.3)
    # print(f"Cluster 2.51: {len(pairs_251)} pairs found")
    # 
    # # Isolated pair at ~2.806
    # pairs_2806 = find_pairs(comps, [2.7, 2.9], 100, 5.0)
    # print(f"Pair 2.806: {pairs_2806}")
    # 
    # # Example: mean ratio for cluster
    # if pairs_251:
    # ratios = [p[2] for p in pairs_251]
    # print(f"Mean ratio: {np.mean(ratios):.4f}")
