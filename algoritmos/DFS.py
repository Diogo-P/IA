import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from puzzle import gerar_sucessores


def buscar_dfs_real(estado_inicial, limite_profundidade=30):
    """
    Executa a Busca em Profundidade (DFS) com limite para o 8-Puzzle.
    Retorna: (caminho_completo, total_nos_visitados, profundidade)
    """
    estado_meta = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    if estado_inicial == estado_meta:
        return [estado_inicial], 1, 0

    pilha = [(estado_inicial, [estado_inicial])]

    visitados = {tuple(estado_inicial): 0}

    nos_visitados = 0

    while pilha:
        estado_atual, caminho_atual = pilha.pop()
        nos_visitados += 1

        profundidade_atual = len(caminho_atual) - 1

        if profundidade_atual >= limite_profundidade:
            continue

        # CORRIGIDO: desempacota (filho, acao) pois gerar_sucessores retorna tuplas
        # Invertemos para manter a ordem de exploração correta na pilha
        for filho, _ in reversed(gerar_sucessores(estado_atual)):

            if filho == estado_meta:
                caminho_final = caminho_atual + [filho]
                return caminho_final, nos_visitados, len(caminho_final) - 1

            filho_tupla = tuple(filho)
            nova_profundidade = profundidade_atual + 1

            if filho_tupla not in visitados or nova_profundidade < visitados[filho_tupla]:
                visitados[filho_tupla] = nova_profundidade
                pilha.append((filho, caminho_atual + [filho]))

    return [], nos_visitados, 0