# Determine a raiz positiva de f(x) = x − x ∗ ln(x) com ε = 10−3 utilizando o Método da Bisseção no intervalo [2, 7; 2, 8]

import numpy as np

def f(x):
    return x - x * np.log(x)

def bissecao(a, b, tol):
    iteracao = 0
    xm = 0
    while True:
        print(iteracao, a, b)
        xm = round((a + b) / 2.0, 4)
        fxm = round(f(xm), 4)
        if abs(fxm) < tol:
            break
        elif f(a) * fxm < 0:
            b = xm
        else:
            a = xm
        print(xm, fxm, "\n\n")
        iteracao += 1
    
    xm = round((a + b) / 2.0, 4)
    fxm = round(f(xm), 4)
    print(xm, fxm, "\n\n")
    return xm

# Intervalo [a, b] e precisão de 10^-3
raiz = bissecao(2.7, 2.8, 1e-3)
print("A raiz aproximada é:", raiz)