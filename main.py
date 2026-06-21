import tkinter as tk
from interface import App8Puzzle

def main():
    # 1. Cria a janela principal do Tkinter
    root = tk.Tk()
    
    # 2. Inicializa a aplicação passando a janela para a classe da GUI
    app = App8Puzzle(root)
    
    # 3. Mantém a janela aberta e escutando os eventos do usuário
    root.mainloop()

if __name__ == "__main__":
    main()