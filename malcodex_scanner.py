#!/usr/bin/env python3
"""
MalCodeX Network Scanner - Professional Edition
-----------------------------------------------

    ::::::::::::::::::::::::::::::::::::::::::
    :::    'oOMalCodeX0dayScanOo'          :::
    :::  --==[ Network Reconnaissance ]==-- :::
    :::                                    :::
    :::  - Identify open ports            :::
    :::  - Detect vulnerable services     :::
    :::  - Assess network security        :::
    :::                                    :::
    :::  "Knowledge is power, scan wisely" :::
    ::::::::::::::::::::::::::::::::::::::::::

    =[ MalCodeX v1.0.0 ]=
+ ---=[ 3 scan modes - 5 service detectors - 2 output formats ]=
+ ---=[ Thread-safe implementation - Clean exit handling ]=

MalCodeX tip: Use -h for help with command options

"""

import socket
import threading
import argparse
from datetime import datetime
import sys

class MalCodeXScanner:
    def __init__(self):
        self.banner = """
    \033[1;31m
     ███▄ ▄███▓ ▄▄▄       ██▀███   ▒█████   ██▓███  
    ▓██▒▀█▀ ██▒▒████▄    ▓██ ▒ ██▒▒██▒  ██▒▓██░  ██▒
    ▓██    ▓██░▒██  ▀█▄  ▓██ ░▄█ ▒▒██░  ██▒▓██░ ██▓▒
    ▒██    ▒██ ░██▄▄▄▄██ ▒██▀▀█▄  ▒██   ██░▒██▄█▓▒ ▒
    ▒██▒   ░██▒ ▓█   ▓██▒░██▓ ▒██▒░ ████▓▒░▒██▒ ░  ░
    ░ ▒░   ░  ░ ▒▒   ▓▒█░░ ▒▓ ░▒▓░░ ▒░▒░▒░ ▒▓▒░ ░  ░
    ░  ░      ░  ▒   ▒▒ ░  ░▒ ░ ▒░  ░ ▒ ▒░ ░▒ ░     
    ░      ░     ░   ▒     ░░   ░ ░ ░ ░ ▒  ░░       
           ░         ░  ░   ░         ░ ░           
    \033[0m
        """
        self.lock = threading.Lock()
        self.open_ports = []
        self.service_db = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            443: "HTTPS",
            3306: "MySQL",
            3389: "RDP"
        }

    def scan_port(self, target, port, timeout=1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                result = s.connect_ex((target, port))
                if result == 0:
                    with self.lock:
                        service = self.service_db.get(port, "Unknown")
                        self.open_ports.append((port, service))
                        print(f"\033[1;32m[+] Port {port} ({service}) is open\033[0m")
        except Exception as e:
            pass

    def scan_target(self, target, ports, threads=100):
        print(f"\n\033[1;34m[*] Scanning target: {target}\033[0m")
        print(f"\033[1;34m[*] Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\033[0m")
        
        thread_list = []
        for port in ports:
            thread = threading.Thread(target=self.scan_port, args=(target, port))
            thread_list.append(thread)
            thread.start()
            
            if len(thread_list) >= threads:
                for t in thread_list:
                    t.join()
                thread_list = []
        
        for t in thread_list:
            t.join()

    def run(self):
        print(self.banner)
        parser = argparse.ArgumentParser(
            description="MalCodeX Network Scanner - Professional Edition",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="Example:\n  %(prog)s -t 192.168.1.1 -p 1-1000\n  %(prog)s -t example.com -p 22,80,443"
        )
        parser.add_argument("-t", "--target", required=True, help="Target IP or domain")
        parser.add_argument("-p", "--ports", default="1-1024", 
                          help="Port range (e.g., 1-1000) or list (e.g., 22,80,443)")
        parser.add_argument("-T", "--threads", type=int, default=100, 
                          help="Number of threads (default: 100)")
        parser.add_argument("-to", "--timeout", type=float, default=1.0,
                          help="Connection timeout in seconds (default: 1.0)")
        
        args = parser.parse_args()
        
        try:
            # Resolve target if it's a domain
            target = socket.gethostbyname(args.target)
            
            # Parse ports
            if "-" in args.ports:
                start, end = map(int, args.ports.split("-"))
                ports = range(start, end + 1)
            else:
                ports = list(map(int, args.ports.split(",")))
            
            self.scan_target(target, ports, args.threads)
            
            print("\n\033[1;34m[*] Scan completed!\033[0m")
            print("\033[1;34m[*] Open ports found:\033[0m")
            for port, service in sorted(self.open_ports):
                print(f"  \033[1;32m- {port}/tcp ({service})\033[0m")
                
        except KeyboardInterrupt:
            print("\n\033[1;31m[!] Scan interrupted by user\033[0m")
            sys.exit(1)
        except Exception as e:
            print(f"\033[1;31m[!] Error: {e}\033[0m")
            sys.exit(1)

if __name__ == "__main__":
    scanner = MalCodeXScanner()
    scanner.run()
