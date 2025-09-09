import math
import matplotlib.pyplot as plt
import numpy as np

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


def simulate_availability(n: int, k: int, p: float, num_rounds: int = 100000):
    successful_rounds = 0
    for _ in range(num_rounds):
        available_servers = np.sum(np.random.rand(n) <= p)
        if available_servers >= k:
            successful_rounds += 1
    return successful_rounds / num_rounds

if __name__ == "__main__":
    
    num_simulations = 100000
    
    print(f"Executando simulação com {num_simulations} rodadas por cenário.\n")
    
    p_fixo = 0.95
    n_valores = [3, 5, 7, 9, 11, 13, 15]
    disp_leitura_n_vals, sim_leitura_n_vals = [], []
    disp_quorum_n_vals, sim_quorum_n_vals = [], []
    disp_escrita_n_vals, sim_escrita_n_vals = [], []
    
    print(f"\nCenário 1: Disponibilidade variando 'n' (com p = {p_fixo:.2f} fixo)\n")
    print(" n  | k (leitura) | Disp. Analítica | Disp. Sim.   | k (quórum) | Disp. Analítica | Disp. Sim.   | k (escrita) | Disp. Analítica | Disp. Sim.")
    print("----|-------------|-----------------|--------------|------------|-----------------|--------------|-------------|-----------------|--------------")
    
    for n in n_valores:
        k_leitura = 1
        disp_leitura = availability_general(n, k_leitura, p_fixo)
        sim_leitura = simulate_availability(n, k_leitura, p_fixo, num_simulations)
        k_quorum = math.floor(n / 2) + 1
        disp_quorum = availability_general(n, k_quorum, p_fixo)
        sim_quorum = simulate_availability(n, k_quorum, p_fixo, num_simulations)
        k_escrita = n
        disp_escrita = availability_general(n, k_escrita, p_fixo)
        sim_escrita = simulate_availability(n, k_escrita, p_fixo, num_simulations)
        disp_leitura_n_vals.append(disp_leitura)
        sim_leitura_n_vals.append(sim_leitura)
        disp_quorum_n_vals.append(disp_quorum)
        sim_quorum_n_vals.append(sim_quorum)
        disp_escrita_n_vals.append(disp_escrita)
        sim_escrita_n_vals.append(sim_escrita)
        print(f"{n:^4}|{k_leitura:^13}| {disp_leitura:^15.6f} | {sim_leitura:^12.6f} |{k_quorum:^12}| {disp_quorum:^15.6f} | {sim_quorum:^12.6f} |{k_escrita:^13}| {disp_escrita:^15.6f} | {sim_escrita:^12.6f}")
    
    plt.figure(figsize=(12, 7))
    plt.plot(n_valores, disp_leitura_n_vals, 'b-', label='k=1 (Teórico)')
    plt.plot(n_valores, disp_quorum_n_vals, 'g--', label='k=n/2+1 (Teórico)')
    plt.plot(n_valores, disp_escrita_n_vals, 'r:', label='k=n (Teórico)')
    plt.plot(n_valores, sim_leitura_n_vals, 'bo', label='k=1 (Simulado)', markersize=8, alpha=0.7)
    plt.plot(n_valores, sim_quorum_n_vals, 'gs', label='k=n/2+1 (Simulado)', markersize=8, alpha=0.7)
    plt.plot(n_valores, sim_escrita_n_vals, 'rx', label='k=n (Simulado)', markersize=8, alpha=0.7)
    
    plt.xlabel('Número de Servidores (n)')
    plt.ylabel('Disponibilidade')
    plt.title(f'Disponibilidade vs. Número de Servidores (p = {p_fixo:.2f}) - Teórico vs. Simulado')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.ylim(0, 1.05) 
    plt.xticks(n_valores)
    print("\n" + "="*80 + "\n")
    
    
    n_fixo = 5
    p_valores_grafico = np.linspace(0.80, 1.0, 21) 
    k_leitura_n5 = 1
    k_quorum_n5 = math.floor(n_fixo / 2) + 1
    k_escrita_n5 = n_fixo
    
    print(f"Cenário 2: Disponibilidade variando 'p' (com n = {n_fixo} fixo)\n")
    print(f" (k para leitura={k_leitura_n5}, k para quórum={k_quorum_n5}, k para escrita={k_escrita_n5})\n")
    print(" p    | k=1 Analítico  | k=1 Simulado   | k=3 Analítico  | k=3 Simulado   | k=5 Analítico  | k=5 Simulado")
    print("------|----------------|----------------|----------------|----------------|----------------|----------------")
    
    p_valores_tabela = [0.80, 0.90, 0.95, 0.99, 0.999]
    for p in p_valores_tabela:
        disp_l = availability_general(n_fixo, k_leitura_n5, p)
        sim_l = simulate_availability(n_fixo, k_leitura_n5, p, num_simulations)
        disp_q = availability_general(n_fixo, k_quorum_n5, p)
        sim_q = simulate_availability(n_fixo, k_quorum_n5, p, num_simulations)
        disp_e = availability_general(n_fixo, k_escrita_n5, p)
        sim_e = simulate_availability(n_fixo, k_escrita_n5, p, num_simulations)
        print(f"{p:^6.3f}| {disp_l:^14.6f} | {sim_l:^14.6f} | {disp_q:^14.6f} | {sim_q:^14.6f} | {disp_e:^14.6f} | {sim_e:^14.6f}")
        
        
    disp_leitura_p_vals = [availability_general(n_fixo, k_leitura_n5, p) for p in p_valores_grafico]
    sim_leitura_p_vals = [simulate_availability(n_fixo, k_leitura_n5, p, num_simulations) for p in p_valores_grafico]
    disp_quorum_p_vals = [availability_general(n_fixo, k_quorum_n5, p) for p in p_valores_grafico]
    sim_quorum_p_vals = [simulate_availability(n_fixo, k_quorum_n5, p, num_simulations) for p in p_valores_grafico]
    disp_escrita_p_vals = [availability_general(n_fixo, k_escrita_n5, p) for p in p_valores_grafico]
    sim_escrita_p_vals = [simulate_availability(n_fixo, k_escrita_n5, p, num_simulations) for p in p_valores_grafico]
    
    plt.figure(figsize=(12, 7))
    
    plt.plot(p_valores_grafico, disp_leitura_p_vals, 'b-', label=f'k={k_leitura_n5} (Teórico)')
    plt.plot(p_valores_grafico, sim_leitura_p_vals, 'bo', alpha=0.7)
    plt.plot(p_valores_grafico, disp_quorum_p_vals, 'g--', label=f'k={k_quorum_n5} (Teórico)')
    plt.plot(p_valores_grafico, sim_quorum_p_vals, 'gs', alpha=0.7)
    plt.plot(p_valores_grafico, disp_escrita_p_vals, 'r:', label=f'k={k_escrita_n5} (Teórico)')
    plt.plot(p_valores_grafico, sim_escrita_p_vals, 'rx', alpha=0.7)
    
    plt.xlabel('Probabilidade de um Servidor Estar Disponível (p)')
    plt.ylabel('Disponibilidade Total do Serviço')
    plt.title(f'Disponibilidade vs. Confiabilidade Individual (n={n_fixo}) - Teórico vs. Simulado')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.ylim(0, 1.05)
    plt.tight_layout()
    plt.show()