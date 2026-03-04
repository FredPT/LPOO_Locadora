from datetime import datetime, timedelta
from model.Categoria import Categoria
from model.VeiculoFactory import VeiculoFactory
from model.Carro import Carro
from model.Motorhome import Motorhome
from model.Locacao import Locacao, DataInvalidaError, ExcecaoValorInvalido


def main():
    carro = VeiculoFactory.criar_veiculo('carro', placa="ABC1234", taxa_diaria=100.0, categoria=Categoria.ECONOMICO)
    motorhome = VeiculoFactory.criar_veiculo('motorhome', placa="XYZ9B99", taxa_diaria=250.0, categoria=Categoria.EXECUTIVO)
    
    print(carro)
    print(motorhome)


if __name__ == "__main__":
    main()
