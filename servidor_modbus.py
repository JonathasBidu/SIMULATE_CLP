from pyModbusTCP.server import ModbusServer
import random
from time import sleep

"""
    Este script tem a finalidade de simular um CLP como servidor Modbus TCP/IP...
    Obs: Testar no cmd se a porta 502 está em uso com o seguinte comando:
    (netstat -ano | findstr :502).
"""

class CLPServidorModBus():

    def __init__(self, host = 'localhost', port = 502, temp = 1):

        '''Atributos da classe'''
        self._server = ModbusServer(host = host, port = port, no_block = True)
        self._host = host
        self._port = port
        self._temp = temp
        

    def run(self):

        try:
            self._server.start()
            print(f'Servidor VPP ModBus iniciado {self._host}:{self._port}\n')

            while True:
                sleep(self._temp)

        except KeyboardInterrupt:
            print("\nEncerrando o Servidor")

        except Exception as e:
            print("Erro: ", e.args)

        finally:
            self._server.stop()
            print('Servidor ModBus encerrado com sucesso\n')

    def disconnect(self):
        self._server.stop()
        print(f'Servidor desligado\n')

if __name__ == '__main__':

    s = CLPServidorModBus(host = 'localhost', port = 502, temp = 1)
    s.run()