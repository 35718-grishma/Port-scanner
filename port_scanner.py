import socket
import threading
import argparse
from datetime import datetime

# List to store open ports
open_ports = []

# Lock for thread safety
lock = threading.Lock()


def scan_port(target, port):
    """
    Attempts to connect to a specific port on the target IP.
    If connection is successful, port is considered open.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((target, port))

        if result == 0:
            with lock:
                open_ports.append(port)

        sock.close()

    except socket.error:
        pass


def start_scan(target, start_port, end_port):
    """
    Starts multi-threaded scanning over given port range.
    """
    threads = []

    print("\n[+] Starting scan on target:", target)
    print("[+] Scanning ports from", start_port, "to", end_port)

    start_time = datetime.now()

    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(target, port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = datetime.now()
    duration = end_time - start_time

    print("\n[+] Scan Completed!")
    print("[+] Open Ports:")

    if open_ports:
        for port in sorted(open_ports):
            print("    Port", port, "is OPEN")
    else:
        print("    No open ports found.")

    print("\n[+] Scan Duration:", duration)


def main():
    parser = argparse.ArgumentParser(description="Multi-threaded Port Scanner Tool")

    parser.add_argument("target", help="Target IP address")
    parser.add_argument("start_port", type=int, help="Starting port number")
    parser.add_argument("end_port", type=int, help="Ending port number")

    args = parser.parse_args()

    start_scan(args.target, args.start_port, args.end_port)


if __name__ == "__main__":
    main()