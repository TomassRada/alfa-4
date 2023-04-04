import socket
import threading
import queue
import datetime
import yaml
import os
from loging import log
from translate import translate_local, translate_scan


class Server:
    def __init__(self):
        # path
        cwd = os.getcwd()
        self.log_path = os.path.join(os.path.dirname(cwd), 'log', 'log.txt')
        conf_path = os.path.join(os.path.dirname(cwd), 'config', 'config.yml')

        # config
        with open(conf_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Adresy a porty v síti, na kterých mohou být další slovníkové programy
        self.start_ip = self.config['start_ip']
        self.end_ip = self.config['end_ip']
        self.start_port = self.config['start_port']
        self.end_port = self.config['end_port']

        # client queue
        self.client_queue = queue.Queue()

    def handle_client(self, clientsocket):
        """Obsluha jednoho klienta"""
        request = ""

        while True:
            data = clientsocket.recv(1024)
            if not data:
                break

            request += data.decode('utf-8')

            if request.endswith("\n"):
                request = request.rstrip("\n")
                response = self.handle_request(request)
                clientsocket.sendall(response.encode('utf-8'))
                request = ""

        clientsocket.close()

    def handle_connections(self):
        """Obsluha fronty připojení"""
        while True:
            clientsocket, request = self.client_queue.get()

            response = self.handle_request(request)
            clientsocket.sendall(response.encode('utf-8'))

            self.client_queue.task_done()

    def handle_request(self, request):
        """Zpracování jednotlivých požadavků na překlad"""
        lines = request.strip().split("\n")
        response = ""
        for line in lines:
            parts = line.strip().split('"')
            if parts[0] == "TRANSLATEPING":
                response += 'TRANSLATEPONG"Tomuv slovnikovy program"\n'
            elif parts[0] == "TRANSLATELOCL":
                word = parts[1].strip('"')
                response += translate_local(word) + "\n"
            elif parts[0] == "TRANSLATESCAN":
                word = parts[1].strip('"')
                response += translate_scan(word,self.start_ip, self.end_ip, self.start_port, self.end_port)[0] + "\n"
            else:
                response += 'INVALID COMMAND "' + line + '"\n'

        log(f"REQUEST: {request}, RESPONSE: {response}", path=self.log_path)
        return response


    def run_server(self):
        """Spustí server na ip a portu z konfiguračního souboru"""
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        host = self.config['host']
        port = self.config['port']

        serversocket.bind((host, port))

        serversocket.listen(5)

        print("Server is listening on host %s and port %d" % (host, port))

        while True:
            clientsocket, addr = serversocket.accept()
            print("Got a connection from %s" % str(addr))

            clientthread = threading.Thread(target=self.handle_client, args=(clientsocket,))
            clientthread.start()


if __name__ == '__main__':
    server = Server()
    server_thread = threading.Thread(target=server.handle_connections)
    server_thread.start()
    server.run_server()