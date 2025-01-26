import numpy as np
from scipy.optimize import minimize_scalar, root_scalar


def matrix_multiplication(matrix_a, matrix_b):
    if len(matrix_a[0]) != len(matrix_b):
        raise ValueError("Произведение матриц невозможно")
    else:
        m, n, p = len(matrix_a), len(matrix_b), len(matrix_b[0])
        C = [[0] * p for _ in range(m)]

        for i in range(m):
            for k in range(p):
                C[i][k] = sum(matrix_a[i][j] * matrix_b[j][k] for j in range(n))

        print("Результат умножения матриц:")
        answers = []
        for row in C:
            print(row)
            answers.append(row)

        return answers
    pass


def functions(coefficients1, coefficients2, x_range=(-100, 100)):
    a11, a12, a13 = map(float, coefficients1.split())
    a21, a22, a23 = map(float, coefficients2.split())

    def F(x):
        return a11 * x ** 2 + a12 * x + a13

    def P(x):
        return a21 * x ** 2 + a22 * x + a23

    def find_extremum(X, x_range):
        res = minimize_scalar(X, bounds=x_range, method='bounded')
        if res.success:
            return (res.x, res.fun)  # x, F(x)
        else:
            return None

    def G(x):
        return F(x) - P(x)

    if (a11 == a21) and (a12 == a22) and (a13 == a23):
        return None

    #extremum_F = find_extremum(F, x_range)
    #extremum_P = find_extremum(P, x_range)

    roots = []
    for x0 in np.linspace(*x_range, 100):
        try:
            sol = root_scalar(G, bracket=(x0 - 1, x0 + 1), method='brentq')
            if sol.converged and x_range[0] <= sol.root <= x_range[1]:
                roots.append(sol.root)
        except ValueError:
            pass

    roots = sorted(set(np.round(root, 6) for root in roots))

    roots_with_values = []
    for root in roots:
        f_value = F(root)
        roots_with_values.append((root, f_value))

    return roots_with_values
    pass


def skew(x):
    mean_sample = np.mean(x)
    n = len(x)

    m2 = np.sum((x - mean_sample) ** 2) / n  # Дисперсия
    m3 = np.sum((x - mean_sample) ** 3) / n  # Момент 3-го порядка

    return round(m3 / np.sqrt(m2 ** 3), 2)
    pass


def kurtosis(x):
    mean_sample = np.mean(x)
    n = len(x)

    # Центральные моменты
    m2 = np.sum((x - mean_sample) ** 2) / n  # Дисперсия
    m4 = np.sum((x - mean_sample) ** 4) / n

    return round(m4 / np.sqrt(m2 ** 4) - 3, 2)
    pass
