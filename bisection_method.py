import numpy as np

def f(x):
    return x**5 - (10/9)*x**3 + (5/21)*x

def bissecao(a, b, tol):
    iteracao = 0
    xm = 0
    while True:
        print(f"iteração: {iteracao}  a: {a}  b: {b}")
        xm = round((a + b) / 2.0, 5)
        fxm = round(f(xm), 5)
        if abs(fxm) < tol:
            break
        elif f(a) * fxm < 0:
            b = xm
        else:
            a = xm
        print(f"xm: {xm}  fxm: {fxm} \n\n")
        iteracao += 1
    
    xm = round((a + b) / 2.0, 5)
    fxm = round(f(xm), 5)
    print(f"xm: {xm}  fxm: {fxm} \n\n")
    return xm

# Intervalo [a, b] e precisão de 10^-4
raiz = bissecao(-0.65, -0.52, 1e-4)
print("A raiz aproximada é:", raiz)