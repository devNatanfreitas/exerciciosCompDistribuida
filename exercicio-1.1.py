import math
import matplotlib.pyplot as plt
import numpy as np

def availability_general(n, k, p):
    """
    Calcula a disponibilidade geral do serviço usando a fórmula da distribuição binomial.
    """
    if not (isinstance(n, int) and n > 0):
        raise ValueError("n deve ser um inteiro positivo.")
    if not (isinstance(k, int) and 0 < k <= n):
        raise ValueError("k deve ser um inteiro tal que 0 < k <= n.")
    if not (0.0 <= p <= 1.0):
        raise ValueError("p deve ser uma probabilidade entre 0 e 1.")

    total_availability = 0.0
    for i in range(k, n + 1):
        combinations = math.comb(n, i)
        prob = combinations * (p ** i) * ((1 - p) ** (n - i))
        total_availability += prob

    return total_availability

def availability_k_equals_1(n: int, p: float) -> float:
    """
    Fórmula otimizada para k=1.
    """
    return 1 - (1 - p) ** n

def availability_k_equals_n(n: int, p: float) -> float:
    """
    Fórmula otimizada para k=n.
    """
    return p ** n

if __name__ == "__main__":

    # --- Cenário 1: Variando o número de servidores (n) ---
    p_fixo = 0.95
    n_valores = [3, 5, 7, 9, 11, 13, 15]

    # Listas para armazenar resultados para o gráfico
    disp_leitura_n_vals = []
    disp_quorum_n_vals = []
    disp_escrita_n_vals = []

    print(f"\nCenário 1: Disponibilidade variando 'n' (com p = {p_fixo:.2f} fixo)\n")
    print(" n  | k (leitura) | Disp. (k=1)  | k (quórum) | Disp. (k=n/2) | k (escrita) | Disp. (k=n)")
    print("----|-------------|--------------|------------|---------------|-------------|--------------")

    for n in n_valores:
        k_leitura = 1
        disp_leitura = availability_general(n, k_leitura, p_fixo)
        
        k_quorum = math.floor(n / 2) + 1
        disp_quorum = availability_general(n, k_quorum, p_fixo)

        k_escrita = n
        disp_escrita = availability_general(n, k_escrita, p_fixo)
        
        # Armazena os resultados para plotagem
        disp_leitura_n_vals.append(disp_leitura)
        disp_quorum_n_vals.append(disp_quorum)
        disp_escrita_n_vals.append(disp_escrita)
        
        print(f"{n:^4}|{k_leitura:^13}| {disp_leitura:^12.6f} |{k_quorum:^12}| {disp_quorum:^13.6f} |{k_escrita:^13}| {disp_escrita:^12.6f}")

    # --- Visualização Gráfica do Cenário 1 ---
    plt.figure(figsize=(10, 6))
    plt.plot(n_valores, disp_leitura_n_vals, marker='o', linestyle='-', label=f'k = 1 (Leitura)')
    plt.plot(n_valores, disp_quorum_n_vals, marker='s', linestyle='--', label=f'k = n/2+1 (Quórum)')
    plt.plot(n_valores, disp_escrita_n_vals, marker='x', linestyle=':', label=f'k = n (Escrita)')
    plt.xlabel('Número de Servidores (n)')
    plt.ylabel('Disponibilidade')
    plt.title(f'Disponibilidade vs. Número de Servidores (p = {p_fixo:.2f})')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.ylim(0, 1.01) # Limita eixo y entre 0 e 1
    plt.xticks(n_valores)

    print("\n" + "="*80 + "\n")

    # --- Cenário 2: Variando a probabilidade de disponibilidade (p) ---
    n_fixo = 5
    p_valores = np.linspace(0.80, 1.0, 21) # Valores de p de 0.80 a 1.0

    # Listas para armazenar resultados para o gráfico
    disp_leitura_p_vals = []
    disp_quorum_p_vals = []
    disp_escrita_p_vals = []
    
    k_leitura_n5 = 1
    k_quorum_n5 = math.floor(n_fixo / 2) + 1  # k = 3
    k_escrita_n5 = n_fixo
    
    print(f"Cenário 2: Disponibilidade variando 'p' (com n = {n_fixo} fixo)\n")
    print(f" (k para leitura={k_leitura_n5}, k para quórum={k_quorum_n5}, k para escrita={k_escrita_n5})\n")
    print(" p    | Disp. (k=1)  | Disp. (k=3)  | Disp. (k=5)")
    print("------|--------------|--------------|--------------")

    # Imprime alguns valores representativos na tabela
    p_valores_tabela = [0.80, 0.90, 0.95, 0.99, 0.999]
    for p in p_valores_tabela:
        disp_leitura = availability_general(n_fixo, k_leitura_n5, p)
        disp_quorum = availability_general(n_fixo, k_quorum_n5, p)
        disp_escrita = availability_general(n_fixo, k_escrita_n5, p)
        print(f"{p:^6.3f}| {disp_leitura:^12.6f} | {disp_quorum:^12.6f} | {disp_escrita:^12.6f}")

    # Calcula todos os valores para o gráfico
    for p in p_valores:
        disp_leitura_p_vals.append(availability_general(n_fixo, k_leitura_n5, p))
        disp_quorum_p_vals.append(availability_general(n_fixo, k_quorum_n5, p))
        disp_escrita_p_vals.append(availability_general(n_fixo, k_escrita_n5, p))

    # --- Visualização Gráfica do Cenário 2 ---
    plt.figure(figsize=(10, 6))
    plt.plot(p_valores, disp_leitura_p_vals, marker='', linestyle='-', label=f'k = {k_leitura_n5} (Leitura)')
    plt.plot(p_valores, disp_quorum_p_vals, marker='', linestyle='--', label=f'k = {k_quorum_n5} (Quórum)')
    plt.plot(p_valores, disp_escrita_p_vals, marker='', linestyle=':', label=f'k = {k_escrita_n5} (Escrita)')
    plt.xlabel('Probabilidade de um Servidor Estar Disponível (p)')
    plt.ylabel('Disponibilidade Total do Serviço')
    plt.title(f'Disponibilidade vs. Confiabilidade Individual (n = {n_fixo})')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.ylim(0, 1.01)

    # Exibe os dois gráficos
    plt.tight_layout()
    plt.show()