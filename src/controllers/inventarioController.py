from services.inventario_services import InventarioService

class InventarioController:
    def __init__(self):
        self.inventario_services = InventarioService()
    
    def agregar_producto(self, nombre: str, modelo:str, submodelo:str, marca:str, proveedor:str, categoria:str,
                         subcategoria:str, foto:bytes, manual:bytes, descripcion: str, precio: float, stock: int):
        try:
            producto = self.inventario_services.agregar_producto(nombre, modelo, submodelo, marca, proveedor,
                        categoria, subcategoria, foto, manual, descripcion, precio, stock)
            print(f"Producto agregado: {producto.nombre} con ID {producto.id_producto}")
            return producto
        except ValueError as e:
            print(f"Error al agregar producto: {e}")
            return None
        
    def registrar_movimiento(self, id_producto: int, tipo: str, cantidad: int):
        try:
            movimiento = self.inventario_services.registrar_movimiento(id_producto, tipo, cantidad)
            print(f"Movimiento registrado: {movimiento}")
            return movimiento
        except ValueError as e:
            print(f"Error al registrar movimiento: {e}")
            return None
        
    def listar_productos(self):
        try:
            productos = self.inventario_services.listar_productos()
            if productos:
                print("Lista de productos:")
                for producto in productos:
                    print(producto)
            else:
                print("No hay productos disponibles.")
            return productos
        except Exception as e:
            print(f"Error al listar productos: {e}")
            return []
    
    def reporte_stock_bajo(self, limite: int):
        try:
            productos_bajos = self.inventario_services.reporte_stock_bajo(limite)
            if productos_bajos:
                print("Productos con stock bajo:")
                for producto in productos_bajos:
                    print(producto)
            else:
                print("No hay productos con stock bajo.")
            return productos_bajos
        except ValueError as e:
            print(f"Error al generar reporte de stock bajo: {e}")
            return []