import streamlit as st
import pandas as pd
import xlrd
import tempfile
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
st.set_page_config(layout="wide")   
def main():
    st.title("Gerar gráfico de acompanhamento OBMEP 2025")
    uploaded_file_1 = st.file_uploader("Carregue a planilha cadastro MEC de 2024-19ªOBMEP (.xls)", type="xls")
    uploaded_file_2 = st.file_uploader("Carregue a planilha cadastro MEC de 2025-20ªOBMEP (.xls)", type="xls")

    if uploaded_file_1 and uploaded_file_2:
        BM = pd.read_excel(uploaded_file_2)
        total = len(BM)
        BM['Total Alunos'] = BM[['1ª Série', '2ª Série', '3ª Série', '4ª Série', '6ª Ano', '7ª Ano', '8ª Ano', '9ª Ano', 'Nao Seriado']].sum(axis=1)
        total_alunos = BM['Total Alunos'].sum()
        BMi = BM[BM['Data da Inscrição'] != 'Não foi Inscrita até o momento'].reset_index(drop=True)
        BMi['Data da Inscrição'] = pd.to_datetime(BMi['Data da Inscrição'], format="%d/%m/%Y")

        inicio_inscricao = pd.to_datetime("2025-02-05")
        fim_inscricao = pd.to_datetime("2025-03-17")
        ultima_data_inscricao = BMi["Data da Inscrição"].max()
        dias = pd.date_range(start=inicio_inscricao, end=ultima_data_inscricao, freq="D")

        inscricoes_por_dia = BMi['Data da Inscrição'].value_counts().reindex(dias, fill_value=0).sort_index()
        inscricoes_acumuladas = inscricoes_por_dia.cumsum()
        total_dias = (fim_inscricao - inicio_inscricao).days + 1

        df = pd.DataFrame({"Data": dias, "Inscricoes_Acumuladas": inscricoes_acumuladas})
        df["Percentual_Inscricoes"] = (df["Inscricoes_Acumuladas"] / total) * 100
        df["Percentual_Periodo"] = (((df["Data"] - inicio_inscricao).dt.days + 1) / total_dias) * 100

        inscricoes_alunos_por_dia = BMi.groupby('Data da Inscrição')['Total Alunos'].sum().reindex(dias, fill_value=0).sort_index()
        inscricoes_alunos_por_dia_acumuladas = inscricoes_alunos_por_dia.cumsum()

        df['Inscricoes_Acumuladas_alunos'] = inscricoes_alunos_por_dia_acumuladas
        df["Percentual_alunos"] = (df['Inscricoes_Acumuladas_alunos'] / total_alunos) * 100

        # Segundo arquivo (2024)
        BM2 = pd.read_excel(uploaded_file_1)
        total2 = len(BM2)
        BM2['Total Alunos'] = BM2[['1ª Série', '2ª Série', '3ª Série', '4ª Série', '6ª Ano', '7ª Ano', '8ª Ano', '9ª Ano', 'Nao Seriado']].sum(axis=1)
        total_alunos2 = BM2['Total Alunos'].sum()
        BMi2 = BM2[BM2['Data da Inscrição'] != 'Não foi Inscrita até o momento'].reset_index(drop=True)
        BMi2['Data da Inscrição'] = pd.to_datetime(BMi2['Data da Inscrição'], format="%d/%m/%Y")

        inicio_inscricao2 = pd.to_datetime("2024-02-05")
        fim_inscricao2 = pd.to_datetime("2024-03-15")
        ultima_data_inscricao2 = BMi2["Data da Inscrição"].max()
        dias2 = pd.date_range(start=inicio_inscricao2, end=ultima_data_inscricao2, freq="D")

        inscricoes_por_dia2 = BMi2['Data da Inscrição'].value_counts().reindex(dias2, fill_value=0).sort_index()
        inscricoes_acumuladas2 = inscricoes_por_dia2.cumsum()
        total_dias2 = (fim_inscricao2 - inicio_inscricao2).days + 1

        df2 = pd.DataFrame({"Data": dias2, "Inscricoes_Acumuladas": inscricoes_acumuladas2})
        df2["Percentual_Inscricoes"] = (df2["Inscricoes_Acumuladas"] / total2) * 100
        df2["Percentual_Periodo"] = (((df2["Data"] - inicio_inscricao2).dt.days + 1) / total_dias2) * 100

        inscricoes_alunos_por_dia2 = BMi2.groupby('Data da Inscrição')['Total Alunos'].sum().reindex(dias2, fill_value=0).sort_index()
        inscricoes_alunos_por_dia_acumuladas2 = inscricoes_alunos_por_dia2.cumsum()

        df2['Inscricoes_Acumuladas_alunos'] = inscricoes_alunos_por_dia_acumuladas2
        df2["Percentual_alunos"] = (df2['Inscricoes_Acumuladas_alunos'] / total_alunos2) * 100

        # Criar figura com dois gráficos
        fig, ax = plt.subplots(1, 2, figsize=(14, 6))

        # 🔹 Gráfico 1: Escolas
        ax[0].plot(df["Percentual_Periodo"], df["Percentual_Inscricoes"], color="#003366", marker="o", linestyle="-", label="Escolas(20ª-2025)")
        ax[0].plot(df2["Percentual_Periodo"], df2["Percentual_Inscricoes"], color="#66B2FF", marker="o", linestyle="-", label="Escolas(19ª-2024)")
        ax[0].set_xlabel("Percentual do Período de Inscrição")
        ax[0].set_ylabel("Percentual de Escolas Inscritas")
        ax[0].set_title("Evolução Acumulada das Escolas")
        ax[0].legend(loc="upper left")
        ax[0].grid()
        ax[0].set_xticks(np.arange(0, 110, 10))
        ax[0].set_yticks(np.arange(0, 110, 10))
        ax[0].set_xlim(0, 100)
        ax[0].set_ylim(0, 100)

        # 🔹 Gráfico 2: Alunos
        ax[1].plot(df["Percentual_Periodo"], df["Percentual_alunos"], color="#8B0000", marker="o", linestyle="-", label="Alunos(20ª-2025)")
        ax[1].plot(df2["Percentual_Periodo"], df2["Percentual_alunos"], color="#FF6666", marker="o", linestyle="-", label="Alunos(19ª-2024)")
        ax[1].set_xlabel("Percentual do Período de Inscrição")
        ax[1].set_ylabel("Percentual de Alunos Inscritos")
        ax[1].set_title("Evolução Acumulada dos Alunos")
        ax[1].legend(loc="upper left")
        ax[1].grid()
        ax[1].set_xticks(np.arange(0, 110, 10))
        ax[1].set_yticks(np.arange(0, 110, 10))
        ax[1].set_xlim(0, 100)
        ax[1].set_ylim(0, 100)

        # Ajustar espaçamento entre os gráficos
        plt.tight_layout()

        # Exibir os gráficos no Streamlit
        st.pyplot(fig)

if __name__ == "__main__":
    main()
