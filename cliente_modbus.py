from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils

class VPPClientModBus():

    def __init__(self, host = 'localhost', port = 502):

        self._client = ModbusClient(host = host, port = port)

    def run(self):
        if not self._client.is_open:
            if self._client.open():
                print("Conectado ao servidor MODBUS\n")
            else:
                print("Erro: Falha ao conectar ao servidor MODBUS")

    def disconnect(self):
        if self._client.is_open:
            self._client.close()
            print("\nConexão encerrada\n")

    def write_coil(self, adrr: int, value: int):
        if self._client.is_open:
            return self._client.write_single_coil(adrr, value)
        else:
            print("Primeiro é preciso se conectar")
            return False
    
    def write_float_register(self, addr, value):
        """Escreve um número float (32 bits IEEE 754) em dois registradores consecutivos"""
        if self._client.is_open:
            ieee_32 = utils.encode_ieee(value)  # float -> 32-bit int
            reg1 = (ieee_32 >> 16) & 0xFFFF
            reg2 = ieee_32 & 0xFFFF
            return self._client.write_multiple_registers(addr, [reg1, reg2])
        else:
            print("Primeiro é preciso se conectar")
            return False

    def read_float_register(self, addr):
        """Lê dois registradores consecutivos e converte para float (32 bits IEEE 754)"""
        if self._client.is_open:
            regs = self._client.read_holding_registers(addr, 2)
            if regs and len(regs) == 2:
                ieee_32 = (regs[0] << 16) + regs[1]
                return utils.decode_ieee(ieee_32)
            else:
                print("Erro ao ler registradores")
                return None
        else:
            print("Primeiro é preciso se conectar")
            return None
        
    def read_coil(self, adrr: int):
        if self._client.is_open:
            return self._client.read_coils(adrr, 1)
        else:
            print("Primeiro é preciso se conectar")
            return None        

if __name__ == '__main__':

    from threading import Thread
    from servidor_modbus import CLPServidorModBus
    from pathlib import Path
    from time import sleep
    import numpy as np
    import json

    path = Path(__file__).parent / "dispatch_data.json"

    with open(path, 'r') as arq:
        data = json.load(arq)

    Nt = data['Nt']
    Nbm = data['Nbm']
    u_bm = np.array(data['u_bm'])

    cliente = VPPClientModBus(host = 'localhost', port = 502)
    servidor = CLPServidorModBus(host = 'localhost', port = 502, temp = 1)

    thread_servidor = Thread(target = servidor.run, daemon = True)

    thread_servidor.start()
    sleep(1)
    cliente.run()

    base_adrr = 1000

    for t in range(Nt):
        for i in range(Nbm):

            cliente.write_coil(1000 + i, u_bm[i, t])
            value = cliente.read_coil(1000 + i)
            print(f't = {t}, usina {i}, coil [{1000 + i}] = {value}')

    cliente.disconnect()
    servidor.disconect()
    