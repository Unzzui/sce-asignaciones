import streamlit as st
from PIL import Image
import pandas as pd
from io import BytesIO
from datetime import date

# ---- Start App

img = Image.open('images/oca.jpg')
img1= Image.open('images/oca1.png')

st.set_page_config(page_title="Asignaciones SCE", page_icon=img, layout="wide")
# ---- Web App Title ----

st.markdown(("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""),unsafe_allow_html=True)

st.image(img1 , width=250)
st.markdown('''
#  Asignaciones SCE 
Esta es una app web creada para facilitar las asignaciones realizadas.
---
''')

@st.cache(ttl=60)
def load_csv():
    df = pd.read_csv('data/BD_SCE.csv', sep=";")
    df = df.loc[:,["Número de incidencia","DIRECCION","Observaciones de campo","Centro Operativo" , "Código TdC", "Estado TDC", "Municipio","Fecha de Inicio de Ejecución de Trabajo", "Fecha de fin", "Código Causa", "FECHA_ASIGNADA_OCA", "ESTADO_OCA", "ZONAL" ,"AÑO", "ITO_ASIGNADO"]]
    # df["FECHA_ASIGNADA_OCA"] = pd.to_datetime(df["FECHA_ASIGNADA_OCA"], infer_datetime_format=True)

    return df

df = load_csv()
with st.container():
    st.write("---")
    left_column,right_column = st.columns(2)
    with left_column:
        st.header("")
        st.write("##")


# # ---- PROJECTS ---- 

st.sidebar.header("Filtre Aqui:")

year = st.sidebar.multiselect(
    "Seleccione el Año:", 
    options=df["AÑO"].unique(),
    default=df["AÑO"].unique(),
)

zonal = st.sidebar.multiselect(
    "Seleccione la Zonal:",
    options=df["ZONAL"].unique(),
    default=df["ZONAL"].unique(),
)
estado = st.sidebar.multiselect(
    "Estado:",
    options=df["ESTADO_OCA"].unique(),
    default="PENDIENTE",
)

comuna = st.sidebar.multiselect(
    "Comuna:",
    options=df["Municipio"].unique(),
    default=df["Municipio"].unique(),
    )

ito = st.sidebar.multiselect(
    "ITO:",
    options=df["ITO_ASIGNADO"].unique(),
    default=df["ITO_ASIGNADO"].unique(),
)
df_selection = df.query(
    "AÑO ==@year & ZONAL == @zonal & ESTADO_OCA == @estado & Municipio == @comuna & ITO_ASIGNADO == @ito"
)




# # ---- MainPage ----
st.title(":memo: Asignaciones Servicio Calidad de Emergencias" )
st.markdown("##")

# # ---- Downdload Buttons ----

# ---- To Excel ----
def to_excel(df_selection):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df_selection.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data
 
today = date.today()
today = today.strftime("%d/%m/%Y")

df_selection_xlsx = to_excel(df_selection)   
st.download_button(label='📥 Descargar Excel',
                                data=df_selection_xlsx ,
                                file_name='Asignaciones_'+today +'.xlsx')


# ---- TOP KPI'S ---- 

total_cuenta_pendiente = len(df_selection["ESTADO_OCA"])

left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.subheader("Total Pendientes:")
    st.subheader(f"{total_cuenta_pendiente:}")

st.write(df_selection)
