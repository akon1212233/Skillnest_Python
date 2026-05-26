import os

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

# 1. DEFINICIÓN DE LAS CLASES

class Cliente:
    def __init__(self, nombre, edad, correo, telefono, membresia="Gratis"):
        self.nombre = nombre
        self.edad = edad
        self.correo = correo
        self.telefono = telefono
        self.membresia = membresia
        # Aquí guardaremos el objeto del plan cuando se lo asignemos
        self.plan_asignado = None 

    def mostrar_cliente(self):
        informacion = f"Cliente: {self.nombre} | Teléfono: {self.telefono} | Membresía: {self.membresia}"
        if self.plan_asignado != None:
            informacion = informacion + f" | Plan: {self.plan_asignado.rutina}"
        else:
            informacion = informacion + " | Plan: Ninguno"
        return informacion

    def actualizar_telefono(self, nuevo_telefono):
        self.telefono = nuevo_telefono
        print("¡Teléfono actualizado con éxito!")


class Entrenador:
    def __init__(self, nombre, edad, correo, telefono, salario):
        self.nombre = nombre
        self.edad = edad
        self.correo = correo
        self.telefono = telefono
        self.salario = salario
        self.lista_de_clientes = []

    def mostrar_entrenador(self):
        return f"Entrenador: {self.nombre} | Salario Actual: ${self.salario} | Clientes a cargo: {self.lista_de_clientes}"

    def asignar_cliente(self, nombre_cliente):
        self.lista_de_clientes.append(nombre_cliente)
        self.salario = self.salario + 4990
        print(f"¡Cliente asignado al entrenador {self.nombre}!")


class PlanEntrenamiento:
    def __init__(self, rutina, horario, dieta, duracion_en_dias):
        self.rutina = rutina
        self.horario = horario
        self.dieta = dieta
        self.duracion_en_dias = duracion_en_dias

    def mostrar_plan(self):
        return f"Rutina: {self.rutina} | Horario: {self.horario} | Dieta: {self.dieta} | Duración: {self.duracion_en_dias} días"

    def modificar_duracion(self, nueva_duracion):
        self.duracion_en_dias = nueva_duracion
        print("¡Duración del plan modificada!")


# 2. LISTAS PARA ALMACENAR LOS DATOS
todos_los_clientes = []
todos_los_entrenadores = []
todos_los_planes = []


# 3. MENÚ INTERACTIVO (WHILE)
continuar = True

while continuar:
    print("\n==========================================")
    print("      SISTEMA DE GESTIÓN DE GIMNASIO      ")
    print("==========================================")
    print("1. Registrar Cliente")
    print("2. Registrar Entrenador")
    print("3. Mostrar Clientes")
    print("4. Mostrar Entrenadores")
    print("5. Asignar Cliente a Entrenador")
    print("6. Asignar Plan de Entrenamiento a Cliente")
    print("0. Salir")
    print("==========================================")
    
    opcion = int(input("Elige una opción: "))

    if opcion == 1:
        print("\n--- REGISTRO DE CLIENTE ---")
        nombre = input("Nombre: ")
        edad = int(input("Edad: "))
        correo = input("Correo: ")
        telefono = input("Teléfono: ")
        membresia = input("Membresía (Gratis/Premium/Golden): ")

        nuevo_cliente = Cliente(nombre, edad, correo, telefono, membresia)
        todos_los_clientes.append(nuevo_cliente)
        print("Cliente registrado exitosamente.")

    elif opcion == 2:
        print("\n--- REGISTRO DE ENTRENADOR ---")
        nombre = input("Nombre: ")
        edad = int(input("Edad: "))
        correo = input("Correo: ")
        telefono = input("Teléfono: ")
        salario = float(input("Salario Base: "))

        nuevo_entrenador = Entrenador(nombre, edad, correo, telefono, salario)
        todos_los_entrenadores.append(nuevo_entrenador)
        print("Entrenador registrado exitosamente.")

    elif opcion == 3:
        print("\n--- LISTA DE CLIENTES ---")
        if len(todos_los_clientes) == 0:
            print("No hay clientes registrados.")
        else:
            for posicion, un_cliente in enumerate(todos_los_clientes):
                print(f"[{posicion}] {un_cliente.mostrar_cliente()}")

    elif opcion == 4:
        print("\n--- LISTA DE ENTRENADORES ---")
        if len(todos_los_entrenadores) == 0:
            print("No hay entrenadores registrados.")
        else:
            for posicion, un_entrenador in enumerate(todos_los_entrenadores):
                print(f"[{posicion}] {un_entrenador.mostrar_entrenador()}")

    elif opcion == 5:
        print("\n--- ASIGNAR CLIENTE A ENTRENADOR ---")
        if len(todos_los_clientes) == 0 or len(todos_los_entrenadores) == 0:
            print("Necesitas clientes y entrenadores en el sistema.")
        else:
            print("Selecciona el número de entrenador:")
            for posicion, un_entrenador in enumerate(todos_los_entrenadores):
                print(f"[{posicion}] {un_entrenador.nombre}")
            numero_entrenador = int(input("Número de entrenador: "))

            print("Selecciona el número de cliente:")
            for posicion, un_cliente in enumerate(todos_los_clientes):
                print(f"[{posicion}] {un_cliente.nombre}")
            numero_cliente = int(input("Número de cliente: "))

            entrenador_seleccionado = todos_los_entrenadores[numero_entrenador]
            cliente_seleccionado = todos_los_clientes[numero_cliente]

            entrenador_seleccionado.asignar_cliente(cliente_seleccionado.nombre)

    elif opcion == 6:
        print("\n--- ASIGNAR PLAN A CLIENTE ---")
        if len(todos_los_clientes) == 0:
            print("No hay clientes para asignarles un plan.")
        else:
            print("Selecciona el cliente:")
            for posicion, un_cliente in enumerate(todos_los_clientes):
                print(f"[{posicion}] {un_cliente.nombre}")
            numero_cliente = int(input("Número de cliente: "))

            print("\nSelecciona el plan disponible:")
            for posicion, un_plan in enumerate(todos_los_planes):
                print(f"[{posicion}] {un_plan.mostrar_plan()}")
            numero_plan = int(input("Número de plan: "))

            cliente_seleccionado = todos_los_clientes[numero_cliente]
            plan_seleccionado = todos_los_planes[numero_plan]

            # Conectamos el objeto Plan dentro del objeto Cliente
            cliente_seleccionado.plan_asignado = plan_seleccionado
            print(f"¡Plan '{plan_seleccionado.rutina}' asignado a {cliente_seleccionado.nombre}!")

    elif opcion == 0:
        limpiar_consola()
        print("Saliendo del sistema... ¡Hasta luego!")
        continuar = False

    else:
        print("Opción inválida, intenta de nuevo.")

