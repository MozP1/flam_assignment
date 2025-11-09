## Objective
The variables are calculated by minimizing the L1 error by measuring how far the predicted curve is from observed points (x,y values from the xy_data.csv)

L1 error= ∑​∣xi​−x(ti​)∣+∣yi​−y(ti​)∣

## Results

- theta (deg): **28.116682**
- M: **0.021380**
- X: **54.895153**
- L1_error: 37865.10157330653

**LaTeX equation**

```latex
x(t) = t\cos(28.116682^{\circ}) - e^{0.021380|t|}\sin(0.3t)\sin(28.116682^{\circ}) + 54.895153,y(t) = 42 + t\sin(28.116682^{\circ}) + e^{0.021380|t|}\sin(0.3t)\cos(28.116682^{\circ})
```

** Resulting Equation
-
"\left(t\cdot\cos\left(0.498\right)-e^{0.0214\left|t\right|}\cdot\sin\left(0.3t\right)\sin\left(0.4908\right)+54.895,\ 42+t\cdot\sin\left(0.4908\right)+e^{0.0214\left|t\right|}\cdot\sin\left(0.3t\right)\cos\left(0.4098\right)\right)"
