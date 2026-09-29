import streamlit as st
import math

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Simulador de Fisicoquímica", layout="wide")

# --- FUNCIONES DE CONVERSIÓN ---
def convertir_a_kelvin(valor, unidad):
    return valor + 273.15 if unidad == "°C" else valor

def convertir_a_litros(valor, unidad):
    if unidad == "mL": return valor / 1000.0
    elif unidad == "m³": return valor * 1000.0
    return valor

def convertir_a_atm(valor, unidad):
    if unidad == "mmHg": return valor / 760.0
    elif unidad == "Pa": return valor / 101325.0
    return valor

# Constantes
R = 0.08206  # L·atm/(mol·K)
N_A = 6.022e23 # Número de Avogadro

# --- BARRA LATERAL (NAVEGACIÓN) ---
st.sidebar.title("Navegación")
modulo = st.sidebar.radio(
    "Selecciona un módulo:",
    ["1. Gases Ideales", "2. Gases Reales", "3. Estado Gaseoso II", "4. Estado Sólido", "📖 Tutorial de Uso"]
)

st.sidebar.markdown("---")
st.sidebar.info("Desarrollado para estudiantes de Ingeniería Industrial.")

# ==========================================
# MÓDULO 1: GASES IDEALES
# ==========================================
if modulo == "1. Gases Ideales":
    st.title("🧪 Módulo 1: Gases Ideales")
    st.markdown("Calculadora interactiva basada en la Ecuación de Estado: $PV = nRT$")

    variable_calcular = st.selectbox("¿Qué variable deseas calcular?", ["Presión (P)", "Volumen (V)", "Moles (n)", "Temperatura (T)"])
    st.divider()

    col1, col2 = st.columns(2)
    P_val, V_val, n_val, T_val = None, None, None, None

    with col1:
        if variable_calcular != "Presión (P)":
            p_unit = st.selectbox("Unidad de P", ["atm", "mmHg", "Pa"])
            p_input = st.number_input("Presión", min_value=0.0001, value=1.0, format="%.4f")
            P_val = convertir_a_atm(p_input, p_unit)
        if variable_calcular != "Volumen (V)":
            v_unit = st.selectbox("Unidad de V", ["L", "mL", "m³"])
            v_input = st.number_input("Volumen", min_value=0.0001, value=1.0, format="%.4f")
            V_val = convertir_a_litros(v_input, v_unit)
    with col2:
        if variable_calcular != "Moles (n)":
            n_val = st.number_input("Cantidad de sustancia (moles)", min_value=0.0001, value=1.0, format="%.4f")
        if variable_calcular != "Temperatura (T)":
            t_unit = st.selectbox("Unidad de T", ["K", "°C"])
            t_input = st.number_input("Temperatura", value=25.0, format="%.2f")
            T_val = convertir_a_kelvin(t_input, t_unit)

    if st.button("Calcular Gas Ideal", type="primary"):
        st.subheader("Procedimiento Paso a Paso")
        if T_val is not None and T_val < 0:
            st.error("⚠️ Error: Temperatura por debajo del cero absoluto.")
        else:
            if variable_calcular == "Presión (P)":
                P_calc = (n_val * R * T_val) / V_val
                st.latex(r"P = \frac{nRT}{V}")
                st.latex(f"P = \\frac{{({n_val}) \\cdot (0.08206) \\cdot ({T_val:.2f})}}{{{V_val:.4f}}}")
                st.success(f"**P = {P_calc:.4f} atm**")
            elif variable_calcular == "Volumen (V)":
                V_calc = (n_val * R * T_val) / P_val
                st.latex(r"V = \frac{nRT}{P}")
                st.latex(f"V = \\frac{{({n_val}) \\cdot (0.08206) \\cdot ({T_val:.2f})}}{{{P_val:.4f}}}")
                st.success(f"**V = {V_calc:.4f} L**")
            elif variable_calcular == "Moles (n)":
                n_calc = (P_val * V_val) / (R * T_val)
                st.latex(r"n = \frac{PV}{RT}")
                st.latex(f"n = \\frac{{({P_val:.4f}) \\cdot ({V_val:.4f})}}{{0.08206 \\cdot ({T_val:.2f})}}")
                st.success(f"**n = {n_calc:.4f} mol**")
            elif variable_calcular == "Temperatura (T)":
                T_calc = (P_val * V_val) / (n_val * R)
                st.latex(r"T = \frac{PV}{nR}")
                st.latex(f"T = \\frac{{({P_val:.4f}) \\cdot ({V_val:.4f})}}{{({n_val}) \\cdot 0.08206}}")
                st.success(f"**T = {T_calc:.2f} K** ({T_calc - 273.15:.2f} °C)")

# ==========================================
# MÓDULO 2: GASES REALES
# ==========================================
elif modulo == "2. Gases Reales":
    st.title("🌐 Módulo 2: Gases Reales")
    st.markdown("Cálculo de presión real (Ecuación de Van der Waals) y Factor de Compresibilidad (Z).")
    
    # Constantes a (L^2 atm / mol^2) y b (L / mol)
    vdw_constantes = {
        "Oxígeno (O2)": {"a": 1.36, "b": 0.0318},
        "Nitrógeno (N2)": {"a": 1.39, "b": 0.0391},
        "Dióxido de Carbono (CO2)": {"a": 3.59, "b": 0.0427},
        "Metano (CH4)": {"a": 2.25, "b": 0.0428},
        "Helio (He)": {"a": 0.034, "b": 0.0237}
    }
    
    col1, col2 = st.columns(2)
    with col1:
        gas_seleccionado = st.selectbox("Selecciona un gas común", list(vdw_constantes.keys()))
        a = vdw_constantes[gas_seleccionado]["a"]
        b = vdw_constantes[gas_seleccionado]["b"]
        st.info(f"Constantes de Van der Waals:\n\na = {a} L²·atm/mol²\nb = {b} L/mol")
        
    with col2:
        T_real = st.number_input("Temperatura (K)", min_value=0.1, value=298.15)
        V_real = st.number_input("Volumen (L)", min_value=0.001, value=1.0)
        n_real = st.number_input("Moles (n)", min_value=0.001, value=1.0)

    if st.button("Calcular Presión Real y Z", type="primary"):
        # Cálculo de Presión Ideal para comparar
        P_ideal = (n_real * R * T_real) / V_real
        
        # Ecuación de Van der Waals para P
        termino1 = (n_real * R * T_real) / (V_real - (n_real * b))
        termino2 = a * ((n_real / V_real) ** 2)
        P_real = termino1 - termino2
        
        # Factor Z
        Z = (P_real * V_real) / (n_real * R * T_real)
        
        st.subheader("Procedimiento Paso a Paso")
        st.latex(r"\left( P + a\frac{n^2}{V^2} \right)(V - nb) = nRT \implies P = \frac{nRT}{V - nb} - a\frac{n^2}{V^2}")
        st.latex(f"P = \\frac{{{n_real} \\cdot 0.08206 \\cdot {T_real}}}{{{V_real} - ({n_real} \\cdot {b})}} - {a}\\left(\\frac{{{n_real}}}{{{V_real}}}\\right)^2")
        st.latex(f"P_{{real}} = {termino1:.4f} - {termino2:.4f}")
        
        st.success(f"**Presión Real (Van der Waals):** {P_real:.4f} atm")
        st.info(f"*(Para comparación, la Presión Ideal sería: {P_ideal:.4f} atm)*")
        
        st.markdown("---")
        st.markdown("**Factor de Compresibilidad (Z):**")
        st.latex(r"Z = \frac{P_{real} V}{nRT}")
        st.latex(f"Z = \\frac{{{P_real:.4f} \\cdot {V_real}}}{{{n_real} \\cdot 0.08206 \\cdot {T_real}}}")
        st.success(f"**Z = {Z:.4f}**")
        if Z < 1:
            st.caption("Z < 1: Predominan las fuerzas de atracción intermolecular.")
        elif Z > 1:
            st.caption("Z > 1: Predominan las fuerzas de repulsión.")

# ==========================================
# MÓDULO 3: ESTADO GASEOSO II (Mezclas)
# ==========================================
elif modulo == "3. Estado Gaseoso II":
    st.title("💨 Módulo 3: Mezclas y Cinética")
    
    tab1, tab2 = st.tabs(["Ley de Dalton (Presiones Parciales)", "Ley de Graham (Efusión)"])
    
    with tab1:
        st.markdown("### Ley de Dalton")
        num_gases = st.number_input("Número de gases en la mezcla", min_value=2, max_value=5, value=2, step=1)
        
        moles_lista = []
        for i in range(num_gases):
            moles = st.number_input(f"Moles del Gas {i+1}", min_value=0.001, value=1.0, key=f"mol_{i}")
            moles_lista.append(moles)
            
        P_total = st.number_input("Presión Total del sistema (atm)", min_value=0.01, value=1.0)
        
        if st.button("Calcular Presiones Parciales"):
            moles_totales = sum(moles_lista)
            st.latex(f"n_{{total}} = \\sum n_i = {moles_totales:.4f} \\text{{ mol}}")
            
            for i, n in enumerate(moles_lista):
                frac_molar = n / moles_totales
                p_parcial = frac_molar * P_total
                st.markdown(f"**Gas {i+1}:**")
                st.latex(f"X_{i+1} = \\frac{{{n}}}{{{moles_totales:.4f}}} = {frac_molar:.4f}")
                st.latex(f"P_{i+1} = X_{i+1} \\cdot P_{{total}} = {frac_molar:.4f} \\cdot {P_total} = {p_parcial:.4f} \\text{{ atm}}")
                
    with tab2:
        st.markdown("### Ley de Graham")
        st.markdown("Compara las velocidades de efusión/difusión de dos gases.")
        col1, col2 = st.columns(2)
        with col1:
            M1 = st.number_input("Masa Molar Gas 1 (g/mol)", min_value=1.0, value=2.016) # ej. H2
        with col2:
            M2 = st.number_input("Masa Molar Gas 2 (g/mol)", min_value=1.0, value=31.998) # ej. O2
            
        if st.button("Calcular Relación de Velocidades"):
            relacion = math.sqrt(M2 / M1)
            st.latex(r"\frac{v_1}{v_2} = \sqrt{\frac{M_2}{M_1}}")
            st.latex(f"\\frac{{v_1}}{{v_2}} = \\sqrt{{\\frac{{{M2}}}{{{M1}}}}}")
            st.success(f"El Gas 1 efunde/difunde **{relacion:.4f} veces más rápido** que el Gas 2.")

# ==========================================
# MÓDULO 4: ESTADO SÓLIDO
# ==========================================
elif modulo == "4. Estado Sólido":
    st.title("🧊 Módulo 4: Estado Sólido")
    st.markdown("Cálculos de celdas unitarias cristalinas.")
    
    tipo_celda = st.selectbox("Tipo de Celda Unitaria", [
        "Cúbica Simple (SC)", 
        "Cúbica Centrada en el Cuerpo (BCC)", 
        "Cúbica Centrada en las Caras (FCC)"
    ])
    
    col1, col2 = st.columns(2)
    with col1:
        radio_pm = st.number_input("Radio Atómico (picómetros - pm)", min_value=1.0, value=125.0)
    with col2:
        masa_molar = st.number_input("Masa Molar (g/mol)", min_value=1.0, value=50.0)
        
    if st.button("Calcular Parámetros y Densidad"):
        # Asignar átomos por celda (z) y relación de arista (a) según el tipo
        r_cm = radio_pm * 1e-10  # Convertir pm a cm
        
        if "SC" in tipo_celda:
            z = 1
            arista = 2 * radio_pm
            formula_a = r"a = 2r"
        elif "BCC" in tipo_celda:
            z = 2
            arista = (4 * radio_pm) / math.sqrt(3)
            formula_a = r"a = \frac{4r}{\sqrt{3}}"
        else: # FCC
            z = 4
            arista = math.sqrt(8) * radio_pm
            formula_a = r"a = \sqrt{8}r"
            
        arista_cm = arista * 1e-10
        volumen_cm3 = arista_cm ** 3
        densidad = (z * masa_molar) / (volumen_cm3 * N_A)
        
        st.subheader("Procedimiento Paso a Paso")
        st.markdown(f"**1. Átomos por celda (z):** {z}")
        st.markdown("**2. Cálculo de la Arista (a):**")
        st.latex(formula_a)
        st.latex(f"a = {arista:.2f} \\text{{ pm}} = {arista_cm:.2e} \\text{{ cm}}")
        
        st.markdown("**3. Cálculo de la Densidad Teórica ($\\rho$):**")
        st.latex(r"\rho = \frac{z \cdot M}{N_A \cdot a^3}")
        st.latex(f"\\rho = \\frac{{{z} \\cdot {masa_molar}}}{{(6.022 \\times 10^{{23}}) \\cdot ({arista_cm:.2e})^3}}")
        st.success(f"**Densidad Teórica:** {densidad:.4f} g/cm³")

# ==========================================
# MÓDULO 5: TUTORIAL
# ==========================================
elif modulo == "📖 Tutorial de Uso":
    st.title("📖 Tutorial de Uso del Simulador")
    
    st.markdown("""
    ¡Bienvenido al simulador de Fisicoquímica! Esta herramienta está diseñada para ayudarte a comprobar tus ejercicios manuales, mostrando no solo el resultado final, sino también el procedimiento matemático paso a paso.
    
    ### ¿Cómo usar la interfaz?
    
    **1. Navegación**
    * Utiliza la barra lateral (a la izquierda) para moverte entre los diferentes temas. 
    * Si estás en un dispositivo móvil, toca el ícono de la flecha en la esquina superior izquierda para abrir el menú.
    
    **2. Módulo de Gases Ideales**
    * Selecciona primero **qué variable necesitas averiguar** (P, V, n, T) en la lista desplegable.
    * Ingresa los valores que sí tienes en los campos de abajo.
    * Asegúrate de elegir las **unidades correctas** (ej. si tu problema está en mmHg, selecciona mmHg; la app hará la conversión a atmósferas por ti internamente).
    * Haz clic en *Calcular*. Verás la fórmula despejada y el reemplazo de datos.
    
    **3. Módulo de Gases Reales**
    * Sirve para comparar cómo se comporta un gas asumiendo la Ecuación de Van der Waals vs la Ideal.
    * Selecciona el gas que indica tu problema. La app cargará automáticamente las constantes $a$ y $b$.
    * Ingresa la temperatura, el volumen y los moles. El simulador calculará la presión real y el factor de compresibilidad (Z).
    
    **4. Módulo de Mezclas y Cinética**
    * **Pestaña de Dalton:** Si tienes varios gases mezclados, indica cuántos son y sus moles. Ingresa la presión total del recipiente para hallar las fracciones molares y presiones parciales de cada uno.
    * **Pestaña de Graham:** Ingresa las masas molares de dos gases distintos para saber cuántas veces más rápido se mueve uno respecto al otro (útil para ejercicios de difusión).
    
    **5. Módulo de Estado Sólido**
    * Selecciona la estructura cristalina (Cúbica Simple, BCC o FCC).
    * Ingresa el radio atómico (en picómetros) y la masa molar del elemento.
    * La app usará la geometría de la celda unitaria y el Número de Avogadro para calcular cuánto mide la arista y cuál es la densidad teórica del cristal en $g/cm^3$.
    """)
    st.info("💡 **Tip para comprobar ejercicios:** Realiza primero el ejercicio en tu cuaderno con lápiz y papel. Luego, introduce tus datos aquí para verificar si el despeje de la fórmula y el cálculo coinciden con tu respuesta.")