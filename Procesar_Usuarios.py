import json
from datetime import datetime
from collections import defaultdict

#Es necesario crear tres funciones. Una función será la principal y usará las dos restantes para procesar los datos.

# FUNCIÓN PARA FORMATEAR LAS FECHAS POR "YYYY-MM-DD"
def formatear_fecha(fecha):

    # Diccionario que mapea los nombres de los meses en español a sus valores numéricos
    meses = {
        'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04', 
        'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08', 
        'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
    }

    # Divide la fecha en tres partes usando ' de ' como delimitador
    # Ejemplo: "10 de mayo de 1980" -> ["10", "mayo", "1980"]
    partes = fecha.split(' de ')

    # Construye la fecha en el formato 'YYYY-MM-DD'
    # partes[2] -> año, partes[1] -> mes en texto, partes[0] -> día
    # Utiliza el diccionario 'meses' para convertir el mes de texto a numérico
    # Convierte el día a un entero y luego a un string con dos dígitos (02d)
    return f"{partes[2]}-{meses[partes[1].lower()]}-{int(partes[0]):02d}"

# FUNCIÓN PARA CALCULAR LA EDAD ACTUAL
def calcular_edad(fecha_nacimiento):

    # Convierte la cadena de texto 'fecha_nacimiento' al formato de fecha de Python (datetime)
    # Utiliza el formato 'YYYY-MM-DD' para la conversión
    fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")

    # Obtiene la fecha actual
    hoy = datetime.today()

    # Calcula la edad como la diferencia entre el año actual y el año de nacimiento
    # Si el mes y el día actuales son anteriores al mes y día de nacimiento, resta 1 a la edad

    #edad = hoy.year - fecha_nacimiento.year calcula la diferencia en años entre el año actual (hoy.year) y el año de nacimiento (fecha_nacimiento.year).
    #La expresión ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)) verifica si el mes y el día actuales son anteriores al mes y día de nacimiento:
    #(hoy.month, hoy.day) crea una tupla con el mes y día actuales.
    #(fecha_nacimiento.month, fecha_nacimiento.day) crea una tupla con el mes y día de nacimiento.
    #Si la tupla actual es menor que la tupla de nacimiento, significa que aún no se ha alcanzado el cumpleaños de este año, por lo que se resta 1 de la edad.
    #El resultado final es la edad actual, ajustada según si el cumpleaños ya ha ocurrido en el año actual.

    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

    # Devuelve la edad calculada
    return edad

# FUNCIÓN PRINCIPAL
def procesar_usuarios(json_data):

    # Crea un diccionario para almacenar usuarios únicos. 
    # Usamos defaultdict para inicializar automáticamente los saldos a 0.
    usuarios_unicos = defaultdict(lambda: {'saldo': 0})

    # Itera sobre cada usuario en los datos JSON
    for usuario in json_data:

        # Extrae el nombre completo, la fecha de nacimiento y el saldo del usuario actual
        nombre_completo = usuario['nombre_completo']
        fecha_nacimiento = formatear_fecha(usuario['fecha_nacimiento'])
        saldo = usuario['saldo']
        
        # Si el nombre completo ya está en el diccionario, suma el saldo
        if nombre_completo in usuarios_unicos:
            usuarios_unicos[nombre_completo]['saldo'] += saldo

        # Si el usuario es nuevo, separa el nombre completo en partes    
        else:
            nombre_parts = nombre_completo.split()
            nombre = nombre_parts[0]
            apellido_paterno = nombre_parts[1]
            apellido_materno = nombre_parts[2] if len(nombre_parts) > 2 else ""
            
            # Guarda los datos del usuario en el diccionario
            usuarios_unicos[nombre_completo] = {
                'nombre': nombre,
                'apellido_paterno': apellido_paterno,
                'apellido_materno': apellido_materno,
                'fecha_nacimiento': fecha_nacimiento,
                'edad': calcular_edad(fecha_nacimiento),
                'saldo': saldo
            }

    # Crea una lista para almacenar los usuarios procesados
    lista_usuarios = []

    # Itera sobre los datos de los usuarios únicos
    for datos in usuarios_unicos.values():

        # Construye un diccionario con los datos finales del usuario
        usuario = {
            "Nombre": datos['nombre'],
            "Apellido_Paterno": datos['apellido_paterno'],
            "Apellido_Materno": datos['apellido_materno'],
            "Fecha_Nacimiento": datos['fecha_nacimiento'],
            "Edad_Actual": datos['edad'],
            "Saldo_Actual": datos['saldo']
        }

        # Agrega el diccionario del usuario a la lista
        lista_usuarios.append(usuario)

        # Imprime los detalles del usuario en el formato especificado
        print(f"{usuario['Nombre']} {usuario['Apellido_Paterno']} {usuario['Apellido_Materno']} nació en {usuario['Fecha_Nacimiento']} tiene actualmente {usuario['Edad_Actual']} años y un saldo de {usuario['Saldo_Actual']} MXN")
        #print(f"{usuario['Nombre']} {usuario['Apellido_Paterno']} {usuario['Apellido_Materno']} es nuestro usuario estrella, nacido el {usuario['Fecha_Nacimiento']}. ¡Cumple {usuario['Edad_Actual']} años y tiene un impresionante saldo de {usuario['Saldo_Actual']} MXN!")

    # Devuelve la lista de usuarios procesados
    return lista_usuarios

# FUNCIO PARA LEER EL DOCUMENTO .JSON
# EJECUATAR LA FUNCIÓN PRINCIPAL

# Lectura del Archivo JSON: El script lee el archivo Saldos_Usuarios.json y carga su contenido en una variable.

if __name__ == "__main__":
    with open('Saldos_Usuarios.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    
    procesar_usuarios(json_data)
