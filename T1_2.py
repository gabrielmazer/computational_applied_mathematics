import numpy as np
from scipy.linalg import lu, inv

def calculo_determinante(ordem, matriz):
    if not isinstance(ordem, int) or not isinstance(matriz, list):
        raise TypeError("Os parâmetros devem ser um inteiro e uma lista, respectivamente.")
    if ordem != len(matriz) or any(len(linha) != ordem for linha in matriz):
        raise ValueError("A matriz deve ser quadrada e corresponder à ordem especificada.")
    
    matriz_np = np.array(matriz)
    if matriz_np.shape[0] != matriz_np.shape[1]:
        raise ValueError("A matriz não é quadrada.")
    
    return round(np.linalg.det(matriz_np), 4)

def sistema_triangular_inferior(ordem, matriz_coeficientes, vetor_termos_independentes):
    if not isinstance(ordem, int) or not isinstance(matriz_coeficientes, list) or not isinstance(vetor_termos_independentes, list):
        raise TypeError("Os parâmetros devem ser um inteiro e duas listas, respectivamente.")
    if len(vetor_termos_independentes) != ordem or any(len(linha) != ordem for linha in matriz_coeficientes):
        raise ValueError("A ordem do sistema e as dimensões da matriz e do vetor devem ser compatíveis.")
    
    vetor_solucao = [0] * ordem
    for i in range(ordem):
        soma = sum(matriz_coeficientes[i][j] * vetor_solucao[j] for j in range(i))
        vetor_solucao[i] = (vetor_termos_independentes[i] - soma) / matriz_coeficientes[i][i]
    
    return vetor_solucao

def sistema_triangular_superior(ordem, matriz_coeficientes, vetor_termos_independentes):
    if not isinstance(ordem, int) or not isinstance(matriz_coeficientes, list) or not isinstance(vetor_termos_independentes, list):
        raise TypeError("Os parâmetros devem ser um inteiro e duas listas, respectivamente.")
    if len(vetor_termos_independentes) != ordem or any(len(linha) != ordem for linha in matriz_coeficientes):
        raise ValueError("A ordem do sistema e as dimensões da matriz e do vetor devem ser compatíveis.")
    
    vetor_solucao = [0] * ordem
    for i in range(ordem-1, -1, -1):
        soma = sum(matriz_coeficientes[i][j] * vetor_solucao[j] for j in range(i+1, ordem))
        vetor_solucao[i] = (vetor_termos_independentes[i] - soma) / matriz_coeficientes[i][i]
    
    return vetor_solucao

def decomposicao_LU(ordem, matriz_coeficientes, vetor_termos_independentes):
    if np.linalg.det(matriz_coeficientes) == 0:
        return "Erro: A matriz de coeficientes é singular e não pode ser decomposta."
    L = np.zeros((ordem, ordem))
    U = np.zeros((ordem, ordem))
    for i in range(ordem):
        for j in range(i, ordem):
            U[i, j] = matriz_coeficientes[i][j] - sum(L[i, k] * U[k, j] for k in range(i))
        for j in range(i, ordem):
            if i == j:
                L[i, i] = 1
            else:
                L[j, i] = (matriz_coeficientes[j][i] - sum(L[j, k] * U[k, i] for k in range(i))) / U[i, i]
    
    y = np.zeros(ordem)
    for i in range(ordem):
        y[i] = vetor_termos_independentes[i] - sum(L[i, j] * y[j] for j in range(i))
    
    x = np.zeros(ordem)
    for i in reversed(range(ordem)):
        x[i] = (y[i] - sum(U[i, j] * x[j] for j in range(i+1, ordem))) / U[i, i]
    
    return [round(num, 4) for num in x.tolist()]

def cholesky(ordem, matriz_coeficientes, vetor_termos_independentes):
    L = np.linalg.cholesky(matriz_coeficientes)
    y = np.linalg.solve(L, vetor_termos_independentes)
    x = np.linalg.solve(L.T, y)
    return [round(num, 4) for num in x.tolist()]

def gauss_compacto(ordem, matriz_coeficientes, vetor_termos_independentes):
    A = np.array(matriz_coeficientes, float)
    b = np.array(vetor_termos_independentes, float)

    for i in range(ordem):
        pivot = A[i][i]
        for j in range(i, ordem):
            A[i][j] /= pivot
        b[i] /= pivot

        for k in range(i+1, ordem):
            fator = A[k][i]
            for j in range(i, ordem):
                A[k][j] -= fator * A[i][j]
            b[k] -= fator * b[i]

    x = np.zeros(ordem)
    for i in range(ordem-1, -1, -1):
        x[i] = b[i] - sum(A[i][j] * x[j] for j in range(i+1, ordem))
        x[i] = round(x[i], 4)

    return x.tolist()

def gauss_jordan(ordem, matriz_coeficientes, vetor_termos_independentes):
    A = np.array(matriz_coeficientes, dtype=float)
    b = np.array(vetor_termos_independentes, dtype=float).reshape(ordem, 1)
    
    if np.linalg.det(A) == 0:
        return "Erro: A matriz de coeficientes é singular e não pode ser utilizada no método de Gauss Jordan."
    
    aug_matriz = np.hstack((A, b))

    for i in range(ordem):
        aug_matriz[i] = aug_matriz[i] / aug_matriz[i, i]
        for j in range(ordem):
            if i != j:
                aug_matriz[j] = aug_matriz[j] - aug_matriz[j, i] * aug_matriz[i]

    x = aug_matriz[:, -1]
    return np.round(x, 4).tolist()

def jacobi(ordem, coeficientes, termos_independentes, aproximacao_inicial, precisao, max_iteracoes):
    A = np.array(coeficientes, dtype=float)

    if not np.all(np.abs(A.diagonal()) > np.sum(np.abs(A), axis=1) - np.abs(A.diagonal())):
        return "Erro: A matriz de coeficientes não é estritamente diagonal dominante."
    
    if len(aproximacao_inicial) != ordem:
        return "Erro: O vetor de aproximação inicial deve ter o mesmo número de elementos que a ordem do sistema."
    
    x = np.array(aproximacao_inicial, dtype=float)
    x_novo = np.copy(x)
    
    for _ in range(max_iteracoes):
        for i in range(ordem):
            soma = sum(coeficientes[i][j] * x[j] for j in range(ordem) if j != i)
            x_novo[i] = (termos_independentes[i] - soma) / coeficientes[i][i]
        
        if np.allclose(x, x_novo, atol=precisao):
            return np.round(x_novo, 4).tolist()
        
        x = np.copy(x_novo)
    
    return np.round(x_novo, 4).tolist()

def gauss_seidel(ordem, matriz_coeficientes, vetor_termos_independentes, aproximacao_inicial, precisao, max_iteracoes):    
    x = np.array(aproximacao_inicial, dtype=float)
    for k in range(max_iteracoes):
        x_novo = np.copy(x)
        for i in range(ordem):
            s1 = sum(matriz_coeficientes[i][j] * x_novo[j] for j in range(i))
            s2 = sum(matriz_coeficientes[i][j] * x[j] for j in range(i + 1, ordem))
            x_novo[i] = (vetor_termos_independentes[i] - s1 - s2) / matriz_coeficientes[i][i]
        
        if np.linalg.norm(x - x_novo, ord=np.inf) < precisao:
            return x_novo, k+1
        
        x = x_novo
    
    return x, k

def matriz_inversa(ordem, matriz, metodo):
    if not isinstance(ordem, int) or not isinstance(matriz, list):
        raise TypeError("Os parâmetros devem ser um inteiro e uma lista, respectivamente.")
    if ordem != len(matriz) or any(len(linha) != ordem for linha in matriz):
        raise ValueError("A matriz deve ser quadrada e corresponder à ordem especificada.")

    matriz_np = np.array(matriz)
    if matriz_np.shape[0] != matriz_np.shape[1]:
        raise ValueError("A matriz não é quadrada.")

    if metodo == 'LU':
        P, L, U = lu(matriz_np)
        if np.linalg.det(U) == 0:
            return "Erro: A matriz de coeficientes é singular e não pode ser decomposta."
        inversa = inv(U) @ inv(L) @ P.T
    elif metodo == 'Gauss':
        inversa = inv(matriz_np)
    else:
        raise ValueError("Método inválido. Escolha 'LU' ou 'Gauss'.")

    return np.round(inversa, 4).tolist()

def main():
    continuar = True
    while continuar:
        escolha = input("\nEscolha o método:\n(1) para determinante\n(2) para sistema triangular inferior\n"
                        "(3) para sistema triangular superior\n(4) para decomposição LU\n"
                        "(5) para Cholesky\n(6) para Gauss Compacto\n(7) para Gauss Jordan\n"
                        "(8) para Jacobi\n(9) para Gauss-Seidel\n(10) para matriz inversa: ")
        
        if escolha == '1':
            ordem = int(input("Digite a ordem da matriz: "))
            matriz = []
            for i in range(ordem):
                linha = list(map(float, input(f"Digite a linha {i+1} da matriz: ").split()))
                matriz.append(linha)
            print(f"Determinante: {calculo_determinante(ordem, matriz)}")
 
        elif escolha == '2':
            ordem = int(input("Digite a ordem do sistema: "))
            matriz_coeficientes = []
            for i in range(ordem):
                linha = list(map(float, input(f"Digite a linha {i+1} dos coeficientes: ").split()))
                matriz_coeficientes.append(linha)
            vetor_termos_independentes = list(map(float, input("Digite o vetor de termos independentes: ").split()))
            print(f"Vetor solução: {sistema_triangular_inferior(ordem, matriz_coeficientes, vetor_termos_independentes)}")
        
        elif escolha == '3':
            ordem = int(input("Digite a ordem do sistema: "))
            matriz_coeficientes = []
            for i in range(ordem):
                linha = list(map(float, input(f"Digite a linha {i+1} dos coeficientes: ").split()))
                matriz_coeficientes.append(linha)
            vetor_termos_independentes = list(map(float, input("Digite o vetor de termos independentes: ").split()))
            print(f"Vetor solução: {sistema_triangular_superior(ordem, matriz_coeficientes, vetor_termos_independentes)}")
        
        elif escolha == '4':
            ordem = int(input("Digite a ordem do sistema: "))
            matriz_coeficientes = []
            for i in range(ordem):
                linha = list(map(float, input(f"Digite a linha {i+1} dos coeficientes: ").split()))
                matriz_coeficientes.append(linha)
            vetor_termos_independentes = list(map(float, input("Digite o vetor de termos independentes: ").split()))
            print(f"Vetor solução: {decomposicao_LU(ordem, matriz_coeficientes, vetor_termos_independentes)}")
        
        elif escolha == '5':
            ordem = int(input("Digite a ordem do sistema: "))
            matriz_coeficientes = []
            for i in range(ordem):
                linha = list(map(float, input(f"Digite a linha {i+1} dos coeficientes: ").split()))
                matriz_coeficientes.append(linha)
            vetor_termos_independentes = list(map(float, input("Digite o vetor de termos independentes: ").split()))
            print(f"Vetor solução: {cholesky(ordem, matriz_coeficientes, vetor_termos_independentes)}")
        
        elif escolha == '6':
            ordem = int(input("Digite a ordem do sistema: "))
            matriz_coeficientes = []
            for i in range(ordem):
                linha = list(map(float, input(f"Digite a linha {i+1} dos coeficientes: ").split()))
                matriz_coeficientes.append(linha)
            vetor_termos_independentes = list(map(float, input("Digite o vetor de termos independentes: ").split()))
            print(f"Vetor solução: {gauss_compacto(ordem, matriz_coeficientes, vetor_termos_independentes)}")
        
        elif escolha == '7':
            ordem = int(input("Digite a ordem do sistema: "))
            matriz_coeficientes = []
            for i in range(ordem):
                linha = list(map(float, input(f"Digite a linha {i+1} dos coeficientes: ").split()))
                matriz_coeficientes.append(linha)
            vetor_termos_independentes = list(map(float, input("Digite o vetor de termos independentes: ").split()))
            print(f"Vetor solução: {gauss_jordan(ordem, matriz_coeficientes, vetor_termos_independentes)}")

        elif escolha == '8' or escolha == '9':
            ordem = int(input("Digite a ordem do sistema: "))
            coeficientes = []
            for i in range(ordem):
                linha = list(map(float, input(f"Digite a linha {i+1} dos coeficientes: ").split()))
                coeficientes.append(linha)
            termos_independentes = list(map(float, input("Digite o vetor de termos independentes: ").split()))
            aproximacao_inicial = list(map(float, input("Digite o vetor de aproximação inicial: ").split()))
            precisao = float(input("Digite a precisão desejada: "))
            max_iteracoes = int(input("Digite o número máximo de iterações: "))
            if escolha == '8':
                resultado = jacobi(ordem, coeficientes, termos_independentes, aproximacao_inicial, precisao, max_iteracoes)
            elif escolha == '9':
                resultado, iteracoes = gauss_seidel(ordem, coeficientes, termos_independentes, aproximacao_inicial, precisao, max_iteracoes)
                resultado_formatado = [f"{num:.4f}" for num in resultado]
                print("Vetor solução: [" + ", ".join(resultado_formatado) + f"], Iterações: {iteracoes}")

        elif escolha == '10':
            ordem = int(input("Digite a ordem da matriz: "))
            matriz = []
            for i in range(ordem):
                linha = list(map(float, input(f"Digite a linha {i+1} da matriz: ").split()))
                matriz.append(linha)
            metodo = input("Escolha o método ('LU' ou 'Gauss'): ")
            print(f"Matriz inversa: {matriz_inversa(ordem, matriz, metodo)}")

        else:
            print("Opção inválida.")
        
        resposta = input("Deseja realizar outra operação? (sim para continuar, não para sair): ").strip().lower()
        if resposta not in ['sim', 's']:
            continuar = False

if __name__ == "__main__":
    main()