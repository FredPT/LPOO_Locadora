from model.Decoradores import GPSDecorator, SeguroTerceirosDecorator
from model.Locacao import Locacao
from model.Veiculo import Veiculo
from model.Categoria import Categoria
from model.VeiculoFactory import VeiculoFactory
from datetime import date
# ... restantes das suas importações


print("Criação via Factory:")
carro = VeiculoFactory.criar_veiculo('carro', "ABC1234", 150.0, Categoria.ECONOMICO)
    
print("\n--- TESTANDO O PADRÃO DECORATOR ---")
# 1. Base simples
locacao_base = Locacao(veiculo=carro, data_inicio=date(2026, 3, 1), data_fim=date(2026, 3, 5))
print(f"Valor Base (somente Diária + Seguro Base): R$ {locacao_base.calcular_valor_locacao()}")

# 2. Base + GPS
locacao_com_gps = GPSDecorator(locacao_base)
print(f"Valor somado do pacote + GPS: R$ {locacao_com_gps.calcular_valor_locacao()}")

# 3. Empurrar SeguroTerceiros Por Cima De Tudo (Envelopamento)
locacao_vip_top = SeguroTerceirosDecorator(locacao_com_gps)
print(f"Valor pacote completão (Base + GPS + Seg.Terceiros): R$ {locacao_vip_top.calcular_valor_locacao()}")
