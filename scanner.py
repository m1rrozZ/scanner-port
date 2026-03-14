import socket

def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)

    try:
        result = s.connect_ex((ip, port))
        if result == 0:
            print(f'Port {port} is OPEN')
        s.close()
    except:
        pass


target = 'google.com'
print(f'Scanning target: {target}')

for port in range(1, 1025):
    scan_port(target, port)

print('Scan finished.')
