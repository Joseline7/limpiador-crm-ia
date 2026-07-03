import streamlit as st
import pandas as pd
from openai import OpenAI
from schema import BaseDatosLimpia

st.set_page_config(page_title="Limpiador de Leads con IA", page_icon="🪄")
st.title("🪄 Limpiador Inteligente de Leads para CRM")
st.subheader("Pega tus datos sucios y la IA los estructurará automáticamente")

api_key = st.sidebar.text_input("Introduce tu OpenAI API Key", type="password")

datos_sucios = st.text_area(
    "Pega aquí tus filas de Excel, texto desordenado, apuntes de blocks de notas o CSV caótico:",
    height=200,
    placeholder="ejemplo:\nJOSELINE AGUIRRE ; 51987654321 ; j.aguirre@gmail.co\njuan perez, 955332211, jperez@hotmial.com"
)

if st.button("Limpiar y Estructurar Datos") and datos_sucios:
    if not api_key:
        st.error("Por favor, introduce tu API Key de OpenAI en la barra lateral.")
    else:
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
