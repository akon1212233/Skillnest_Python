import os
import sys
import time
from utils import ejecutar_menu, errorPrint, newInput
from usuario import Usuario

colors = {
    "VERDE": "\033[1;92m",
    "AZUL": "\033[1;94m",
    "AZUL_CLARO": "\033[1;96m",
    "RESET": "\033[0m"
}

def panel_administrador(datos_admin):
    # datos_admin[1] contiene el nickname (ej: 'Carlos')
    nombre_admin = datos_admin[1]
    
    opciones_admin = [
        "Registrar usuario",
        "Listar usuarios",
        "Buscar usuario",
        "Modificar usuario",
        "Eliminar usuario",
        "Cerrar sesión"
    ]
    
    usuario_dao = Usuario()
    
    while True:
        titulo = f"Bienvenido Administrador:\n        {nombre_admin}"
        seleccion = ejecutar_menu(titulo, opciones_admin)
        
        os.system('cls' if os.name == 'nt' else 'clear')
        
        if seleccion == 0:
            print(f"\n--- REGISTRAR USUARIO ---")
            nick = newInput("Usuario: ")
            email = newInput("Email: ")
            contra = newInput("Contraseña: ", type="password")
            
            tipo_sel = ejecutar_menu("Seleccione Tipo de Usuario", ["ADMIN", "USER"])
            tipo = 1 if tipo_sel == 0 else 2 # 1=Admin, 2=User según tus inserts
            
            usuario_dao.registrarUsuario(tipo, nick, contra, email)
            errorPrint("✔ Usuario registrado con éxito.", colors["VERDE"])
            time.sleep(1)
            
        elif seleccion == 1:
            print(f"\n{"ID":<5} {"Usuario":<15} {"Tipo":<10}")
            print("-" * 35)
            # Lista los registros activos
            for u in usuario_dao.listarUsuarios():
                # u[0]=idUsuario, u[1]=nombreUsuario, u[2]=idTipoUsuario (1=ADMIN, 2=USER)
                rol = "ADMIN" if u[2] == 1 else "USER"
                print(f"{u[0]:<5} {u[1]:<15} {rol:<10}")
            input("\nPresione Enter para continuar...")
            
        elif seleccion == 2:
            print(f"\n--- BUSCAR USUARIO ---")
            id_buscar = newInput("Ingrese ID del usuario: ")
            
            # Buscamos en la lista completa para extraer la información exacta
            encontrado = False
            for u in usuario_dao.listarUsuarios():
                if str(u[0]) == id_buscar:
                    rol = "ADMIN" if u[2] == 1 else "USER"
                    print(f"\nID: {u[0]}\nUsuario: {u[1]}\nEmail: {u[2]}\nTipo: {rol}")
                    encontrado = True
                    break
            if not encontrado:
                errorPrint("⚠ Usuario no encontrado.")
            input("\nPresione Enter para continuar...")
            
        elif seleccion == 3:
            print(f"\n--- MODIFICAR USUARIO ---")
            id_mod = newInput("Ingrese ID a modificar: ")
            
            encontrado = False
            for u in usuario_dao.listarUsuarios():
                if str(u[0]) == id_mod:
                    encontrado = True
                    print(f"\nModificando a: {u[1]}")
                    nuevo_nick = newInput("Nuevo Usuario: ")
                    nuevo_email = newInput("Nuevo Email: ")
                    nueva_contra = newInput("Nueva Contraseña: ", type="password")
                    
                    tipo_sel = ejecutar_menu("Nuevo Tipo de Usuario", ["ADMIN", "USER"])
                    nuevo_tipo = 1 if tipo_sel == 0 else 2
                    
                    usuario_dao.modificarUsuario(id_mod, nuevo_nick, nueva_contra, nuevo_email)
                    errorPrint("✔ Usuario modificado con éxito.", colors["VERDE"])
                    time.sleep(1)
                    break
            if not encontrado:
                errorPrint("⚠ ID no encontrado.")
                time.sleep(1)
                
        elif seleccion == 4:
            print(f"\n--- ELIMINAR USUARIO ---")
            id_eli = newInput("Ingrese ID a eliminar: ")
            usuario_dao.eliminarUsuario(id_eli)
            errorPrint("✔ Registro eliminado correctamente.", colors["VERDE"])
            time.sleep(1)
            
        elif seleccion == 5:
            break

def panel_usuario(datos_user):
    # datos_user[1] contiene el nickname (ej: 'Juan Pérez')
    nombre_user = datos_user[1]
    
    while True:
        titulo = f"Bienvenido\n\n        {nombre_user}\n\n        Tipo de usuario:\n        USER"
        seleccion = ejecutar_menu(titulo, ["Cerrar sesión"])
        if seleccion == 0:
            break

# --- FLUJO PRINCIPAL ---
while True:
    seleccion_inicial = ejecutar_menu("Sistema de Usuarios", ["Iniciar sesión", "Salir"])
    
    if seleccion_inicial == 1:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\nSaliendo de la aplicación...\n")
        sys.exit()
        
    if seleccion_inicial == 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n        ==============================\n                 INICIO DE SESIÓN\n        ==============================")
        
        email = newInput("        Email:      ")
        contrasena = newInput("        Contraseña: ", type="password")
        
        usuario_sistema = Usuario()
        datos_usuario = usuario_sistema.buscarUsuario(email, contrasena)
        
        if not datos_usuario:
            print("")
            errorPrint("        ⚠ Usuario o contraseña incorrectos.")
            time.sleep(1.5)
            continue # Al dar continue vuelve al menú inicial de Selección
            
          # 1. AGREGA ESTA LÍNEA TEMPORAL PARA IMPRIMIR EN CONSOLA QUÉ TRAE LA VARIABLE:
        print(f"\nDEBUG - Datos recibidos: {datos_usuario}")
        input("Presione Enter para continuar...") # Pausa el programa para que alcances a leerlo

        # 2. MODIFICA LA VALIDACIÓN PARA ASEGURAR QUE CORRESPONDA AL ÍNDICE 4 O AL CAMPO CORRECTO:
        if str(datos_usuario[2]) == "1":
            panel_administrador(datos_usuario)
        else:
            panel_usuario(datos_usuario)
