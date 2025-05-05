from datetime import datetime
from models.producto import Producto
from models.movimiento import Movimiento
from data.movimiento_repository import MovimientoRepository
from data.producto_repository import ProductoRepository

class InventarioService:
    def __init__(self, producto_repo: ProductoRepository = ProductoRepository(), movimiento_repo: MovimientoRepository= MovimientoRepository()):
        self.producto_repo = producto_repo
        self.movimiento_repo = movimiento_repo

    def agregar_producto(self, nombre: str, descripcion: str, precio: float, stock: int) -> Producto:
        if stock < 0:
            raise ValueError("El stock no puede ser negativo")
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")
        producto = Producto(id_producto=None, nombre=nombre, descripcion=descripcion, precio=precio, stock=stock, disponibilidad=True)
        return self.producto_repo.add(producto)
    
    def registrar_movimiento(self, id_producto: int, tipo:str, cantidad: int) -> Movimiento:
        if tipo not in ("entrada", "salida"):
            raise ValueError("El tipo de movimiento debe ser 'entrada' o 'salida'")
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
        producto = self.producto_repo.get(id_producto)
        if producto is None:
            raise ValueError("Producto no encontrado")
        
        if tipo == "salida" and producto.stock < cantidad:
            raise ValueError("No hay suficiente stock para realizar la salida")
        
        movimiento = Movimiento(
            id_movimiento=None,
            id_producto=id_producto,
            tipo=tipo,
            cantidad=cantidad,
            fecha= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        movimiento = self.movimiento_repo.record(movimiento)
        # Actualizar el stock del producto
        if tipo == "entrada":
            producto.stock += cantidad
        else:
            producto.stock -= cantidad
        self.producto_repo.update(producto)
        return movimiento
    
    def obtener_producto(self, id_producto: int) -> Producto:
        producto = self.producto_repo.get(id_producto)
        if producto is None:
            raise ValueError("Producto no encontrado")
        return producto
    
    def listar_productos(self) -> list:
        return self.producto_repo.list_all()
    
    def reporte_stock_bajo(self, limite: int) -> list:
        if limite < 0:
            raise ValueError("El límite no puede ser negativo")
        return self.producto_repo.low_stock(limite)

    