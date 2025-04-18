# Utilizar caso esteja no kali:
#!/usr/bin/python
from scapy.all import *
import socket
from pyfiglet import Figlet

f = Figlet(font='slant')
print(f.renderText('Scapy Port Scanner'))

def get_service(port):
    try:
        service = socket.getservbyport(port)
        return service
    except:
        return "Desconhecido"

def scan_ports(target, ports, timeout=1):
    open_ports = {}
    for port in ports:
        packet = IP(dst=target)/TCP(dport=port, flags="S")
        response = sr1(packet, timeout=timeout, verbose=False)

        if response and response.haslayer(TCP) and response[TCP].flags == 18:
            service = get_service(port)
            open_ports[port] = service
    return open_ports

def main():
    firewall = "99.99.99.254"
    ports = range(1, 1024)

    open_ports = scan_ports(firewall, ports)

    if open_ports:
        print("Portas abertas em {}:".format(firewall))
        for port, service in open_ports.items():
            print("Porta {}: {}".format(port, service))
    else:
        print("Nenhuma porta aberta encontrada no firewall {}.".format(firewall))

if __name__ == "__main__":
    main()
