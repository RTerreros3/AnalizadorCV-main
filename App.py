import streamlit as st
import openai
from PyPDF2 import PdfReader

# Configuración del estilo y layout
st.set_page_config(
    page_title="Analizador de CV con ChatGPT",
    layout="wide",
)

# Estilos CSS personalizados
st.markdown("""
    <style>
        .big-font {
            font-size:18px !important;
        }
        .file-uploader {
            max-width: 600px;
        }
        .stButton > button {
            width: 150px;
            height: 40px;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)


# Configura tu clave de API de OpenAI aquí


# Función para leer el contenido del archivo PDF cargado
def leer_pdf(archivo):
    reader = PdfReader(archivo)
    num_pages = len(reader.pages)
    texto_cv = ''
    for page in range(num_pages):
        texto_cv += reader.pages[page].extract_text()
    return texto_cv

# Función para enviar el texto a ChatGPT
def enviar_a_chatgpt(api_key, texto, modelo="gpt-4-1106-preview", temperatura=0.7):
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "system", "content": """Como gerente de Recursos humanos de universidad particular mexicana, revisa el CV
                                              que te anexo [experiencia en universidades y en temas académicos], analiza el cv,
                                              genera cuatro tablas.
                                                La primera tabla “Medición de experiencia grados académicos y experiencia laboral” a

modo de rúbrica, colocar 0.5 si tiene Técnico superior universitario, coloca 1 punto si

tiene licenciatura, si tiene más de una licenciatura coloca .05, si tiene estudios de

especialidad coloca 2 puntos, si tiene más de un estudio de especialidad coloca 1

punto, si tiene un doctorado coloca 3 puntos si tiene más de un doctorado coloca 2

puntos, Si expone que habla inglés [idioma] colocar 1 punto, si expone que habla más

de dos idiomas colocar [dominio de más idiomas] 1.5 puntos, colocar 0 puntos si tiene

menos de un año de experiencia laboral, colocar 3 puntos si tiene experiencia de más de

un año y menos de 5 años de experiencia, colocar 5 puntos si tiene más de 6 años de

experiencia, entrega el reporte de análisis en una tabla [primera tabla] y con la

sumatoria de los puntos [colocar el resultado en la columna Puntos]
Segunda Tabla “Resumen de grados académicos” Analiza el CV y genera una tabla,

Columna A Grados académicos [Técnico superior universitario, licenciatura, ingeniería,

especialidad, posgrado, maestría, doctorado, otro] columna B El nombre del estudio, en

los rublos que no hay estudio realizado colocar ”N/A”
Tercera Tabla “Nivel educativo y materias de impartición”. Bajo el criterio que la

universidad imparte todo tipo de educación desde Bachillerato [preparatoria],

licenciatura y maestría Emite una tabla de correlación [nivel educativo y materia que

puede impartir] de las materias que puede impartir basado en su experiencia académica

y experiencia laboral y en que nivel educativo [bachillerato, licenciatura, maestría].

Cuarta Tabla “Información de contacto” Analiza el CV y genera una tabla, Columna 1:

ciudad que esta expuesta en el CV, Columna 2: número o números telefónicos de

contacto, columna 3: email, Columna 4: otros datos [en el caso que existan en el CV, como es Link de Linkedin, redes sociales, etc.] Por último, genera un resumen de su trayectoria como docente [si existe experiencia docente realizar el resumen y en caso que no existe experiencia docente indicar que “No hay experiencia docente”] Analiza el CV varias veces para que puedas emitir la información solicitada [las tablas y el resumen] ... [instrucciones completas]"""},
            {"role": "user", "content": texto}
        ],
        temperature=temperatura
    )
    return response.choices[0].message.content

# Interfaz de usuario de Streamlit
def main():
    st.title("Analizador de CV con ChatGPT")
        # Campo de entrada para la clave de API
    api_key = st.text_input("Ingresa tu clave de API de OpenAI", type="password")
    st.markdown("Carga un CV en formato PDF para analizarlo con la inteligencia de ChatGPT.", unsafe_allow_html=True)

    # Cargar archivo
    with st.container():
        archivo = st.file_uploader("Selecciona el archivo PDF", type=['pdf'], key="file_uploader")

    if archivo is not None and api_key:
        contenido_pdf = leer_pdf(archivo)
        if st.button('Analizar CV', key="analyze_button"):
            with st.spinner('Analizando...'):
                resultado = enviar_a_chatgpt(api_key, contenido_pdf)
                st.markdown(resultado, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
