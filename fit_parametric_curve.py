import argparse
import json
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution


def parse_args():
    p = argparse.ArgumentParser(
        description="Fit theta, M, X for the given parametric curve by minimizing L1 distance.")
    p.add_argument('--csv', required=True, help='Path to xy_data.csv with columns x,y')
    p.add_argument('--out', default='fit_output', help='Directory to write outputs')
    p.add_argument('--tmin', type=float, default=6.0, help='Minimum t (default: 6)')
    p.add_argument('--tmax', type=float, default=60.0, help='Maximum t (default: 60)')
    p.add_argument('--seed', type=int, default=42, help='Random seed for optimizer')
    p.add_argument('--maxiter', type=int, default=200, help='Max iterations for optimizer')
    p.add_argument('--popsize', type=float, default=15, help='Population size multiplier (DE)')
    p.add_argument('--workers', type=int, default=1, help='Parallel workers for DE (>=1)')
    return p.parse_args()


def model(theta_deg, M, X, t):
    """Vectorized model returning x(t), y(t) for numpy array t.
    theta is in degrees.
    """
    th = np.deg2rad(theta_deg)
    exp_term = np.exp(M * np.abs(t)) * np.sin(0.3 * t)
    x = t * np.cos(th) - exp_term * np.sin(th) + X
    y = 42.0 + t * np.sin(th) + exp_term * np.cos(th)
    return x, y


def objective_factory(t, x_obs, y_obs):
    def obj(params):
        theta_deg, M, X = params
        x_pred, y_pred = model(theta_deg, M, X, t)
        return np.sum(np.abs(x_obs - x_pred) + np.abs(y_obs - y_pred))
    return obj


def fit_parameters(t, x_obs, y_obs, seed=42, maxiter=200, popsize=15, workers=1):
    bounds = [(0.0, 50.0), (-0.05, 0.05), (0.0, 100.0)]  # theta, M, X
    obj = objective_factory(t, x_obs, y_obs)
    result = differential_evolution(
        obj, bounds, seed=seed, maxiter=maxiter, popsize=popsize,
        tol=1e-6, workers=workers, updating='deferred' if workers > 1 else 'immediate')
    theta_deg, M, X = result.x
    return {
        'theta_deg': float(theta_deg),
        'M': float(M),
        'X': float(X),
        'L1_error': float(result.fun),
        'nit': int(result.nit),
        'nfev': int(result.nfev),
        'success': bool(result.success),
        'message': str(result.message),
    }


def save_outputs(out_dir, params, t, x_obs, y_obs):
    os.makedirs(out_dir, exist_ok=True)

    # Save params.json
    with open(os.path.join(out_dir, 'params.json'), 'w', encoding='utf-8') as f:
        json.dump(params, f, indent=2)

    # Predicted values and per-point errors
    x_pred, y_pred = model(params['theta_deg'], params['M'], params['X'], t)
    l1_pt = np.abs(x_obs - x_pred) + np.abs(y_obs - y_pred)

    import pandas as _pd
    df_out = _pd.DataFrame({
        't': t,
        'x_obs': x_obs,
        'y_obs': y_obs,
        'x_pred': x_pred,
        'y_pred': y_pred,
        'l1_point': l1_pt,
    })
    df_out.to_csv(os.path.join(out_dir, 'predictions.csv'), index=False)

    # Plot observed points and fitted curve (parametric path)
    plt.style.use('seaborn-v0_8')
    fig, ax = plt.subplots(1, 1, figsize=(7, 6))

    # Observed as scatter
    ax.scatter(x_obs, y_obs, s=10, alpha=0.5, label='Observed (CSV)')

    # Fitted curve sampled densely in [tmin, tmax]
    t_dense = np.linspace(t.min(), t.max(), 600)
    xd, yd = model(params['theta_deg'], params['M'], params['X'], t_dense)
    ax.plot(xd, yd, 'r-', lw=2, label='Fitted curve')

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Observed points vs. fitted parametric curve')
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig_path = os.path.join(out_dir, 'fit_vs_data.png')
    fig.savefig(fig_path, dpi=150)
    plt.close(fig)

    # LaTeX equation
    th = params['theta_deg']
    M = params['M']
    X = params['X']
    latex_eq = (
        r"x(t) = t\cos(%.6f^{\circ}) - e^{%.6f|t|}\sin(0.3t)\sin(%.6f^{\circ}) + %.6f," % (th, M, th, X)
        + "" +
        r"y(t) = 42 + t\sin(%.6f^{\circ}) + e^{%.6f|t|}\sin(0.3t)\cos(%.6f^{\circ})" % (th, M, th)
    )
    with open(os.path.join(out_dir, 'equation_latex.txt'), 'w', encoding='utf-8') as f:
        f.write(latex_eq + "")
    return fig_path




def main():
    args = parse_args()

    # Load data
    df = pd.read_csv(args.csv)
    df.columns = [c.strip() for c in df.columns]
    if not {'x','y'}.issubset(df.columns):
        raise ValueError('Input CSV must have columns x,y')

    x_obs = df['x'].astype(float).values
    y_obs = df['y'].astype(float).values
    n = len(df)

    # Assign t uniformly in [tmin, tmax]
    t = np.linspace(float(args.tmin), float(args.tmax), n)

    # Fit
    params = fit_parameters(t, x_obs, y_obs, seed=args.seed,
                            maxiter=args.maxiter, popsize=args.popsize, workers=args.workers)

    # Save outputs
    out_plot = save_outputs(args.out, params, t, x_obs, y_obs)

    # Console summary
    print('Best-fit parameters:')
    print('  theta (deg) = %.6f' % params['theta_deg'])
    print('  M           = %.6f' % params['M'])
    print('  X           = %.6f' % params['X'])
    print('  L1 error    = %.4f' % params['L1_error'])
    print('Preview plot   :', os.path.abspath(out_plot))


if __name__ == '__main__':
    main()