import streamlit as st
import pandas as pd

# Configuración del título y logos
st.set_page_config(page_title="Algoritmos para detección de isquemia miocárdica aguda en pacientes con dolor torácico agudo y BRIHH")

# Cargar los logos locales
logo_izquierdo = "logo_izquierdo.png"
logo_derecho = "logo_derecho.png"

# Crear columnas para los logos y el título
col1, col2, col3 = st.columns([1, 4, 1])
with col1:
    st.image(logo_izquierdo, use_column_width=False, width=150)
with col2:
    st.title("Algoritmos para detección de isquemia miocárdica aguda en pacientes con dolor torácico agudo y BRIHH nuevo o presumiblemente nuevo")
    st.caption("Autor: Javier A. Rodríguez, MD, MSc")
with col3:
    st.image(logo_derecho, use_column_width=False, width=150)

# Funciones para los algoritmos
def sgarbossa_criteria():
    st.header("Criterios de Sgarbossa")
    score = 0
    if st.checkbox("Elevación del ST ≥ 1 mm concordante con el QRS en cualquier derivación"):
        score += 5
    if st.checkbox("Depresión del ST ≥ 1 mm en V1, V2 o V3"):
        score += 3
    if st.checkbox("Elevación del ST ≥ 5 mm discordante con el QRS en cualquier derivación"):
        score += 2
    st.write(f"**Puntuación Total Sgarbossa:** {score}")
    return score

def smith_modified_sgarbossa():
    st.header("Criterios Modificados de Sgarbossa (Smith)")
    if st.checkbox("Elevación del ST ≥ 1 mm concordante con el QRS en cualquier derivación"):
        return True
    if st.checkbox("Depresión del ST ≥ 1 mm en V1, V2 o V3"):
        return True
    if st.checkbox("Relación ST/S ≤ -0.25 indicando discordancia excesiva del ST"):
        return True
    return False

def barcelona_algorithm():
    st.header("Algoritmo de Barcelona")
    if st.checkbox("Desviación del ST ≥ 1 mm concordante con la polaridad del QRS en cualquier derivación"):
        return True
    if st.checkbox("Desviación del ST ≥ 1 mm discordante con la polaridad del QRS y R|S máximo ≤ 6 mm"):
        return True
    return False

# Obtener respuestas y calcular métricas
score_sgarbossa = sgarbossa_criteria()
is_smith_positive = smith_modified_sgarbossa()
is_barcelona_positive = barcelona_algorithm()

# Presentación del cuadro comparativo
def calcular_metricas():
    data = {
        "Algoritmo": ["Sgarbossa", "Modified Sgarbossa", "Barcelona"],
        "Probabilidad Post-test (%)": [33, 80, 93],
        "Sensibilidad (%)": [33, 80, 93],
        "Especificidad (%)": [99, 99, 94],
        "LR+": [33/99, 80/99, 93/94],
        "LR-": [(100-33)/(100-99), (100-80)/(100-99), (100-93)/(100-94)],
        "Falsos Positivos": [1000 * 0.01, 1000 * 0.01, 1000 * 0.06],
        "Falsos Negativos": [1000 * 0.67, 1000 * 0.20, 1000 * 0.07]
    }
    df = pd.DataFrame(data)
    st.table(df)

if st.button("Calcular Métricas Diagnósticas"):
    calcular_metricas()
