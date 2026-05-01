from dao.veiculo_dao import VeiculoDAO
from model.VeiculoFactory import VeiculoFactory
from model.Categoria import Categoria


class VeiculoController:
    def __init__(self):
        self.veiculo_dao = VeiculoDAO()

    def salvar_veiculo(self, placa: str, tipo_str: str, categoria_str: str, taxa_diaria_str: str):
        if not placa or not tipo_str or not categoria_str or not taxa_diaria_str:
            return False, "Todos os campos são obrigatórios."
        
        try:
            taxa_num = float(taxa_diaria_str.replace(',', '.'))
            if taxa_num <= 0:
                return False, "A taxa diária deve ser um valor positivo."
            
            veiculo_existente = self.veiculo_dao.buscar_por_placa(placa)
            if veiculo_existente:
                return False, "Veículo com esta placa já está cadastrado."
            
            categoria_enum = Categoria[categoria_str.upper()]
            novo_veiculo = VeiculoFactory.criar_veiculo(tipo_str.strip().lower(), placa.upper(), taxa_num, categoria_enum)
            sucesso, msg = self.veiculo_dao.salvar(novo_veiculo)
            return sucesso, msg
        
        except KeyError:
            return False, "Categoria inválida."
        except ValueError as e2:
            return False, f"Formato de taxa inválido. Erro: {e2}"
        except Exception as e3:
            return False, f"Erro ao salvar veículo: {e3}"

    def listar_veiculos(self):
        try:
            return self.veiculo_dao.listar_todos()
        except Exception as e:
            print(f"Erro ao listar veículos: {e}")
            return None

    def buscar_por_placa(self, placa: str):
        try:
            return self.veiculo_dao.buscar_por_placa(placa.strip().upper())
        except Exception as e:
            print(f"Erro ao buscar veículo por placa: {e}")
            return None

    def atualizar_veiculo(self, placa: str, tipo_str: str, categoria_str: str, taxa_diaria_str: str):
        if not placa or not tipo_str or not categoria_str or not taxa_diaria_str:
            return False, "Todos os campos são obrigatórios."

        try:
            taxa_num = float(taxa_diaria_str.replace(',', '.'))
            if taxa_num <= 0:
                return False, "A taxa diária deve ser um valor positivo."

            veiculo_existente = self.veiculo_dao.buscar_por_placa(placa)
            if not veiculo_existente:
                return False, "Veículo não encontrado para edição."

            categoria_enum = Categoria[categoria_str.upper()]
            veiculo_atualizado = VeiculoFactory.criar_veiculo(tipo_str.strip().lower(), placa.upper(), taxa_num, categoria_enum)
            sucesso, msg = self.veiculo_dao.atualizar(veiculo_atualizado)
            return sucesso, msg
        except KeyError:
            return False, "Categoria inválida."
        except ValueError as e:
            return False, f"Formato de taxa inválido. Erro: {e}"
        except Exception as e:
            return False, f"Erro ao atualizar veículo: {e}"

    def remover_veiculo(self, placa: str):
        if not placa:
            return False, "Placa inválida para remoção."

        try:
            sucesso, msg = self.veiculo_dao.remover(placa)
            return sucesso, msg
        except Exception as e:
            print(f"Erro ao remover veículo: {e}")
            return False, "Erro ao remover veículo."

