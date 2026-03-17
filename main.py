import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor


def print_logo():
    logo = r"""
                 _         ____
               /' \       /\  _`\
      ___ ___ /\_, \  _ __\ \ \L\ \
    /' __` __`\/_/\ \/\`'__\ \ ,  /
    /\ \/\ \/\ \ \ \ \ \ \/ \ \ \\ \   __
    \ \_\ \_\ \_\ \ \_\ \_\  \ \_\ \_\/\_\
     \/_/\/_/\/_/  \/_/\/_/   \/_/\/ /\/_/

    """

    for char in logo:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)


def scan_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        result = sock.connect_ex((host, port))
        if result == 0:
            return port
    return None


print_logo()
target = input("\n[TARGET] Enter target host: ")
port_to_scan = range(1, 1025)
print(f"[INFO] Scanning {target}...")

with ThreadPoolExecutor(max_workers=100) as executor:
    result = executor.map(lambda p: scan_port(target, p), port_to_scan)

for port in result:
    if port:
        print(f"[INFO] Port {port} is open")
