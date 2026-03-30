import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.Veiculo import *
from model.VeiculoFactory import VeiculoFactory
from dao.veiculo_dao import VeiculoDAO

dao = VeiculoDAO()

novo_carro = VeiculoFactory.criar_veiculo('carro', "ABC1234", 120.0, Categoria.ECONOMICO)
dao.salvar(novo_carro)

lista_veiculos = dao.listar_todos()
print(f"Total de veículos cadastrados: {len(lista_veiculos)}")

for veiculo in lista_veiculos:
    print(f"Placa: {veiculo.placa}, Tipo: {veiculo.__class__.__name__}, Categoria: {veiculo.categoria.name}, Taxa Diária: {veiculo.taxa_diaria}")