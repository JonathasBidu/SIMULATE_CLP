# from servidor_modbus import CLPServidorModBus
# from cliente_modbus import VPPClientModBus
# from threading import Thread
# from pathlib import Path
# from time import sleep
# import numpy as np
# import json

# # Diretório dos despachos otimizados
# path = Path(__file__).parent / "dispatch_data.json"

# with open(path, 'r') as arq:
#     data = json.load(arq)

# Nt = data['Nt']        # Período da simulação, geralmente 24 horas.
# Nbm = data['Nbm']      # Quantidade de usinas termelétricas a biomassa (UTBMs).
# u_bm = np.array(data['u_bm'])  # Estados das UTBMs
# p_bm = np.array(data['p_bm'])  # Potências das UTBMs

# if __name__ == "__main__":

#     servidor = CLPServidorModBus(host='localhost', port=502, temp=1)
#     cliente = VPPClientModBus(host='localhost', port=502)

#     thread_servidor = Thread(target=servidor.run, daemon=True)
#     thread_servidor.start()

#     thread_cliente = Thread(target=cliente.run, daemon=True)
#     thread_cliente.start()

#     sleep(2)  # Aguarda threads iniciarem

#     based_adrr = 1000

#     # Aguarda até cliente estar conectado
#     while not cliente._client.is_open:
#         print("Aguardando conexão")
#         sleep(0.5)

#     sleep(1)

#     for t in range(Nt):
#         for i in range(Nbm):
#             cliente.write_coil(based_adrr + i, u_bm[i, t])
#             estado = cliente.read_coil(based_adrr + i)
#             print(f"UTBM {i}, Tempo {t}: Estado = {estado}")
#         sleep(1)  # Simula tempo real (1s por hora de simulação)

#     cliente.disconnect()
#     servidor.disconnect()

from servidor_modbus import CLPServidorModBus
from cliente_modbus import VPPClientModBus
from threading import Thread
from pathlib import Path
from time import sleep
import numpy as np
import json
from interface import SupervisoryApp

def iniciar_simulacao(cliente, based_adrr, u_bm, Nt, Nbm):
    """
    Simula a mudança de estado das UTBMs ao longo do tempo.
    """
    for t in range(Nt):
        for i in range(Nbm):
            cliente.write_coil(based_adrr + i, u_bm[i, t])
            estado = cliente.read_coil(based_adrr + i)
            print(f"UTBM {i}, Tempo {t}: Estado = {estado}")
        sleep(1)

if __name__ == "__main__":
    # === Carrega dados simulados ===
    path = Path(__file__).parent / "dispatch_data.json"
    with open(path, 'r') as arq:
        data = json.load(arq)

    Nt = data['Nt']
    Nbm = data['Nbm']
    u_bm = np.array(data['u_bm'])
    p_bm = np.array(data['p_bm'])

    based_adrr = 1000

    # === Inicia servidor Modbus ===
    servidor = CLPServidorModBus(host='localhost', port=502, temp=1)
    thread_servidor = Thread(target=servidor.run, daemon=True)
    thread_servidor.start()

    # === Inicia cliente que alimenta bobinas ===
    cliente = VPPClientModBus(host='localhost', port=502)
    thread_cliente = Thread(target=cliente.run, daemon=True)
    thread_cliente.start()

    # Aguarda conexão
    sleep(2)
    while not cliente._client.is_open:
        print("Aguardando conexão...")
        sleep(0.5)

    # Inicia thread de simulação
    thread_simulacao = Thread(
        target=iniciar_simulacao,
        args=(cliente, based_adrr, u_bm, Nt, Nbm),
        daemon=True
    )
    thread_simulacao.start()

    # === Inicia interface gráfica ===
    SupervisoryApp().run()

    # === Cleanup após fechar interface ===
    cliente.disconnect()
    servidor.disconnect()
