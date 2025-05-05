# File: src/main.py

from data.db import create_table  # asegúrate de que el path y el import sean correctos
from controllers.inventarioController import InventarioController

def main():
    # Inicializa el esquema
    create_table()

    controller = InventarioController()

    print("Agregando producto...")
    producto = controller.agregar_producto("Laptop", "Laptop de alta gama", 1500.0, 10)

    # Resto del código...

if __name__ == "__main__":
    main()