import numpy as np

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

def main():
    continuar = True
    while continuar:
        escolha = input("Escolha o método:\n(1) para determinante\n(2) para sistema triangular inferior\n"
                        "(3) para sistema triangular superior\n(4) para decomposição LU\n"
                        "(5) para Cholesky: ")
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
        else:
            print("Opção inválida.")
        
        resposta = input("Deseja realizar outra operação? (sim para continuar, não para sair): ").strip().lower()
        if resposta not in ['sim', 's']:
            continuar = False

if __name__ == "__main__":
    main()