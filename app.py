import streamlit as st
import pandas as pd
from openai import OpenAI
from schema import BaseDatosLimpia

st.set_page_config(page_title="Limpiador de Leads con IA", page_icon="🪄")
st.title("🪄 Limpiador de Leads para CRM")
st.subheader("Pega tus datos sucios y la IA los estructurará automáticamente")

# 1. Configuración del modelo de negocio en la barra lateral
st.sidebar.header("🔑 Acceso Pro")
codigo_usuario = st.sidebar.text_input("Introduce tu Código de Acceso Pro", type="password", placeholder="Escribe tu código aquí")

# Enlace de pago (reemplázalo por tu link de Gumroad, Lemon Squeezy, Yape, etc.)
LINK_DE_PAGO = "https://tu-pagina-de-pago.com" 
st.sidebar.markdown(f"[🛒 ¿No tienes un código? Adquiere tu Pase Pro aquí]({LINK_DE_PAGO})")

# Código maestro que tú definirás para tus clientes que paguen
CODIGO_PRO_VALIDO = "LEADS_PRO_2026" 

datos_sucios = st.text_area(
    "Pega aquí tus filas de Excel, texto desordenado, apuntes de blocks de notas o CSV caótico:",
    height=200,
    placeholder="ejemplo:\nJOSELINE AGUIRRE ; 51987654321 ; j.aguirre@gmail.co\njuan perez, 955332211, jperez@hotmial.com"
)

if st.button("Limpiar y Estructurar Datos") and datos_sucios:
    # 2. Lógica de conteo de filas para la prueba gratuita
    lineas = [linea.strip() for linea in datos_sucios.strip().split("\n") if linea.strip()]
    total_leads = len(lineas)
    
    es_pro = (codigo_usuario == CODIGO_PRO_VALIDO)
    
    # Permitir procesar si es Pro o si está dentro del límite gratuito (máximo 3 leads)
    if not es_pro and total_leads > 3:
        st.error(f"⚠️ Has ingresado {total_leads} filas. La prueba gratuita solo permite procesar hasta 3 filas.")
        st.info(f"💡 Para limpiar bases de datos completas de forma ilimitada, adquiere tu Pase Pro e introduce tu código en la barra lateral.")
        st.markdown(f"### [👉 Haz clic aquí para comprar tu acceso inmediato]({LINK_DE_PAGO})")
    else:
        # 3. Intentar obtener la API Key guardada de forma segura en Streamlit Secrets
        if "OPENAI_API_KEY" in st.secrets:
            api_key = st.secrets["OPENAI_API_KEY"]
        else:
            st.error("Error de configuración: La API Key de OpenAI no está configurada en los Secrets de la plataforma.")
            st.stop()

        with st.spinner("La IA está ordenando y estandarizando tus datos..."):
            try:
                client = OpenAI(api_key=api_key)
                completion = client.beta.chat.completions.parse(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system", 
                            "content": "Eres un ingeniero de datos experto en limpieza de bases de datos para CRM. Tu trabajo es tomar texto desordenado, identificar los campos de cada persona, corregir errores ortográficos obvios en correos, estandarizar nombres y dar formato E.164 a los teléfonos."
                        },
                        {"role": "user", "content": datos_sucios}
                    ],
                    response_format=BaseDatosLimpia,
                )
                datos_procesados = completion.choices[0].message.parsed
                leads_dict = [lead.model_dump() for lead in datos_procesados.leads]
                df = pd.DataFrame(leads_dict)
                df.columns = ["Nombre", "Apellido", "Teléfono", "Email", "Empresa / Contexto"]

                st.success("¡Datos limpios con éxito!")
                if not es_pro:
                    st.caption("✨ Modo Demo (Prueba Gratuita realizada con éxito)")
                
                st.dataframe(df)

                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Descargar como CSV para CRM",
                    data=csv,
                    file_name="leads_limpios_crm.csv",
                    mime="text/csv",
                )
            except Exception as e:
                st.error(f"Ocurrió un error al procesar los datos: {e}")
