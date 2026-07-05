import socket
import threading
from queue import Queue

print('-' * 30)
target = input(str('Enter target IP: '))
queue = Queue()
open_ports = []

def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((target, port))

        if result == 0:
            open_ports.append(port)
            try:
                banner = s.recv(1024).decode().strip()
                if banner:
                    print(f'[+] Port {port} is OPEN | Service: {banner}')
            except:
                print(f'[+] Port {port} is OPEN')
        s.close()
    except:
        pass


def worker():
    while not queue.empty():
        port = queue.get()
        scan_port(port)
        queue.task_done()

for port in range(1, 1025):
    queue.put(port)

for _ in range(100):
    t = threading.Thread(target=worker)
    t.start()


queue.join()

print('-' * 30)
print('Scan finished.')
