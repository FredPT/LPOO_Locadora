import tkinter as tk
import sys
import os

# Adiciona o diretório raiz ao sys.path para garantir que os módulos sejam encontrados
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from views.veiculo_list_view import JanelaListagemVeiculos

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw() # Esconde a janela principal do Tkinter raiz vazia
    
    app = JanelaListagemVeiculos(master=root)
    # Quando a janela do Toplevel for fechada, encerra o programa
    app.protocol("WM_DELETE_WINDOW", root.destroy)
    
    root.mainloop()