import sqlite3
from data.db import get_connection
from models.producto import Producto

class ProductoRepository:
    def add(self, producto: Producto) -> Producto:
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO productos (nombre, descripcion, precio, stock)
                VALUES (?, ?, ?, ?)
                """,
                (producto.nombre, producto.descripcion, producto.precio, producto.stock)
            )
            producto.id_producto = cursor.lastrowid
            conn.commit()
        except sqlite3.OperationalError as e:
            raise RuntimeError(f"Error al insertar producto en la base de datos: {e}")
        finally:
            if conn is not None:
                conn.close()
        return producto

    def get(self, id_producto: int) -> Producto | None:
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM productos WHERE id = ?", (id_producto,)
        ).fetchone()
        conn.close()
        if row:
            return Producto(
                id_producto=row["id"],
                nombre=row["nombre"],
                descripcion=row["descripcion"],
                stock=row["stock"],
                disponibilidad=row["disponibilidad"],
                precio=row["precio"]
            )
        return None

    def update(self, producto: Producto) -> None:
        conn = get_connection()
        conn.execute(
            """
            UPDATE productos
            SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, disponibilidad = ?
            WHERE id_producto = ?
            """,
            (producto.id_producto, producto.nombre, producto.descripcion, producto.stock, producto.precio, producto.disponibilidad)
        )
        conn.commit()
        conn.close()

    def desactivar_producto(self, id_producto):
        query = "UPDATE productos SET activo = 0 WHERE id_producto = ?;"
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (id_producto,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al desactivar el producto: {e}")
            return False
        finally:
            conn.close()

    def list_all(self) -> list[Producto]:
        conn = get_connection()
        rows = conn.execute("SELECT * FROM productos").fetchall()
        conn.close()
        return [Producto(
            id_producto=row["id"],
            nombre=row["nombre"],
            descripcion=row["descripcion"],
            stock=row["stock"],
            disponibilidad=row["disponibilidad"],
            precio=row["precio"]
        ) for row in rows]

    def low_stock(self, threshold: int = 5) -> list[Producto]:
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM productos WHERE cantidad < ?", (threshold,)
        ).fetchall()
        conn.close()
        return [Producto(
            id_producto=row["id"],
            nombre=row["nombre"],
            descripcion=row["descripcion"],
            stock=row["cantidad"],
            disponibilidad=row["disponibilidad"],
            precio=row["precio"]
        ) for row in rows]
