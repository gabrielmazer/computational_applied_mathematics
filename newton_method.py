import numpy as np

def f(x):
    return round((np.power(x,3) - 9*x + 5), 4)

def df(x):
    return round((3*np.power(x,2) - 9), 4)

def newton_method(x0, tol):
    iteracao = 0
    
    while True:
        fx0 = f(x0)
        dfx0 = df(x0)
        
        if abs(fx0) < tol:
            break
        
        print(iteracao, x0, abs(fx0),  "\n\n")
        x0 = round(x0 - fx0 / dfx0, 4)
        iteracao += 1
    
    print(iteracao, x0, abs(fx0),  "\n\n")
    return x0

x0 = 0.75
raiz = newton_method(x0, 1e-3)
print("A raiz aproximada é:", raiz)
