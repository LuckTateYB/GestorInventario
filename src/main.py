# File: src/main.py

from data.db import create_table
from controllers.inventarioController import InventarioController

create_table()
# Este script es el punto de entrada para la aplicación de inventario.
def main():
    controller = InventarioController()

    while True:
        print("\n--- Menú Inventario ---")
        print("1. Agregar producto")
        print("2. Listar productos")
        print("3. Registrar movimiento")
        print("4. Reporte de stock bajo")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\n--- Agregar Producto ---")
            nombre = input("Nombre del producto: ")
            modelo = input("Modelo: ")
            submodelo = input("Submodelo: ")
            marca = input("Marca: ")
            proveedor = input("Proveedor: ")
            descripcion = input("Descripción: ")
            categoria = input("Categoría principal: ")
            subcategoria = input("Subcategoría: ")
            foto = None  # o b"" si esperas bytes
            manual = None  # o b"" si esperas bytes
            try:
                precio = float(input("Precio: "))
                stock = int(input("Stock: "))
                print(f"Datos enviados: {nombre}, {modelo}, {submodelo}, {marca}, {proveedor}, {categoria}, {subcategoria}, {precio}, {stock}")
                producto = controller.agregar_producto(
                    nombre, modelo, submodelo, marca, proveedor, categoria, subcategoria, foto, manual, descripcion, precio, stock
                )
                if producto:
                    print(f"Producto {producto.nombre} agregado exitosamente con ID {producto.id_producto}")
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "2":
            print("\n--- Lista de Productos ---")
            productos = controller.listar_productos()
            for p in productos:
                print(f"{p.id_producto} - {p.nombre} ({p.modelo}) | Stock: {p.stock}")

        elif opcion == "3":
            print("\n--- Registrar Movimiento ---")
            try:
                id_producto = int(input("ID del producto: "))
                tipo = input("Tipo (entrada/salida): ").lower()
                cantidad = int(input("Cantidad: "))
                movimiento = controller.registrar_movimiento(id_producto, tipo, cantidad)
                if movimiento:
                    print(f"Movimiento {movimiento.tipo} registrado con éxito.")
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "4":
            print("\n--- Reporte de Stock Bajo ---")
            try:
                limite = int(input("Límite de stock para alerta: "))
                productos_bajos = controller.reporte_stock_bajo(limite)
                if productos_bajos:
                    print("Productos con stock bajo:")
                    for p in productos_bajos:
                        print(f"{p.id_producto} - {p.nombre} | Stock: {p.stock}")
                else:
                    print("No hay productos con stock bajo.")
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "5":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()