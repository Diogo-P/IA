def buscar_dfs_real(estado_inicial, limite_profundidade=30):
    """
    Executa a Busca em Profundidade (DFS) com limite para o 8-Puzzle.
    Retorna: (caminho_completo, total_nos_visitados, profundidade)
    """
    # O estado meta que o seu trabalho exige
    estado_meta = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    
    if estado_inicial == estado_meta:
        return [estado_inicial], 1, 0

    # A Pilha (LIFO) armazena tuplas: (estado_atual, caminho_ate_ele)
    # Em Python, uma lista comum funciona perfeitamente como Pilha usando append() e pop()
    pilha = [(estado_inicial, [estado_inicial])]
    
    # O dicionário 'visitados' agora armazena a menor profundidade em que o estado foi visto.
    # Isso é necessário na DFS porque se encontrarmos o mesmo estado por um caminho 
    # mais curto, precisamos reexplorá-lo!
    visitados = {tuple(estado_inicial): 0}
    
    nos_visitados = 0

    while pilha:
        # .pop() sem índice retira o ÚLTIMO elemento que entrou (LIFO - Comportamento de Pilha)
        estado_atual, caminho_atual = pilha.pop()
        nos_visitados += 1
        
        profundidade_atual = len(caminho_atual) - 1
        
        # Se atingir o limite estipulado, corta este ramo e faz o backtracking
        if profundidade_atual >= limite_profundidade:
            continue
            
        # Gerar os vizinhos (filhos)
        # Invertemos a lista de sucessores para que a ordem de exploração (Cima, Baixo...) 
        # seja avaliada corretamente na pilha.
        for filho in reversed(gerar_sucessores(estado_atual)):
            
            # Se achamos o objetivo, encerra e retorna o relatório
            if filho == estado_meta:
                caminho_final = caminho_atual + [filho]
                return caminho_final, nos_visitados, len(caminho_final) - 1
            
            filho_tupla = tuple(filho)
            nova_profundidade = profundidade_atual + 1
            
            # Se o nó é inédito OU se foi achado agora por um caminho mais curto/raso
            if filho_tupla not in visitados or nova_profundidade < visitados[filho_tupla]:
                visitados[filho_tupla] = nova_profundidade
                pilha.append((filho, caminho_atual + [filho]))
                
    # Se esvaziar a pilha e não encontrar dentro do limite
    return [], nos_visitados, 0