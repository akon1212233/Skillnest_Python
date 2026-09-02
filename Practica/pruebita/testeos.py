import sys

# Asegurar soporte ANSI en consolas antiguas de Windows
if sys.platform == "win32":
    import os
    os.system('')

print("\n" + "=" * 50)
print("     CATÁLOGO COMPLETO DE ESTILOS ANSI EN PYTHON")
print("=" * 50 + "\n")

# 1. TODOS LOS FORMATOS Y EFECTOS EXISTENTES
print("--- 1. EFECTOS DE FORMATO (ESTILOS) ---")
formatos = {
    0: "Normal / Reset",
    1: "Negrita (Bold / Extra brillo)",
    2: "Atenuado (Faint / Texto opaco)",
    3: "Cursiva (Italic - Requiere soporte de fuente)",
    4: "Subrayado (Underline - Rayita abajo)",
    5: "Parpadeo lento (Blink - Soportado en algunas terminales)",
    6: "Parpadeo rápido (Rare Blink)",
    7: "Invertir colores (Reverse - Intercambia fondo y letra)",
    8: "Oculto (Conceal / Invisible - El texto no se ve)",
    9: "Tachado (Strikethrough / Rayita en medio)"
}

for codigo, nombre in formatos.items():
    print(f"Código [{codigo}]: \033[{codigo}mTexto con efecto {nombre}\033[0m")


# 2. COMBINACIONES ÚTILES PARA TU MENÚ
print("\n--- 2. COMBINACIONES DE FORMATO + COLOR ---")

# Estructura avanzada: \033[ESTILO;COLOR_LETRA;COLOR_FONDOm
combinaciones = {
    "Subrayado + Cian": "\033[4;36m",
    "Tachado + Rojo": "\033[9;31m",
    "Negrita + Subrayado + Amarillo": "\033[1;4;33m",
    "Cursiva + Verde": "\033[3;32m",
    "Invertido + Magenta (Estilo Botón)": "\033[7;35m",
    "Negrita + Tachado + Blanco + Fondo Azul": "\033[1;9;37;44m",
}

for nombre, ansi in combinaciones.items():
    print(f"{ansi}{nombre}\033[0m")


# 3. EXTRA: DOBLE SUBRAYADO Y MÁS (SOPORTE EXTENDIDO ANSI)
print("\n--- 3. EFECTOS MODERNOS EXTENDIDOS (SOPORTE VT100/ANSI) ---")
# Algunas terminales modernas como la de VS Code soportan variaciones del código 4
print("Código [4:2]: \033[4:2mDoble subrayado (Rayita doble abajo)\033[0m")
print("Código [4:3]: \033[4:3mSubrayado ondeado / rulo (Curly underline)\033[0m")
print("Código:  \033[53mLínea superior (Overline - Rayita arriba)\033[0m")

print("\n" + "=" * 50)
print(" Nota: Si algún estilo no cambia, es porque la fuente")
print(" de tu VS Code no tiene esa variante (ej. Cursiva).")
print("=" * 50 + "\n")
import time

# En lugar de parpadear el texto, puedes alternar el color de fondo rápidamente
for _ in range(3):
    print("\r\033[1;30;101m ⚠ CONTRASEÑA INCORRECTA \033[0m", end="")
    time.sleep(0.3)
    print("\r\033[1;31m ⚠ CONTRASEÑA INCORRECTA \033[0m", end="")
    time.sleep(0.3)
print() # Salto de línea al terminar
import threading
import time
import sys

# Variable global para controlar el parpadeo
parpadear_alerta = False

def bucle_parpadeo():
    global parpadear_alerta
    while parpadear_alerta:
        # Imprime la alerta con fondo rojo invertido
        sys.stdout.write("\r\033[1;30;101m  ⚠ CREDENCIALES INCORRECTAS  \033[0m")
        sys.stdout.flush()
        time.sleep(0.4)
        
        if not parpadear_alerta: break
        
        # Borra la línea y la muestra en rojo normal (Efecto parpadeo)
        sys.stdout.write("\r\033[1;31m  ⚠ CREDENCIALES INCORRECTAS  \033[0m")
        sys.stdout.flush()
        time.sleep(0.4)
    
    # Al apagar el parpadeo, limpiamos esa línea
    sys.stdout.write("\r" + " " * 40 + "\r")
    sys.stdout.flush()

# --- EJEMPLO DE USO CUANDO FALLA EL LOGIN ---
print("Simulando error de login...")
parpadear_alerta = True

# Iniciamos el parpadeo en segundo plano
hilo = threading.Thread(target=bucle_parpadeo)
hilo.start()

# Dejamos que parpadee durante 4 segundos mientras el programa hace otra cosa
time.sleep(4)

# Apagamos el parpadeo de forma limpia
parpadear_alerta = False
hilo.join()

print("El programa continúa normal...")
import time
import sys

print("Comprobando credenciales...")
time.sleep(1)

# Simulación manual de parpadeo (Blink) que funciona en cualquier VS Code del mundo
for _ in range(3):
    # \r regresa el cursor al inicio de la línea sin bajar de renglón
    sys.stdout.write("\r\033[1;31m⚠ ERROR: EMAIL NO REGISTRADO ⚠\033[0m")
    sys.stdout.flush()
    time.sleep(0.4)
    
    # Sobreescribimos con espacios en blanco para "apagar" el texto
    sys.stdout.write("\r" + " " * 35)
    sys.stdout.flush()
    time.sleep(0.3)

print("\r\033[1;33mIntente de nuevo:\033[0m")

