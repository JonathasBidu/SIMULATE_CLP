import json
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt

"""
    Este teste tem a finalidade de demostrar de qual maneira se tem acesso aos despachos otimizados e as projeções iniciais da VPP do arquivo dispatch_data.json.
    
    Projeções iniciais (ativos não despacháveis, não há controle sobre esses dispositivos):
        - Nt: Representa o período da simulação
        - Nbm: Quantidade de usinas de geração a biomassa
        - Nbat: Quantidade de Armazenadores
        - Npv: Quantidade de Usinas fotvoltaicas
        - Nwt: Quantidade de Usinas eólicas
        - Nl: Quantidade de cargas não controláveis
        - Ndl: Quantidade de cargas controláveis
        - p_bm_min: potência mínima a ser gerada pela uisna i, quando a mesma está ligada, dimensão p_bm_min(Nbm,)
        - p_bm_min: potência máxima a ser gerada pela uisna i, quando a mesma está ligada, dimensão p_bm_max(Nbm,)
        - p_bm_rup: potência de ramp up da uisna i, dimensão p_bm_rup(Nbm)
        - p_bm_rdown: potência de ramp up da uisna i, dimensão p_bm_rup(Nbm)
        - kappa_bm: custo operacional da usina i de biomassa
        - kappa_bm_start: custo de inicial da usina i de biomassa
        - kappa_pv: custo operacional da usina i de geração solar
        - kappa_wt: custo operacional da usina i de geração eólica
        - kappa_bat: custo operacional das baterias
        - eta_chg: eficiência de carregamento da bateria i, dimensão eta_chg(Nbat)
        - eta_dch: eficiência de descarregamento da bateria i, dimensão eta_dch(Nbat)
        - soc_min: nível mínimo da bateria i, dimensão soc_min(Nbat)
        - soc_max: nível máximo da bateria i, dimensão soc_min(Nbat)
        - p_bat_max: potência máxima de armazenamento da bateria i, dimensão p_bat_max(Nbat)
        - p_pv: potência de geração solar, dimensão p_pv(Npv, Nt)
        - p_pv: potência de geração eólica, dimensão p_pv(Nwt, Nt)
        - p_l: potência de carga não controlável, dimensão p_l(Nl, Nt)
        - p_dl_ref: potência de referência para o corte de carga, dimensão p_dl_ref(Ndl, Nt)
        - p_dl_max: potência máxima de corte de carga, dimensão p_dl_max(Ndl, Nt)
        - p_dl_min: potência mínima de corte de carga, dimensão p_dl_min(Ndl, Nt)
        - tau_pld: tarifa de preço de liquidação de diferenças
        - tau_dist: tarifa de preço da distribuidora de energia
        - tau_dl: tarifa de compensação pelo corte de carga
    
    Despachos otimizados (ativos despacháveis, ou seja, controláveis):
        - p_bm: despacho otimizado das usinas de geração a biomassa, dimensão p_bm(Nbm, Nt)
        - p_chg: despacho otimizado de carregamento das baterias, dimensão p_chg(Nbat, Nt)
        - p_dch: despacho otimizado de descarregamento das baterias, dimensão p_dch(Nbat, Nt)
        - soc: despacho otimizado do nível de carga dos armazenadores, dimensão soc(Nbat, Nt)
        - p_dl: despacho otimizado das cargas despacháveis
        - u_bm: despacho otimizado dos estados das usinas de geração a biomassa,onde (0=desligado, 1=ligado), dimensão u_bm(Nbm, Nt)
        - u_chg: despacho otimizado dos estados de carregamento dos armazenadores,onde (0=desligado, 1=ligado), dimensão u_chg(Nbat, Nt)
        - u_dch: despacho otimizado dos estados de descarregamento dos armazenadores,onde (0=desligado, 1=ligado), dimensão u_dch(Nbat, Nt)
        - u_dl: despacho otimizado dos estados do corte de carga despachável,onde (0=desligado, 1=ligado), dimensão u_dl(Ndl, Nt)

"""

path = Path(__file__).parent / "dispatch_data.json" # Caminho para o arquivo dispacth_data.json

with open(path, 'r') as arq:
    data = json.load(arq) # atribuição do dicionário dispacth_data a variável data

# Vizualizando as chaves dentro do dicionário data
print(data.keys())

# Obtendo o período simulado
Nt = data['Nt']

# Obtendo as potências das usinas de geração a biomassa
p_bm = np.array(data['p_bm']) # np.array para transforma a lista em matriz, p_bm(Nbm=3, Nt=24)
# Obtendo os estados das usinas de geração a biomassa
u_bm = np.array(data['u_bm']) # np.array para transforma a lista em matriz, u_bm()

# Vizualizando os dados em um print
print(f'\n shape{p_bm.shape}\np_bm == {p_bm}')
print(f'\n shape{u_bm.shape}\nu_bm == {u_bm}')

# Criando um vetor de 0 até Nt, para usar na plotagem
t = np.arange(Nt)

# Plotando um gráfico das usinas de geração a biomassa
plt.figure(figsize = (10, 4))
plt.stackplot(t, p_bm[0, :])
plt.stackplot(t, p_bm[1, :])
plt.stackplot(t, p_bm[2, :])
plt.show()

