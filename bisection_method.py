import numpy as np

def f(x):
    return #sua função aqui

def bissecao(a, b, tol):
    iteracao = 0
    xm = 0
    while True:
        print(f"iteração: {iteracao}  a: {a}  b: {b}")
        xm = round((a + b) / 2.0, 4)
        fxm = round(f(xm), 4)
        if abs(fxm) < tol:
            break
        elif f(a) * fxm < 0:
            b = xm
        else:
            a = xm
        print(f"xm: {xm}  fxm: {fxm} \n\n")
        iteracao += 1
    
    xm = round((a + b) / 2.0, 4)
    fxm = round(f(xm), 4)
    print(f"xm: {xm}  fxm: {fxm} \n\n")
    return xm

# Intervalo [a, b] e precisão de 10^-3
raiz = bissecao(a, b, 1e-3)
print("A raiz aproximada é:", raiz)