import tkinter as tk
from tkinter import ttk, messagebox

from model.VeiculoFactory import VeiculoFactory
from model.Categoria import Categoria


class VeiculoDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Dashboard Locadora - Lista de Veículos Cadastrados')
        self.geometry('780x520')
        self.resizable(True, True)

        self.veiculos = []

        self._build_interface()
        self._criar_veiculos_iniciais()
        self._atualizar_tabela()

    def _build_interface(self):
        # Treeview de veículos cadastrados
        colunas = ('placa', 'tipo', 'categoria', 'taxa', 'estado')
        container = tk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        scroll_y = tk.Scrollbar(container, orient=tk.VERTICAL)
        scroll_x = tk.Scrollbar(container, orient=tk.HORIZONTAL)

        self.tree = ttk.Treeview(
            container,
            columns=colunas,
            show='headings',
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            selectmode='browse'
        )

        for col in colunas:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=130, anchor=tk.CENTER)

        self.tree.column('placa', width=120, anchor=tk.CENTER)
        self.tree.column('tipo', width=100, anchor=tk.CENTER)
        self.tree.column('estado', width=120, anchor=tk.CENTER)

        scroll_y.config(command=self.tree.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        scroll_x.config(command=self.tree.xview)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Rodapé com botões de controle
        rodape = tk.Frame(self, padx=10, pady=10)
        rodape.pack(fill=tk.X)

        botao_novo = tk.Button(rodape, text='Novo', width=15, command=self._abrir_tela_novo)
        botao_novo.pack(side=tk.LEFT, padx=5)

        botao_info = tk.Button(rodape, text='Ver Informações', width=15, command=self._ver_informacoes)
        botao_info.pack(side=tk.LEFT, padx=5)

        botao_remover = tk.Button(rodape, text='Remover', width=15, command=self._remover_selecionado)
        botao_remover.pack(side=tk.LEFT, padx=5)

    def _criar_veiculos_iniciais(self):
        try:
            v1 = VeiculoFactory.criar_veiculo('carro', 'ABC1234', 150.0, Categoria.ECONOMICO)
            v2 = VeiculoFactory.criar_veiculo('motorhome', 'DEF5678', 220.0, Categoria.EXECUTIVO)
            v3 = VeiculoFactory.criar_veiculo('carro', 'GHI9012', 180.0, Categoria.EXECUTIVO)
            self.veiculos.extend([v1, v2, v3])
        except Exception as e:
            messagebox.showerror('Erro inicial', f'Falha ao criar veículos iniciais: {e}')

    def _atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for idx, v in enumerate(self.veiculos, start=1):
            self.tree.insert('', tk.END, iid=str(idx), values=(
                v.placa,
                v.__class__.__name__,
                v.categoria.name,
                f'R$ {v.taxa_diaria:.2f}',
                getattr(v.estado_atual, '__class__', type(v.estado_atual)).__name__.replace('State', '')
            ))

    def _abrir_tela_novo(self):
        form = tk.Toplevel(self)
        form.title('Cadastrar Novo Veículo')
        form.geometry('380x230')
        form.resizable(False, False)

        tk.Label(form, text='Placa:').grid(row=0, column=0, sticky=tk.W, padx=8, pady=8)
        placa_entry = tk.Entry(form, width=20)
        placa_entry.grid(row=0, column=1, padx=8, pady=8)

        tk.Label(form, text='Tipo do Veículo:').grid(row=1, column=0, sticky=tk.W, padx=8, pady=8)
        tipo_combo = ttk.Combobox(form, values=['carro', 'motorhome'], state='readonly', width=18)
        tipo_combo.grid(row=1, column=1, padx=8, pady=8)
        tipo_combo.current(0)

        tk.Label(form, text='Categoria:').grid(row=2, column=0, sticky=tk.W, padx=8, pady=8)
        cat_combo = ttk.Combobox(form, values=['ECONOMICO', 'EXECUTIVO'], state='readonly', width=18)
        cat_combo.grid(row=2, column=1, padx=8, pady=8)
        cat_combo.current(0)

        tk.Label(form, text='Taxa Diária:').grid(row=3, column=0, sticky=tk.W, padx=8, pady=8)
        taxa_entry = tk.Entry(form, width=20)
        taxa_entry.grid(row=3, column=1, padx=8, pady=8)

        def salvar():
            placa = placa_entry.get().strip().upper()
            tipo = tipo_combo.get()
            categoria = cat_combo.get()
            taxa = taxa_entry.get().strip()

            if not placa or not tipo or not categoria or not taxa:
                messagebox.showwarning('Dados incompletos', 'Preencha todos os campos.')
                return

            try:
                taxa_valor = float(taxa)
                if taxa_valor <= 0:
                    raise ValueError('Taxa diária deve ser maior que zero.')

                veiculo = VeiculoFactory.criar_veiculo(tipo, placa, taxa_valor, Categoria[categoria])
                self.veiculos.append(veiculo)
                self._atualizar_tabela()
                form.destroy()

            except ValueError as e:
                messagebox.showerror('Erro de valor', f'Taxa diária inválida: {e}')
            except Exception as e:
                messagebox.showerror('Erro', str(e))

        botao_salvar = tk.Button(form, text='Salvar', width=16, command=salvar)
        botao_salvar.grid(row=4, column=0, columnspan=2, pady=10)

    def _ver_informacoes(self):
        selecionado = self.tree.focus()
        if not selecionado:
            messagebox.showinfo('Selecionar', 'Selecione um veículo para ver informações.')
            return

        indice = int(selecionado) - 1
        if 0 <= indice < len(self.veiculos):
            veiculo = self.veiculos[indice]
            info = veiculo.exibir_dados() if hasattr(veiculo, 'exibir_dados') else str(veiculo)
            messagebox.showinfo('Informações do Veículo', info)

    def _remover_selecionado(self):
        selecionado = self.tree.focus()
        if not selecionado:
            messagebox.showinfo('Selecionar', 'Selecione um veículo para remover.')
            return

        indice = int(selecionado) - 1
        if 0 <= indice < len(self.veiculos):
            del self.veiculos[indice]
            self._atualizar_tabela()


if __name__ == '__main__':
    app = VeiculoDashboard()
    app.mainloop()
