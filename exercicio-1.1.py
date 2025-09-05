import math

def availability_general(n, k, p):
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

    return 1 - (1 - p) ** n

def availability_k_equals_n(n: int, p: float) -> float:

    return p ** n

if __name__ == "__main__":

     # --- Cenário 1: Variando o número de servidores (n) ---
    # Vamos fixar a probabilidade de um servidor estar UP em 95% (p = 0.95)
    # e ver o que acontece quando aumentamos o número de réplicas.
    


    p_fixo = 0.95
    n_valores = [3, 5, 7, 11, 15]

    print(f"\nCenário 1: Disponibilidade variando 'n' (com p = {p_fixo:.2f} fixo)\n")
    print(" n  | k (leitura) | Disp. (k=1)  | k (quórum) | Disp. (k=n/2) | k (escrita) | Disp. (k=n)")
    print("----|-------------|--------------|------------|---------------|-------------|--------------")

    for n in n_valores:
        # k para operação de leitura (pelo menos 1 servidor)
        k_leitura = 1
        disp_leitura = availability_general(n, k_leitura, p_fixo)
        
        # k para operação de quórum (maioria simples)
        k_quorum = math.floor(n / 2) + 1
        disp_quorum = availability_general(n, k_quorum, p_fixo)

        # k para operação de escrita forte (todos os servidores)
        k_escrita = n
        disp_escrita = availability_general(n, k_escrita, p_fixo)
        
        # Imprime a linha da tabela formatada
        print(f"{n:^4}|{k_leitura:^13}| {disp_leitura:^12.6f} |{k_quorum:^12}| {disp_quorum:^13.6f} |{k_escrita:^13}| {disp_escrita:^12.6f}")

    print("\n" + "="*80 + "\n")

    # --- Cenário 2: Variando a probabilidade de disponibilidade (p) ---
    # Vamos fixar o número de servidores em 5 (n = 5) e ver o impacto
    # da confiabilidade individual de cada máquina.
    
    n_fixo = 5
    p_valores = [0.80, 0.90, 0.95, 0.99, 0.999]

    # Calcula os valores de k para n=5
    k_leitura_n5 = 1
    k_quorum_n5 = math.floor(n_fixo / 2) + 1  # k = 3
    k_escrita_n5 = n_fixo
    
    print(f"Cenário 2: Disponibilidade variando 'p' (com n = {n_fixo} fixo)\n")
    print(f" (k para leitura={k_leitura_n5}, k para quórum={k_quorum_n5}, k para escrita={k_escrita_n5})\n")
    print(" p    | Disp. (k=1)  | Disp. (k=3)  | Disp. (k=5)")
    print("------|--------------|--------------|--------------")

    for p in p_valores:
        disp_leitura = availability_general(n_fixo, k_leitura_n5, p)
        disp_quorum = availability_general(n_fixo, k_quorum_n5, p)
        disp_escrita = availability_general(n_fixo, k_escrita_n5, p)

        print(f"{p:^6.3f}| {disp_leitura:^12.6f} | {disp_quorum:^12.6f} | {disp_escrita:^12.6f}")