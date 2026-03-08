from datetime import date, datetime, timedelta
from model.Categoria import Categoria
from model.VeiculoFactory import VeiculoFactory
from model.Locacao import Locacao


def main():    
    print("Criação via Factory:")
    carro = VeiculoFactory.criar_veiculo('carro', "ABC1234", 150.0, Categoria.ECONOMICO)
    print(f"{carro}\n")
    motorhome = VeiculoFactory.criar_veiculo('motorhome', "DEF5678", 200.0, Categoria.EXECUTIVO)
    print(f"{motorhome}\n")
    
    
    print("Cálculo com 3 dias:")
    data_inicio = date(2026, 3, 4)
    data_fim = date(2026, 3, 7)
    locacao = Locacao(carro, data_inicio, data_fim)
    valor = locacao.calcular_valor_locacao()
    print("Taxa diária: R$ 150.00")
    print("Seguro: R$ 50.00")
    print(f"Valor total: ({(data_fim - data_inicio).days} × {carro.taxa_diaria}) + {carro.valor_seguro} = R$ {valor:.2f}\n")
    
    
    print("Cálculo com devolução no mesmo dia:")
    data_inicio = date(2026, 3, 8)
    data_fim = date(2026, 3, 8)
    locacao = Locacao(motorhome, data_inicio, data_fim)
    valor = locacao.calcular_valor_locacao()
    dias = (data_fim - data_inicio).days
    dias_cobrados = 1 if dias == 0 else dias
    print(f"Valor total: ({dias_cobrados} × {motorhome.taxa_diaria}) + {motorhome.valor_seguro} = R$ {valor:.2f}\n")
       
    
    print("Tratamento de tipo inválido:")
    try:
        VeiculoFactory.criar_veiculo('moto', "ABC1234", 50.0)
    except ValueError as e:
        print(f"Exceção capturada: {e}\n")
    
    
    print("Validação de taxa diária inválida:")
    try:
        carro_invalido = VeiculoFactory.criar_veiculo('carro', "XYZ9999", -10.0, Categoria.ECONOMICO)
    except ValueError as e:
        print(f"Exceção capturada: {e}\n")
    
        
        
if __name__ == "__main__":
    main()
