from .Veiculo import Veiculo
from .Categoria import Categoria


class Carro(Veiculo):    
    def __init__(self, placa: str, taxa_diaria: float, categoria: Categoria = Categoria.ECONOMICO):
        super().__init__(placa, taxa_diaria, categoria=categoria)
        self.__valor_seguro = 50.0
    
    @property
    def valor_seguro(self):
        return self.__valor_seguro
    
    def calcular_diaria(self):
        return self.taxa_diaria
    
    def __str__(self):
        return f"Carro: {self.placa} - Categoria: {self.categoria.value} - Seguro: R$ {self.valor_seguro:.2f}"
