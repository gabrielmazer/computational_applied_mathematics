import numpy as np

def f(x):
    fx = round(x**5 - (10/9)*x**3 + (5/21)*x, 5)
    return fx

def df(x):
    return round(5*x**4 - (10/3)*x**2 + 5/21, 5)

def criterio_parada(x0, x1):
    if abs(x1) < 1:
        max = 1
    else:
        max = abs(x1)
    return round((abs(x1-x0)/max), 5)

def newton_method(x0, tol):
    iteracao = 0
    
    while True:
        fx0 = f(x0)
        dfx0 = df(x0)
        
        if iteracao == 0:
            if  abs(fx0) < tol:
                break
        else:
            parada = criterio_parada(x0_aux, x0)
            print(f"cp: {parada}")
            if abs(fx0) < tol or parada  < tol:
                break
        
        print(f"iteração: {iteracao}\nxn: {x0}\nf(xn): {fx0}\n\n")
        x0_aux = x0
        x0 = round(x0 - fx0 / dfx0, 5)
        iteracao += 1
    
    print(f"iteração: {iteracao}\nxn: {x0}\nf(xn): {fx0}\n\n")
    return x0

x0 = -0.85
raiz = newton_method(x0, 1e-4)
print("A raiz aproximada é:", raiz)
