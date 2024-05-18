def calculo_determinante(matriz):
    if not all(len(linha) == len(matriz) for linha in matriz):
        raise ValueError("A matriz deve ser quadrada.")
    
    n = len(matriz)
    det = 1
    
    for i in range(n):
        maxElem = abs(matriz[i][i])
        maxRow = i
        for k in range(i+1, n):
            if abs(matriz[k][i]) > maxElem:
                maxElem = abs(matriz[k][i])
                maxRow = k
        
        if i != maxRow:
            matriz[i], matriz[maxRow] = matriz[maxRow], matriz[i]
            det *= -1 
        
        if matriz[i][i] == 0:
            return 0
        
        det *= matriz[i][i]
        
        for k in range(i+1, n):
            c = -matriz[k][i] / matriz[i][i]
            for j in range(i, n):
                if i == j:
                    matriz[k][j] = 0
                else:
                    matriz[k][j] += c * matriz[i][j]
    
    return det

def sistema_triangular_inferior(ordem, matriz_coeficientes, vetor_termos_independentes):
    if not isinstance(ordem, int) or not isinstance(matriz_coeficientes, list) or not isinstance(vetor_termos_independentes, list):
        raise TypeError("Os parâmetros devem ser um inteiro e duas listas, respectivamente.")
    if len(vetor_termos_independentes) != ordem or any(len(linha) != ordem for linha in matriz_coeficientes):
        raise ValueError("A ordem do sistema e as dimensões da matriz e do vetor devem ser compatíveis.")
    
    for i in range(ordem):
        for j in range(i+1, ordem):
            if matriz_coeficientes[i][j] != 0:
                raise ValueError("A matriz de coeficientes não é triangular inferior.")
    
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
    
    for i in range(1, ordem):
        for j in range(i):
            if matriz_coeficientes[j][i] != 0:
                raise ValueError("A matriz de coeficientes não é triangular superior.")
    
    vetor_solucao = [0] * ordem
    for i in range(ordem-1, -1, -1):
        soma = sum(matriz_coeficientes[i][j] * vetor_solucao[j] for j in range(i+1, ordem))
        vetor_solucao[i] = (vetor_termos_independentes[i] - soma) / matriz_coeficientes[i][i]
    
    return vetor_solucao

def decomposicao_LU(ordem, matriz_coeficientes, vetor_termos_independentes):
    L = [[0.0] * ordem for _ in range(ordem)]
    U = [[0.0] * ordem for _ in range(ordem)]
    
    for i in range(ordem):
        for j in range(i, ordem):
            soma = sum(L[i][k] * U[k][j] for k in range(i))
            U[i][j] = matriz_coeficientes[i][j] - soma
        
        for j in range(i, ordem):
            if i == j:
                L[i][i] = 1
            else:
                soma = sum(L[j][k] * U[k][i] for k in range(i))
                L[j][i] = (matriz_coeficientes[j][i] - soma) / U[i][i]
    
    y = [0.0] * ordem
    for i in range(ordem):
        soma = sum(L[i][j] * y[j] for j in range(i))
        y[i] = vetor_termos_independentes[i] - soma
    
    x = [0.0] * ordem
    for i in reversed(range(ordem)):
        soma = sum(U[i][j] * x[j] for j in range(i+1, ordem))
        x[i] = (y[i] - soma) / U[i][i]
    
    return [round(num, 4) for num in x]

def cholesky(ordem, matriz_coeficientes, vetor_termos_independentes):
    for i in range(ordem):
        for j in range(i):
            if matriz_coeficientes[i][j] != matriz_coeficientes[j][i]:
                return "Erro: A matriz de coeficientes deve ser simétrica e positiva definida."
    
    L = [[0.0] * ordem for _ in range(ordem)]
    
    for i in range(ordem):
        for j in range(i+1):
            soma = sum(L[i][k] * L[j][k] for k in range(j))
            if i == j: 
                L[i][j] = (matriz_coeficientes[i][i] - soma) ** 0.5
            else:
                L[i][j] = (1.0 / L[j][j] * (matriz_coeficientes[i][j] - soma))
    
    y = [0.0] * ordem
    for i in range(ordem):
        y[i] = (vetor_termos_independentes[i] - sum(L[i][j] * y[j] for j in range(i))) / L[i][i]
    
    x = [0.0] * ordem
    for i in reversed(range(ordem)):
        x[i] = (y[i] - sum(L[j][i] * x[j] for j in range(i+1, ordem))) / L[i][i]
    
    return [round(num, 4) for num in x]

def gauss_compacto(ordem, matriz_coeficientes, vetor_termos_independentes):
    A = [list(map(float, linha)) for linha in matriz_coeficientes]
    b = list(map(float, vetor_termos_independentes))

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

    x = [0.0 for _ in range(ordem)]
    for i in range(ordem-1, -1, -1):
        x[i] = b[i] - sum(A[i][j] * x[j] for j in range(i+1, ordem))
        x[i] = round(x[i], 4)

    return x

def gauss_jordan(ordem, matriz_coeficientes, vetor_termos_independentes):
    aug_matriz = [linha + [vetor_termos_independentes[i]] for i, linha in enumerate(matriz_coeficientes)]
    
    for i in range(ordem):
        pivot = aug_matriz[i][i]
        if pivot == 0:
            return "Erro: Pivô zero encontrado, o método de Gauss Jordan não pode prosseguir."
        
        for j in range(ordem + 1):
            aug_matriz[i][j] /= pivot
        
        for k in range(ordem):
            if i != k:
                fator = aug_matriz[k][i]
                for j in range(ordem + 1):
                    aug_matriz[k][j] -= fator * aug_matriz[i][j]
    
    x = [linha[-1] for linha in aug_matriz]
    return x

def jacobi(ordem, coeficientes, termos_independentes, aproximacao_inicial, precisao, max_iteracoes):
    for i in range(ordem):
        if abs(coeficientes[i][i]) <= sum(abs(coeficientes[i][j]) for j in range(ordem) if j != i):
            return "Erro: A matriz de coeficientes não é estritamente diagonal dominante."
    
    if len(aproximacao_inicial) != ordem:
        return "Erro: O vetor de aproximação inicial deve ter o mesmo número de elementos que a ordem do sistema."
    
    x = aproximacao_inicial[:]
    x_novo = x[:]
    
    for iteracao in range(max_iteracoes):
        for i in range(ordem):
            soma = sum(coeficientes[i][j] * x[j] for j in range(ordem) if j != i)
            x_novo[i] = (termos_independentes[i] - soma) / coeficientes[i][i]
        
        if all(abs(x_novo[i] - x[i]) < precisao for i in range(ordem)):
            return [round(num, 4) for num in x_novo], iteracao + 1
        
        x = x_novo[:]
    
    return [round(num, 4) for num in x_novo], max_iteracoes

def gauss_seidel(ordem, matriz_coeficientes, vetor_termos_independentes, aproximacao_inicial, precisao, max_iteracoes):
    x = aproximacao_inicial[:]
    for k in range(max_iteracoes):
        x_novo = x[:]
        for i in range(ordem):
            s1 = sum(matriz_coeficientes[i][j] * x_novo[j] for j in range(i))
            s2 = sum(matriz_coeficientes[i][j] * x[j] for j in range(i + 1, ordem))
            x_novo[i] = (vetor_termos_independentes[i] - s1 - s2) / matriz_coeficientes[i][i]
        
        if all(abs(x_novo[i] - x[i]) < precisao for i in range(ordem)):
            return x_novo, k+1
        
        x = x_novo[:]
    
    return x, k

def matriz_inversa(ordem, matriz, metodo):
    if not isinstance(ordem, int) or not isinstance(matriz, list):
        raise TypeError("Os parâmetros devem ser um inteiro e uma lista, respectivamente.")
    if ordem != len(matriz) or any(len(linha) != ordem for linha in matriz):
        raise ValueError("A matriz deve ser quadrada e corresponder à ordem especificada.")

    if calculo_determinante(matriz) == 0:
        return "Erro: A matriz de coeficientes é singular e não pode ser decomposta."

    inversa = []

    if metodo == 'LU':
        for i in range(ordem):
            vetor_termos_independentes = [0] * ordem
            vetor_termos_independentes[i] = 1
            coluna_inversa = decomposicao_LU(ordem, matriz, vetor_termos_independentes)
            inversa.append(coluna_inversa)

    elif metodo == 'Gauss':
        for i in range(ordem):
            vetor_termos_independentes = [0] * ordem
            vetor_termos_independentes[i] = 1
            coluna_inversa = gauss_compacto(ordem, matriz, vetor_termos_independentes)
            inversa.append(coluna_inversa)

    else:
        raise ValueError("Método inválido. Escolha 'LU' ou 'Gauss'.")

    inversa_transposta = []
    for i in range(ordem):
        inversa_transposta.append([coluna[i] for coluna in inversa])

    return inversa_transposta

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
            print(f"Determinante: {calculo_determinante(matriz)}")
 
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
            
            solucao = decomposicao_LU(ordem, matriz_coeficientes, vetor_termos_independentes)
            if isinstance(solucao, str):
                print(solucao)
            else:
                print(f"Vetor solução: {solucao}")
        
        elif escolha == '5':
            ordem = int(input("Digite a ordem do sistema: "))
            matriz_coeficientes = []
            for i in range(ordem):
                linha = list(map(float, input(f"Digite a linha {i+1} dos coeficientes: ").split()))
                matriz_coeficientes.append(linha)
            vetor_termos_independentes = list(map(float, input("Digite o vetor de termos independentes: ").split()))
            
            solucao = cholesky(ordem, matriz_coeficientes, vetor_termos_independentes)
            if isinstance(solucao, str):
                print(solucao)
            else:
                print(f"Vetor solução: {solucao}")
        
        elif escolha == '6':
            ordem = int(input("Digite a ordem do sistema: "))
            matriz_coeficientes = []
            for i in range(ordem):
                linha = list(map(float, input(f"Digite a linha {i+1} dos coeficientes: ").split()))
                matriz_coeficientes.append(linha)
            vetor_termos_independentes = list(map(float, input("Digite o vetor de termos independentes: ").split()))
            
            solucao = gauss_compacto(ordem, matriz_coeficientes, vetor_termos_independentes)
            print(f"Vetor solução: {solucao}")
        
        elif escolha == '7':
            ordem = int(input("Digite a ordem do sistema: "))
            matriz_coeficientes = []
            for i in range(ordem):
                linha = list(map(float, input(f"Digite a linha {i+1} dos coeficientes: ").split()))
                matriz_coeficientes.append(linha)
            vetor_termos_independentes = list(map(float, input("Digite o vetor de termos independentes: ").split()))
            
            solucao = gauss_jordan(ordem, matriz_coeficientes, vetor_termos_independentes)
            if isinstance(solucao, str):
                print(solucao)
            else:
                print(f"Vetor solução: {solucao}")

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
                resultado, iteracoes = jacobi(ordem, coeficientes, termos_independentes, aproximacao_inicial, precisao, max_iteracoes)
                resultado_formatado = [f"{num:.4f}" for num in resultado]
                print("Vetor solução: [" + ", ".join(resultado_formatado) + f"], Iterações: {iteracoes}")
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