# puzzle.py

def obter_posicao_vazio(estado):
    """Retorna o índice onde está o zero (espaço vazio)."""
    return estado.index(0)

def teste_objetivo(estado):
    """
    Verifica se o estado atual é o estado objetivo exigido pelo trabalho.
    Objetivo: [0, 1, 2, 3, 4, 5, 6, 7, 8]
    """
    return estado == [0, 1, 2, 3, 4, 5, 6, 7, 8]

def verificar_solubilidade(estado):
    """
    Nem toda configuração inicial tem solução[cite: 11].
    Para o 8-puzzle com o vazio na posição final (topo-esquerda, índice 0),
    o tabuleiro é solúvel se o número de inversões for PAR.
    """
    # Remove o zero para contar as inversões das peças numeradas
    pecas = [num for num in estado if num != 0]
    inversoes = 0
    
    for i in range(len(pecas)):
        for j in range(i + 1, len(pecas)):
            if pecas[i] > pecas[j]:
                inversoes += 1
                
    # Retorna True se for par (solúvel), False se for ímpar (insolúvel)
    return inversoes % 2 == 0

def gerar_sucessores(estado):
    """
    Modelo de Transição / Conjunto de Ações.
    Move a peça adjacente para o espaço vazio (cima, baixo, esquerda ou direita)[cite: 10].
    Retorna uma lista de tuplas: (novo_estado, acao_tomada)
    """
    sucessores = []
    vazio = obter_posicao_vazio(estado)
    
    # Representação visual das linhas/colunas no vetor de 9 posições:
    # [0, 1, 2] -> Linha 0
    # [3, 4, 5] -> Linha 1
    # [6, 7, 8] -> Linha 2
    linha = vazio // 3
    coluna = vazio % 3
    
    # Definindo os movimentos possíveis para o VAZIO (0)
    # (parâmetro de linha, parâmetro de coluna, nome da ação da PEÇA que se move)
    movimentos = [
        (-1, 0, "CIMA"),    # Move a peça de cima para baixo (vazio sobe)
        (1, 0, "BAIXO"),    # Move a peça de baixo para cima (vazio desce)
        (0, -1, "ESQUERDA"),# Move a peça da esquerda para a direita (vazio vai para esquerda)
        (0, 1, "DIREITA")   # Move a peça da direita para a esquerda (vazio vai para direita)
    ]
    
    for dl, dc, acao in movimentos:
        nova_linha = linha + dl
        nova_coluna = coluna + dc
        
        # Verifica se o movimento está dentro dos limites do tabuleiro 3x3
        if 0 <= nova_linha < 3 and 0 <= nova_coluna < 3:
            novo_vazio = nova_linha * 3 + nova_coluna
            
            # Cria uma cópia do estado atual para aplicar a transição
            novo_estado = list(estado)
            # Inverte a posição do vazio com a peça adjacente
            novo_estado[vazio], novo_estado[novo_vazio] = novo_estado[novo_vazio], novo_estado[vazio]
            
            sucessores.append((novo_estado, acao))
            
    return sucessores