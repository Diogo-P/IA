import heapq
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from puzzle import gerar_sucessores


def calcular_manhattan(estado):
    """
    Calcula a Distância de Manhattan total para o tabuleiro atual.
    O estado objetivo esperado é [0, 1, 2, 3, 4, 5, 6, 7, 8].
    """
    distancia = 0
    posicoes_objetivo = {
        0: (0, 0), 1: (0, 1), 2: (0, 2),
        3: (1, 0), 4: (1, 1), 5: (1, 2),
        6: (2, 0), 7: (2, 1), 8: (2, 2)
    }

    for indice_atual, peca in enumerate(estado):
        if peca != 0:
            linha_atual, col_atual = indice_atual // 3, indice_atual % 3
            linha_obj, col_obj = posicoes_objetivo[peca]
            distancia += abs(linha_atual - linha_obj) + abs(col_atual - col_obj)

    return distancia


def calcular_pecas_fora_do_lugar(estado):
    """
    Heurística secundária: conta quantas peças estão na posição errada.
    """
    estado_meta = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    fora_do_lugar = 0
    for i in range(9):
        if estado[i] != 0 and estado[i] != estado_meta[i]:
            fora_do_lugar += 1
    return fora_do_lugar


def buscar_a_estrela_real(estado_inicial, tipo_heuristica="Manhattan"):
    """
    Executa o algoritmo A* para o 8-Puzzle.
    Retorna: (caminho_completo, total_nos_visitados, profundidade)
    """
    estado_meta = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    if estado_inicial == estado_meta:
        return [estado_inicial], 1, 0

    if tipo_heuristica == "Peças Fora do Lugar":
        h_func = calcular_pecas_fora_do_lugar
    else:
        h_func = calcular_manhattan

    heap = []
    contador = 0

    h_inicial = h_func(estado_inicial)
    heapq.heappush(heap, (h_inicial, contador, estado_inicial, [estado_inicial]))

    visitados_custo = {tuple(estado_inicial): 0}
    nos_visitados = 0

    while heap:
        f_atual, _, estado_atual, caminho_atual = heapq.heappop(heap)
        nos_visitados += 1

        if estado_atual == estado_meta:
            return caminho_atual, nos_visitados, len(caminho_atual) - 1

        g_atual = len(caminho_atual) - 1

        if g_atual > visitados_custo.get(tuple(estado_atual), float('inf')):
            continue

        # CORRIGIDO: desempacota (filho, acao) pois gerar_sucessores retorna tuplas
        for filho, _ in gerar_sucessores(estado_atual):
            g_filho = g_atual + 1
            filho_tupla = tuple(filho)

            if filho_tupla not in visitados_custo or g_filho < visitados_custo[filho_tupla]:
                visitados_custo[filho_tupla] = g_filho

                f_filho = g_filho + h_func(filho)

                contador += 1
                heapq.heappush(heap, (f_filho, contador, filho, caminho_atual + [filho]))

    return [], nos_visitados, 0