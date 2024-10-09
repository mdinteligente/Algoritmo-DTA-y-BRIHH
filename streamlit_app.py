import streamlit as st

# Título de la aplicación
st.title("Algoritmo 0-3 de Troponinas Cardiacas de Alta Sensibilidad (Tnc AS)")

# Sección inicial de evaluación
st.header("Evaluación Clínica Inicial")
st.subheader("¿Hay elevación del segmento ST?")
st.markdown("Si hay elevación del ST, considere intervenciones como la ICP primaria o fibrinólisis.")

# Pregunta inicial
elevacion_st = st.radio("¿Hay elevación del ST?", ("Sí", "No"))

if elevacion_st == "Sí":
    st.error("IAM-ST. Considere ICP primaria o fibrinólisis.")
else:
    # Continuación del algoritmo para pacientes sin elevación del ST
    st.subheader("Evaluación de la Troponina Cardíaca (Tnc AS)")

    # Primera medición de Troponina
    primera_tn = st.number_input("Ingresa el valor de la primera Troponina (pg/mL):", min_value=0.0, step=0.1)

    # Definir valores de LoD y P99
    st.markdown("Valores de referencia de troponinas")
    lod = st.number_input("Límite de Detección (LoD) en pg/mL:", value=5.0)
    p99 = st.number_input("Percentil 99 (P99) en pg/mL:", value=14.0)

    if primera_tn < lod:
        st.info("Primera Tnc AS por debajo del LoD.")
        evolucion_dolor = st.radio("¿Evolución del dolor torácico mayor a 3 horas?", ("Sí", "No"))
        if evolucion_dolor == "Sí":
            # Se pide la segunda troponina
            segunda_tn = st.number_input("Segunda Troponina (pg/mL):", min_value=0.0, step=0.1)
            if segunda_tn < lod:
                st.success("Baja probabilidad de Infarto Agudo al Miocardio.")
            elif segunda_tn >= p99:
                st.warning("Alta probabilidad de injuria miocárdica aguda.")
            else:
                st.info("Realice la tercera medición.")
                tercera_tn = st.number_input("Tercera Troponina (pg/mL):", min_value=0.0, step=0.1)
                delta = tercera_tn - primera_tn
                if delta >= 0.5 * p99:
                    st.warning("Alta probabilidad de injuria miocárdica aguda (Delta >= 50% del P99).")
                else:
                    st.success("Baja probabilidad de injuria miocárdica aguda.")
        else:
            st.success("Baja probabilidad de injuria miocárdica aguda.")
    elif primera_tn >= lod and primera_tn < p99:
        st.info("Primera Tnc AS entre LoD y P99. Se requiere una segunda medición a las 3 horas.")
        segunda_tn = st.number_input("Segunda Troponina a las 3 horas (pg/mL):", min_value=0.0, step=0.1)
        
        if segunda_tn >= p99:
            st.warning("Alta probabilidad de injuria miocárdica aguda.")
        else:
            delta = segunda_tn - primera_tn
            if delta >= 0.5 * p99:
                st.warning("Alta probabilidad de injuria miocárdica aguda (Delta >= 50% del P99).")
            else:
                st.info("Realice la tercera medición y evalúe.")
                tercera_tn = st.number_input("Tercera Troponina (pg/mL):", min_value=0.0, step=0.1)
                delta_tercera = tercera_tn - primera_tn
                if delta_tercera >= 0.5 * p99:
                    st.warning("Alta probabilidad de injuria miocárdica aguda (Delta >= 50% del P99 entre tercera y primera).")
                else:
                    st.success("Baja probabilidad de infarto agudo al miocardio.")

    elif primera_tn >= p99:
        st.warning("Primera Troponina >= P99, alta probabilidad de injuria miocárdica aguda.")
        delta_5x = primera_tn >= 5 * p99
        if delta_5x:
            st.error("La Tnc AS es >= 5xP99. Alta probabilidad de infarto agudo.")
        else:
            segunda_tn = st.number_input("Segunda Troponina a las 3 horas (pg/mL):", min_value=0.0, step=0.1)
            delta = (segunda_tn - primera_tn) / primera_tn * 100
            if delta >= 20:
                st.warning("Delta >= 20%. Alta probabilidad de injuria miocárdica aguda.")
            else:
                st.info("Baja probabilidad de injuria miocárdica aguda.")
                tercera_tn = st.number_input("Tercera Troponina (pg/mL):", min_value=0.0, step=0.1)
                delta_tercera = tercera_tn - segunda_tn
                if delta_tercera >= 0.5 * p99:
                    st.warning("Delta >= 50% entre tercera y segunda. Alta probabilidad de injuria miocárdica aguda.")
                else:
                    st.success("Baja probabilidad de infarto agudo al miocardio.")
