from .Carro import Carro
from .Motorhome import Motorhome
from .Categoria import Categoria


class VeiculoFactory:
    @staticmethod
    def criar_veiculo(tipo: str, placa: str, taxa_diaria: float, categoria: Categoria = Categoria.ECONOMICO):
        tipos = {
            'carro': Carro,
            'motorhome': Motorhome
        }
        
        tipo_lower = tipo.lower()
        if tipo_lower not in tipos:
            raise ValueError(f"Tipo de veículo inválido: {tipo}. Use 'carro' ou 'motorhome'")
        
        return tipos[tipo_lower](placa, taxa_diaria, categoria)
