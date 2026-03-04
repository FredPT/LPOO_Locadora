from .Veiculo import Veiculo
from .Categoria import Categoria


class Motorhome(Veiculo):
    def __init__(self, placa, taxa_diaria, categoria: Categoria = Categoria.ECONOMICO):
        super().__init__(placa, taxa_diaria, categoria)
        self._valor_seguro = 120.0
    
    @property
    def valor_seguro(self):
        return self._valor_seguro
    
    def calcular_diaria(self):
        return self.taxa_diaria
    
    def __str__(self):
        return f"Motorhome: {self.placa} - Categoria: {self.categoria.value} - Seguro: R$ {self.valor_seguro:.2f}"
