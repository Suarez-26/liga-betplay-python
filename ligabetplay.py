import os

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    print("--- BIENVENIDO A LA LIGA BETPLAY ---")
    print("1. Registrar equipo")
    print("2. Registrar platilla de jugadores")
    print("3. Programar fecha")
    print("4. Registrar marcador de un partido")
    print("5. Ver equipo con más goles a favor")
    print("6. Ver equipo con más goles en contra")
    print("7. Ver tabla posiciones")
    print("8. Salir")

def ingresar_equipos(equipos):
    nombre = input("Ingrese el nombre del equipo: ")
    if nombre in equipos:
        print("El equipo ya está registrado.")
    elif nombre:
        equipos[nombre] = {'PJ':0,'PG':0, 'PE':0, 'PP':0, 'GF':0, 'GC':0}
        print(f"Equipo '{nombre}' registrado con éxito.")
    else:
        print("Error: El nombre del equipo no puede estar vacío.")


def registrar_plantilla(equipos):
    nombre_equipo = input("Introduce el nombre del equipo para registrar su plantilla: ").strip()

    if nombre_equipo not in equipos:
        print("Error: El equipo no está registrado.")
        return

    print(f"Registrando plantilla para el equipo {nombre_equipo}:")

    plantilla = []

    while True:
        print("\nRegistrando un nuevo jugador.")
        nombre_jugador = input("Introduce el nombre del jugador (o presiona 'Enter' para finalizar): ").strip()

        if nombre_jugador == "":
            break  

        dorsal = input(f"Introduce el dorsal de {nombre_jugador}: ").strip()
        posicion = input(f"Introduce la posición de {nombre_jugador}: ").strip()
        edad = input(f"Introduce la edad de {nombre_jugador}: ").strip()

        jugador = {"nombre": nombre_jugador,"dorsal": dorsal,"posicion": posicion,"edad": edad}

        plantilla.append(jugador)

    equipos[nombre_equipo]["plantilla"] = plantilla
    print(f"Plantilla de '{nombre_equipo}' registrada con éxito.")
    for jugador in plantilla:
        print(f"{jugador['nombre']} - Dorsal: {jugador['dorsal']}, Posición: {jugador['posicion']}, Edad: {jugador['edad']}, Centro Médico: {jugador['centro_medico']}")



def definir_encuentro(equipos, fechas):
    if len(equipos) < 2:
        print("Error: Debe haber al menos dos equipos registrados.")
        return
    local = input("Ingrese el nombre del equipo local: ")
    visitante = input("Ingrese el nombre del equipo visitante: ")
    fecha = input("Ingrese la fecha del partido: ")

    if local not in equipos or visitante not in equipos:
        print("Error: Uno o ambos equipos no están registrados.")
    elif local == visitante:
        print("Error: Un equipo no puede jugar contra sí mismo.")
    elif fecha =="":
        print("ingresa la fecha el partido")
    else:
        partido = {"local": local,"visitante": visitante,"fecha":fecha, "marcador_local": None,"marcador_visitante": None}
        fechas.append(partido)
        print(f"Partido '{local} vs {visitante}' programado con éxito para {fecha}.")

def registrar_marcador(equipos, fechas):
    pendientes = [p for p in fechas if p["marcador_local"] is None]
    if not pendientes:
        print("No hay partidos pendientes.")
        return

    print("Partidos pendientes:")
    for i, p in enumerate(pendientes):
        print(f"{i + 1}. {p['local']} vs {p['visitante']}")

    try:
        seleccion = int(input("Selecciona el número del partido: ")) - 1
        if 0 <= seleccion < len(pendientes):
            partido = pendientes[seleccion]
            goles_local = int(input(f"Goles de {partido['local']}: "))
            goles_visitante = int(input(f"Goles de {partido['visitante']}: "))

            partido["marcador_local"] = goles_local
            partido["marcador_visitante"] = goles_visitante

            local = partido["local"]
            visitante = partido["visitante"]

            equipos[local]["PJ"] += 1
            equipos[visitante]["PJ"] += 1
            equipos[local]["GF"] += goles_local
            equipos[visitante]["GF"] += goles_visitante
            equipos[local]["GC"] += goles_visitante
            equipos[visitante]["GC"] += goles_local

            if goles_local > goles_visitante:
                equipos[local]["PG"] += 1
                equipos[visitante]["PP"] += 1
            elif goles_visitante > goles_local:
                equipos[visitante]["PG"] += 1
                equipos[local]["PP"] += 1
            else:
                equipos[local]["PE"] += 1
                equipos[visitante]["PE"] += 1

            print("Marcador registrado con éxito.")
        else:
            print("Opción no válida.")
    except ValueError:
        print("Error: Debes introducir un número.")

def equipo_com_mas_goles_a_favor(equipos):
    if not equipos:
        print("No hay equipos registrados.")
        return
    equipo_max_GF = max(equipos, key=lambda e: equipos[e]['GF'])
    print(f"El equipo con más goles a favor es: {equipo_max_GF} ({equipos[equipo_max_GF]['GF']} goles).")

def equipo_com_mas_goles_contra(equipos):
    if not equipos:
        print("No hay equipos registrados.")
        return

    equipo_max_GC = max(equipos, key=lambda e: equipos[e]['GC'])
    print(f"El equipo con más goles en contra es: {equipo_max_GC} ({equipos[equipo_max_GC]['GC']} goles).")
def mostrar_tabla_posiciones(equipos):
    if not equipos:
        print("No hay equipos registrados.")
        return

    tabla = []
    for equipo, datos in equipos.items():
        dg = datos["GF"] - datos["GC"]
        pts = datos["PG"] * 3 + datos["PE"] * 1
        tabla.append({"Equipo": equipo,"PJ": datos["PJ"],"PG": datos["PG"],"PE": datos["PE"],"PP": datos["PP"],"GF": datos["GF"],"GC": datos["GC"],"DG": dg,"PTS": pts})

    tabla_ordenada = sorted(tabla, key=lambda x: (x["PTS"], x["DG"], x["GF"]), reverse = True)

    print("\nTABLA DE POSICIONES - Liga BetPlay")
    print("=" * 75)
    print(f"{'Pos':<4} {'Equipo':<20} {'PJ':<3} {'PG':<3} {'PE':<3} {'PP':<3} {'GF':<3} {'GC':<3} {'DG':<4} {'PTS':<4}")
    print("-" * 75)
    
    for idx, fila in enumerate(tabla_ordenada, 1):
        print(f"{idx:<4} {fila['Equipo']:<20} {fila['PJ']:<3} {fila['PG']:<3} {fila['PE']:<3} {fila['PP']:<3} {fila['GF']:<3} {fila['GC']:<3} {fila['DG']:<4} {fila['PTS']:<4}")
    print("=" * 75)

def mainMenu():
    equipos = {}
    calendario = []

    while True:
        limpiar_consola()
        mostrar_menu()
        opcion = input("Elige una opción: ")

        if opcion == '1':
            ingresar_equipos(equipos)
        elif opcion == '2':
            registrar_plantilla(equipos)
        elif opcion == '3':
            definir_encuentro(calendario, equipos)
        elif opcion == '4':
            registrar_marcador(equipos, calendario)
        elif opcion == '5':
            equipo_com_mas_goles_a_favor(equipos)
        elif opcion == '6':
            equipo_com_mas_goles_contra(equipos)
        elif opcion == '7':
            mostrar_tabla_posiciones(equipos)
        elif opcion == '8':
            print("Saliendo del programa. ¡Hasta pronto!")
        else:
            print("Opción no válida. Inténtalo de nuevo.")
        
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    mainMenu()
