import streamlit as st

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
        valor_float = float(valor)
        if valor_float <= 0:
            st.warning("Advertencia: La troponina ingresada es 0 o menor, verifique el valor.")
        return valor_float
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
    delta = (valor_final - valor_inicial) / valor_inicial * 100
    st.write(f"Delta calculado: {delta:.2f}%")
    return delta

# Función para identificar el escenario correcto basado en el valor de troponina
def identificar_escenario(valor_inicial, lod, p99):
    if valor_inicial < lod:
        return "B"  # Escenario B: troponina inicial menor al LoD
    elif valor_inicial >= lod and valor_inicial < p99:
        return "C"  # Escenario C: troponina inicial entre LoD y P99
    elif valor_inicial >= p99 and valor_inicial < p99 * 5:
        return "D1"  # Escenario D1: troponina inicial mayor o igual al P99 pero menor a 5xP99
    else:
        return "D2"  # Escenario D2: troponina inicial mayor o igual a 5xP99

# Función para ejecutar el escenario A (ST elevado)
def ejecutar_escenario_a():
    st.write("Elevación del segmento ST detectada.")
    st.write("IAM-ST. Seguir las directrices de tratamiento de las guías vigentes para SCA ST.")

# Función para ejecutar el escenario B (LoD <= troponina < P99, 3 o más horas de dolor)
def ejecutar_escenario_b(valor_inicial, lod, p99, horas_dolor_toracico):
    st.write("Ejecutando Escenario B...")

    if horas_dolor_toracico >= 3:
        st.write("Baja probabilidad de injuria miocárdica aguda.")
        st.write("No se necesita segunda troponina. Considerar otros diagnósticos.")
    else:
        st.write("Dolor menor a 3 horas. Evaluar segunda troponina.")
        ejecutar_segunda_troponina(valor_inicial, p99)

# Función para ejecutar la segunda troponina en escenario C o B con menos de 3 horas de dolor
def ejecutar_segunda_troponina(valor_inicial, p99):
    st.write("Realizando segunda medición de troponina...")

    unidades_segunda = st.selectbox("Seleccione las unidades de la segunda Tnc AS:", ["ng/mL", "ng/L", "pg/mL"], key="unidades_segunda")
    valor_segunda_tnc = validar_valor_decimal(st.text_input("Ingrese el valor de la segunda Tnc AS:", key="valor_segunda_tnc"))
    if valor_segunda_tnc is None:
        st.stop()

    valor_segunda_tnc_convertido = convertir_unidades(valor_segunda_tnc, unidades_segunda)
    delta = calcular_y_mostrar_delta(valor_inicial, valor_segunda_tnc_convertido)

    if delta >= 50 and valor_segunda_tnc_convertido >= p99:
        st.write("Alta probabilidad de injuria miocárdica aguda.")
        preguntar_sintomas_ecg()
    elif delta >= 50 and valor_segunda_tnc_convertido < p99:
        st.write("Delta >= 50%, pero la segunda troponina es menor al P99. Realizar una tercera medición a las 6 horas de la admisión.")
        preguntar_tercera_troponina(valor_inicial, p99)
    elif delta < 0:  # Si hay un delta negativo, considerar fase descendente
        st.write("Delta negativo. Considerar fase descendente de una injuria miocárdica previa.")
        st.write("Reevaluar los síntomas y ECG para definir la causa.")
        preguntar_sintomas_ecg()
    else:
        st.write("Delta < 50%. Evaluar más muestras para confirmar el diagnóstico.")
        preguntar_tercera_troponina(valor_inicial, p99)

# Función para ejecutar el escenario D1 (primera troponina >= P99 pero menor a 5xP99)
def ejecutar_escenario_d1(valor_inicial, p99):
    st.write("Primera troponina >= P99 pero menor a 5xP99.")
    st.write("Realizar segunda medición de troponina.")

    unidades_segunda = st.selectbox("Seleccione las unidades de la segunda Tnc AS:", ["ng/mL", "ng/L", "pg/mL"], key="unidades_segunda_d1")
    valor_segunda_tnc = validar_valor_decimal(st.text_input("Ingrese el valor de la segunda Tnc AS:", key="valor_segunda_tnc_d1"))
    if valor_segunda_tnc is None:
        st.stop()

    valor_segunda_tnc_convertido = convertir_unidades(valor_segunda_tnc, unidades_segunda)
    delta = calcular_y_mostrar_delta(valor_inicial, valor_segunda_tnc_convertido)

    if delta >= 20:
        st.write("Alta probabilidad de injuria miocárdica aguda.")
        preguntar_sintomas_ecg()
    elif delta < 0:
        st.write("Delta negativo. Considerar resolución de la injuria miocárdica previa.")
        preguntar_sintomas_ecg()
    else:
        st.write("Baja probabilidad de injuria miocárdica aguda.")
        preguntar_tercera_troponina(valor_inicial, p99)

# Función para ejecutar el escenario D2 (troponina >= 5xP99)
def ejecutar_escenario_d2():
    st.write("Primera troponina >= 5xP99.")
    st.write("Alta probabilidad de injuria miocárdica aguda.")
    preguntar_sintomas_ecg()

# Función para preguntar por la tercera troponina
def preguntar_tercera_troponina(valor_inicial, p99):
    tercera_tnc = st.radio("¿Desea realizar una tercera medición de troponina? (Recomendado solo para valores limítrofes)", ["Sí", "No"], key="tercera_tnc")
    
    if tercera_tnc == "Sí":
        unidades_tercera = st.selectbox("Seleccione las unidades de la tercera Tnc AS:", ["ng/mL", "ng/L", "pg/mL"], key="unidades_tercera")
        valor_tercera_tnc = validar_valor_decimal(st.text_input("Ingrese el valor de la tercera Tnc AS:", key="valor_tercera_tnc"))
        if valor_tercera_tnc is None:
            st.stop()

        valor_tercera_tnc_convertido = convertir_unidades(valor_tercera_tnc, unidades_tercera)
        delta_tercera = calcular_y_mostrar_delta(valor_inicial, valor_tercera_tnc_convertido)
        
        if delta_tercera >= 50 and valor_tercera_tnc_convertido >= p99:
            st.write("Alta probabilidad de injuria miocárdica aguda con la tercera muestra.")
            preguntar_sintomas_ecg()
        elif delta_tercera < 0:
            st.write("Delta negativo. Considerar resolución de la injuria miocárdica previa.")
            preguntar_sintomas_ecg()
        else:
            st.write("Baja probabilidad de injuria miocárdica aguda.")
    else:
        st.write("Baja probabilidad de injuria miocárdica aguda.")

# Función para preguntar por los síntomas y ECG
def preguntar_sintomas_ecg():
    sintomas_ecg = st.radio("¿Síntomas y/o ECG indicativos de isquemia miocárdica aguda?", ["Sí", "No"], key="sintomas_ecg")
    
    if sintomas_ecg == "Sí":
        st.write("Alta probabilidad de Infarto agudo al miocardio No ST.")
      
    else:
        st.write("Considerar injuria miocárdica aguda no aterotrombótica.")

# Función principal para ejecutar el algoritmo completo
def main():
    st.title("Versión de prueba - Algoritmo 0-3/h de hs cTn")
    st.subheader("Autor: Javier Armando Rodriguez Prada. MD- MSc.")
    st.markdown("Unidad de Investigación y Educación - Instituto del Corazón de Bucaramanga.")

    # Preguntar si hay elevación del segmento ST
    st_segmento_st = st.radio("¿Hay elevación del segmento ST?", ["Sí", "No"], key="st_segmento_st")
    if st_segmento_st == "Sí":
        ejecutar_escenario_a()
        st.stop()

    # Flujo del algoritmo cuando NO hay elevación del segmento ST
    tipo_ensayo = st.selectbox("Seleccione el tipo de ensayo de troponina", ["T", "I"], key="tipo_ensayo")
    referencia_p99 = st.selectbox("Seleccione el P99 de referencia", ["Global", "Hombres", "Mujeres"], key="referencia_p99")
    
    ensayo = ensayos_troponinas[tipo_ensayo]
    # Corregir para usar las claves del diccionario correctamente
    if referencia_p99 == "Global":
        p99 = ensayo["P99_global"]
    elif referencia_p99 == "Hombres":
        p99 = ensayo["P99_hombres"]
    elif referencia_p99 == "Mujeres":
        p99 = ensayo["P99_mujeres"]

    lod = ensayo["LoD"]

    # Primera medición de troponina
    unidades_primera = st.selectbox("Seleccione las unidades de la primera Tnc AS:", ["ng/mL", "ng/L", "pg/mL"], key="unidades_primera")
    valor_primera_tnc = validar_valor_decimal(st.text_input("Ingrese el valor de la primera Tnc AS:", key="valor_primera_tnc"))
    if valor_primera_tnc is None:
        st.stop()

    valor_primera_tnc_convertido = convertir_unidades(valor_primera_tnc, unidades_primera)

    # Preguntar por el tiempo de evolución del dolor torácico solo una vez
    horas_dolor_toracico = validar_valor_decimal(st.text_input("Ingrese el tiempo de evolución del dolor torácico (en horas):", key="horas_dolor"))
    if horas_dolor_toracico is None:
        st.stop()

    # Identificar el escenario correcto
    escenario = identificar_escenario(valor_primera_tnc_convertido, lod, p99)

    # Ejecutar el escenario correcto
    if escenario == "B":
        ejecutar_escenario_b(valor_primera_tnc_convertido, lod, p99, horas_dolor_toracico)
    elif escenario == "C":
        ejecutar_segunda_troponina(valor_primera_tnc_convertido, p99)
    elif escenario == "D1":
        ejecutar_escenario_d1(valor_primera_tnc_convertido, p99)
    elif escenario == "D2":
        ejecutar_escenario_d2()

if __name__ == "__main__":
    main()
