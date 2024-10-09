import streamlit as st
from PIL import Image

# Diccionario que contiene los valores de LoD y P99 para cada tipo de ensayo de troponina
ensayos_troponinas = {
    "T": {
        "LoD": 5,  # ng/L
        "P99_global": 14,  # ng/L
        "P99_hombres": 9,  # ng/L
        "P99_mujeres": 16,  # ng/L
    },
    "I": {
        "LoD": 2,  # pg/mL
        "P99_global": 28,  # pg/mL
        "P99_hombres": 17,  # pg/mL
        "P99_mujeres": 35,  # pg/mL
    }
}

# Función para validar y convertir el valor ingresado
def validar_valor_decimal(valor):
    try:
        if ',' in valor:
            st.error("Por favor, ingrese un número válido utilizando punto (.) para decimales.")
            return None
        return float(valor)
    except ValueError:
        st.error("Por favor, ingrese un número válido.")
        return None

# Función para convertir unidades
def convertir_unidades(valor, unidades):
    if unidades == "ng/mL":
        return valor * 1000  # Convertir de ng/mL a ng/L
    elif unidades == "pg/mL":
        return valor  # pg/mL es equivalente a ng/L en este caso
    return valor  # Si ya está en ng/L, no se convierte

# Función para calcular el delta entre dos valores
def calcular_y_mostrar_delta(valor_inicial, valor_final):
    delta = abs(valor_final - valor_inicial) / valor_inicial * 100
    st.write(f"Delta calculado: {delta:.2f}%")
    return delta

# Función para identificar el escenario correcto basado en el valor de troponina
def identificar_escenario(valor_inicial, lod, p99):
    if valor_inicial < lod:
        return "A"
    elif valor_inicial >= lod and valor_inicial < p99:
        return "B"
    elif valor_inicial >= p99 and valor_inicial < p99 * 5:
        return "C"
    else:
        return "D"

# Función para ejecutar el escenario A
def ejecutar_escenario_a():
    st.write("Ejecutando Escenario A...")
    st.write("Baja probabilidad de injuria miocárdica aguda.")
    st.write("No se necesita segunda troponina.")
    st.write("Considerar angina inestable u otros diagnósticos diferenciales.")

# Función para ejecutar el escenario B (LoD <= troponina < P99)
def ejecutar_escenario_b(valor_inicial, p99):
    st.write("Ejecutando Escenario B...")

    # Preguntar por las horas de evolución del dolor torácico
    horas_dolor_toracico = validar_valor_decimal(st.text_input("Ingrese el tiempo de evolución del dolor torácico (en horas):"))
    if horas_dolor_toracico is None:
        st.stop()

    # Si el tiempo es mayor o igual a 3 horas, baja probabilidad de injuria miocárdica aguda
    if horas_dolor_toracico >= 3:
        st.write("Baja probabilidad de injuria miocárdica aguda.")
        st.write("Baja probabilidad de infarto agudo al miocárdico.")
        st.write("Según los síntomas y el ECG, considerar angina inestable u otros diagnósticos diferenciales.")
    # Si el tiempo es menor a 3 horas, sugerir segunda troponina
    else:
        st.write("Tomar segunda troponina y reevaluar.")
        ejecutar_segunda_troponina(valor_inicial, p99)

# Función para ejecutar la segunda troponina y pasar al escenario B o C
def ejecutar_segunda_troponina(valor_inicial, p99):
    # Pedir segunda troponina
    st.write("Realizando segunda medición de troponina...")

    unidades_segunda = st.selectbox("Seleccione las unidades de la segunda Tnc AS:", ["ng/mL", "ng/L", "pg/mL"])
    valor_segunda_tnc = validar_valor_decimal(st.text_input("Ingrese el valor de la segunda Tnc AS:"))
    if valor_segunda_tnc is None:
        st.stop()

    valor_segunda_tnc_convertido = convertir_unidades(valor_segunda_tnc, unidades_segunda)
    delta = calcular_y_mostrar_delta(valor_inicial, valor_segunda_tnc_convertido)

    # Si la segunda troponina es mayor o igual al P99, ejecutar escenario C
    if valor_segunda_tnc_convertido >= p99:
        ejecutar_escenario_c(valor_inicial, p99, valor_segunda_tnc_convertido)
    else:
        ejecutar_escenario_b(valor_inicial, p99)

# Función para ejecutar el escenario C (P99 <= troponina < 5xP99)
def ejecutar_escenario_c(valor_inicial, p99, valor_segunda_tnc):
    st.write("Ejecutando Escenario C...")

    delta = calcular_y_mostrar_delta(valor_inicial, valor_segunda_tnc)

    # Alta probabilidad de injuria miocárdica solo si el delta >= 50% y la segunda troponina >= P99
    if delta >= 50 and valor_segunda_tnc >= p99:
        st.write("Alta probabilidad de injuria miocárdica aguda.")
        preguntar_sintomas_ecg()
    elif delta >= 50 and valor_segunda_tnc < p99:
        st.write("Delta >= 50%, pero la segunda troponina es menor al P99. Sugerir una tercera medición de troponina.")
        preguntar_tercera_troponina(valor_inicial, p99)
    elif delta >= 20 and valor_segunda_tnc >= p99:
        st.write("Delta entre 20% y 50%. Alta probabilidad de injuria miocárdica aguda.")
        preguntar_sintomas_ecg()
    else:
        st.write("Delta < 20% o segunda troponina < P99. Evaluar más muestras para confirmar el diagnóstico.")
        preguntar_tercera_troponina(valor_inicial, p99)

# Función para ejecutar el escenario D (troponina >= 5xP99)
def ejecutar_escenario_d():
    st.write("Ejecutando Escenario D...")
    st.write("Alta probabilidad de injuria miocárdica aguda.")
    preguntar_sintomas_ecg()

# Función para preguntar por la tercera troponina
def preguntar_tercera_troponina(valor_inicial, p99):
    tercera_tnc = st.radio("¿Desea realizar una tercera medición de troponina? (Recomendado solo para deltas limítrofes)", ["Sí", "No"])
    
    if tercera_tnc == "Sí":
        unidades_tercera = st.selectbox("Seleccione las unidades de la tercera Tnc AS:", ["ng/mL", "ng/L", "pg/mL"])
        valor_tercera_tnc = validar_valor_decimal(st.text_input("Ingrese el valor de la tercera Tnc AS:"))
        if valor_tercera_tnc is None:
            st.stop()

        valor_tercera_tnc_convertido = convertir_unidades(valor_tercera_tnc, unidades_tercera)
        delta_tercera = calcular_y_mostrar_delta(valor_inicial, valor_tercera_tnc_convertido)
        
        if delta_tercera >= 50 and valor_tercera_tnc_convertido >= p99:
            st.write("Alta probabilidad de injuria miocárdica aguda con la tercera muestra.")
            preguntar_sintomas_ecg()
        else:
            st.write("Baja probabilidad de injuria miocárdica aguda.")
    else:
        st.write("Baja probabilidad de injuria miocárdica aguda.")

# Función para preguntar por los síntomas y ECG
def preguntar_sintomas_ecg():
    sintomas_ecg = st.radio("¿Síntomas y/o ECG indicativos de isquemia miocárdica aguda?", ["Sí", "No"])
    if sintomas_ecg == "Sí":
        st.write("Alta probabilidad de Infarto agudo al miocardio No ST.")
    else:
        st.write("Considerar injuria miocárdica aguda no aterotrombótica.")

# **Función para mostrar el descargo de responsabilidad**
def mostrar_descargo_responsabilidad():
    st.markdown("""
    **Descargo de responsabilidad**

    Al utilizar esta herramienta, usted acepta que cualquier decisión o tratamiento médico se basará en una evaluación clínica completa y no únicamente en el uso de esta herramienta.

    La herramienta está destinada a ser utilizada únicamente por médicos cardiólogos y médicos de urgencias. Ninguna persona debe entender ni utilizar la información contenida en este documento como sustituto de la obtención de asesoramiento o tratamiento médico profesional.

    El uso de esta herramienta es bajo su propio riesgo. El Instituto del Corazón de Bucaramanga S.A. no se responsabiliza de cualquier decisión o acción tomada basándose en la información contenida o proporcionada por esta herramienta.
    """)

    if st.radio("¿Acepta los términos del descargo de responsabilidad?", ["Sí", "No"]) == "No":
        st.write("Gracias por su interés en la aplicación.")
        st.stop()

# Función principal para ejecutar el algoritmo completo
def main():
    # Cargar las imágenes desde el directorio local
    logo_1 = Image.open('logo1.png')
    logo_2 = Image.open('logo2.png')

    # Títulos y logos
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.image(logo_1, width=100)  # Mostrar imagen local
        
    with col2:
        st.title("Versión de prueba - Algoritmo 0-3/h de hs cTn I (Abbott/Architect)")
        st.subheader("Autor: Javier Armando Rodriguez Prada. MD- MSc.")
        st.markdown("Unidad de Investigación y Educación - Instituto del Corazón de Bucaramanga.")
    
    with col3:
        st.image(logo_2, width=150)  # Mostrar otra imagen local

    # Mostrar descargo de responsabilidad
    mostrar_descargo_responsabilidad()

    # Preguntar si hay elevación del segmento ST
    st_segmento_st = st.radio("¿Hay elevación del segmento ST?", ["Sí", "No"])
    if st_segmento_st == "Sí":
        st.write("IAMEST (A1.1). Seguir las directrices de tratamiento de las guías vigentes para SCA ST.")
        st.stop()

    # Flujo del algoritmo cuando NO hay elevación del segmento ST
    tipo_ensayo = st.selectbox("Seleccione el tipo de ensayo de troponina", ["T", "I"])
    referencia_p99 = st.selectbox("Seleccione el P99 de referencia", ["Global", "Hombre", "Mujer"])
    
    ensayo = ensayos_troponinas[tipo_ensayo]
    p99 = ensayo[f"P99_{referencia_p99.lower()}"]
    lod = ensayo["LoD"]

    # Primera medición de troponina
    unidades_primera = st.selectbox("Seleccione las unidades de la primera Tnc AS:", ["ng/mL", "ng/L", "pg/mL"])
    valor_primera_tnc = validar_valor_decimal(st.text_input("Ingrese el valor de la primera Tnc AS:"))
    if valor_primera_tnc is None:
        st.stop()

    valor_primera_tnc_convertido = convertir_unidades(valor_primera_tnc, unidades_primera)

    # **Preguntar siempre por el tiempo de evolución del dolor torácico**
    horas_dolor_toracico = validar_valor_decimal(st.text_input("Ingrese el tiempo de evolución del dolor torácico (en horas):"))
    if horas_dolor_toracico is None:
        st.stop()

    # Identificar el escenario correcto
    escenario = identificar_escenario(valor_primera_tnc_convertido, lod, p99)

    # Ejecutar el escenario correcto
    if escenario == "A":
        ejecutar_escenario_a()
    elif escenario == "B":
        ejecutar_escenario_b(valor_primera_tnc_convertido, p99)
    elif escenario == "C":
        ejecutar_escenario_c(valor_primera_tnc_convertido, p99, valor_primera_tnc_convertido)
    elif escenario == "D":
        ejecutar_escenario_d()

if __name__ == "__main__":
    main()
