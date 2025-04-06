import os
import streamlit as st
import pandas as pd
import gspread
import json
from google.oauth2.service_account import Credentials
from datetime import datetime  # Importar para manejar fechas y horas

# 📌 Configuración de Google Sheets
SHEET_NAME = "resultados_entrenadores"  # Cambia esto por el nombre de tu hoja de cálculo

# 📌 Función para conectar con Google Sheets
def conectar_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # ✅ Opción segura: Leer las credenciales desde variable de entorno
    json_key = os.getenv("GOOGLE_SHEETS_KEY_JSON")

    if not json_key:
        raise ValueError("No se encontró la variable de entorno 'GOOGLE_SHEETS_KEY_JSON'")

    info = json.loads(json_key)
    creds = Credentials.from_service_account_info(info, scopes=scope)
    cliente = gspread.authorize(creds)
    hoja = cliente.open(SHEET_NAME).sheet1
    return hoja

# 📌 Función para centrar los datos en Google Sheets
def centrar_datos_google_sheets():
    hoja = conectar_google_sheets()
    # Obtener el rango de datos
    num_filas = len(hoja.get_all_values())
    num_columnas = len(hoja.row_values(1))
    rango = f"A1:{chr(64 + num_columnas)}{num_filas}"  # Ejemplo: A1:D10
    # Aplicar formato centrado
    hoja.format(rango, {"horizontalAlignment": "CENTER"})

# 📌 Función para guardar datos en Google Sheets
def guardar_datos_google_sheets(nuevos_datos):
    hoja = conectar_google_sheets()
    # Convertir los datos a una lista en el orden correcto
    fila = [
        nuevos_datos["Fecha de Registro"],
        nuevos_datos["Nombre Entrenador"],
        nuevos_datos["Liga"],
        nuevos_datos["Documento de Identidad"],
        nuevos_datos["Evento"],
        nuevos_datos["Fecha"],
        nuevos_datos["Lugar"],
        nuevos_datos["Prueba"],
        nuevos_datos["Tipo de Función"],
        nuevos_datos["Oro"],
        nuevos_datos["Plata"],
        nuevos_datos["Bronce"],
        nuevos_datos["Posición 4-8"],
        nuevos_datos["Nombre Deportistas"],
    ]
    hoja.append_row(fila)  # Agregar la fila al final de la hoja
    centrar_datos_google_sheets()  # Centrar los datos

# 📌 Función para guardar datos (solo en Google Sheets)
def guardar_datos(nuevos_datos):
    guardar_datos_google_sheets(nuevos_datos)

# 📌 Diseño de la aplicación Streamlit
st.set_page_config(page_title="Encuesta Indeportes", page_icon="🏅", layout="wide")

# 📌 Mostrar el Logo
logo_path = "style/logo_indeportes_2025.jpg"
if os.path.exists(logo_path):
    st.image(logo_path, width=250)
else:
    st.warning(f"⚠ No se encontró el logo en {logo_path}")

st.title("🏆 Encuesta de Resultados - Indeportes Antioquia")
st.write("Registra los eventos deportivos y resultados de los entrenadores.")

# 📌 BLOQUE 1: INFORMACIÓN PERSONAL (visible directamente)
st.subheader("📌 **Bloque 1: Información Personal**")
col1, col2 = st.columns(2)
with col1:
    nombre_entrenador = st.text_input("Nombre Completo", key="nombre_entrenador")
    documento = st.text_input("Documento de Identidad", key="documento_entrenador")
with col2:
    liga = st.text_input("Liga", key="liga_entrenador")

# Línea debajo del Bloque 1
st.markdown("---")
st.markdown("### ESCOGER QUÉ INFORMACIÓN LLENAR")

# 📌 BLOQUE 2: EVENTOS NACIONALES
with st.expander("📌 **Bloque 2: Eventos Nacionales**"):
    tipo_evento_nac = st.selectbox("Evento Nacional", [
        "Juegos Nacionales",
        "Campeonato Nacional"
    ], key="evento_nacional")
    col1, col2 = st.columns(2)
    with col1:
        fecha_nac = st.date_input("Fecha del Evento", key="fecha_nacional")
        lugar_nac = st.text_input("Lugar del Evento", key="lugar_nacional")
    with col2:
        prueba_nac = st.text_input("Prueba en la que participó", key="prueba_nacional")
        tipo_funcion_nac = st.radio("Tipo de Función", ["Principal", "Asistente"], key="funcion_nacional")
    st.subheader("📌 Resultados")
    col1, col2 = st.columns(2)
    with col1:
        oro_nac = st.number_input("Medallas de Oro", min_value=0, step=1, key="oro_nacional")
        plata_nac = st.number_input("Medallas de Plata", min_value=0, step=1, key="plata_nacional")
    with col2:
        bronce_nac = st.number_input("Medallas de Bronce", min_value=0, step=1, key="bronce_nacional")
        posicion_nac = st.number_input("Posiciones 4-8", min_value=0, step=1, key="posicion_nacional")

    # 📌 Agregar múltiples nombres de deportistas
    st.subheader("📌 Deportistas")
    nombres_deportistas = []  # Lista para almacenar los nombres
    if "deportistas" not in st.session_state:
        st.session_state["deportistas"] = []

    # Mostrar los nombres ya agregados
    for i, deportista in enumerate(st.session_state["deportistas"]):
        st.text(f"{i + 1}. {deportista}")

    # Campo para agregar un nuevo deportista
    nuevo_deportista = st.text_input("Agregar Nombre del Deportista", key="nuevo_deportista")
    if st.button("Agregar Deportista"):
        if nuevo_deportista.strip():
            st.session_state["deportistas"].append(nuevo_deportista.strip())
            st.success(f"✅ Deportista '{nuevo_deportista}' agregado.")
        else:
            st.warning("⚠ Por favor, ingresa un nombre válido.")

    # Botón para limpiar la lista de deportistas
    if st.button("Limpiar Lista de Deportistas"):
        st.session_state["deportistas"] = []
        st.success("✅ Lista de deportistas limpiada.")

    if st.button("Guardar Evento Nacional"):
        guardar_datos({
            "Fecha de Registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Fecha con hora actual
            "Nombre Entrenador": nombre_entrenador,
            "Liga": liga,
            "Documento de Identidad": documento,
            "Evento": tipo_evento_nac,
            "Fecha": fecha_nac.strftime("%Y-%m-%d"),  # Solo la fecha
            "Lugar": lugar_nac,
            "Prueba": prueba_nac,
            "Tipo de Función": tipo_funcion_nac,
            "Oro": oro_nac,
            "Plata": plata_nac,
            "Bronce": bronce_nac,
            "Posición 4-8": posicion_nac,
            "Nombre Deportistas": ", ".join(st.session_state["deportistas"]),  # Unir nombres con comas
        })
        st.success("✅ Registro guardado correctamente")
        st.session_state["deportistas"] = []  # Limpiar la lista después de guardar

# 📌 BLOQUE 3: EVENTOS INTERNACIONALES - CICLO OLÍMPICO
with st.expander("📌 **Bloque 3: Eventos Internacionales - Ciclo Olímpico**"):
    tipo_evento_ciclo = st.selectbox("Evento Internacional", [
        "Juegos Suramericanos",
        "Juegos Panamericanos",
        "Juegos Olímpicos"
    ], key="evento_ciclo")
    col1, col2 = st.columns(2)
    with col1:
        fecha_ciclo = st.date_input("Fecha del Evento", key="fecha_ciclo")
        lugar_ciclo = st.text_input("Lugar del Evento", key="lugar_ciclo")
    with col2:
        prueba_ciclo = st.text_input("Prueba en la que participó", key="prueba_ciclo")
        tipo_funcion_ciclo = st.radio("Tipo de Función", ["Principal", "Asistente"], key="funcion_ciclo")
    st.subheader("📌 Resultados")
    col1, col2 = st.columns(2)
    with col1:
        oro_ciclo = st.number_input("Medallas de Oro", min_value=0, step=1, key="oro_ciclo")
        plata_ciclo = st.number_input("Medallas de Plata", min_value=0, step=1, key="plata_ciclo")
    with col2:
        bronce_ciclo = st.number_input("Medallas de Bronce", min_value=0, step=1, key="bronce_ciclo")
        posicion_ciclo = st.number_input("Posiciones 4-8", min_value=0, step=1, key="posicion_ciclo")

    # 📌 Agregar múltiples nombres de deportistas
    st.subheader("📌 Deportistas")
    if "deportistas_ciclo" not in st.session_state:
        st.session_state["deportistas_ciclo"] = []

    # Mostrar los nombres ya agregados
    for i, deportista in enumerate(st.session_state["deportistas_ciclo"]):
        st.text(f"{i + 1}. {deportista}")

    # Campo para agregar un nuevo deportista
    nuevo_deportista_ciclo = st.text_input("Agregar Nombre del Deportista", key="nuevo_deportista_ciclo")
    if st.button("Agregar Deportista - Ciclo"):
        if nuevo_deportista_ciclo.strip():
            st.session_state["deportistas_ciclo"].append(nuevo_deportista_ciclo.strip())
            st.success(f"✅ Deportista '{nuevo_deportista_ciclo}' agregado.")
        else:
            st.warning("⚠ Por favor, ingresa un nombre válido.")

    # Botón para limpiar la lista de deportistas
    if st.button("Limpiar Lista de Deportistas - Ciclo"):
        st.session_state["deportistas_ciclo"] = []
        st.success("✅ Lista de deportistas limpiada.")

    if st.button("Guardar Evento Internacional"):
        guardar_datos({
            "Fecha de Registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Nombre Entrenador": nombre_entrenador,
            "Liga": liga,
            "Documento de Identidad": documento,
            "Evento": tipo_evento_ciclo,
            "Fecha": fecha_ciclo.strftime("%Y-%m-%d"),
            "Lugar": lugar_ciclo,
            "Prueba": prueba_ciclo,
            "Tipo de Función": tipo_funcion_ciclo,
            "Oro": oro_ciclo,
            "Plata": plata_ciclo,
            "Bronce": bronce_ciclo,
            "Posición 4-8": posicion_ciclo,
            "Nombre Deportistas": ", ".join(st.session_state["deportistas_ciclo"]),
        })
        st.success("✅ Registro guardado correctamente.")

# 📌 BLOQUE 4: EVENTOS INTERNACIONALES - CAMPEONATOS
with st.expander("📌 **Bloque 4: Eventos Internacionales - Campeonatos**"):
    tipo_campeonato = st.selectbox("Campeonato Internacional", [
        "Campeonato Suramericano",
        "Campeonato Centroamericano",
        "Campeonato Panamericano",
        "Campeonato Mundial"
    ], key="evento_campeonato")
    col1, col2 = st.columns(2)
    with col1:
        fecha_camp = st.date_input("Fecha del Evento", key="fecha_campeonato")
        lugar_camp = st.text_input("Lugar del Evento", key="lugar_campeonato")
    with col2:
        prueba_camp = st.text_input("Prueba en la que participó", key="prueba_campeonato")
        tipo_funcion_camp = st.radio("Tipo de Función", ["Principal", "Asistente"], key="funcion_campeonato")
    st.subheader("📌 Resultados")
    col1, col2 = st.columns(2)
    with col1:
        oro_camp = st.number_input("Medallas de Oro", min_value=0, step=1, key="oro_campeonato")
        plata_camp = st.number_input("Medallas de Plata", min_value=0, step=1, key="plata_campeonato")
    with col2:
        bronce_camp = st.number_input("Medallas de Bronce", min_value=0, step=1, key="bronce_campeonato")
        posicion_camp = st.number_input("Posiciones 4-8", min_value=0, step=1, key="posicion_campeonato")

    # 📌 Agregar múltiples nombres de deportistas
    st.subheader("📌 Deportistas")
    if "deportistas_campeonato" not in st.session_state:
        st.session_state["deportistas_campeonato"] = []

    # Mostrar los nombres ya agregados
    for i, deportista in enumerate(st.session_state["deportistas_campeonato"]):
        st.text(f"{i + 1}. {deportista}")

    # Campo para agregar un nuevo deportista
    nuevo_deportista_campeonato = st.text_input("Agregar Nombre del Deportista", key="nuevo_deportista_campeonato")
    if st.button("Agregar Deportista - Campeonato"):
        if nuevo_deportista_campeonato.strip():
            st.session_state["deportistas_campeonato"].append(nuevo_deportista_campeonato.strip())
            st.success(f"✅ Deportista '{nuevo_deportista_campeonato}' agregado.")
        else:
            st.warning("⚠ Por favor, ingresa un nombre válido.")

    # Botón para limpiar la lista de deportistas
    if st.button("Limpiar Lista de Deportistas - Campeonato"):
        st.session_state["deportistas_campeonato"] = []
        st.success("✅ Lista de deportistas limpiada.")

    if st.button("Guardar Campeonato Internacional"):
        guardar_datos({
            "Fecha de Registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Nombre Entrenador": nombre_entrenador,
            "Liga": liga,
            "Documento de Identidad": documento,
            "Evento": tipo_campeonato,
            "Fecha": fecha_camp.strftime("%Y-%m-%d"),
            "Lugar": lugar_camp,
            "Prueba": prueba_camp,
            "Tipo de Función": tipo_funcion_camp,
            "Oro": oro_camp,
            "Plata": plata_camp,
            "Bronce": bronce_camp,
            "Posición 4-8": posicion_camp,
            "Nombre Deportistas": ", ".join(st.session_state["deportistas_campeonato"]),
        })
        st.success("✅ Registro guardado correctamente.")

