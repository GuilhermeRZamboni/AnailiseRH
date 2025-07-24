import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
#Rodar o coigo stream lit
#python -m streamlit run app.py
st.set_page_config(page_title="Analise de Funcionarios", layout="wide")
st.title("📊Analise de Funcionarios da Empresa")

st.sidebar.write("Upload de Arquivos Excel")
arquivo = st.sidebar.file_uploader('Selecione a planilha de funcionarios', type=["xlsx"])

if arquivo:
    df = pd.read_excel(arquivo)
    df["Data de Contratacao"] = pd.to_datetime(df["Data de Contratacao"], errors="coerce")
    df["Data de Demissao"] = pd.to_datetime(df["Data de Demissao"],  errors="coerce")

    #Crir coluna de status
    df['Status'] = df['Data de Demissao'].isna().map({True:"Ativo", False:"Inativo"})
    total_ativos = df[df['Status']== "Ativo"].shape[0]
    total_inativos = df[df['Status']== "Inativo"].shape[0]
    total_contratacao=df["Data de Contratacao"].notna().sum()

    #Folha salarial
    folha_salarial = (df["Salario"] + df["VT"] + df["VR"])[df["Status"]=="Ativo"].sum()
    folha_salarial = float(folha_salarial)
    
    #Gerar filtros
    st.sidebar.markdown("### Filtro")
    status_opcao = ["Ativo", "Inativo"]
    status_selecionado = st.sidebar.multiselect("Status", status_opcao, default=status_opcao)
    
    sexo = df["Genero"].dropna().unique()
    sexo_selecionado = st.sidebar.multiselect("Sexo", sorted(sexo), default=sorted(sexo))
    
    area_opcao = df["Área"].dropna().unique()
    area_selecionada = st.sidebar.multiselect("Área", sorted(area_opcao), default=sorted(area_opcao))
    df = df[
        (df["Status"].isin(status_selecionado)) & 
        (df["Genero"].isin(sexo_selecionado)) &
        (df["Área"].isin(area_selecionada))
        ]
    #Criar cartões
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Ativos", total_ativos)
    col2.metric("Inativos", total_inativos)
    col3.metric("Contratações", total_contratacao)
    col4.metric("Folha Salarial", f"R${folha_salarial:,.2f}")

    #Criar abas dos graficos
    aba1, aba2, aba3, aba4 = st.tabs(["Visão Geral", "Gráficos por Área", "Contratações vs Demições", "Tabela de Dados"])    
    with aba1:
        contar_sexo = df ["Genero"].value_counts()
        #fig1 = Figura (Papel todo)
        #ax1 =  Eixo(Ou quadro) desenha os graficos
        fig1, ax1 = plt.subplots()
        #Criar barras
        barras = ax1.bar(contar_sexo.index, contar_sexo.values, color=["skyblue", "pink"])
        ax1.bar_label(barras, padding=-15)
        ax1.set_title("Funcionários por sexo")
        st.pyplot(fig1)
    with aba2:
        col5, col6 = st.columns(2)
        with col5:
            salario_area = df.groupby("Área")["Salario"].median().sort_values()
            fig2, ax2 = plt.subplots()
            salario_area.plot(kind="barh", color = "darkGreen", ax=ax2)
            ax2.bar_label(ax2.containers[0], padding = -60, color = "white", fmt="R$ %.2f")
            ax2.set_title("Salário Médio por Área💰")
            ax2.set_ylabel("")
            st.pyplot(fig2)
        with col6:
            horas_area = df.groupby("Área")["Horas Extras"].median().sort_values()
            fig3, ax3 = plt.subplots()
            horas_area.plot(kind="barh", color = "darkBlue", ax=ax3)
            ax3.bar_label(ax3.containers[0], padding = -45, color = "white")
            ax3.set_title("Média de Horas Extras por Área⌚")
            ax3.set_ylabel("")
            st.pyplot(fig3)
    with aba3:
        contratacoes_por_ano = df["Data de Contratacao"].dt.year.value_counts().sort_index()
        demissoes_por_ano = df["Data de Demissao"].dropna().dt.year.value_counts().sort_index()
        fig9, ax9 = plt.subplots(figsize=(5,4))
        contratacoes_por_ano.plot(kind="line", label= "Contratações", color='DarkBlue', ax=ax9 )
        demissoes_por_ano.plot(kind="line",  color='Red', label= "Demissões", ax=ax9 )
        plt.plot(demissoes_por_ano.index, demissoes_por_ano.values, 'r')
        plt.xlabel('Ano')

        plt.legend()
        plt.title('Contratações vs Demissões ')
        
        st.pyplot(fig9)
        
    with aba4:
        df["Nome Completo"] = df["Nome"] + " " + df["Sobrenome"]
        df.drop(columns=["Nome","Sobrenome"], inplace=True)
        busca = st.text_input("Pesquisar por nome completo")
        if busca:
         # Filtra linhas que contêm o texto digitado (case insensitive)
        # filtra as linhas que contêm o texto digitado, ignorando maiúsculas/minúsculas.
           # trata valores ausentes (NaN) como False, ou seja, se o campo
         # estiver vazio, não vai causar erro e nem retornar True.
            df_filtrado = df[df["Nome Completo"].str.contains(busca, case=False, na=False)]
        else:
            df_filtrado = df
            # st.dataframe(df)
            st.dataframe(df_filtrado[['Nome Completo', 'Cargo', 'Área', 'Horas Extras', 'Salario', 'Avaliação do Funcionário']])
else:       
    st.warning("Por favor, carregue um arquivo excel para iniciar a analise")