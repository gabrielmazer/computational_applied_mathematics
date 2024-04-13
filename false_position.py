import numpy as np

def f(x):
    return round(x**5 - (10/9)*x**3 + (5/21)*x, 4)

def falsa_posicao(a, b, tol):
    iteracao = 0
    while True:
        print(iteracao, a, b)
        fa = f(a)
        fb = f(b)
        xm = round((a * fb - b * fa) / (fb - fa), 4)
        fxm = round(f(xm), 4)
        if abs(fxm) < tol:
            break
        elif fa * fxm < 0:
            b = xm
        else:
            a = xm
        print(f"xm: {xm}   fxm: {fxm}\n\n")
        iteracao += 1
    
    xm = round((a * fb - b * fa) / (fb - fa), 4)
    fxm = round(f(xm), 4)
    print(f"xm: {xm}   fxm: {fxm}\n\n")
    return xm

# Intervalo [a, b] e precisão de 10^-3
a = -0.3
b = 0.25
raiz = falsa_posicao(a, b, 1e-3)
print("A raiz aproximada é:", raiz)