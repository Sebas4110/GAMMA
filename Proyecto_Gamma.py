import sqlite3
import os

# ----- limpiar la pantalla -----
def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")#nt = windows

# ----- Conectarse a la base de datos -----
conexion = sqlite3.connect("gamma.db")
#conn es igual a conexion
cursor = conexion.cursor()
# c es igual a cursor

# ===== TABLAS =====
# ----- jugadores -----
cursor.execute("""CREATE TABLE IF NOT EXISTS jugadores (
    id_jugador INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    vida INTEGER NOT NULL,
    dinero INTEGER NOT NULL DEFAULT 0,
    porcentaje REAL NOT NULL DEFAULT 0
    )
""")
# ----- inventario -----
cursor.execute('''CREATE TABLE IF NOT EXISTS inventario (
    id_inventario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    poder TEXT NOT NULL,
    uso TEXT NOT NULL,
    cantidad INTEGER DEFAULT 1,
    id_jugador INTEGER NOT NULL,
    FOREIGN KEY (id_jugador) REFERENCES jugadores(id_inventario)
)''')
# ----- habilidades -----
cursor.execute('''CREATE TABLE IF NOT EXISTS habilidades (
    id_habilidades INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    nivel INTEGER NOT NULL DEFAULT 1,
    desbloqueada INTEGER NOT NULL,
    elementos_compatibles TEXT NOT NULL,
    id_jugador INTEGER NOT NULL,
    FOREIGN KEY (id_jugador) REFERENCES jugadores(id_jugador)
)''')

conexion.commit()
# ===== CHECKPOINT 1 =====

def agregar_jugador():
    limpiar_pantalla()
    print("=== Agregar Jugador ===")
    
    nombre = str(input("Nombre del jugador: "))
    vida = int(input("Vida: "))
    dinero = int(input("Dinero: "))
    porcentaje = float(input("Porcentaje completado: "))

    cursor.execute("INSERT INTO jugadores (nombre, vida, dinero, porcentaje) VALUES (?, ?, ?, ?)",
        (nombre, vida, dinero, porcentaje))
    conexion.commit()
    print(f"\nJugador '{nombre}' agregado correctamente.")

# ===== CHECKPOINT 2 =====

def listar_jugadores():
    limpiar_pantalla()
    print("=== Lista de Jugadores ===")

    cursor.execute("SELECT * FROM jugadores")
    jugadores = cursor.fetchall()
    if jugadores:
        print("-"*40)
        for jugador in jugadores:
            print(f"Nombre: {jugador[0]} \nVida: {jugador[1]} \nDinero: {jugador[2]} \nPorcentaje: {jugador[3]}")
        print("-"*40)
    else:
        print("No hay jugadores existentes")

# ===== CHECKPOINT 3 =====