import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# ============ CONFIGURACION ============
st.set_page_config(
    page_title="NutriLab",
    page_icon="N",
    layout="centered"
)

st.title("NutriLab")
st.subheader("Tu nutriologo digital basado en analisis clinicos")
st.write("---")

if "paso" not in st.session_state:
    st.session_state.paso = 1

# ============ PASO 1: BIENVENIDA ============
if st.session_state.paso == 1:
    st.markdown("""
    ### Bienvenido

    Esta app analiza tus resultados de laboratorio y te genera 
    recomendaciones alimenticias personalizadas.

    **Como funciona:**
    1. Ingresas tus datos basicos
    2. Introduces tus valores de laboratorio
    3. Recibes un plan alimenticio adaptado a ti
    """)
    st.info("Esta app es orientativa y no sustituye la consulta con un profesional de la salud.")
    if st.button("Comenzar", use_container_width=True):
        st.session_state.paso = 2
        st.rerun()

# ============ PASO 2: DATOS DEL PACIENTE ============
elif st.session_state.paso == 2:
    st.header("Datos del paciente")
    with st.form("form_datos"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre", value=st.session_state.get("nombre", ""))
            edad = st.number_input("Edad (años)", min_value=10, max_value=100, value=st.session_state.get("edad", 25))
        with col2:
            sexo = st.selectbox("Sexo", ["Masculino", "Femenino", "Otro"],
                                index=["Masculino", "Femenino", "Otro"].index(st.session_state.get("sexo", "Masculino")))
            peso = st.number_input("Peso (kg)", min_value=30.0, max_value=250.0,
                                   value=float(st.session_state.get("peso", 70.0)), step=0.5)
        talla = st.number_input("Talla (cm)", min_value=100.0, max_value=230.0,
                                value=float(st.session_state.get("talla", 170.0)), step=0.5)
        objetivo = st.selectbox("Objetivo principal", [
            "Bajar de peso", "Ganar masa muscular", "Mantener peso",
            "Mejorar salud metabolica",
            "Controlar una condicion (diabetes, colesterol, etc.)"
        ])
        enviado = st.form_submit_button("Guardar y continuar", use_container_width=True)
        if enviado:
            talla_m = talla / 100
            imc = peso / (talla_m ** 2)
            st.session_state.nombre = nombre
            st.session_state.edad = edad
            st.session_state.sexo = sexo
            st.session_state.peso = peso
            st.session_state.talla = talla
            st.session_state.imc = imc
            st.session_state.objetivo = objetivo
            st.session_state.paso = 3
            st.rerun()
    if st.button("Regresar"):
        st.session_state.paso = 1
        st.rerun()

# ============ PASO 3: RESUMEN ============
elif st.session_state.paso == 3:
    st.header("Datos guardados")
    st.success("Tu informacion se registro correctamente.")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Nombre", st.session_state.nombre or "Sin nombre")
        st.metric("Edad", f"{st.session_state.edad} años")
        st.metric("Sexo", st.session_state.sexo)
    with col2:
        st.metric("Peso", f"{st.session_state.peso} kg")
        st.metric("Talla", f"{st.session_state.talla} cm")
        st.metric("IMC", f"{st.session_state.imc:.1f}")
    imc = st.session_state.imc
    if imc < 18.5:
        st.warning("Tu IMC indica bajo peso.")
    elif imc < 25:
        st.success("Tu IMC esta en rango normal.")
    elif imc < 30:
        st.warning("Tu IMC indica sobrepeso.")
    else:
        st.error("Tu IMC indica obesidad.")
    st.write("---")
    st.info(f"Objetivo: {st.session_state.objetivo}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Regresar", use_container_width=True):
            st.session_state.paso = 2
            st.rerun()
    with col2:
        if st.button("Analisis de laboratorio", use_container_width=True, type="primary"):
            st.session_state.paso = 4
            st.rerun()

# ============ PASO 4: LABORATORIO ============
elif st.session_state.paso == 4:
    st.header("Analisis de laboratorio")
    st.write("Ingresa tus valores. Si no tienes alguno, deja el valor por defecto.")
    with st.form("form_lab"):
        st.markdown("##### Perfil metabolico")
        col1, col2 = st.columns(2)
        with col1:
            glucosa = st.number_input("Glucosa (mg/dL)", min_value=40.0, max_value=400.0, value=90.0, step=1.0)
            colesterol = st.number_input("Colesterol total (mg/dL)", min_value=80.0, max_value=500.0, value=170.0, step=1.0)
        with col2:
            hdl = st.number_input("Colesterol HDL (mg/dL)", min_value=10.0, max_value=150.0, value=55.0, step=1.0)
            ldl = st.number_input("Colesterol LDL (mg/dL)", min_value=20.0, max_value=400.0, value=100.0, step=1.0)
        trigliceridos = st.number_input("Trigliceridos (mg/dL)", min_value=30.0, max_value=800.0, value=130.0, step=1.0)

        st.markdown("##### Otros valores")
        col3, col4 = st.columns(2)
        with col3:
            hemoglobina = st.number_input("Hemoglobina (g/dL)", min_value=5.0, max_value=25.0, value=14.5, step=0.1)
            acido_urico = st.number_input("Acido urico (mg/dL)", min_value=1.0, max_value=15.0, value=5.0, step=0.1)
        with col4:
            vitamina_d = st.number_input("Vitamina D (ng/mL)", min_value=5.0, max_value=100.0, value=30.0, step=1.0)
            hierro = st.number_input("Hierro (ug/dL)", min_value=20.0, max_value=300.0, value=90.0, step=1.0)

        st.markdown("##### Funcion tiroidea, renal y metabolica")
        col5, col6, col7 = st.columns(3)
        with col5:
            tsh = st.number_input("TSH (mUI/L)", min_value=0.1, max_value=20.0, value=2.0, step=0.1)
        with col6:
            creatinina = st.number_input("Creatinina (mg/dL)", min_value=0.3, max_value=10.0, value=1.0, step=0.1)
        with col7:
            insulina = st.number_input("Insulina (uUI/mL)", min_value=1.0, max_value=100.0, value=10.0, step=1.0)

        enviado = st.form_submit_button("Analizar resultados", use_container_width=True)

        if enviado:
            st.session_state.glucosa = glucosa
            st.session_state.colesterol = colesterol
            st.session_state.hdl = hdl
            st.session_state.ldl = ldl
            st.session_state.trigliceridos = trigliceridos
            st.session_state.hemoglobina = hemoglobina
            st.session_state.acido_urico = acido_urico
            st.session_state.vitamina_d = vitamina_d
            st.session_state.hierro = hierro
            st.session_state.tsh = tsh
            st.session_state.creatinina = creatinina
            st.session_state.insulina = insulina
            st.session_state.paso = 5
            st.rerun()
    if st.button("Regresar"):
        st.session_state.paso = 3
        st.rerun()

# ============ PASO 5: RESULTADOS ============
elif st.session_state.paso == 5:
    st.header("Resultados de tu analisis")
    st.write(f"**Paciente:** {st.session_state.nombre} - {st.session_state.edad} años - {st.session_state.sexo}")

    # ============ SEMAFORO DE SALUD ============
    verdes = 0
    amarillos = 0
    rojos = 0

    # Glucosa
    g = st.session_state.glucosa
    if g < 70 or g > 125:
        rojos += 1
    elif g > 99:
        amarillos += 1
    else:
        verdes += 1

    # Colesterol
    c = st.session_state.colesterol
    if c >= 240:
        rojos += 1
    elif c >= 200:
        amarillos += 1
    else:
        verdes += 1

    # HDL
    h = st.session_state.hdl
    if h < 40:
        rojos += 1
    elif h < 60:
        amarillos += 1
    else:
        verdes += 1

    # LDL
    l = st.session_state.ldl
    if l >= 160:
        rojos += 1
    elif l >= 100:
        amarillos += 1
    else:
        verdes += 1

    # Trigliceridos
    t = st.session_state.trigliceridos
    if t >= 200:
        rojos += 1
    elif t >= 150:
        amarillos += 1
    else:
        verdes += 1

    # Hemoglobina
    hb = st.session_state.hemoglobina
    rango_hb = (13.5, 17.5) if st.session_state.sexo == "Masculino" else (12.0, 15.5)
    if hb < rango_hb[0] or hb > rango_hb[1]:
        amarillos += 1
    else:
        verdes += 1

    # Acido urico
    au = st.session_state.acido_urico
    if au > 7.2:
        rojos += 1
    elif au < 3.5:
        amarillos += 1
    else:
        verdes += 1

    # Vitamina D
    vd = st.session_state.vitamina_d
    if vd < 20:
        rojos += 1
    elif vd < 30:
        amarillos += 1
    else:
        verdes += 1

    # Hierro
    hi = st.session_state.hierro
    if hi < 60 or hi > 170:
        amarillos += 1
    else:
        verdes += 1

    # TSH
    tsh = st.session_state.tsh
    if tsh < 0.4 or tsh > 4.0:
        amarillos += 1
    else:
        verdes += 1

    # Creatinina
    cr = st.session_state.creatinina
    if cr < 0.7 or cr > 1.3:
        amarillos += 1
    else:
        verdes += 1

    # Insulina
    ins = st.session_state.insulina
    if ins < 2.6 or ins > 24.9:
        amarillos += 1
    else:
        verdes += 1

    total = verdes + amarillos + rojos
    porcentaje_salud = round((verdes / total) * 100)

    # Mostrar semaforo
    st.markdown("### Semaforo de salud")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("En rango", verdes)
    with col2:
        st.metric("En alerta", amarillos)
    with col3:
        st.metric("En riesgo", rojos)
    with col4:
        st.metric("Salud general", f"{porcentaje_salud}%")

    st.progress(porcentaje_salud / 100)

    if porcentaje_salud >= 80:
        st.success(f"Tu estado general de salud es BUENO ({porcentaje_salud}% de valores en rango).")
    elif porcentaje_salud >= 60:
        st.warning(f"Tu estado general es ACEPTABLE ({porcentaje_salud}%). Hay areas por mejorar.")
    else:
        st.error(f"Tu estado general requiere ATENCION ({porcentaje_salud}%). Consulta a un profesional.")

    st.write("---")
    st.markdown("### Interpretacion detallada de valores")

    # Glucosa
    if g < 70:
        st.warning(f"Glucosa: {g} mg/dL - BAJA (hipoglucemia)")
    elif g <= 99:
        st.success(f"Glucosa: {g} mg/dL - NORMAL")
    elif g <= 125:
        st.warning(f"Glucosa: {g} mg/dL - PREDIABETES")
    else:
        st.error(f"Glucosa: {g} mg/dL - DIABETES (consultar medico)")

    # Colesterol
    if c < 200:
        st.success(f"Colesterol total: {c} mg/dL - NORMAL")
    elif c < 240:
        st.warning(f"Colesterol total: {c} mg/dL - LIMITE ALTO")
    else:
        st.error(f"Colesterol total: {c} mg/dL - ALTO")

    # HDL
    if h >= 60:
        st.success(f"HDL (colesterol bueno): {h} mg/dL - OPTIMO")
    elif h >= 40:
        st.info(f"HDL (colesterol bueno): {h} mg/dL - ACEPTABLE")
    else:
        st.error(f"HDL (colesterol bueno): {h} mg/dL - BAJO (riesgo cardiovascular)")

    # LDL
    if l < 100:
        st.success(f"LDL (colesterol malo): {l} mg/dL - OPTIMO")
    elif l < 130:
        st.info(f"LDL (colesterol malo): {l} mg/dL - ACEPTABLE")
    elif l < 160:
        st.warning(f"LDL (colesterol malo): {l} mg/dL - LIMITE ALTO")
    else:
        st.error(f"LDL (colesterol malo): {l} mg/dL - ALTO")

    # Trigliceridos
    if t < 150:
        st.success(f"Trigliceridos: {t} mg/dL - NORMAL")
    elif t < 200:
        st.warning(f"Trigliceridos: {t} mg/dL - LIMITE ALTO")
    else:
        st.error(f"Trigliceridos: {t} mg/dL - ALTO")

    # Hemoglobina
    if hb < rango_hb[0]:
        st.warning(f"Hemoglobina: {hb} g/dL - BAJA (posible anemia)")
    elif hb > rango_hb[1]:
        st.warning(f"Hemoglobina: {hb} g/dL - ALTA")
    else:
        st.success(f"Hemoglobina: {hb} g/dL - NORMAL")

    # Acido urico
    if au < 3.5:
        st.info(f"Acido urico: {au} mg/dL - BAJO")
    elif au <= 7.2:
        st.success(f"Acido urico: {au} mg/dL - NORMAL")
    else:
        st.error(f"Acido urico: {au} mg/dL - ALTO (riesgo de gota)")

    # Vitamina D
    if vd < 20:
        st.error(f"Vitamina D: {vd} ng/mL - DEFICIENCIA")
    elif vd < 30:
        st.warning(f"Vitamina D: {vd} ng/mL - INSUFICIENTE")
    elif vd <= 100:
        st.success(f"Vitamina D: {vd} ng/mL - NORMAL")
    else:
        st.warning(f"Vitamina D: {vd} ng/mL - ALTA")

    # Hierro
    if hi < 60:
        st.warning(f"Hierro: {hi} ug/dL - BAJO")
    elif hi <= 170:
        st.success(f"Hierro: {hi} ug/dL - NORMAL")
    else:
        st.warning(f"Hierro: {hi} ug/dL - ALTO")

    # TSH
    if tsh < 0.4:
        st.warning(f"TSH: {tsh} mUI/L - BAJO (posible hipertiroidismo)")
    elif tsh <= 4.0:
        st.success(f"TSH: {tsh} mUI/L - NORMAL")
    else:
        st.error(f"TSH: {tsh} mUI/L - ALTO (posible hipotiroidismo)")

    # Creatinina
    if cr < 0.7:
        st.info(f"Creatinina: {cr} mg/dL - BAJO")
    elif cr <= 1.3:
        st.success(f"Creatinina: {cr} mg/dL - NORMAL")
    else:
        st.error(f"Creatinina: {cr} mg/dL - ALTO (revisar funcion renal)")

    # Insulina
    if ins < 2.6:
        st.info(f"Insulina: {ins} uUI/mL - BAJA")
    elif ins <= 24.9:
        st.success(f"Insulina: {ins} uUI/mL - NORMAL")
    else:
        st.error(f"Insulina: {ins} uUI/mL - ALTA (posible resistencia a la insulina)")

    # ============ GRAFICO DE BARRAS ============
    st.write("---")
    st.markdown("### Grafico de valores")

    # Datos para el grafico
    valores_grafico = [
        {"nombre": "Glucosa", "valor": g, "min": 70, "max": 99, "unidad": "mg/dL"},
        {"nombre": "Colesterol", "valor": c, "min": 0, "max": 199, "unidad": "mg/dL"},
        {"nombre": "HDL", "valor": h, "min": 40, "max": 60, "unidad": "mg/dL"},
        {"nombre": "LDL", "valor": l, "min": 0, "max": 99, "unidad": "mg/dL"},
        {"nombre": "Trigliceridos", "valor": t, "min": 0, "max": 149, "unidad": "mg/dL"},
        {"nombre": "Acido urico", "valor": au, "min": 3.5, "max": 7.2, "unidad": "mg/dL"},
        {"nombre": "Vitamina D", "valor": vd, "min": 30, "max": 100, "unidad": "ng/mL"},
        {"nombre": "TSH", "valor": tsh, "min": 0.4, "max": 4.0, "unidad": "mUI/L"},
        {"nombre": "Creatinina", "valor": cr, "min": 0.7, "max": 1.3, "unidad": "mg/dL"},
        {"nombre": "Insulina", "valor": ins, "min": 2.6, "max": 24.9, "unidad": "uUI/mL"},
    ]

    nombres = [v["nombre"] for v in valores_grafico]
    valores = [v["valor"] for v in valores_grafico]
    maximos = [v["max"] for v in valores_grafico]

    # Colores segun estado
    colores = []
    for v in valores_grafico:
        if v["valor"] < v["min"] or v["valor"] > v["max"]:
            if v["valor"] > v["max"] * 1.5 or v["valor"] < v["min"] * 0.5:
                colores.append("#d62728")  # rojo
            else:
                colores.append("#ff7f0e")  # naranja
        else:
            colores.append("#2ca02c")  # verde

    fig = go.Figure()

    # Barra de rango maximo (referencia)
    fig.add_trace(go.Bar(
        x=nombres,
        y=maximos,
        name="Rango maximo normal",
        marker_color="rgba(200, 200, 200, 0.3)",
        hoverinfo="skip"
    ))

    # Barra de valores actuales
    fig.add_trace(go.Bar(
        x=nombres,
        y=valores,
        name="Tus valores",
        marker_color=colores,
        text=[f"{v:.1f}" for v in valores],
        textposition="outside"
    ))

    fig.update_layout(
        title="Tus valores vs rango maximo normal",
        xaxis_title="Analito",
        yaxis_title="Valor",
        barmode="overlay",
        height=500,
        showlegend=True,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption("Verde = en rango normal | Naranja = fuera de rango | Rojo = valor critico")

    # ============ GRAFICO CIRCULAR DE MACROS ============
    st.write("---")
    st.markdown("### Distribucion de macronutrientes")

    peso_actual = st.session_state.peso
    talla_actual = st.session_state.talla
    edad_actual = st.session_state.edad
    sexo_actual = st.session_state.sexo
    objetivo_actual = st.session_state.objetivo

    if sexo_actual == "Masculino":
        tmb_calc = (10 * peso_actual) + (6.25 * talla_actual) - (5 * edad_actual) + 5
    else:
        tmb_calc = (10 * peso_actual) + (6.25 * talla_actual) - (5 * edad_actual) - 161

    tdee_calc = tmb_calc * 1.55

    if objetivo_actual == "Bajar de peso":
        cal_objetivo = tdee_calc - 500
        prot_g = peso_actual * 2.0
    elif objetivo_actual == "Ganar masa muscular":
        cal_objetivo = tdee_calc + 300
        prot_g = peso_actual * 1.8
    else:
        cal_objetivo = tdee_calc
        prot_g = peso_actual * 1.2

    gras_g = (cal_objetivo * 0.25) / 9
    cal_restantes = cal_objetivo - (prot_g * 4) - (gras_g * 9)
    carb_g = cal_restantes / 4

    # Grafico circular
    fig2 = go.Figure(data=[go.Pie(
        labels=["Proteinas", "Carbohidratos", "Grasas"],
        values=[prot_g * 4, carb_g * 4, gras_g * 9],
        hole=0.4,
        marker=dict(colors=["#1f77b4", "#ff7f0e", "#2ca02c"]),
        textinfo="label+percent",
        textfont=dict(size=14)
    )])

    fig2.update_layout(
        title=f"Distribucion calorica diaria (Total: {int(cal_objetivo)} kcal)",
        height=450,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.caption(f"Proteinas: {int(prot_g)}g | Carbohidratos: {int(carb_g)}g | Grasas: {int(gras_g)}g")


    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Regresar", use_container_width=True):
            st.session_state.paso = 4
            st.rerun()
    with col2:
        if st.button("Ver recomendaciones", use_container_width=True, type="primary"):
            st.session_state.paso = 6
            st.rerun()

# ============ PASO 6: RECOMENDACIONES ============
elif st.session_state.paso == 6:
    st.header("Recomendaciones alimenticias personalizadas")
    st.write(f"**Paciente:** {st.session_state.nombre}")

    hay_alertas = False

    # GLUCOSA ALTA
    if st.session_state.glucosa > 99:
        hay_alertas = True
        st.subheader("Control de glucosa")
        st.error("Tus niveles de glucosa estan elevados.")
        st.markdown("""
        **Alimentos recomendados:**
        - Avena integral, quinoa, arroz integral
        - Verduras de hoja verde (espinaca, acelga, kale)
        - Leguminosas (frijol, lenteja, garbanzo)
        - Frutas con bajo indice glucemico: manzana, pera, fresas, kiwi
        - Pescado (salmon, atun, sardina)
        - Nueces y almendras

        **Alimentos a evitar:**
        - Refrescos y jugos azucarados
        - Pan blanco, pasta refinada, arroz blanco
        - Dulces, galletas, pastelillos
        - Frutas muy dulces: mango, platano maduro, uva

        **Consejos:**
        - Come cada 3-4 horas
        - Acompana carbohidratos con proteina
        - Camina 30 minutos al dia
        """)

    # TRIGLICERIDOS ALTOS
    if st.session_state.trigliceridos > 150:
        hay_alertas = True
        st.subheader("Control de trigliceridos")
        st.error("Tus trigliceridos estan elevados.")
        st.markdown("""
        **Alimentos recomendados:**
        - Pescados ricos en omega-3: salmon, atun, sardina, macarela
        - Semillas de chia, linaza, nueces
        - Aceite de oliva extra virgen
        - Verduras y hortalizas variadas
        - Avena y cereales integrales
        - Leguminosas

        **Alimentos a evitar:**
        - Azucares refinados y miel
        - Harinas blancas
        - Bebidas alcoholicas
        - Frituras y comida rapida
        - Carnes rojas grasosas
        - Embutidos

        **Consejos:**
        - Reduce el azucar al minimo
        - Prefiere pescado sobre carne roja
        - Ejercicio aerobico 4-5 veces por semana
        """)

    # COLESTEROL / LDL ALTO
    if st.session_state.colesterol > 199 or st.session_state.ldl > 129:
        hay_alertas = True
        st.subheader("Control de colesterol")
        st.warning("Tus niveles de colesterol estan elevados.")
        st.markdown("""
        **Alimentos recomendados:**
        - Avena, cebada, salvado
        - Leguminosas (frijol, lenteja, garbanzo)
        - Frutas: manzana, pera, citricos, aguacate
        - Verduras y hortalizas
        - Frutos secos: nueces, almendras, pistachos
        - Aceite de oliva
        - Pescado azul

        **Alimentos a evitar:**
        - Carnes rojas y embutidos
        - Mantequilla, crema, queso amarillo
        - Yema de huevo en exceso
        - Frituras
        - Productos de panaderia industrial
        - Camarones y mariscos

        **Consejos:**
        - Aumenta la fibra soluble
        - Cocina al vapor, horno o plancha
        """)

    # HDL BAJO
    if st.session_state.hdl < 40:
        hay_alertas = True
        st.subheader("Aumentar colesterol bueno (HDL)")
        st.warning("Tu HDL esta bajo.")
        st.markdown("""
        **Alimentos recomendados:**
        - Aguacate
        - Aceite de oliva extra virgen
        - Pescado graso (salmon, sardina)
        - Nueces y almendras
        - Semillas de linaza y chia

        **Consejos:**
        - Ejercicio aerobico regular
        - Deja de fumar si fumas
        - Reduce azucares refinados
        """)

    # VITAMINA D BAJA
    if st.session_state.vitamina_d < 30:
        hay_alertas = True
        st.subheader("Vitamina D")
        st.error("Tienes deficiencia de vitamina D.")
        st.markdown("""
        **Alimentos recomendados:**
        - Pescados grasos: salmon, atun, sardina, macarela
        - Yema de huevo
        - Hongos expuestos al sol
        - Leche y yogur fortificados
        - Quesos madurados

        **Consejos:**
        - Exponte al sol 15-20 minutos al dia (brazos y cara)
        - Considera suplementacion (consulta a tu medico)
        - La mejor hora: antes de las 11 am o despues de las 4 pm
        """)

    # HEMOGLOBINA BAJA
    rango_hb = (13.5, 17.5) if st.session_state.sexo == "Masculino" else (12.0, 15.5)
    if st.session_state.hemoglobina < rango_hb[0]:
        hay_alertas = True
        st.subheader("Prevencion de anemia")
        st.warning("Tu hemoglobina esta baja.")
        st.markdown("""
        **Alimentos recomendados:**
        - Carnes rojas magras
        - Higado y visceras
        - Leguminosas (frijol, lenteja)
        - Verduras de hoja verde oscuro
        - Remolacha
        - Frutos secos

        **Consejos:**
        - Combina hierro con vitamina C (citricos) para mejor absorcion
        - Evita te y cafe junto a las comidas
        """)

    # ACIDO URICO ALTO
    if st.session_state.acido_urico > 7.2:
        hay_alertas = True
        st.subheader("Control de acido urico")
        st.error("Tu acido urico esta elevado (riesgo de gota).")
        st.markdown("""
        **Alimentos recomendados:**
        - Agua: al menos 2 litros al dia
        - Frutas: cereza, fresa, manzana
        - Verduras: apio, pepino, zanahoria
        - Cereales integrales
        - Lacteos bajos en grasa

        **Alimentos a evitar:**
        - Carnes rojas y visceras
        - Mariscos y pescados grasos
        - Cerveza
        - Refrescos con fructosa
        """)

    # TSH ALTO (hipotiroidismo)
    if st.session_state.tsh > 4.0:
        hay_alertas = True
        st.subheader("Funcion tiroidea (hipotiroidismo)")
        st.error("Tu TSH esta elevado, posible hipotiroidismo.")
        st.markdown("""
        **Alimentos recomendados:**
        - Sal yodada (con moderacion)
        - Pescados y mariscos
        - Algas marinas (nori, wakame)
        - Huevo
        - Lacteos
        - Nueces de Brasil (selenio)

        **Alimentos a evitar:**
        - Soya en grandes cantidades
        - Col, brocoli, coliflor crudos en exceso
        - Yuca cruda

        **Consejos:**
        - Consulta a un endocrinologo
        - No suspendas medicacion sin indicacion medica
        """)

    # CREATININA ALTA (funcion renal)
    if st.session_state.creatinina > 1.3:
        hay_alertas = True
        st.subheader("Funcion renal")
        st.error("Tu creatinina esta elevada.")
        st.markdown("""
        **Alimentos recomendados:**
        - Agua: 2-3 litros al dia
        - Frutas: manzana, pera, uva
        - Verduras: calabaza, zanahoria, ejotes
        - Cereales refinados en moderacion
        - Clara de huevo

        **Alimentos a evitar:**
        - Exceso de proteinas
        - Sal en exceso
        - Embutidos y conservas
        - Refrescos oscuros
        - Alimentos procesados

        **Consejos:**
        - Consulta a un nefrologo
        - Evita antiinflamatorios sin receta
        """)

    # INSULINA ALTA (resistencia)
    if st.session_state.insulina > 24.9:
        hay_alertas = True
        st.subheader("Resistencia a la insulina")
        st.error("Tu insulina esta elevada.")
        st.markdown("""
        **Alimentos recomendados:**
        - Vegetales no feculentos (espinaca, brocoli, pepino)
        - Proteinas magras (pollo, pescado, huevo)
        - Grasas saludables (aguacate, aceite de oliva, nueces)
        - Leguminosas
        - Frutos rojos
        - Avena y cereales integrales

        **Alimentos a evitar:**
        - Azucares y dulces
        - Harinas blancas y pan
        - Refrescos y jugos
        - Arroz blanco
        - Papas y platano maduro
        - Comida procesada

        **Consejos:**
        - Ejercicio: combina cardio y fuerza
        - Come cada 3-4 horas
        - Duerme bien (7-8 horas)
        - Consulta a un endocrinologo
        """)

    # SI TODO ESTA BIEN
    if not hay_alertas:
        st.success("Todos tus valores estan en rango normal. Manten tus habitos saludables.")
        st.markdown("""
        **Recomendaciones generales:**
        - Dieta balanceada con todos los grupos de alimentos
        - 5 porciones de frutas y verduras al dia
        - 2 litros de agua al dia
        - Ejercicio 30 minutos, 5 dias a la semana
        - Dormir 7-8 horas
        - Chequeo anual de laboratorio
        """)

    st.write("---")
    st.info("Estas recomendaciones son orientativas. Consulta a un nutriologo o medico para un plan personalizado.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Regresar", use_container_width=True):
            st.session_state.paso = 5
            st.rerun()
    with col2:
        if st.button("Ver menu del dia", use_container_width=True, type="primary"):
            st.session_state.paso = 7
            st.rerun()

# ============ PASO 7: MENU DE EJEMPLO ============
elif st.session_state.paso == 7:
    st.header("Menu de ejemplo de un dia")
    st.write(f"**Paciente:** {st.session_state.nombre} - Objetivo: {st.session_state.objetivo}")

    g = st.session_state.glucosa
    t = st.session_state.trigliceridos
    c = st.session_state.colesterol
    l = st.session_state.ldl
    h = st.session_state.hdl
    vd = st.session_state.vitamina_d
    hb = st.session_state.hemoglobina
    au = st.session_state.acido_urico
    tsh = st.session_state.tsh
    ins = st.session_state.insulina
    cr = st.session_state.creatinina

    rango_hb = (13.5, 17.5) if st.session_state.sexo == "Masculino" else (12.0, 15.5)

    # Personalizar menu segun valores
    notas_personalizadas = []
    if g > 99:
        notas_personalizadas.append("Control de glucosa: preferir carbohidratos de bajo indice glucemico")
    if t > 150:
        notas_personalizadas.append("Control de trigliceridos: aumentar omega-3, reducir azucares")
    if c > 199 or l > 129:
        notas_personalizadas.append("Control de colesterol: aumentar fibra soluble, reducir grasas saturadas")
    if h < 40:
        notas_personalizadas.append("Aumentar HDL: incluir aguacate, aceite de oliva, pescado graso")
    if vd < 30:
        notas_personalizadas.append("Vitamina D baja: incluir pescados grasos, huevo, lacteos fortificados")
    if hb < rango_hb[0]:
        notas_personalizadas.append("Anemia: incluir carnes magras, leguminosas, hojas verdes")
    if au > 7.2:
        notas_personalizadas.append("Acido urico alto: mucha agua, evitar carnes rojas y mariscos")
    if tsh > 4.0:
        notas_personalizadas.append("Hipotiroidismo: incluir yodo (sal yodada, pescado, algas), selenio (nueces de Brasil)")
    if ins > 24.9:
        notas_personalizadas.append("Resistencia a la insulina: reducir azucares y harinas refinadas, aumentar fibra y proteina")
    if cr > 1.3:
        notas_personalizadas.append("Funcion renal alterada: moderar proteinas, reducir sal, mucha agua")

    if notas_personalizadas:
        st.markdown("### Consideraciones para tu menu")
        for nota in notas_personalizadas:
            st.info(nota)

    st.write("---")
    st.markdown("### Menu sugerido")

    st.markdown("#### Desayuno (7:00 - 8:00 am)")
    st.markdown("""
    - 1 taza de avena cocida con leche descremada
    - 1 platano pequeno o 1 taza de fresas
    - 2 claras de huevo + 1 huevo entero revueltos
    - 1 cucharada de nueces picadas
    - Cafe o te sin azucar
    """)
    st.caption("Aporte aproximado: 400 kcal | 20g proteina | 50g carbohidratos | 12g grasas")

    st.markdown("#### Colacion media mañana (10:30 - 11:00 am)")
    st.markdown("""
    - 1 manzana o 1 pera
    - 15 almendras o nueces
    - 1 vaso de agua
    """)
    st.caption("Aporte aproximado: 180 kcal")

    st.markdown("#### Comida (1:00 - 2:00 pm)")
    st.markdown("""
    - 120g de pechuga de pollo asada o pescado al horno
    - 1 taza de arroz integral o quinoa
    - Ensalada verde grande (lechuga, espinaca, tomate, pepino)
    - 1/2 aguacate
    - Aderezo: aceite de oliva + limon
    - Agua natural
    """)
    st.caption("Aporte aproximado: 550 kcal | 35g proteina | 55g carbohidratos | 18g grasas")

    st.markdown("#### Colacion tarde (4:30 - 5:00 pm)")
    st.markdown("""
    - 1 yogurt natural sin azucar
    - 1 cucharada de semillas de chia
    - 1 taza de melon o sandia
    """)
    st.caption("Aporte aproximado: 150 kcal")

    st.markdown("#### Cena (7:30 - 8:30 pm)")
    st.markdown("""
    - 1 taza de sopa de verduras
    - 100g de salmon o atun al horno
    - Verduras al vapor (brocoli, zanahoria, calabaza)
    - 1 rebanada de pan integral
    - Te de manzanilla
    """)
    st.caption("Aporte aproximado: 400 kcal | 30g proteina | 30g carbohidratos | 15g grasas")
        # ============ CALCULO DE CALORIAS Y MACROS ============
    st.write("---")
    st.markdown("### Calculo personalizado de calorias y macros")

    # Nivel de actividad (widget)
    nivel_actividad = st.selectbox(
        "Selecciona tu nivel de actividad fisica:",
        [
            "Sedentario (poco o nada de ejercicio)",
            "Ligero (1-3 dias por semana)",
            "Moderado (3-5 dias por semana)",
            "Intenso (6-7 dias por semana)",
            "Muy intenso (atleta, 2 veces al dia)"
        ],
        key="nivel_actividad"
    )

    # Factores de actividad
    factores = {
        "Sedentario (poco o nada de ejercicio)": 1.2,
        "Ligero (1-3 dias por semana)": 1.375,
        "Moderado (3-5 dias por semana)": 1.55,
        "Intenso (6-7 dias por semana)": 1.725,
        "Muy intenso (atleta, 2 veces al dia)": 1.9
    }
    factor = factores[nivel_actividad]

    # TMB - Formula Mifflin-St Jeor
    peso_actual = st.session_state.peso
    talla_actual = st.session_state.talla
    edad_actual = st.session_state.edad
    sexo_actual = st.session_state.sexo

    if sexo_actual == "Masculino":
        tmb = (10 * peso_actual) + (6.25 * talla_actual) - (5 * edad_actual) + 5
    else:
        tmb = (10 * peso_actual) + (6.25 * talla_actual) - (5 * edad_actual) - 161

    # TDEE
    tdee = tmb * factor

    # Ajuste segun objetivo
    objetivo_actual = st.session_state.objetivo
    if objetivo_actual == "Bajar de peso":
        calorias_objetivo = tdee - 500
        nota_objetivo = "Deficit de 500 kcal para perder ~0.5 kg por semana"
    elif objetivo_actual == "Ganar masa muscular":
        calorias_objetivo = tdee + 300
        nota_objetivo = "Superavit de 300 kcal para ganar musculo limpio"
    else:
        calorias_objetivo = tdee
        nota_objetivo = "Calorias de mantenimiento"

    # Macros
    # Proteina: 1.8 g/kg para ganar musculo, 2.0 g/kg para bajar, 1.2 g/kg mantener
    if objetivo_actual == "Ganar masa muscular":
        proteina_g = peso_actual * 1.8
    elif objetivo_actual == "Bajar de peso":
        proteina_g = peso_actual * 2.0
    else:
        proteina_g = peso_actual * 1.2

    # Grasas: 25% de las calorias
    grasas_g = (calorias_objetivo * 0.25) / 9

    # Carbohidratos: el resto
    calorias_restantes = calorias_objetivo - (proteina_g * 4) - (grasas_g * 9)
    carbos_g = calorias_restantes / 4

    # Mostrar resultados
    st.markdown("#### Tus numeros diarios")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("TMB", f"{int(tmb)} kcal", help="Calorias que quemas en reposo")
    with col2:
        st.metric("TDEE", f"{int(tdee)} kcal", help="Calorias que quemas con tu actividad")
    with col3:
        st.metric("Objetivo diario", f"{int(calorias_objetivo)} kcal", help=nota_objetivo)

    st.caption(f"Nota: {nota_objetivo}")

    st.markdown("#### Distribucion de macronutrientes")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Proteinas", f"{int(proteina_g)} g", help="4 kcal por gramo")
    with col2:
        st.metric("Carbohidratos", f"{int(carbos_g)} g", help="4 kcal por gramo")
    with col3:
        st.metric("Grasas", f"{int(grasas_g)} g", help="9 kcal por gramo")

    # Explicacion
    st.info(f"""
    **Como interpretar esto:**
    - Debes consumir aproximadamente **{int(calorias_objetivo)} kcal** al dia
    - **{int(proteina_g)} g** de proteina (para {objetivo_actual.lower()})
    - **{int(carbos_g)} g** de carbohidratos
    - **{int(grasas_g)} g** de grasas saludables
    """)

    st.write("---")
    st.markdown("### Recomendaciones generales")
    st.markdown("""
    - **Agua:** minimo 2 litros al dia
    - **Ejercicio:** 30-45 minutos, 5 dias a la semana
    - **Sueno:** 7-8 horas diarias
    - **Comidas:** cada 3-4 horas, no saltarse ninguna
    - **Coccion:** al vapor, horno, plancha o crudo. Evitar frituras
    """)

    st.info("Este menu es orientativo. Ajusta las porciones segun tu apetito y consulta a un nutriologo.")

    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Regresar", use_container_width=True):
            st.session_state.paso = 6
            st.rerun()
    with col2:
        if st.button("Continuar", use_container_width=True, type="primary", disabled=True):
            pass
