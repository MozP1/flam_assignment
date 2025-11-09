
# Parametric Curve Fitting — θ, M, X (L1 Minimization)

This project estimates the unknown parameters **θ (theta)**, **M**, and **X** in the parametric curve:

\[
\begin{aligned}
 x(t) &= t\cos(\theta) - e^{M|t|}\,\sin(0.3t)\sin(\theta) + X, \\
 y(t) &= 42 + t\sin(\theta) + e^{M|t|}\,\sin(0.3t)\cos(\theta)
\end{aligned}
\]

using the observed points in `xy_data.csv` by minimizing the **L1 distance** between the observed and predicted coordinates.

---

## 1) Problem & Constraints
- Unknowns and bounds:
  - \(\theta \in [0^\circ, 50^\circ]\)
  - \(M \in [-0.05, 0.05]\)
  - \(X \in [0, 100]\)
- Parameter range: \(t \in (6, 60)\)
- Input data: `xy_data.csv` with columns `x, y`.

**Goal**: Find \(\theta, M, X\) that minimize
\[\sum_i \big(|x_{obs,i} - x(t_i)| + |y_{obs,i} - y(t_i)|\big).\]

---

## 2) Data Assumption
The CSV does not include `t`. We therefore assume the points are uniformly sampled over the provided range and assign
\[ t_i = \text{linspace}(6, 60, n), \]
where \(n\) is the number of rows in the CSV.

---

## 3) Model (Computational Form)
Given a candidate \((\theta, M, X)\), the model predicts
\[
\begin{aligned}
 x_i &= t_i\cos(\theta) - e^{M|t_i|}\,\sin(0.3 t_i)\sin(\theta) + X, \\
 y_i &= 42 + t_i\sin(\theta) + e^{M|t_i|}\,\sin(0.3 t_i)\cos(\theta).
\end{aligned}
\]

For computation, \(\theta\) is converted to **radians**.

---

## 4) Objective Function (L1)
We minimize the **sum of L1 distances** over all rows:
\[
\text{Error} = \sum_{i=1}^n \big(|x_{obs,i} - x_i| + |y_{obs,i} - y_i|\big).
\]
L1 is robust to outliers and matches the assignment criteria.

---

## 5) Optimization Strategy
We use **SciPy Differential Evolution** (global optimizer) to handle the non-linear, potentially multi-modal objective. Bounds:

- \(\theta \in [0, 50]\) (degrees)
- \(M \in [-0.05, 0.05]\)
- \(X \in [0, 100]\)

Default settings in the script:
- `maxiter=200`, `tol=1e-6`, `seed=42`, `popsize=15`. You can increase `maxiter/popsize` for more exhaustive search.

---



## 6) Results (from provided xy_data.csv)
After optimization on the supplied data:

- **θ (degrees):** 28.119942°
- **θ (radians):** 0.4908
- **M:** 0.021397
- **X:** 54.899452
- **L1 error (sum):** 37865.0962

### Final Parametric Equation — LaTeX (degrees)
```latex
\[
\begin{aligned}
 x(t) &= t\cos(28.119942^\circ) - e^{0.021397|t|}\sin(0.3t)\sin(28.119942^\circ) + 54.899452, \\
 y(t) &= 42 + t\sin(28.119942^\circ) + e^{0.021397|t|}\sin(0.3t)\cos(28.119942^\circ)
\end{aligned}
\]
```

### Final Parametric Equation — Compact Submission Format (radians)
```
\left(t*\cos(0.4908)-e^{0.0214\left|t\right|}\cdot\sin(0.3t)\sin(0.4908)+54.8995,\;42+t*\sin(0.4908)+e^{0.0214\left|t\right|}\cdot\sin(0.3t)\cos(0.4908)\right)
```


---

## 7) Validation & Diagnostics
- Visual check with `fit_vs_data.png` (observed scatter vs. fitted curve) to confirm the curve tracks the cloud of points.
- Residuals reviewed via per-point L1 in `predictions.csv`. No extreme anomalies were observed.
- Optimizer reported successful convergence within bounds.

---

## 8) Files in this repo
- `fit_parametric_curve.py` — main script to fit parameters and generate artifacts
- `xy_data.csv` — input data (x, y)
- `results/` — output folder (created on run) containing params, LaTeX, predictions, and plot

---

## 9) Plot

<img width="1050" height="900" alt="fit_vs_data" src="https://github.com/user-attachments/assets/e6380118-ac97-423a-8170-a99ca5e27b39" />

