#i ===== IMPORTACIONES Y FUNCIONES =====
import sqlite3
import os
import time
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
    elemento TEXT NOT NULL,
    nivel INTEGER NOT NULL DEFAULT 1,
    desbloqueada INTEGER NOT NULL,
    elementos_compatibles TEXT NOT NULL,
    id_jugador INTEGER NOT NULL,
    FOREIGN KEY (id_jugador) REFERENCES jugadores(id_jugador)
)''')

conexion.commit()

# ===== CHECKPOINT 1 =====
# ===== CRUD JUGADORES ===== 
# -----  C -----

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

# -----  R -----

def listar_jugador():
    limpiar_pantalla()
    print("===== Lista de Jugadores =====")

    cursor.execute("SELECT * FROM jugadores")
    jugadores = cursor.fetchall()
    if jugadores:
        print("-"*40)
        for jugador in jugadores:
            print(f"ID: {jugador[0]} \nNombre: {jugador[1]} \nVida: {jugador[2]} \nDinero: {jugador[3]} \nPorcentaje: {jugador[4]}%")
            print("-"*40)
    else:
        print("No hay jugadores existentes")

# -----  U -----

def actualizar_jugador():
    limpiar_pantalla()
    id_jugador = int(input("ID del jugador a actualizar: "))
    
    print("\n¿Qué deseas actualizar?")
    print("1. Nombre")
    print("2. Vida")
    print("3. Dinero")
    print("4. Porcentaje")
    op = int(input("\nElige una opción: "))
    match op:
        case 1:
            nuevo_valor = input("Nuevo nombre: ")
            cursor.execute("UPDATE jugadores SET nombre = ? WHERE id_jugador = ?", (nuevo_valor, id_jugador))
        case 2:
            nuevo_valor = int(input("Nueva vida: "))
            cursor.execute("UPDATE jugadores SET vida = ? WHERE id_jugador = ?", (nuevo_valor, id_jugador))
        case 3:
            nuevo_valor = int(input("Nuevo monto de dinero: "))
            cursor.execute("UPDATE jugadores SET dinero = ? WHERE id_jugador = ?", (nuevo_valor, id_jugador))
        case 4:
            nuevo_valor = float(input("Nuevo porcentaje alcanzado: "))
            cursor.execute("UPDATE jugadores SET porcentaje = ? WHERE id_jugador = ?", (nuevo_valor, id_jugador))
        case _:
            print("----- OPCIÓN NO VALIDA -----")
            print("----- INTENTELO NUEVAMENTE -----")
            time.sleep(4)
            return
    conexion.commit()
    print("\n===== jugador actualizado correctamente =====")

# -----  D -----

def eliminar_jugador():
    limpiar_pantalla()
    id_jugador = int(input("ID del jugador a eliminar: "))
    print("¿Estas seguro que quieres eliminar este jugador? (si/no)")
    op = str(input(": ")).lower()
    if op == "si":
        cursor.execute("DELETE FROM jugadores WHERE id_jugador =?", (id_jugador,))
    else:
        print("===== jugador no eliminado =====")
        time.sleep(4)
        return
    conexion.commit()
    print("===== Jugador eliminado correctamente =====")

# ===== CHECKPOINT 2 =====
# ===== INVENTARIO =====
# -----  C -----

def agregar_inventario():
    limpiar_pantalla()
    print("=== Agregar Ítem al Inventario ===")
    
    id_jugador = int(input("ID del jugador: "))
    nombre = input("Nombre del ítem: ")
    poder = float(input("Poder del ítem (1 a 10): "))
    uso = input("¿Uso permanente o limitado? (permanente/limitado): ").lower()
    
    if uso == "limitado":
        cantidad = int(input("cuanta cantidad de ese objeto tienes?: "))
    else:
        cantidad = None
    
    cursor.execute("INSERT INTO inventario (nombre, poder, uso, cantidad, id_jugador) VALUES (?, ?, ?, ?, ?)",
              (nombre, poder, uso, cantidad, id_jugador))
    conexion.commit()
    print(f"\nÍtem '{nombre}' agregado correctamente.")

# ===== R =====

def listar_inventario():  
    limpiar_pantalla()
    print("===== Lista de Items =====")
    cursor.execute("SELECT * FROM inventario")
    items = cursor.fetchall()
    if items:
        print("-"*40)
        for item in items:
            print(f"ID: {item[0]} \nNombre: {item[1]} \nPoder: {item[2]} \nUso: {item[3]} \nCantidad: {item[4]}")
            print("-"*40)
    else:
        print("No hay items existentes")

# ===== U =====

def actualizar_inventario():
    limpiar_pantalla()
    id_item = int(input("ID del item a actualizar: "))
    
    print("\n¿Qué deseas actualizar?")
    print("1. Nombre")
    print("2. Poder")
    print("3. Uso")
    print("4. Cantidad")
    op = int(input("\nElige una opción: "))
    match op:
        case 1:
            nuevo_valor = input("Nuevo nombre: ")
            cursor.execute("UPDATE inventario SET nombre = ? WHERE id_inventario = ?", (nuevo_valor, id_item))
        case 2:
            nuevo_valor = int(input("Nuevo poder: "))
            cursor.execute("UPDATE inventario SET poder = ? WHERE id_inventario = ?", (nuevo_valor, id_item))
        case 3:
            nuevo_valor = int(input("Nuevo tipo de uso: "))
            cursor.execute("UPDATE inventario SET uso = ? WHERE id_inventario = ?", (nuevo_valor, id_item))
        case 4:
            nuevo_valor = float(input("Nueva cantidad: "))
            cursor.execute("UPDATE inventario SET cantidad = ? WHERE id_inventario = ?", (nuevo_valor, id_item))
        case _:
            print("----- OPCIÓN NO VALIDA -----")
            print("----- INTENTELO NUEVAMENTE -----")
            time.sleep(4)
            return
    conexion.commit()
    print("\n===== item actualizado correctamente =====")

# ===== D =====

def eliminar_inventario():
    limpiar_pantalla()
    id_item = int(input("ID del item a eliminar: "))
    cursor.execute("SELECT * FROM inventario WHERE id_inventario = ?", (id_item,))
    item = cursor.fetchone()
    print(f"¿Estas seguro que quieres eliminar el item {item[1]}? (si/no)")
    op = str(input(": ")).lower()
    if op == "si":
        cursor.execute("DELETE FROM inventario WHERE id_inventario =?", (id_item,))
    else:
        print("===== Item no eliminado =====")
        time.sleep(4)
        return
    conexion.commit()
    print("===== Item Eliminado Correctamente =====")

# ===== CHECKPOINT 3 =====
# ===== C =====
def agregar_habilidad():
    limpiar_pantalla()
    print("==== Agregar Habilidad ====")
    id_jugador = int(input("ID del jugador: "))
    nombre = input("Nombre de la habilidad: ")
    elemento = input("Elemento de la habilidad: ")
    nivel = int(input("Nivel de la habilidad: "))
    desbloqueada = input("¿Está desbloqueada? (si/no): ").lower()
    if desbloqueada == "si":
        desbloqueada = "si"
    else:
        desbloqueada = "no"
    elementos_compatibles = input("Elementos compatibles (separados por coma): ")
    
    cursor.execute("INSERT INTO habilidades (nombre, elemento, nivel, desbloqueada, elementos_compatibles, id_jugador) VALUES (?, ?, ?, ?, ?, ?)",
              (nombre, elemento, nivel, desbloqueada, elementos_compatibles, id_jugador))
    conexion.commit()
    print(f"\nHabilidad '{nombre}' agregada correctamente.")

# ===== R =====

def listar_habilidad():  
    limpiar_pantalla()
    print("===== Lista de Habilidad =====")
    cursor.execute("SELECT * FROM habilidades")
    habilidades = cursor.fetchall()
    if habilidades:
        print("-"*40)
        for habilidad in habilidades:
            print(f"ID: {habilidad[0]} \nNombre: {habilidad[1]} \nElemento: {habilidad[2]} \nNivel: {habilidad[3]} \nDesbloqueada: {habilidad[4]} \nElementos compatibles: {habilidad[5]}")
            print("-"*40)
    else:
        print("No hay habilidades existentes")

# ===== U =====

def actualizar_habilidad():
    limpiar_pantalla()
    id_poder = int(input("ID de la habilidad a actualizar: "))
    
    print("\n¿Qué deseas actualizar?")
    print("1. Nombre")
    print("2. Elemento")
    print("3. Nivel")
    print("4. Desbloqueado")
    print("5. Elementos compatibles")
    op = int(input("\nElige una opción: "))
    match op:
        case 1:
            nuevo_valor = input("Nuevo nombre: ")
            cursor.execute("UPDATE habilidades SET nombre = ? WHERE id_habilidades = ?", (nuevo_valor, id_poder))
        case 2:
            nuevo_valor = input("Nuevo elemento: ")
            cursor.execute("UPDATE habilidades SET elemento = ? WHERE id_habilidades = ?", (nuevo_valor, id_poder))
        case 3:
            nuevo_valor = int(input("Nuevo nivel: "))
            cursor.execute("UPDATE habilidades SET nivel = ? WHERE id_habilidades = ?", (nuevo_valor, id_poder))
        case 4:
            nuevo_valor = input("¿Esta desbloqueado?(si/no): ").lower()
            if nuevo_valor == "si" or nuevo_valor == "no":
                cursor.execute("UPDATE habilidades SET desbloqueada = ? WHERE id_habilidades = ?", (nuevo_valor, id_poder))
            else:
                print("Respuesta no valida")
                return
        case 5:
            nuevo_valor = float(input("Nuevos elementos compatibles: "))
            cursor.execute("UPDATE habilidades SET elementos_compatibles = ? WHERE id_habilidades = ?", (nuevo_valor, id_poder))
        case _:
            print("----- OPCIÓN NO VALIDA -----")
            print("----- INTENTELO NUEVAMENTE -----")
            time.sleep(4)
            return
    conexion.commit()
    print("\n===== habilidad actualizada correctamente =====")

# ===== D =====

def eliminar_habilidad():
    limpiar_pantalla()
    id_poder = int(input("ID del item a eliminar: "))
    cursor.execute("SELECT * FROM habilidades WHERE id_habilidades = ?", (id_poder,))
    poder = cursor.fetchone()
    print(f"¿Estas seguro que quieres eliminar la habilidad {poder[1]}? (si/no)")
    op = str(input(": ")).lower()
    if op == "si":
        cursor.execute("DELETE FROM habilidades WHERE id_habilidades =?", (id_poder,))
    else:
        print("===== Habilidad no eliminado =====")
        time.sleep(4)
        return
    conexion.commit()
    print("===== Habilidad Eliminado Correctamente =====")

eliminar_habilidad()


# agregar el 'time.sleep' a los que requieran