
# Arquivo: app_gestao_processos.py
import pandas as pd
import streamlit as st
import os

CAMINHO_ARQUIVO = "planilha_processos.xlsx"

st.title("Gestão de Processos com Valores a Receber")

# Funções de apoio
def carregar_planilha(caminho):
    if os.path.exists(caminho):
        return pd.read_excel(caminho)
    else:
        colunas = ["Cliente", "Processo", "Parte Devedora", "Tipo", "Valor a Receber (R$)",
                   "Valor Recebido (R$)", "Total (R$)", "Andamento Atual", "Data da Última Movimentação",
                   "Pendência", "Observações"]
        return pd.DataFrame(columns=colunas)

def salvar_planilha(df, caminho):
    df.to_excel(caminho, index=False)

# Carregar dados existentes
df = carregar_planilha(CAMINHO_ARQUIVO)

# Formulário para novo processo
with st.form("Adicionar Novo Processo"):
    cliente = st.text_input("Cliente")
    processo = st.text_input("Número do Processo")
    parte_devedora = st.text_input("Parte Devedora")
    tipo = st.selectbox("Tipo", ["Cumprimento de Sentença", "Execução"])
    valor_receber = st.number_input("Valor a Receber (R$)", min_value=0.0, step=100.0)
    valor_recebido = st.number_input("Valor Recebido (R$)", min_value=0.0, step=100.0)
    andamento = st.text_input("Andamento Atual")
    data_movimentacao = st.date_input("Data da Última Movimentação")
    pendencia = st.text_input("Pendência")
    observacoes = st.text_area("Observações")
    enviar = st.form_submit_button("Adicionar Processo")

    if enviar:
        novo = {
            "Cliente": cliente,
            "Processo": processo,
            "Parte Devedora": parte_devedora,
            "Tipo": tipo,
            "Valor a Receber (R$)": valor_receber,
            "Valor Recebido (R$)": valor_recebido,
            "Total (R$)": valor_receber - valor_recebido,
            "Andamento Atual": andamento,
            "Data da Última Movimentação": data_movimentacao,
            "Pendência": pendencia,
            "Observações": observacoes
        }
        df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
        salvar_planilha(df, CAMINHO_ARQUIVO)
        st.success("Processo adicionado com sucesso!")

# Exibir dados atualizados
st.subheader("Processos Registrados")
st.dataframe(df)
