from abc import ABC, abstractmethod
from .Categoria import Categoria
from .ExcecoesPersonalizadas import PlacaInvalidaError, DataInvalidaError

class Veiculo(ABC):
    def __init__(self, placa: str, taxa_diaria: float, categoria: Categoria = Categoria.ECONOMICO):
        self.placa = placa
        self.categoria = categoria
        self.taxa_diaria = taxa_diaria
    
    @property
    def placa(self):
        return self.__placa
    
    @placa.setter
    def placa(self, valor):
        if self.validar_placa(valor):
            self.__placa = valor
    
    @property
    def taxa_diaria(self):
        return self.__taxa_diaria
    
    @taxa_diaria.setter
    def taxa_diaria(self, valor):
        self.__taxa_diaria = valor

    def validar_placa(self, placa):
        placa = placa.strip().replace("-", "").upper()
        if (len(placa) != 7):
            raise PlacaInvalidaError("Placa inválida: deve conter exatamente 7 caracteres.")
        else:
            if not placa[0:3].isalpha():
                raise PlacaInvalidaError("Placa inválida: os três primeiros caracteres devem ser letras.")
            if not placa[3].isdigit() or not placa[5:7].isdigit():
                raise PlacaInvalidaError("Placa inválida: os caracteres 4, 6 e 7 devem ser números.")
            elif not placa[4].isalnum():
                raise PlacaInvalidaError("Placa inválida: o caractere 5 deve ser uma letra ou um número.")
            else:    
                print(f"Placa '{placa}' válida.")
                return True 
    
    @property
    def categoria(self):
        return self.__categoria
    
    @categoria.setter
    def categoria(self, valor):
        self.__categoria = valor
    
    @abstractmethod
    def calcular_diaria(self):
        pass
    
    def __str__(self):
        return f"Veículo: {self.placa} - Categoria: {self.categoria.value} - Taxa: R$ {self.taxa_diaria:.2f}"
