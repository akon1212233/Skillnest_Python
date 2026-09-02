import socket
from threading import Thread

def port_scanner(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex((ip, port))
            if result == 0:
                print(f'{ip}:{port} - PORTA ABIERTO')
                if port == 22:
                    # intentar conectarse con credenciales por defecto
                    try:
                        s.sendall(b'SSH root@localhost')
                        result = s.recv(1024)
                        print(f'{ip}:{port} - Conectado como root/root')
                    except Exception as e:
                        print(f'Error de conexión: {e}')
            else:
                print(f'{ip}:{port} - PORTA CERRADO')
    except Exception as e:
        print(f'Error en la función: {e}')

def scan_range(start, end):
    for ip in range(start, end + 1):
        ip = f'192.168.100.{ip}'
        print(f'Examinando {ip}')
        thread = Thread(target=port_scanner, args=(ip, 22))
        thread.start()
        
        thread = Thread(target=port_scanner, args=(ip, 80))
        thread.start()
        
        thread = Thread(target=port_scanner, args=(ip, 443))
        thread.start()

scan_range(1, 254)