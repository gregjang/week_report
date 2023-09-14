import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_lottie import st_lottie
import json

st.set_page_config(layout="wide", page_title='주간보고서')

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

@st.cache
def get_data_from_excel(filename):
    df = pd.read_excel(
            filename,
            sheet_name='engineer',
            usecols='B:L',
            header=1)
    return df

# --- STREAMLIT SELECTION
owner = ['deega','andy','roy','teo', 'bryan']
selected_owner = st.sidebar.selectbox("발표자를 선택하세요.", owner)


#--- FILE SELECTION
report_file = st.file_uploader('발표자료를 선택하세요')
if report_file is not None:
    filename = report_file.name
    if(filename[0:4] != '2023'):
        lottie = load_lottiefile('animation_error.json')
        st_lottie(lottie, height=200, speed=1.5, loop=True)

        st.markdown("<h2 style='text-align: center; color: white;'>엑셀파일을 선택하쇼잉</h2>", unsafe_allow_html=True)
        st.stop()
    df = get_data_from_excel(report_file)
    
else:
    st.stop()

# --- DISPLAY IMAGE & DATAFRAME
col1, col2 = st.columns((1,9))
with col1:
    lottie = load_lottiefile('animation_sandclock.json')
    st_lottie(lottie, height=200, speed=1.5, loop=True)

with col2:
    #--- HEADER DISPLAY
    header_year = report_file.name[0:4]
    header_week = report_file.name[5:7]
    st.subheader(header_year+'년'+' '+header_week+'주차')

    # --- WEEKLY DISPLAY
    df_report = df[df['Owner']==selected_owner]
    df_report = df_report.loc[:,['Customer', 'Vendor', 'Devices', 'Issue', 'Progress(Task)', 'Status']]

    df_report = df_report.applymap(lambda x: x.replace('\r\n', '<br>'))
    df_report = df_report.applymap(lambda x: x.replace('\t', ''))
    st.markdown(df_report.to_html(escape=False), unsafe_allow_html=True)
