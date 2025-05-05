from .db import get_connection
from models.movimiento import Movimiento

class MovimientoRepository:
    def record(self, movimiento: Movimiento) -> Movimiento:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO movimientos (id_movimiento, id_producto, tipo, cantidad, fecha)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                movimiento.id_movimiento,
                movimiento.id_producto,
                movimiento.tipo,
                movimiento.cantidad,
                movimiento.fecha,
            ),
        )
        movimiento.id_movimiento = cursor.lastrowid
        conn.commit()
        conn.close()
        return movimiento

    def fetch_movimientos(self, query: str, params: tuple = ()) -> list[Movimiento]:
        """Método privado para ejecutar consultas y mapear resultados a objetos Movimiento."""
        conn = get_connection()
        rows = conn.execute(query, params).fetchall()
        conn.close()
        return [
            Movimiento(
                id_movimiento=row["id_movimiento"],
                id_producto=row["id_producto"],
                tipo=row["tipo"],
                cantidad=row["cantidad"],
                fecha=row["fecha"],
            )
            for row in rows
        ]

    def list_all(self) -> list[Movimiento]:
        """Listar todos los movimientos."""
        return self.fetch_movimientos("SELECT * FROM movimientos")

    def list_by_date(self, date: str) -> list[Movimiento]:
        """Listar movimientos por una fecha específica."""
        return self.fetch_movimientos(
            "SELECT * FROM movimientos WHERE DATE(fecha) = DATE(?)", (date,)
        )

    def list_by_month(self, month_year: str) -> list[Movimiento]:
        """Listar movimientos por un mes específico (formato MM-YYYY)."""
        return self.fetch_movimientos(
            "SELECT * FROM movimientos WHERE strftime('%m-%Y', fecha) = ?", (month_year,)
        )

    def sales_report(self, period: str) -> list[dict]:
        """
        Generar un reporte de ventas y disponibilidad de productos.
        El parámetro `period` puede ser 'day', 'week', o 'month'.
        """
        conn = get_connection()
        if period == "day":
            query = """
            SELECT p.nombre, p.stock, SUM(m.cantidad) AS total_vendido
            FROM movimientos m
            JOIN productos p ON m.id_producto = p.id_producto
            WHERE m.tipo = 'venta' AND DATE(m.fecha) = DATE('now')
            GROUP BY p.id_producto
            """
        elif period == "week":
            query = """
            SELECT p.nombre, p.stock, SUM(m.cantidad) AS total_vendido
            FROM movimientos m
            JOIN productos p ON m.id_producto = p.id_producto
            WHERE m.tipo = 'venta' AND strftime('%W', m.fecha) = strftime('%W', 'now')
            GROUP BY p.id_producto
            """
        elif period == "month":
            query = """
            SELECT p.nombre, p.stock, SUM(m.cantidad) AS total_vendido
            FROM movimientos m
            JOIN productos p ON m.id_producto = p.id_producto
            WHERE m.tipo = 'venta' AND strftime('%m-%Y', m.fecha) = strftime('%m-%Y', 'now')
            GROUP BY p.id_producto
            """
        else:
            raise ValueError("El período debe ser 'day', 'week' o 'month'.")

        rows = conn.execute(query).fetchall()
        conn.close()
        return [
            {"nombre": row["nombre"], "stock": row["stock"], "total_vendido": row["total_vendido"]}
            for row in rows
        ]