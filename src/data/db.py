import sqlite3

def get_connection():
    conn = sqlite3.connect('inventario.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    sql_products = """
    CREATE TABLE IF NOT EXISTS productos (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    modelo TEXT NOT NULL,
    submodelo TEXT,
    marca TEXT NOT NULL,
    proveedor TEXT NOT NULL,
    categoria TEXT NOT NULL,
    subcategoria TEXT,
    foto BLOB,
    manual BLOB,
    descripcion TEXT NOT NULL,
    precio REAL NOT NULL CHECK(precio >= 0),
    activo INTEGER NOT NULL DEFAULT 1,
    disponibilidad text GENERATED ALWAYS AS (CASE WHEN stock > 0 THEN 'disponible' ELSE 'no disponible' END) VIRTUAL,
    stock INTEGER NOT NULL CHECK(stock >= 0)
    );
    """
    sql_movimientos = """
    CREATE TABLE IF NOT EXISTS movimientos (
    id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_producto INTEGER NOT NULL,
    tipo TEXT NOT NULL CHECK(tipo IN ('entrada', 'salida')),
    cantidad INTEGER NOT NULL CHECK(cantidad > 0),
    fecha TEXT NOT NULL DEFAULT (datetime('now')),
    foreign key (id_producto) references productos (id_producto)
    );
    """
    conn = get_connection()
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute(sql_products)
    conn.execute(sql_movimientos)
    conn.commit()
    conn.close()

create_table()