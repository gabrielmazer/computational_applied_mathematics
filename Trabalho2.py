def newton_interpolation(x, y, xp):
    n = len(x)
    coef = [0] * n
    for i in range(n):
        coef[i] = y[i]
    
    for j in range(1, n):
        for i in range(n-1, j-1, -1):
            coef[i] = (coef[i] - coef[i-1]) / (x[i] - x[i-j])
    
    result = coef[n-1]
    for i in range(n-2, -1, -1):
        result = result * (xp - x[i]) + coef[i]
    return result

def newton_gregory_interpolation(x, y, xp):
    n = len(x)
    diff = [[0] * n for _ in range(n)]
    for i in range(n):
        diff[i][0] = y[i]
    
    for j in range(1, n):
        for i in range(n-j):
            diff[i][j] = diff[i+1][j-1] - diff[i][j-1]
    
    h = x[1] - x[0]
    u = (xp - x[0]) / h
    result = diff[0][0]
    fact = 1
    for i in range(1, n):
        fact *= u - (i-1)
        result += (diff[0][i] * fact) / fact_factorial(i)
    return result

def fact_factorial(n):
    if n == 0:
        return 1
    f = 1
    for i in range(1, n + 1):
        f *= i
    return f

def coefficient_of_determination(x, y, y_adj):
    mean_y = sum(y) / len(y)
    ss_total = sum((yi - mean_y) ** 2 for yi in y)
    ss_res = sum((yi - yai) ** 2 for yi, yai in zip(y, y_adj))
    return 1 - (ss_res / ss_total)

def linear_regression(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_x2 = sum(xi ** 2 for xi in x)
    
    a1 = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    a0 = (sum_y - a1 * sum_x) / n
    
    y_adj = [a0 + a1 * xi for xi in x]
    r2 = coefficient_of_determination(x, y, y_adj)
    
    return a0, a1, y_adj, r2

def polynomial_regression(x, y, degree):
    n = len(x)
    A = [[0] * (degree + 1) for _ in range(degree + 1)]
    B = [0] * (degree + 1)
    
    for i in range(degree + 1):
        for j in range(degree + 1):
            A[i][j] = sum(xi ** (i + j) for xi in x)
        B[i] = sum(yi * (xi ** i) for xi, yi in zip(x, y))
    
    coef = gauss_elimination(A, B)
    
    y_adj = [sum(coef[j] * (xi ** j) for j in range(degree + 1)) for xi in x]
    r2 = coefficient_of_determination(x, y, y_adj)
    
    return coef, y_adj, r2

def gauss_elimination(A, B):
    n = len(B)
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        B[i], B[max_row] = B[max_row], B[i]
        
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            B[j] -= factor * B[i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
    
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (B[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def exponential_regression(x, y):
    log_y = [log(yi) for yi in y]
    a0, a1, log_y_adj, r2 = linear_regression(x, log_y)
    a = exp(a0)
    b = exp(a1)
    y_adj = [a * (b ** xi) for xi in x]
    r2 = coefficient_of_determination(x, y, y_adj)
    
    return a, b, y_adj, r2

def log(x):
    n = 1000.0
    return n * ((x ** (1/n)) - 1)

def exp(x):
    n = 1000.0
    return (1 + x/n) ** n

def read_float(prompt):
    while True:
        try:
            return float(input(prompt).replace(',', '.'))
        except ValueError:
            print("Valor inválido. Por favor, digite um número válido.")

def main():
    while True:
        print("\nEscolha uma das opções:")
        print("1. Interpolação Polinomial de Newton")
        print("2. Interpolação Polinomial de Newton-Gregory")
        print("3. Ajuste Linear")
        print("4. Ajuste Polinomial de Grau Desejado")
        print("5. Ajuste Exponencial")
        print("6. Sair")
        
        choice = input("Digite sua escolha (1-6): ")
        
        if choice == '6':
            break
        
        n = int(input("Digite o número de pontos: "))
        x = []
        y = []
        for i in range(n):
            xi = read_float(f"Digite x[{i}]: ")
            yi = read_float(f"Digite y[{i}]: ")
            x.append(xi)
            y.append(yi)
        
        if choice == '1':
            xp = read_float("Digite o ponto onde deseja conhecer o valor interpolado: ")
            result = newton_interpolation(x, y, xp)
            print(f"Resultado da Interpolação de Newton em x = {xp}: {result}")
        
        elif choice == '2':
            xp = read_float("Digite o ponto onde deseja conhecer o valor interpolado: ")
            result = newton_gregory_interpolation(x, y, xp)
            print(f"Resultado da Interpolação de Newton-Gregory em x = {xp}: {result}")
        
        elif choice == '3':
            a0, a1, y_adj, r2 = linear_regression(x, y)
            print(f"Coeficientes da Regressão Linear: a0 = {a0}, a1 = {a1}")
            print(f"Valores ajustados: {y_adj}")
            print(f"Coeficiente de Determinação: {r2}")
        
        elif choice == '4':
            degree = int(input("Digite o grau do polinômio: "))
            coef, y_adj, r2 = polynomial_regression(x, y, degree)
            print(f"Coeficientes da Regressão Polinomial: {coef}")
            print(f"Valores ajustados: {y_adj}")
            print(f"Coeficiente de Determinação: {r2}")
        
        elif choice == '5':
            a, b, y_adj, r2 = exponential_regression(x, y)
            print(f"Coeficientes da Regressão Exponencial: a = {a}, b = {b}")
            print(f"Valores ajustados: {y_adj}")
            print(f"Coeficiente de Determinação: {r2}")
        
        else:
            print("Escolha inválida. Tente novamente.")

if __name__ == "__main__":
    main()