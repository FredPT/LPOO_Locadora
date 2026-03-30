import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.VeiculoFactory import *
from model.Veiculo import *
from dao.db_config import DatabaseConfig
from dao.generic_dao import GenericDAO


class VeiculoDAO(GenericDAO):
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()

    def salvar(self, objeto_veiculo):
        if not self.conexao:
            raise Exception("Não foi possível conectar ao banco de dados.")
        
        try:
            cursor = self.conexao.cursor()
            query = """
                INSERT INTO tb_veiculos (vei_placa, vei_categoria, vei_taxa_diaria, vei_estado_atual, vei_tipo)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(query, (
                objeto_veiculo.placa,
                objeto_veiculo.categoria.value,
                objeto_veiculo.taxa_diaria,
                objeto_veiculo.estado_atual.__class__.__name__,
                objeto_veiculo.__class__.__name__
            ))
            self.conexao.commit()
            return True, "Veículo cadastrado com sucesso!"

        except Exception as e:
            print(f"Erro ao inserir o veiculo: {objeto_veiculo.placa}: {e}")
            self.conexao.rollback()
            return False, "Erro ao cadastrar veículo!"
        
        finally:
            if cursor:
                cursor.close()
            
    def listar_todos(self):
        if not self.conexao:
            return []
        
        try:
            cursor = self.conexao.cursor()
            query = "SELECT vei_tipo, vei_placa, vei_taxa_diaria, vei_categoria FROM tb_veiculos"
            cursor.execute(query)
            linhas = cursor.fetchall()
            veiculos = []
            for linha in linhas:
                obj = VeiculoFactory.criar_veiculo(linha[0], linha[1], float(linha[2]), linha[3])
                veiculos.append(obj)

            return veiculos
        except Exception as e:
            print(f"Erro ao listar veículos: {e}")
            return []
        finally:
            if cursor:
                cursor.close()


    def remover(self, id_objeto):
        pass

    def atualizar(self, objeto):
        pass

