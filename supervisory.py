from servidor_modbus import CLPServidorModBus
from cliente_modbus import VPPClientModBus
from kivy.lang import Builder
from kivy.clock import Clock
from threading import Thread
from kivy.app import App
from pathlib import Path
from time import sleep
import numpy as np
import json

class Supervisory(App): 

    def build(self):
        path = Path(__file__).parent / 'dispatch_data.json'

        with open(path, 'r') as arq:
            data = json.load(arq)          

        self.Nt = data['Nt']
        self.Nbm = data['Nbm']
        self.u_bm = np.array(data['u_bm'])
        self.p_bm = np.array(data['p_bm'])

        self.root = Builder.load_file("supervisory.kv")
        self.client = VPPClientModBus(host = 'localhost', port = 502)
        self.server = CLPServidorModBus(host = 'localhost', port = 502, temp = 1)
        self.base_adrr = 1000
        self.t_atual = 0

        thread_server = Thread(target = self.server.run, daemon = True).start()
        thread_client = Thread(target = self.client.run, daemon = True).start()

        while not self.client._client.is_open:
            print("Aguardando conexão")
            sleep(0.5)

        Clock.schedule_interval(self.update_status, 1)

        return self.root
    
    # Método para atualizar hora atual
    def formatar_temp(self, t):
        horas = t % 24
        return f"{horas:02d}:00"

    # Método para atualizar a imagem de acordo com o estado atual da usina
    def update_status(self, dt):
        try:
            if self.t_atual >= self.Nt:
                self.t_atual = 0

            for i in range(self.Nbm):               
                self.client.write_coil(self.base_adrr + i, self.u_bm[i, self.t_atual])

                is_conect = self.client.read_coil(self.base_adrr + i)
                if is_conect is not None:
                    is_conect = is_conect[0]
                else:
                    is_conect = False                
                image_path = "IMGs/conectado.png" if is_conect else "IMGs/desconectado.png"

                if i == 0:
                    self.root.ids['conexão_1'].source = image_path
                elif i == 1:
                    self.root.ids['conexão_2'].source = image_path
                elif i == 2:
                    self.root.ids['conexão_3'].source = image_path

            self.t_atual += 1
            self.root.ids.relogio.text = self.formatar_temp(self.t_atual)
    
        except Exception as e:
            print(f'[Erro Update_status] {e}')


if __name__ == '__main__':

    Supervisory().run()


