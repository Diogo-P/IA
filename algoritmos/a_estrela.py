import heapq  # <--- Certifique-se de ter esse import no topo de buscas.py
from algoritmos.BFS import gerar_sucessores

def calcular_manhattan(estado):
    """
    Calcula a Distância de Manhattan total para o tabuleiro atual.
    O estado objetivo esperado é [0, 1, 2, 3, 4, 5, 6, 7, 8].
    """
    distancia = 0
    # Mapeamento da posição correta (linha, coluna) de cada peça no objetivo:
    # Índice representa a peça. Ex: peça 1 deve estar na linha 0, coluna 1.
    posicoes_objetivo = {
        0: (0, 0), 1: (0, 1), 2: (0, 2),
        3: (1, 0), 4: (1, 1), 5: (1, 2),
        6: (2, 0), 7: (2, 1), 8: (2, 2)
    }
    
    for indice_atual, peca in enumerate(estado):
        if peca != 0:  # A heurística clássica ignora o espaço vazio
            # Linha e coluna atuais na matriz 3x3
            linha_atual, col_atual = indice_atual // 3, indice_atual % 3
            # Linha e coluna onde a peça DEVERIA estar
            linha_obj, col_obj = posicoes_objetivo[peca]
            
            # Soma as distâncias verticais e horizontais (|x1 - x2| + |y1 - y2|)
            distancia += abs(linha_atual - linha_obj) + abs(col_atual - col_obj)
            
    return distancia

def calcular_pecas_fora_do_lugar(estado):
    """
    Heurística secundária: conta simplesmente quantas peças estão na posição errada.
    """
    estado_meta = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    fora_do_lugar = 0
    for i in range(9):
        if estado[i] != 0 and estado[i] != estado_meta[i]:
            fora_do_lugar += 1
    return fora_do_lugar

def calcular_distancia_euclidiana(estado):
    """
    Calcula a soma das distâncias euclidianas de cada peça até seu destino.
    """
    distancia = 0.0
    posicoes_objetivo = {
        0: (0, 0), 1: (0, 1), 2: (0, 2),
        3: (1, 0), 4: (1, 1), 5: (1, 2),
        6: (2, 0), 7: (2, 1), 8: (2, 2)
    }

    for indice_atual, peca in enumerate(estado):
        if peca != 0:
            linha_atual, col_atual = indice_atual // 3, indice_atual % 3
            linha_obj, col_obj = posicoes_objetivo[peca]
            distancia += ((linha_atual - linha_obj) ** 2 + (col_atual - col_obj) ** 2) ** 0.5

    return distancia

def buscar_a_estrela_real(estado_inicial, tipo_heuristica="Manhattan"):
    """
    Executa o algoritmo A* para o 8-Puzzle.
    Retorna: (caminho_completo, total_nos_visitados, profundidade)
    """
    estado_meta = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    
    if estado_inicial == estado_meta:
        return [estado_inicial], 1, 0

    # Escolhe a função heurística selecionada na interface
    if tipo_heuristica == "Peças Fora do Lugar":
        h_func = calcular_pecas_fora_do_lugar
    elif tipo_heuristica == "Distância Euclidiana":
        h_func = calcular_distancia_euclidiana
    else:
        h_func = calcular_manhattan # Padrão
        
    # A Fila de Prioridades (Heap) armazena tuplas: (f_custo_total, contador, estado, caminho)
    # O 'contador' serve apenas para desatar nós se dois tabuleiros tiverem o mesmo custo f.
    heap = []
    contador = 0
    
    # Custo inicial: g(n) = 0, f(n) = 0 + h(n)
    h_inicial = h_func(estado_inicial)
    heapq.heappush(heap, (h_inicial, contador, estado_inicial, [estado_inicial]))
    
    # Controla o menor custo g(n) para chegar a cada estado
    visitados_custo = {tuple(estado_inicial): 0}
    nos_visitados = 0

    while heap:
        # Extrai o nó com o MENOR custo f(n) da fila automaticamente (O(log n))
        f_atual, _, estado_atual, caminho_atual = heapq.heappop(heap)
        nos_visitados += 1
        
        if estado_atual == estado_meta:
            return caminho_atual, nos_visitados, len(caminho_atual) - 1
            
        g_atual = len(caminho_atual) - 1
        
        # Se encontramos um caminho pior para um estado já processado, ignora
        if g_atual > visitados_custo.get(tuple(estado_atual), float('inf')):
            continue

        for filho in gerar_sucessores(estado_atual):
            g_filho = g_atual + 1
            filho_tupla = tuple(filho)
            
            # Se o filho é inédito OU encontramos um caminho mais curto (g menor) até ele
            if filho_tupla not in visitados_custo or g_filho < visitados_custo[filho_tupla]:
                visitados_custo[filho_tupla] = g_filho
                
                # f(n) = g(n) + h(n)
                f_filho = g_filho + h_func(filho)
                
                contador += 1
                heapq.heappush(heap, (f_filho, contador, filho, caminho_atual + [filho]))

    return [], nos_visitados, 0