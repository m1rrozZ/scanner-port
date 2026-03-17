import argparse
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
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            if sock.connect_ex((host, port)) == 0:
                try:
                    service = socket.getservbyport(port, "tcp")
                except:
                    service = "uknown"
                return port, service
    except:
        pass
    return None, None


def get_args():
    parser = argparse.ArgumentParser(description="Port scanner")
    parser.add_argument("target", help="Target host")
    parser.add_argument(
        "-p", "--ports", default="1-1024", help="Port range (ex: 1-1000)"
    )
    parser.add_argument(
        "-t", "--threads", default=100, type=int, help="Number of threads to use"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    print_logo()

    try:
        start_port, end_port = map(int, args.ports.split("-"))
        port_to_scan = range(start_port, end_port + 1)
    except ValueError:
        print("[ERROR] Invalid port range")
        sys.exit(1)

    print(f"\n[INFO] Scanning ports {start_port}-{end_port} on {args.target}")
    print(f"[INFO] Using {len(port_to_scan)} threads\n")
    print("-" * 30)

    found_any = False

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        # result
        results = executor.map(lambda p: scan_port(args.target, p), port_to_scan)

        for port, service in results:
            if port:
                print(f"[INFO] Port: {port} | Service: ({service})")
                found_any = True
    if not found_any:
        print("\n[INFO] No open ports found")

    print("\n[INFO] Scan complete")
