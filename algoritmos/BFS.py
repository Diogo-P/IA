from collections import deque

def encontrar_posicao_zero(estado):
    """Retorna o índice (0 a 8) onde o espaço vazio (0) está localizado."""
    return estado.index(0)

def gerar_sucessores(estado):
    """
    Gera os estados filhos (vizinhos) a partir dos movimentos válidos do zero.
    As movimentações simulam um tabuleiro 3x3 em uma fita linear de 9 posições.
    """
    filhos = []
    pos_zero = encontrar_posicao_zero(estado)
    
    # Mapeamento de movimentos baseados no índice do vetor linear:
    # Cada tupla contém (mudança de índice, condição para o movimento ser válido)
    movimentos = {
        "CIMA":    (-3, pos_zero >= 3),
        "BAIXO":   ( 3, pos_zero <= 5),
        "ESQUERDA":(-1, pos_zero % 3 != 0),
        "DIREITA": ( 1, pos_zero % 3 != 2)
    }
    
    for direcao, (deslocamento, condicao_valida) in movimentos.items():
        if condicao_valida:
            # Cria uma cópia do estado atual para aplicar a jogada
            novo_estado = list(estado)
            # Troca o zero de lugar com a peça adjacente
            alvo = pos_zero + deslocamento
            novo_estado[pos_zero], novo_estado[alvo] = novo_estado[alvo], novo_estado[pos_zero]
            filhos.append(novo_estado)
            
    return filhos

def buscar_bfs_real(estado_inicial):
    """
    Executa a Busca em Largura (BFS) para o 8-Puzzle.
    Retorna: (caminho_completo, total_nos_visitados, profundidade)
    """
    # O estado meta que o seu trabalho exige
    estado_meta = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    
    # Caso o estado inicial já seja o objetivo
    if estado_inicial == estado_meta:
        return [estado_inicial], 1, 0

    # A Fila (FIFO) armazena tuplas: (estado_atual, caminho_ate_ele)
    # Usamos o 'deque' do Python porque o pop(0) de uma lista comum é lento O(n),
    # enquanto o popleft() do deque é O(1), ideal para IA.
    fila = deque([ (estado_inicial, [estado_inicial]) ])
    
    # Conjunto de visitados armazena tuplas (já que listas não podem ser indexadas em sets)
    visitados = set([tuple(estado_inicial)])
    
    nos_visitados = 0

    while fila:
        # Retira o primeiro elemento que entrou na fila (Busca em Largura)
        estado_atual, caminho_atual = fila.popleft()
        nos_visitados += 1
        
        # Gerar os vizinhos (filhos) do nó atual através do grafo implícito
        for filho in gerar_sucessores(estado_atual):
            
            # Se achamos o objetivo, encerra e retorna o relatório
            if filho == estado_meta:
                caminho_final = caminho_atual + [filho]
                profundidade = len(caminho_final) - 1
                return caminho_final, nos_visitados, profundidade
            
            # Se for um vértice inédito, adiciona na fila e marca como visitado
            filho_tupla = tuple(filho)
            if filho_tupla not in visitados:
                visitados.add(filho_tupla)
                fila.append((filho, caminho_atual + [filho]))
                
    # Se a fila esvaziar e não achar nada (o que não acontece se passou pelo teste de paridade)
    return [], nos_visitados, 0

