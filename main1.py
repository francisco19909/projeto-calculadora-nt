import numpy as np
import pandas as pd
import streamlit as st
from io import BytesIO

# Configurar layout da página
st.set_page_config(page_title="Calculadora de Médias", layout="centered")

# Estilizar a interface
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #4CAF50; 
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Título
st.title("🎓 Calculadora de Médias - Engenharia")

# Entrada de número de notas
st.write("Insira as informações abaixo:")
number = st.number_input("Quantas notas você quer inserir?", min_value=1, step=1)
number = int(number)

# Coletar as notas
st.write("Insira as notas parciais:")
notas = []
for i in range(number):
    nota = st.number_input(f"Nota {i + 1}:", min_value=0.0, max_value=10.0)
    notas.append(nota)

# Botão para calcular a média
if st.button("Calcular Média"):
    notas = np.array(notas)
    media_notas = notas.mean()
    st.subheader(f"Média das notas regulares: {media_notas:.2f}")

    # Cálculo da nota mínima no exame
    if media_notas >= 5:
        st.success("Parabéns! Você já atingiu a média necessária.")
        nota_minima = 0
    else:
        nota_minima = (5 - media_notas * 0.6) / 0.4
        st.warning(f"Nota mínima necessária no exame: {nota_minima:.2f}")

    # Criar DataFrame para exportação
    df = pd.DataFrame(
        {
            "Notas Parciais": notas,
            "Média": [media_notas],
            "Nota Mínima no Exame": [nota_minima],
        }
    )

    # Função para gerar arquivo Excel
    def gerar_excel(dataframe):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            dataframe.to_excel(writer, index=False, sheet_name="Resultados")
        return output.getvalue()

    # Botão para download
    excel_data = gerar_excel(df)
    st.download_button(
        label="📥 Baixar Resultados em Excel",
        data=excel_data,
        file_name="resultados_média_notas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )