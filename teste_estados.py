from model.Categoria import Categoria
from model.VeiculoFactory import VeiculoFactory
print("\n--- TESTANDO O PADRÃO STATE RESTRITIVO ---")
carro_estado = VeiculoFactory.criar_veiculo("carro", "HJI3K45", taxa_diaria=15.0, categoria=Categoria.ECONOMICO)

# 1. Tentar alugar um carro de frota normal
carro_estado.tentar_alugar() # OK - Transitará

# 2. Tentar locar novamente para outro!
carro_estado.tentar_alugar() # Erro Interativo ("Já está alugado!")

# 3. Tentar mandar pra manutenção com cleinte
carro_estado.reter_na_frota_pra_conserto() # Bloqueado

# 4. Devolver 
carro_estado.tentar_devolver() # Ok (Retorna)

# 5. Colocar em checkups da empresa
carro_estado.reter_na_frota_pra_conserto() # Ok 
carro_estado.tentar_alugar() # Falha! Está em Manutenção.