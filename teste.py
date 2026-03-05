from datetime import date, datetime, timedelta
from model.Categoria import Categoria
from model.VeiculoFactory import VeiculoFactory
from model.Locacao import Locacao


def main():    
    print("1. Criação via Factory:")
    carro = VeiculoFactory.criar_veiculo('carro', "ABC1234", 150.0, Categoria.ECONOMICO)
    print(f"{carro}\n")
    
    
    print("Cálculo com 3 dias:")
    data_inicio = datetime.strptime("04-03-2026", '%d-%m-%Y').date()
    data_fim = datetime.strptime("07-03-2026", '%d-%m-%Y').date()
    locacao = Locacao(carro, data_inicio, data_fim)
    valor = locacao.calcular_valor_locacao()
    print("Taxa diária: R$ 150.00")
    print("Seguro: R$ 50.00")
    print(f"Valor total: (3 × 150) + 50 = R$ {valor:.2f}\n")
    
    
    print("Cálculo com devolução em 1 dia:")
    data_inicio = datetime.strptime("07-03-2026", '%d-%m-%Y').date()
    data_fim = datetime.strptime("08-03-2026", '%d-%m-%Y').date()
    locacao = Locacao(carro, data_inicio, data_fim)
    valor = locacao.calcular_valor_locacao()
    print(f"Valor total: (1 × 150) + 50 = R$ {valor:.2f}\n")
    

    print("Tratamento de tipo inválido:")
    try:
        VeiculoFactory.criar_veiculo('moto', "ABC1234", 50.0)
    except ValueError as e:
        print(f"Exceção capturada: {e}\n")


if __name__ == "__main__":
    main()
