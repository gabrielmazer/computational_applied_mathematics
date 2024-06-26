import numpy as np

def f(x):
    return round("Sua função aqui", 4)

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
            a = xm
        else:
            b = xm
        print(f"xm: {xm}   fxm: {fxm}\n\n")
        iteracao += 1
    
    xm = round((a * fb - b * fa) / (fb - fa), 4)
    fxm = round(f(xm), 4)
    print(f"xm: {xm}   fxm: {fxm}\n\n")
    return xm

# Intervalo [a, b] e precisão de 10^-4
a = #valor de a
b = #valor de b
raiz = falsa_posicao(a, b, 1e-4)
print("A raiz aproximada é:", raiz)