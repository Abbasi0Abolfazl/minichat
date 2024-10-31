from multiprocessing.connection import Listener, Client
from multiprocessing import AuthenticationError
import threading
import time
import sys
import os

class MiniChat:
    def __init__(self, host_and_port, nickname, auth_key):
        self.chat_log = []
        self.host, self.port = host_and_port.split(':')
        self.port = int(self.port)
        self.nickname = nickname
        self.auth_key = auth_key
        self.running = True
        self.connection = None
        self.listener = None
        self.clear_console()

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def stop(self):
        self.running = False
        if self.connection:
            self.connection.close()

    def add_message(self, message):
        self.chat_log.append(message)
        self.clear_console()
        print('\n'.join(self.chat_log))

    def run_host(self):
        self._run_threaded(self._run_host_forever)

    def run_client(self):
        self._run_threaded(self._run_client_forever)

    def _run_threaded(self, target):
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
        self.handle_inputs()

    def _run_host_forever(self):
        self.add_message(f'Chat server running on port {self.port}')
        self.listener = Listener((self.host, self.port), authkey=self.auth_key.encode())
        while self.running:
            try:
                self.connection = self.listener.accept()
                self.add_message('Client has connected.')
                self.handle_messages()
            except (IOError, EOFError):
                if self.running:
                    self.add_message('Client has disconnected.')
            except AuthenticationError:
                self.add_message('Client tried to connect with wrong password.')
        self.listener.close()

    def _run_client_forever(self):
        self.add_message(f'Connecting to chat server {self.host} on port {self.port}')
        while self.running:
            try:
                self.connection = Client((self.host, self.port), authkey=self.auth_key.encode())
                self.add_message('Connected to host.')
                self.handle_messages()
            except (IOError, EOFError):
                if self.running:
                    self.add_message('Host has disconnected. Retrying in 5 seconds...')
                    time.sleep(5)
            except AuthenticationError:
                self.add_message('Wrong password.')
                self.stop()

    def handle_messages(self):
        while self.running:
            try:
                message = self.connection.recv()
                self.add_message(message)
            except (EOFError, ConnectionResetError):
                print('Host has disconnected.')
                self.stop()
                break
        self.connection.close()

    def handle_inputs(self):
        while self.running:
            while self.running and not self.connection:
                time.sleep(0.2)
            if self.connection:
                text = input(f"{self.nickname} >> ")
                if text.strip():  
                    message = f"{self.nickname}: {text}"  
                    self.add_message(message)  
                    self.connection.send(message)  


                    
if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('usage server: python minichat.py -host host:port nickname password \nusage client: python minichat.py -connect host:port nickname password\nCTRL+C to exit.')
    else:
        try:
            chat = MiniChat(host_and_port=sys.argv[2], nickname=sys.argv[3], auth_key=sys.argv[4])
            if sys.argv[1] == '-host':
                chat.run_host()
            elif sys.argv[1] == '-connect':
                chat.run_client()
        except KeyboardInterrupt:
            chat.stop()
            print('Chat ended.')
        except ValueError as e:
            print('Invalid argument: ' + str(e))

