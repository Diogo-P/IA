import tkinter as tk
from tkinter import ttk, messagebox
from algoritmos.a_estrela import buscar_a_estrela_real
from algoritmos.BFS import buscar_bfs_real
from algoritmos.DFS import buscar_dfs_real
from puzzle import verificar_solubilidade
import time


# =====================================================================
# FUNÇÕES DE INTEGRAÇÃO
# =====================================================================

def executar_busca(algoritmo, heuristica, estado_inicial):
    """
    Executa o algoritmo de busca escolhido e mede o tempo real.
    Retorna: (caminho_de_estados, nos_visitados, profundidade, tempo_execucao)
    """
    print(f"Executando {algoritmo} com a heurística {heuristica} para o estado {estado_inicial}...")

    inicio = time.time()

    if algoritmo == "BFS":
        caminho, nos_visitados, profundidade = buscar_bfs_real(estado_inicial)
    elif algoritmo == "DFS":
        caminho, nos_visitados, profundidade = buscar_dfs_real(estado_inicial)
    elif algoritmo == "A*":
        caminho, nos_visitados, profundidade = buscar_a_estrela_real(estado_inicial, heuristica)
    else:
        messagebox.showwarning("Aviso", "Algoritmo não implementado.")
        return [], 0, 0, 0.0

    tempo = time.time() - inicio
    return caminho, nos_visitados, profundidade, tempo


# =====================================================================
# CLASSE DA INTERFACE GRÁFICA (GUI)
# =====================================================================

class App8Puzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver - PUC Minas")
        self.root.geometry("750x550")
        self.root.resizable(False, False)

        self.caminho_solucao = []
        self.passo_atual = 0

        self.criar_widgets()

    def criar_widgets(self):
        # --- Painel Superior: Configurações ---
        frame_config = ttk.LabelFrame(self.root, text=" Configurações de Busca ", padding=10)
        frame_config.pack(fill="x", padx=15, pady=10)

        ttk.Label(frame_config, text="Estado Inicial (0 para vazio):").grid(row=0, column=0, columnspan=3, sticky="w", pady=5)

        self.entradas_tabuleiro = []
        valores_padrao = ["1", "2", "3", "0", "4", "5", "6", "7", "8"]

        frame_grid_input = ttk.Frame(frame_config)
        frame_grid_input.grid(row=1, column=0, rowspan=2, padx=5, pady=5)

        for i in range(9):
            ent = ttk.Entry(frame_grid_input, width=3, font=('Arial', 12, 'bold'), justify='center')
            ent.insert(0, valores_padrao[i])
            ent.grid(row=i//3, column=i%3, padx=2, pady=2)
            self.entradas_tabuleiro.append(ent)

        ttk.Label(frame_config, text="Algoritmo:").grid(row=1, column=3, padx=10, sticky="e")
        self.combo_algoritmo = ttk.Combobox(frame_config, values=["A*", "BFS", "DFS"], state="readonly", width=15)
        self.combo_algoritmo.set("A*")
        self.combo_algoritmo.grid(row=1, column=4, padx=5, sticky="w")
        self.combo_algoritmo.bind("<<ComboboxSelected>>", self.toggle_heuristica)

        ttk.Label(frame_config, text="Heurística:").grid(row=2, column=3, padx=10, sticky="e")
        self.combo_heuristica = ttk.Combobox(frame_config, values=["Manhattan", "Peças Fora do Lugar"], state="readonly", width=18)
        self.combo_heuristica.set("Manhattan")
        self.combo_heuristica.grid(row=2, column=4, padx=5, sticky="w")

        self.btn_resolver = ttk.Button(frame_config, text="Resolver", command=self.resolver_puzzle)
        self.btn_resolver.grid(row=1, column=5, rowspan=2, padx=20, ipadx=10, ipady=5)

        # --- Painel Central: Tabuleiro e Métricas ---
        frame_corpo = ttk.Frame(self.root)
        frame_corpo.pack(fill="both", expand=True, padx=15, pady=5)

        self.frame_tabuleiro = ttk.LabelFrame(frame_corpo, text=" Visualização do Tabuleiro ", padding=15)
        self.frame_tabuleiro.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.botoes_tabuleiro = []
        for i in range(9):
            btn = tk.Button(self.frame_tabuleiro, text="", font=('Arial', 24, 'bold'), bg="#e0e0e0", relief="groove")
            btn.grid(row=i//3, column=i%3, sticky="nsew", padx=4, pady=4)
            self.frame_tabuleiro.grid_rowconfigure(i//3, weight=1)
            self.frame_tabuleiro.grid_columnconfigure(i%3, weight=1)
            self.botoes_tabuleiro.append(btn)

        frame_lateral = ttk.Frame(frame_corpo, width=250)
        frame_lateral.pack(side="right", fill="both")

        frame_metricas = ttk.LabelFrame(frame_lateral, text=" Saída Obrigatória ", padding=10)
        frame_metricas.pack(fill="x", pady=(0, 10))

        self.lbl_tempo = ttk.Label(frame_metricas, text="Tempo de Execução: ---", font=('Arial', 10))
        self.lbl_tempo.pack(anchor="w", pady=2)
        self.lbl_nos = ttk.Label(frame_metricas, text="Nós Visitados: ---", font=('Arial', 10))
        self.lbl_nos.pack(anchor="w", pady=2)
        self.lbl_profundidade = ttk.Label(frame_metricas, text="Profundidade: ---", font=('Arial', 10))
        self.lbl_profundidade.pack(anchor="w", pady=2)

        frame_navegacao = ttk.LabelFrame(frame_lateral, text=" Controle do Passo a Passo ", padding=10)
        frame_navegacao.pack(fill="both", expand=True)

        self.lbl_passo = ttk.Label(frame_navegacao, text="Passo: 0 / 0", font=('Arial', 11, 'bold'))
        self.lbl_passo.pack(pady=5)

        self.btn_anterior = ttk.Button(frame_navegacao, text="⏮ Anterior", command=self.passo_anterior, state="disabled")
        self.btn_anterior.pack(fill="x", pady=2)

        self.btn_proximo = ttk.Button(frame_navegacao, text="Próximo ⏭", command=self.proximo_passo, state="disabled")
        self.btn_proximo.pack(fill="x", pady=2)

        self.atualizar_tabuleiro_visual([0]*9)

    # --- Lógica de Interface ---

    def toggle_heuristica(self, event=None):
        alg = self.combo_algoritmo.get()
        if alg in ["A*"]:
            self.combo_heuristica.configure(state="readonly")
        else:
            self.combo_heuristica.configure(state="disabled")

    def obter_estado_inicial(self):
        try:
            estado = []
            for ent in self.entradas_tabuleiro:
                val = int(ent.get().strip())
                if val < 0 or val > 8:
                    raise ValueError
                estado.append(val)

            if len(set(estado)) != 9:
                raise ValueError
            return estado
        except ValueError:
            messagebox.showerror("Erro de Entrada", "Insira números de 0 a 8 sem repetições (0 representa o espaço vazio).")
            return None

    def atualizar_tabuleiro_visual(self, estado):
        for i, val in enumerate(estado):
            if val == 0:
                self.botoes_tabuleiro[i].config(text="", bg="#104E8B")
            else:
                self.botoes_tabuleiro[i].config(text=str(val), bg="#B0E2FF")

    def resolver_puzzle(self):
        estado_inicial = self.obter_estado_inicial()
        if not estado_inicial:
            return

        # CORRIGIDO: usa verificar_solubilidade importada de puzzle.py (lógica real)
        if not verificar_solubilidade(estado_inicial):
            messagebox.showwarning("Insolúvel", "Esta configuração inicial não possui solução!")
            return

        alg = self.combo_algoritmo.get()
        heur = self.combo_heuristica.get() if alg == "A*" else "N/A"

        caminho, nos, prof, tempo = executar_busca(alg, heur, estado_inicial)

        if not caminho:
            messagebox.showwarning("Sem solução", "O algoritmo não encontrou solução dentro do limite.")
            return

        self.lbl_tempo.config(text=f"Tempo de Execução: {tempo:.4f}s")
        self.lbl_nos.config(text=f"Nós Visitados: {nos}")
        self.lbl_profundidade.config(text=f"Profundidade: {prof}")

        self.caminho_solucao = caminho
        self.passo_atual = 0
        self.lbl_passo.config(text=f"Passo: {self.passo_atual} / {len(self.caminho_solucao)-1}")

        self.atualizar_tabuleiro_visual(self.caminho_solucao[0])

        if len(self.caminho_solucao) > 1:
            self.btn_proximo.configure(state="normal")
        else:
            self.btn_proximo.configure(state="disabled")
        self.btn_anterior.configure(state="disabled")

    def proximo_passo(self):
        if self.passo_atual < len(self.caminho_solucao) - 1:
            self.passo_atual += 1
            self.atualizar_tabuleiro_visual(self.caminho_solucao[self.passo_atual])
            self.lbl_passo.config(text=f"Passo: {self.passo_atual} / {len(self.caminho_solucao)-1}")
            self.btn_anterior.configure(state="normal")

            if self.passo_atual == len(self.caminho_solucao) - 1:
                self.btn_proximo.configure(state="disabled")

    def passo_anterior(self):
        if self.passo_atual > 0:
            self.passo_atual -= 1
            self.atualizar_tabuleiro_visual(self.caminho_solucao[self.passo_atual])
            self.lbl_passo.config(text=f"Passo: {self.passo_atual} / {len(self.caminho_solucao)-1}")
            self.btn_proximo.configure(state="normal")

            if self.passo_atual == 0:
                self.btn_anterior.configure(state="disabled")


# --- Inicialização da Aplicação ---
if __name__ == "__main__":
    root = tk.Tk()
    app = App8Puzzle(root)
    root.mainloop()