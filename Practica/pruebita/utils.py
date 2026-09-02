import os,sys,pwinput,time,re

reset = "\033[0m"

if sys.platform == "win32":
    os.system('')
    import msvcrt
else:
    import tty
    import termios

def leer_tecla():
    if sys.platform == "win32":
        ch = msvcrt.getch()
        if ch in (b'\x00', b'\xe0'):
            ch = msvcrt.getch()
            if ch == b'H': return "ARRIBA"
            if ch == b'P': return "ABAJO"
        if ch in (b'\r', b'\n'): return "ENTER"
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch2 = sys.stdin.read(1)
                ch3 = sys.stdin.read(1)
                if ch3 == 'A': return "ARRIBA"
                if ch3 == 'B': return "ABAJO"
            if ch in ('\r', '\n'): return "ENTER"
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return None

def ejecutar_menu(titulo, opciones):
    seleccionado = 0
    total = len(opciones)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n        ==============================\n        {titulo.upper()}\n        ==============================")
        for indice, texto_opcion in enumerate(opciones):
            marcador = "+" if indice == seleccionado else " "
            print(f"        [\033[97m{marcador}\033[0m] \033[1;97m{texto_opcion}\033[0m")
        print("        ==============================")
        
        tecla = leer_tecla()
        if tecla == "ARRIBA":
            seleccionado = (seleccionado - 1) % total
        elif tecla == "ABAJO":
            seleccionado = (seleccionado + 1) % total
        elif tecla == "ENTER":
            return seleccionado


import time
import re

def errorPrint(message, ansi="\033[1;91m"):
    reset = "\033[0m"
    
    # Parpadeo 1: Texto color X, fondo negro por defecto (tu código original)
    parpadeo_texto = ansi
    
    # Parpadeo 2: Transformamos el código para que sea FONDO X con letras negras
    # Extraemos el número de color (ej: 92) usando expresiones regulares
    match = re.search(r';(\d+)m', ansi) or re.search(r'\[(\d+)m', ansi)
    
    if match:
        num_color = int(match.group(1))
        # Si es color de texto de alta intensidad (90-97), le sumamos 10 para volverlo fondo (100-107)
        if 90 <= num_color <= 97:
            num_fondo = num_color + 10
            parpadeo_fondo = f"\033[1;30;{num_fondo}m" # 1=Negrita, 30=Letra Negra, num_fondo=Fondo X
        else:
            # Opción de respaldo genérica si entra otro tipo de código
            parpadeo_fondo = ansi.replace("[", "[7;") 
    else:
        parpadeo_fondo = "\033[1;30;101m" # Fondo rojo por defecto si no detecta patrón

    # Bucle de parpadeo alternado
    for _ in range(3):
        # Letras color X, fondo negro
        print(f"\r{parpadeo_texto} {message} {reset}\033[K", end="", flush=True)
        time.sleep(0.3)
        
        # Fondo color X, letras negras
        print(f"\r{parpadeo_fondo} {message} {reset}\033[K", end="", flush=True)
        time.sleep(0.3)
        
    print() # Salto de línea final



def newInput(prompt, ansi="\033[1;96m", type="text"):
    if type == "password":
        print(f"{ansi}{prompt}{reset}", end="", flush=True)
        inputValue = pwinput.pwinput(prompt="", mask="*")
    else:
        inputValue = input(f"{ansi}{prompt}{reset}")
    return inputValue

"""
Como mover el cursor en la terminal:
\033[n;mH: Mueve el cursor a la posición (n, m) en la terminal.
\033[nA: Mueve el cursor hacia arriba n líneas.
\033[nB: Mueve el cursor hacia abajo n líneas.
\033[nC: Mueve el cursor hacia la derecha n columnas.
\033[nD: Mueve el cursor hacia la izquierda n columnas.
\033[s: Guarda la posición actual del cursor.
\033[u: Restaura la posición del cursor guardada previamente.
\033[2J: Limpia la pantalla de la terminal.
\033[H: Mueve el cursor a la posición (0, 0) en la terminal.
\033[?25l: Oculta el cursor en la terminal.
\033[?25h: Muestra el cursor en la terminal.
\033[?7h: Habilita el modo de desplazamiento de la terminal.
\033[?7l: Deshabilita el modo de desplazamiento de la terminal.
\033[?25h: Muestra el cursor en la terminal.
\033[?25l: Oculta el cursor en la terminal.
\033[?1h: Habilita el modo de cursor de una sola línea en la terminal.
\033[?1l: Deshabilita el modo de cursor de una sola línea en la terminal.
"""