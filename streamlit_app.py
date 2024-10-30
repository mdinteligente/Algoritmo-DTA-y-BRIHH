import streamlit as st
import pandas as pd

# Configuración del título y logos
st.set_page_config(page_title="Algoritmos para detección de isquemia miocárdica aguda en pacientes con dolor torácico agudo y BRIHH")

# Cargar los logos desde URLs (repositorio de GitHub)
logo_izquierdo = "https://github.com/mdinteligente/Algoritmo-DTA-y-BRIHH/blob/0c4c02744711b3f4093107f85d702883339ee703/logo_izquierdo.png?raw=true"
logo_derecho = "https://github.com/mdinteligente/Algoritmo-DTA-y-BRIHH/blob/0c4c02744711b3f4093107f85d702883339ee703/logo_derecho.jpg?raw=true"

# Crear columnas para los logos y el título
col1, col2, col3 = st.columns([1, 4, 1])
with col1:
    st.image(logo_izquierdo, use_column_width=False, width=150)
with col2:
    st.markdown("<h3 style='text-align: center;'>{}</h3>".format("Algoritmos para detección de isquemia miocárdica aguda en pacientes con dolor torácico agudo y BRIHH nuevo o presumiblemente nuevo"), unsafe_allow_html=True)
    st.caption("Autor: Javier A. Rodríguez, MD, MSc")
with col3:
    st.image(logo_derecho, use_column_width=False, width=100)

# Funciones para los algoritmos
def sgarbossa_criteria():
    st.header("Criterios de Sgarbossa")
    score = 0
    if st.checkbox("Elevación del ST ≥ 1 mm concordante con el QRS en cualquier derivación", key="sgarbossa_1"):
        st.image("https://github.com/mdinteligente/Algoritmo-DTA-y-BRIHH/blob/cf7a40979e11c8c01ffd1bc86091bc43e2b2b4d7/Desviacion%20positiva%20concordante.PNG ", caption="Elevación del ST concordante con el QRS")
        score += 5
    if st.checkbox("Depresión del ST ≥ 1 mm en V1, V2 o V3", key="sgarbossa_2"):
        st.image("https://github.com/mdinteligente/Algoritmo-DTA-y-BRIHH/blob/cf7a40979e11c8c01ffd1bc86091bc43e2b2b4d7/Desviacion%20negativa%20concordante.PNG ", caption="Depresión del ST en V1, V2 o V3")
        score += 3
    if st.checkbox("Elevación del ST ≥ 5 mm discordante con el QRS en cualquier derivación", key="sgarbossa_3"):
        st.image("https://github.com/mdinteligente/Algoritmo-DTA-y-BRIHH/blob/cf7a40979e11c8c01ffd1bc86091bc43e2b2b4d7/Desviacion%20mayor%20o%20igual%20a%205%20mm%20discordante.PNG ", caption="Elevación del ST discordante con el QRS")
        score += 2
    st.write(f"**Puntuación Total Sgarbossa:** {score}")
    return score

def smith_modified_sgarbossa():
    st.header("Criterios Modificados de Sgarbossa (Smith)")
    if st.checkbox("Elevación del ST ≥ 1 mm concordante con el QRS en cualquier derivación", key="smith_1"):
        st.image("https://github.com/mdinteligente/Algoritmo-DTA-y-BRIHH/blob/cf7a40979e11c8c01ffd1bc86091bc43e2b2b4d7/Desviacion%20positiva%20concordante.PNG ")
        return True
    if st.checkbox("Depresión del ST ≥ 1 mm en V1, V2 o V3", key="smith_2"):
        st.image("https://github.com/mdinteligente/Algoritmo-DTA-y-BRIHH/blob/cf7a40979e11c8c01ffd1bc86091bc43e2b2b4d7/Desviacion%20negativa%20concordante.PNG ", caption="Depresión del ST en V1, V2 o V3 (Smith)")
        return True
    if st.checkbox("Relación ST/S ≤ -0.25 indicando discordancia excesiva del ST", key="smith_3"):
        st.image("https://github.com/mdinteligente/Algoritmo-DTA-y-BRIHH/blob/f507334992da9b4d39deb2c0df68f3170f90c89e/Sgarbosa%20modificado.PNG", caption="Relación ST/S ≤ -0.25 (Smith)")
        return True
    return False

def barcelona_algorithm():
    st.header("Algoritmo de Barcelona")
    if st.checkbox("Desviación del ST ≥ 1 mm concordante con la polaridad del QRS en cualquier derivación", key="barcelona_1"):
        st.image("https://github.com/mdinteligente/Algoritmo-DTA-y-BRIHH/blob/main/figuras/barcelona_1.png?raw=true", caption="Desviación del ST concordante con la polaridad del QRS (Barcelona)")
        return True
    if st.checkbox("Desviación del ST ≥ 1 mm discordante con la polaridad del QRS y R|S máximo ≤ 6 mm", key="barcelona_2"):
        st.image("https://github.com/mdinteligente/Algoritmo-DTA-y-BRIHH/blob/main/figuras/barcelona_2.png?raw=true", caption="Desviación del ST discordante con la polaridad del QRS (Barcelona)")
        return True
    return False

# Obtener respuestas y calcular métricas
score_sgarbossa = sgarbossa_criteria()
is_smith_positive = smith_modified_sgarbossa()
is_barcelona_positive = barcelona_algorithm()

# Presentación del cuadro comparativo
def calcular_metricas():
    global df
    prevalencia = 0.4
    n_pacientes = 1000

    # Informar explícitamente la prevalencia
    st.info("Solo el 40% de los pacientes con dolor torácico agudo y BRIHH nuevo o presumiblente nuevo tiene isquemia miocárdica aguda (probabilidad pre-test)")

    # Datos de sensibilidad y especificidad
    sensibilidad = [0.33, 0.80, 0.93]
    especificidad = [0.99, 0.99, 0.94]

    # Cálculo de probabilidades post-test y métricas diagnósticas
    data = {
        "Algoritmo": ["Sgarbossa", "Modified Sgarbossa", "Barcelona"],
        "Probabilidad Post-test (%)": [round((sens * prevalencia) / ((sens * prevalencia) + ((1 - espec) * (1 - prevalencia))) * 100, 2) for sens, espec in zip(sensibilidad, especificidad)],
        "Sensibilidad (%)": [round(sens * 100, 2) for sens in sensibilidad],
        "Especificidad (%)": [round(espec * 100, 2) for espec in especificidad],
        "LR+": [round(sens / (1 - espec), 2) for sens, espec in zip(sensibilidad, especificidad)],
        "LR-": [round((1 - sens) / espec, 2) for sens, espec in zip(sensibilidad, especificidad)],
        "Falsos Positivos": [round(n_pacientes * (1 - espec) * (1 - prevalencia)) for espec in especificidad],
        "Falsos Negativos": [round(n_pacientes * (1 - sens) * prevalencia) for sens in sensibilidad]
    }
    df = pd.DataFrame(data)
    st.caption("Los valores de falsos positivos y falsos negativos están calculados para una muestra de 1000 pacientes.")
if st.button("Calcular Métricas Diagnósticas", key="calcular_metricas_btn"):
    calcular_metricas()
    st.table(df)
