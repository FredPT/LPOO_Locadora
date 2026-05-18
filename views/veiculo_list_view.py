import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox
from control.veiculo_controller import VeiculoController
from views.veiculo_view import JanelaCadastroVeiculo

class JanelaListagemVeiculos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Veículos Cadastrados")
        self.geometry("600x400")
        
        self.controller = VeiculoController()

        self.criar_widgets()
        self.carregar_dados()

    def criar_widgets(self):
        lbl_titulo = tk.Label(self, text="Veículos Cadastrados", font=("Helvetica", 16, "bold"))
        lbl_titulo.pack(pady=10)

        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=20, pady=10)

        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side="right", fill="y")

        colunas = ("Placa", "Tipo", "Categoria", "Taxa Diária (R$)")
        self.tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", yscrollcommand=scrollbar.set)
       
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        self.tree.pack(expand=True, fill="both")
        scrollbar.config(command=self.tree.yview)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=20, pady=5)

        btn_novo = tk.Button(frame_botoes, text="Novo", width=10, command=self.abrir_novo)
        btn_novo.pack(side="left", padx=5)

        btn_editar = tk.Button(frame_botoes, text="Editar", width=15, command=self.abrir_editar)
        btn_editar.pack(side="left", padx=5)

        btn_remover = tk.Button(frame_botoes, text="Remover", width=10, command=self.remover_veiculo)
        btn_remover.pack(side="left", padx=5)

        btn_fechar = tk.Button(frame_botoes, text="Fechar", width=10, command=self.destroy)
        btn_fechar.pack(side="right", padx=5)

    def abrir_novo(self):
        janela_cadastro = JanelaCadastroVeiculo(self)
        self.wait_window(janela_cadastro)
        self.carregar_dados()

    def abrir_editar(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um veículo para editar.", parent=self)
            return

        item = self.tree.item(selecionado[0])
        placa = item['values'][0]
        veiculo = self.controller.buscar_por_placa(placa)

        if not veiculo:
            messagebox.showerror("Erro", "Veículo não encontrado.", parent=self)
            return

        janela_edicao = JanelaCadastroVeiculo(self, veiculo=veiculo)
        self.wait_window(janela_edicao)
        self.carregar_dados()


    def remover_veiculo(self):
        selecionado = self.tree.selection()
        
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um veículo para remover.", parent=self)
            return

        item = self.tree.item(selecionado[0])
        placa = item['values'][0]
        
        resposta = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja remover o veículo de placa {placa}?", parent=self)
        if resposta:
            sucesso, msg = self.controller.remover_veiculo(placa)
            if sucesso:
                self.carregar_dados()
                messagebox.showinfo("Sucesso", msg, parent=self)
            else:
                messagebox.showerror("Erro", msg, parent=self)

    def carregar_dados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        veiculos = self.controller.listar_veiculos()
        
        if veiculos is None:
             messagebox.showerror("Erro", "Erro ao carregar veículos.", parent=self)
             return
             
        for v in veiculos:
            tipo_nome = type(v).__name__
            taxa_formatada = f"R$ {v.taxa_diaria:.2f}".replace('.', ',')
            categoria_texto = v.categoria.name if hasattr(v.categoria, 'name') else str(v.categoria)
            
            self.tree.insert("", "end", values=(
                v.placa, 
                tipo_nome, 
                categoria_texto, 
                taxa_formatada
            ))