# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Admisiones, Retención y Satisfacción (Juan Caro, Juan Perez y Edy Corro)",layout="wide",page_icon="📊")

@st.cache_data
def load_data(csv_path: str):
    df = pd.read_csv(csv_path, low_memory=False)
    return df

df = load_data("university_student_data.csv")

dept_map = {"Ingeniería":"Engineering Enrolled","Negocios":"Business Enrolled","Artes":"Arts Enrolled","Ciencias":"Science Enrolled"}

st.title("📊 Dashboard: Admisiones, Retención y Satisfacción")

st.sidebar.header("Filtros")
sel_years = st.sidebar.multiselect("Año", sorted(df["Year"].unique()), default=sorted(df["Year"].unique()))
sel_terms = st.sidebar.multiselect("Periodo (Term)", sorted(df["Term"].unique()), default=sorted(df["Term"].unique()))
sel_dept_es = st.sidebar.selectbox("Departamento", list(dept_map.keys()))

dept_col = dept_map[sel_dept_es]

filtered = df[(df["Year"].isin(sel_years)) & (df["Term"].isin(sel_terms))]

col1,col2,col3,col4,col5 = st.columns(5)
col1.metric("Aplicaciones", filtered["Applications"].sum())
col2.metric("Admitidos", filtered["Admitted"].sum())
col3.metric("Matriculados", filtered["Enrolled"].sum())
col4.metric("Retención promedio (%)", round(filtered["Retention Rate (%)"].mean(),2))
col5.metric("Satisfacción promedio (%)", round(filtered["Student Satisfaction (%)"].mean(),2))

g1 = filtered.groupby("Year")["Retention Rate (%)"].mean().reset_index()
st.plotly_chart(px.line(g1,x="Year",y="Retention Rate (%)",title="Retención por año",markers=True), use_container_width=True)

g2 = filtered.groupby("Year")["Student Satisfaction (%)"].mean().reset_index()
st.plotly_chart(px.bar(g2,x="Year",y="Student Satisfaction (%)",title="Satisfacción por año"), use_container_width=True)

g3 = filtered.groupby("Term")["Enrolled"].mean().reset_index()
st.plotly_chart(px.bar(g3,x="Term",y="Enrolled",title="Matriculados promedio por Term"), use_container_width=True)

g5 = filtered.groupby("Year")[dept_col].sum().reset_index()
st.plotly_chart(px.line(g5,x="Year",y=dept_col,title=f"Evolución Departamento: {sel_dept_es}",markers=True), use_container_width=True)
