class SuscripcionStreaming:
    costos_suscripcion = {"Gratis": 0, "Estándar": 5.99, "Premium": 10.99}

    def __init__(self, usuario, tipoSuscripcion="Gratis"):
        self.usuario = usuario
        self.tipoSuscripcion = tipoSuscripcion
        self.costoMensual = self.costos_suscripcion[tipoSuscripcion]
        self.saldoPendiente = self.costoMensual

    def realizar_pago(self, monto):
        """Reduce el saldo pendiente según el monto pagado."""
        self.saldoPendiente -= monto
        if self.saldoPendiente < 0:
            self.saldoPendiente = 0
        print(f"{self.usuario} pagó ${monto}")

    def cambiar_suscripcion(self, nuevoTipo):
        """Cambia el tipo de suscripción y actualiza el costo mensual."""
        if nuevoTipo in self.costos_suscripcion:
            self.tipoSuscripcion = nuevoTipo
            self.costoMensual = self.costos_suscripcion[nuevoTipo]
            self.saldoPendiente = self.costoMensual
            print(f"{self.usuario} cambió a suscripción {nuevoTipo}")
        else:
            print("Tipo de suscripción no válido")

    def ver_contenido_exclusivo(self):
        """Permite ver contenido exclusivo según el tipo de suscripción."""
        if self.tipoSuscripcion == "Premium":
            print("Puedes ver contenido exclusivo Premium")
        elif self.tipoSuscripcion == "Estándar":
            print("Puedes ver contenido estándar")
        else:
            print("La cuenta Gratis no tiene contenido exclusivo")
    def mostrar_info_suscripcion(self):
        """Muestra la información de la suscripción del usuario."""
        print("------ INFORMACIÓN ------")
        print(f"Usuario: {self.usuario}")
        print(f"Tipo: {self.tipoSuscripcion}")
        print(f"Costo mensual: ${self.costoMensual}")
        print(f"Saldo pendiente: ${self.saldoPendiente}")
        print("-------------------------")

user1 = SuscripcionStreaming("Marcelo")
user2 = SuscripcionStreaming("Benja", "Estándar")
user3 = SuscripcionStreaming("Mauricio", "Premium")

user3.ver_contenido_exclusivo()
user2.realizar_pago(5)
user2.mostrar_info_suscripcion()
user1.cambiar_suscripcion("Premium")
user1.mostrar_info_suscripcion()