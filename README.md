# Riemann-prime-fourier-analysis

Code accompanying the preprint:  
Kaden, T. (2026). *Prime-Indexed Fourier Components of Normalized Riemann Zero Spacings: A Numerical Cluster Analysis up to p < 10^4*. Zenodo. https://doi.org/10.5281/zenodo.19883993

## Abstract
Numerical analysis of discrete Fourier transform of normalized Riemann zero spacings δ_k. Exhaustive search of 743,644 prime pairs for p < 10^4 yields a cluster at amplitude ratio 2.51 and isolated pair (607, 137) at 2.806.

## Reproducibility
Raw computation output SHA256: `a7d376e271ae3025c2c1fd6605c4761a1656afd3dc8c95eac025e728aaa3e034`

## Installation
```bash
pip install -r requirements.txt


Usage
Download first 10^6 Riemann zeros from LMFDB or Andrew Odlyzko's tables
Save as zeros_1e6.txt, one zero per line
Uncomment lines in main.py and run

python main.py

License
MIT License

Citation
If you use this code, please cite:

@misc{kaden2026prime,
  author = {Kaden, Thomas},
  title = {Prime-Indexed Fourier Components of Normalized Riemann Zero Spacings: A Numerical Cluster Analysis up to p < 10^4},
  year = {2026},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.19883993},
  url = {https://doi.org/10.5281/zenodo.19883993}
}
Data Availability
The first 10^6 Riemann zeros are not included due to size. They can be obtained from LMFDB or Odlyzko's published tables.

Contact
Thomas Kaden - Independent Researcher

---

### **WO REINKOPIEREN:**

1. **GitHub → dein Repo → `README.md` anklicken**
2. **Stift-Icon rechts oben**
3. **Alles markieren → löschen → Block oben einfügen**
4. **Commit message:** `Update README with full documentation`
5. **`Commit changes`**

**Danach hast du 3 Files fertig: `main.py`, `requirements.txt`, `README.md`.** 

**Nächster Schritt: Release `v1.0.0` erstellen für die Zenodo-Code-DOI.**
