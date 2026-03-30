import tkinter as tk
from tkinter import ttk, messagebox, Label, Entry, Button, Frame, Scrollbar

from model.VeiculoFactory import VeiculoFactory
from model.Categoria import Categoria


class VeiculoDashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Dashboard Locadora - Lista de Veículos Cadastrados")
        self.geometry("780x520")
        
        self.veiculos = []

        self.frame_tabela = Frame(self)
        self.frame_tabela.pack(fill="both", expand=True, padx=10, pady=(10, 5))
        
        self.frame_rodape = Frame(self, padx=10, pady=10)
        self.frame_rodape.pack(fill="x")

        colunas = ("placa", "tipo", "categoria", "taxa", "estado")
        self.scroll_y = Scrollbar(self.frame_tabela, orient=tk.VERTICAL)
        self.scroll_x = Scrollbar(self.frame_tabela, orient=tk.HORIZONTAL)

        self.tree = ttk.Treeview(
            self.frame_tabela,
            columns=colunas,
            show="headings",
            yscrollcommand=self.scroll_y.set,
            xscrollcommand=self.scroll_x.set,
            selectmode="browse"
        )

        for col in colunas:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=130, anchor=tk.CENTER)
            
        self.tree.column("placa", width=120, anchor=tk.CENTER)
        self.tree.column("tipo", width=100, anchor=tk.CENTER)
        self.tree.column("estado", width=120, anchor=tk.CENTER)

        self.scroll_y.config(command=self.tree.yview)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.scroll_x.config(command=self.tree.xview)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree.pack(fill="both", expand=True)

        self.btn_novo = Button(self.frame_rodape, text="Novo", width=15, command=self.abrir_tela_novo)
        self.btn_novo.pack(side="left", padx=5)

        self.btn_info = Button(self.frame_rodape, text="Ver Informações", width=15, command=self.ver_informacoes)
        self.btn_info.pack(side="left", padx=5)

        self.btn_remover = Button(self.frame_rodape, text="Remover", width=15, command=self.remover_selecionado)
        self.btn_remover.pack(side="left", padx=5)

        self.criar_veiculos_iniciais()
        self.atualizar_tabela()

    def criar_veiculos_iniciais(self):
        try:
            v1 = VeiculoFactory.criar_veiculo("carro", "ABC1234", 150.0, Categoria.ECONOMICO)
            v2 = VeiculoFactory.criar_veiculo("motorhome", "DEF5678", 220.0, Categoria.EXECUTIVO)
            v3 = VeiculoFactory.criar_veiculo("carro", "GHI9012", 180.0, Categoria.EXECUTIVO)
            self.veiculos.extend([v1, v2, v3])
        except Exception as e:
            messagebox.showerror("Erro inicial", f"Falha ao criar veículos iniciais: {e}")

    def atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for idx, v in enumerate(self.veiculos, start=1):
            estado_nome = getattr(v.estado_atual, "__class__", type(v.estado_atual)).__name__.replace("State", "")
            self.tree.insert("", tk.END, iid=str(idx), values=(
                v.placa,
                v.__class__.__name__,
                v.categoria.name,
                f"R$ {v.taxa_diaria:.2f}",
                estado_nome
            ))

    def abrir_tela_novo(self):
        form = tk.Toplevel(self)
        form.title("Cadastrar Novo Veículo")
        form.geometry("380x230")
        form.resizable(False, False)

        lbl_placa = Label(form, text="Placa:")
        lbl_placa.grid(row=0, column=0, sticky="w", padx=8, pady=8)
        txt_placa = Entry(form, width=20)
        txt_placa.grid(row=0, column=1, padx=8, pady=8)

        lbl_tipo = Label(form, text="Tipo do Veículo:")
        lbl_tipo.grid(row=1, column=0, sticky="w", padx=8, pady=8)
        txt_tipo = ttk.Combobox(form, values=["carro", "motorhome"], state="readonly", width=18)
        txt_tipo.grid(row=1, column=1, padx=8, pady=8)
        txt_tipo.current(0)

        lbl_cat = Label(form, text="Categoria:")
        lbl_cat.grid(row=2, column=0, sticky="w", padx=8, pady=8)
        txt_cat = ttk.Combobox(form, values=["ECONOMICO", "EXECUTIVO"], state="readonly", width=18)
        txt_cat.grid(row=2, column=1, padx=8, pady=8)
        txt_cat.current(0)

        lbl_taxa = Label(form, text="Taxa Diária:")
        lbl_taxa.grid(row=3, column=0, sticky="w", padx=8, pady=8)
        txt_taxa = Entry(form, width=20)
        txt_taxa.grid(row=3, column=1, padx=8, pady=8)

        def salvar():
            placa = txt_placa.get().strip().upper()
            tipo = txt_tipo.get()
            categoria = txt_cat.get()
            taxa = txt_taxa.get().strip().replace(",", ".")

            if not placa or not tipo or not categoria or not taxa:
                messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
                return

            try:
                taxa_val = float(taxa)
                if taxa_val <= 0:
                    raise ValueError("A taxa deve ser maior que zero.")

                veiculo = VeiculoFactory.criar_veiculo(tipo, placa, taxa_val, Categoria[categoria])
                self.veiculos.append(veiculo)
                
                self.atualizar_tabela()
                form.destroy()
                messagebox.showinfo("Sucesso", "Veículo cadastrado com sucesso!")

            except ValueError:
                messagebox.showerror("Erro", "Insira um valor numérico válido para a taxa diária (ex: 150.50).")
            except Exception as e:
                messagebox.showerror("Erro ao Salvar", str(e))

        btn_salvar = Button(form, text="Salvar", width=16, command=salvar)
        btn_salvar.grid(row=4, column=0, columnspan=2, pady=10)

    def ver_informacoes(self):
        selecionado = self.tree.focus()
        if not selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione um veículo na tabela primeiro.")
            return

        indice = int(selecionado) - 1
        if 0 <= indice < len(self.veiculos):
            veiculo = self.veiculos[indice]
            
            info = veiculo.exibir_dados()
            messagebox.showinfo("Informações do Veículo", info)

    def remover_selecionado(self):
        selecionado = self.tree.focus()
        if not selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione um veículo para remover.")
            return


        resposta = messagebox.askyesno("Confirmar Remoção", "Tem certeza que deseja remover este veículo?")
        if resposta:
            indice = int(selecionado) - 1
            if 0 <= indice < len(self.veiculos):
                del self.veiculos[indice]
                self.atualizar_tabela()


if __name__ == "__main__":
    app = VeiculoDashboard()
    app.mainloop()