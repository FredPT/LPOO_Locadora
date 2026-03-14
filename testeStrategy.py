from datetime import date
from model.Veiculo import Veiculo
from model.Locacao import Locacao, DataInvalidaError, ExcecaoValorInvalido
from model.LocacaoStrategy import CalculoPadraoStrategy, CalculoVIPStrategy
from model.VeiculoFactory import VeiculoFactory
from model.Categoria import Categoria

carro = VeiculoFactory.criar_veiculo('carro', "ABC1234", 200.0, Categoria.ECONOMICO)
locacao_strategy = CalculoPadraoStrategy()
valor = locacao_strategy.calcular_diarias(carro, 3)
print(f"Valor total para 3 dias: R$ {valor:.2f}")

locacao_strategy_vip = CalculoVIPStrategy()
valor_vip = locacao_strategy_vip.calcular_diarias(carro, 3)
print(f"Valor total para 3 dias (VIP): R$ {valor_vip:.2f}")


data_inicio = date(2026, 3, 4)
data_fim = date(2026, 3, 7)
locacao = Locacao(carro, data_inicio, data_fim, estrategia=CalculoVIPStrategy())
valor_locacao = locacao.calcular_valor_locacao()
print(f"Valor total da locação (VIP): R$ {valor_locacao:.2f}")



