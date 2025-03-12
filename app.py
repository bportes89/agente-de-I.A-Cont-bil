import streamlit as st
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente
load_dotenv()

# Verificação da chave API
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    st.error('Erro: Chave API da OpenAI não encontrada. Verifique seu arquivo .env')
    st.stop()

# Configuração do cliente OpenAI
client = OpenAI(api_key=api_key)

# Configuração da página
st.set_page_config(page_title="Assistente Contábil IA", layout="wide")
st.title("Assistente Contábil IA")

# Sidebar para seleção de funcionalidades
opcao = st.sidebar.selectbox(
    "Escolha a função desejada",
    ["Análise de Demonstrativos", "Classificação de Contas", "Dúvidas Contábeis", 
     "Cálculos Contábeis", "Folha de Pagamento", "Análise de Balanço", 
     "Controle de Orçamento", "Fluxo de Caixa", "Análise DRE", "Análise de Indicadores"]
)

if opcao == "Análise de Demonstrativos":
    st.header("Análise de Demonstrativos Financeiros")
    
    uploaded_file = st.file_uploader("Faça upload do seu demonstrativo (CSV)", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Dados carregados:")
        st.write(df)
        
        if st.button("Analisar Demonstrativo"):
            prompt = f"Analise os seguintes dados financeiros e forneça insights importantes:\n{df.to_string()}"
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é um especialista contábil."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            st.write("### Análise:")
            st.write(response.choices[0].message.content)

elif opcao == "Classificação de Contas":
    st.header("Classificação de Contas")
    
    descricao = st.text_area("Digite a descrição da transação:")
    
    if st.button("Classificar"):
        prompt = f"Classifique a seguinte transação contábil e sugira a conta adequada:\n{descricao}"
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um especialista contábil."},
                {"role": "user", "content": prompt}
            ]
        )
        
        st.write("### Classificação:")
        st.write(response.choices[0].message.content)

elif opcao == "Cálculos Contábeis":
    st.header("Cálculos Contábeis")
    
    calculo_tipo = st.selectbox(
        "Selecione o tipo de cálculo",
        ["Depreciação", "Margem de Lucro", "Análise de Impostos"]
    )
    
    if calculo_tipo == "Depreciação":
        valor_bem = st.number_input("Valor do bem (R$)", min_value=0.0)
        vida_util = st.number_input("Vida útil (anos)", min_value=1)
        
        if st.button("Calcular Depreciação"):
            depreciacao_anual = valor_bem / vida_util
            depreciacao_mensal = depreciacao_anual / 12
            
            st.write("### Resultados:")
            st.write(f"Depreciação Anual: R$ {depreciacao_anual:.2f}")
            st.write(f"Depreciação Mensal: R$ {depreciacao_mensal:.2f}")
            
            # Gerar tabela de depreciação
            dados_depreciacao = []
            valor_atual = valor_bem
            for ano in range(1, int(vida_util) + 1):
                dados_depreciacao.append({
                    "Ano": ano,
                    "Valor Inicial": valor_atual,
                    "Depreciação": depreciacao_anual,
                    "Valor Final": valor_atual - depreciacao_anual
                })
                valor_atual -= depreciacao_anual
            
            df_depreciacao = pd.DataFrame(dados_depreciacao)
            st.write("### Tabela de Depreciação Anual")
            st.dataframe(df_depreciacao)
    
    elif calculo_tipo == "Margem de Lucro":
        custo = st.number_input("Custo total (R$)", min_value=0.0)
        preco_venda = st.number_input("Preço de venda (R$)", min_value=0.0)
        
        if st.button("Calcular Margem"):
            if preco_venda > 0:
                margem_lucro = ((preco_venda - custo) / preco_venda) * 100
                lucro_valor = preco_venda - custo
                
                st.write("### Resultados:")
                st.write(f"Margem de Lucro: {margem_lucro:.2f}%")
                st.write(f"Lucro em R$: {lucro_valor:.2f}")
                
                # Gráfico de composição
                dados_grafico = pd.DataFrame({
                    'Componente': ['Custo', 'Lucro'],
                    'Valor': [custo, lucro_valor]
                })
                st.bar_chart(dados_grafico.set_index('Componente'))
    
    elif calculo_tipo == "Análise de Impostos":
        valor_base = st.number_input("Valor base (R$)", min_value=0.0)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            pis = st.number_input("PIS (%)", min_value=0.0, value=0.65)
        with col2:
            cofins = st.number_input("COFINS (%)", min_value=0.0, value=3.0)
        with col3:
            iss = st.number_input("ISS (%)", min_value=0.0, value=5.0)
            
        if st.button("Calcular Impostos"):
            valor_pis = valor_base * (pis/100)
            valor_cofins = valor_base * (cofins/100)
            valor_iss = valor_base * (iss/100)
            total_impostos = valor_pis + valor_cofins + valor_iss
            
            st.write("### Resultados:")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("Valores por imposto:")
                st.write(f"PIS: R$ {valor_pis:.2f}")
                st.write(f"COFINS: R$ {valor_cofins:.2f}")
                st.write(f"ISS: R$ {valor_iss:.2f}")
                st.write(f"Total de impostos: R$ {total_impostos:.2f}")
            
            with col2:
                # Gráfico de pizza dos impostos
                dados_impostos = pd.DataFrame({
                    'Imposto': ['PIS', 'COFINS', 'ISS'],
                    'Valor': [valor_pis, valor_cofins, valor_iss]
                })
                st.write("Distribuição dos impostos:")
                st.bar_chart(dados_impostos.set_index('Imposto'))

elif opcao == "Folha de Pagamento":
    st.header("Cálculos de Folha de Pagamento")
    
    salario_base = st.number_input("Salário Base (R$)", min_value=0.0)
    horas_extras = st.number_input("Quantidade de Horas Extras", min_value=0.0)
    valor_hora_extra = st.number_input("Valor da Hora Extra (R$)", min_value=0.0)
    
    # Adicionar outros benefícios
    st.subheader("Benefícios")
    vale_transporte = st.checkbox("Vale Transporte")
    vale_alimentacao = st.number_input("Vale Alimentação (R$)", min_value=0.0)
    
    if st.button("Calcular Folha"):
        # Cálculos básicos
        valor_total_horas_extras = horas_extras * valor_hora_extra
        
        # INSS
        if salario_base <= 1320.00:
            inss = salario_base * 0.075
        elif salario_base <= 2571.29:
            inss = salario_base * 0.09
        elif salario_base <= 3856.94:
            inss = salario_base * 0.12
        else:
            inss = salario_base * 0.14
        
        # Vale Transporte (6% do salário base)
        desconto_vt = salario_base * 0.06 if vale_transporte else 0
        
        # Total de proventos e descontos
        total_proventos = salario_base + valor_total_horas_extras + vale_alimentacao
        total_descontos = inss + desconto_vt
        salario_liquido = total_proventos - total_descontos
        
        # Exibição dos resultados
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Proventos")
            st.write(f"Salário Base: R$ {salario_base:.2f}")
            st.write(f"Horas Extras: R$ {valor_total_horas_extras:.2f}")
            st.write(f"Vale Alimentação: R$ {vale_alimentacao:.2f}")
            st.write(f"**Total Proventos: R$ {total_proventos:.2f}**")
        
        with col2:
            st.write("### Descontos")
            st.write(f"INSS: R$ {inss:.2f}")
            if vale_transporte:
                st.write(f"Vale Transporte: R$ {desconto_vt:.2f}")
            st.write(f"**Total Descontos: R$ {total_descontos:.2f}**")
        
        st.write("---")
        st.write(f"### Salário Líquido: R$ {salario_liquido:.2f}")
        
        # Gráfico de composição salarial
        dados_grafico = pd.DataFrame({
            'Componente': ['Salário Base', 'Horas Extras', 'Benefícios', 'Descontos'],
            'Valor': [salario_base, valor_total_horas_extras, vale_alimentacao, -total_descontos]
        })
        st.write("### Composição Salarial")
        st.bar_chart(dados_grafico.set_index('Componente'))

elif opcao == "Análise de Balanço":
    st.header("Análise de Balanço Patrimonial")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Ativo")
        ativo_circulante = st.number_input("Ativo Circulante (R$)", min_value=0.0)
        disponivel = st.number_input("Disponível (R$)", min_value=0.0)
        estoque = st.number_input("Estoque (R$)", min_value=0.0)
        ativo_total = st.number_input("Ativo Total (R$)", min_value=0.0)
    
    with col2:
        st.subheader("Passivo")
        passivo_circulante = st.number_input("Passivo Circulante (R$)", min_value=0.0)
        passivo_total = st.number_input("Passivo Total (R$)", min_value=0.0)
        patrimonio_liquido = st.number_input("Patrimônio Líquido (R$)", min_value=0.0)
    
    # Dados de Resultado
    st.subheader("Dados de Resultado")
    lucro_liquido = st.number_input("Lucro Líquido (R$)", min_value=0.0)
    vendas_liquidas = st.number_input("Vendas Líquidas (R$)", min_value=0.0)
    
    if st.button("Calcular Índices"):
        # Cálculo dos índices
        liquidez_corrente = ativo_circulante / passivo_circulante if passivo_circulante != 0 else 0
        liquidez_seca = (ativo_circulante - estoque) / passivo_circulante if passivo_circulante != 0 else 0
        liquidez_imediata = disponivel / passivo_circulante if passivo_circulante != 0 else 0
        
        endividamento = (passivo_total / ativo_total * 100) if ativo_total != 0 else 0
        rentabilidade_pl = (lucro_liquido / patrimonio_liquido * 100) if patrimonio_liquido != 0 else 0
        margem_liquida = (lucro_liquido / vendas_liquidas * 100) if vendas_liquidas != 0 else 0
        
        # Exibição dos resultados
        st.write("### Índices de Liquidez")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Liquidez Corrente", f"{liquidez_corrente:.2f}")
        with col2:
            st.metric("Liquidez Seca", f"{liquidez_seca:.2f}")
        with col3:
            st.metric("Liquidez Imediata", f"{liquidez_imediata:.2f}")
        
        st.write("### Índices de Estrutura e Rentabilidade")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Endividamento", f"{endividamento:.2f}%")
        with col2:
            st.metric("Rentabilidade do PL", f"{rentabilidade_pl:.2f}%")
        with col3:
            st.metric("Margem Líquida", f"{margem_liquida:.2f}%")
        
        # Análise automática dos índices
        st.write("### Análise dos Índices")
        analise = []
        
        if liquidez_corrente > 1:
            analise.append("✅ A empresa possui boa liquidez corrente")
        else:
            analise.append("⚠️ A liquidez corrente está abaixo do ideal")
            
        if endividamento < 60:
            analise.append("✅ Nível de endividamento adequado")
        else:
            analise.append("⚠️ Alto nível de endividamento")
            
        if rentabilidade_pl > 10:
            analise.append("✅ Boa rentabilidade do Patrimônio Líquido")
        else:
            analise.append("⚠️ Rentabilidade do PL abaixo do esperado")
        
        for item in analise:
            st.write(item)
        
        # Gráfico de composição do Ativo
        dados_ativo = pd.DataFrame({
            'Componente': ['Disponível', 'Estoque', 'Outros Ativos'],
            'Valor': [disponivel, estoque, ativo_total - disponivel - estoque]
        })
        st.write("### Composição do Ativo")
        st.bar_chart(dados_ativo.set_index('Componente'))


elif opcao == "Controle de Orçamento":
    st.header("Controle de Orçamento")
    
    # Seleção do período
    periodo = st.selectbox("Selecione o período", ["Mensal", "Trimestral", "Anual"])
    
    # Categorias de receitas e despesas
    categorias = ["Vendas", "Serviços", "Custos Operacionais", "Despesas Administrativas", 
                 "Despesas com Pessoal", "Marketing", "Outros"]
    
    st.subheader("Valores Orçados vs Realizados")
    
    dados_orcamento = []
    for categoria in categorias:
        col1, col2 = st.columns(2)
        with col1:
            orcado = st.number_input(f"{categoria} - Orçado (R$)", min_value=0.0, key=f"orc_{categoria}")
        with col2:
            realizado = st.number_input(f"{categoria} - Realizado (R$)", min_value=0.0, key=f"real_{categoria}")
        
        dados_orcamento.append({
            "Categoria": categoria,
            "Orçado": orcado,
            "Realizado": realizado,
            "Variação": realizado - orcado,
            "Variação %": ((realizado - orcado) / orcado * 100) if orcado != 0 else 0
        })
    
    if st.button("Analisar Orçamento"):
        df_orcamento = pd.DataFrame(dados_orcamento)
        
        # Totais
        total_orcado = df_orcamento["Orçado"].sum()
        total_realizado = df_orcamento["Realizado"].sum()
        variacao_total = total_realizado - total_orcado
        
        # Exibição dos resultados
        st.write("### Resumo do Orçamento")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Orçado", f"R$ {total_orcado:,.2f}")
        with col2:
            st.metric("Total Realizado", f"R$ {total_realizado:,.2f}")
        with col3:
            st.metric("Variação", f"R$ {variacao_total:,.2f}", 
                     delta=f"{(variacao_total/total_orcado*100 if total_orcado != 0 else 0):,.2f}%")
        
        # Tabela detalhada
        st.write("### Análise Detalhada")
        st.dataframe(df_orcamento.style.format({
            "Orçado": "R$ {:,.2f}",
            "Realizado": "R$ {:,.2f}",
            "Variação": "R$ {:,.2f}",
            "Variação %": "{:,.2f}%"
        }))
        
        # Gráfico comparativo
        chart_data = pd.DataFrame({
            "Categoria": categorias,
            "Orçado": df_orcamento["Orçado"],
            "Realizado": df_orcamento["Realizado"]
        }).melt(id_vars=["Categoria"])
        
        st.write("### Comparativo Orçado vs Realizado")
        st.bar_chart(chart_data.set_index("Categoria"))
        
        # Análise automática
        st.write("### Análise de Variações")
        for _, row in df_orcamento.iterrows():
            if abs(row["Variação %"]) > 10:
                if row["Variação"] > 0:
                    st.warning(f"⚠️ {row['Categoria']}: Realizado {row['Variação %']:.1f}% acima do orçado")
                else:
                    st.info(f"ℹ️ {row['Categoria']}: Realizado {abs(row['Variação %']):.1f}% abaixo do orçado")

elif opcao == "Fluxo de Caixa":
    st.header("Projeção de Fluxo de Caixa")
    
    # Configuração do período
    num_meses = st.slider("Número de meses para projeção", 1, 12, 3)
    saldo_inicial = st.number_input("Saldo Inicial (R$)", value=0.0)
    
    # Entradas recorrentes
    st.subheader("Entradas Recorrentes")
    receita_vendas = st.number_input("Receita Mensal de Vendas (R$)", min_value=0.0)
    receita_servicos = st.number_input("Receita Mensal de Serviços (R$)", min_value=0.0)
    outras_receitas = st.number_input("Outras Receitas Mensais (R$)", min_value=0.0)
    
    # Saídas recorrentes
    st.subheader("Saídas Recorrentes")
    custos_fixos = st.number_input("Custos Fixos Mensais (R$)", min_value=0.0)
    folha_pagamento = st.number_input("Folha de Pagamento Mensal (R$)", min_value=0.0)
    impostos = st.number_input("Impostos Mensais (R$)", min_value=0.0)
    outras_despesas = st.number_input("Outras Despesas Mensais (R$)", min_value=0.0)
    
    if st.button("Gerar Fluxo de Caixa"):
        # Cálculo do fluxo
        meses = [f"Mês {i+1}" for i in range(num_meses)]
        total_entradas = receita_vendas + receita_servicos + outras_receitas
        total_saidas = custos_fixos + folha_pagamento + impostos + outras_despesas
        
        fluxo_mensal = total_entradas - total_saidas
        
        # Criação do DataFrame
        dados_fluxo = []
        saldo_atual = saldo_inicial
        
        for mes in meses:
            saldo_atual += fluxo_mensal
            dados_fluxo.append({
                "Mês": mes,
                "Entradas": total_entradas,
                "Saídas": total_saidas,
                "Fluxo Líquido": fluxo_mensal,
                "Saldo Final": saldo_atual
            })
        
        df_fluxo = pd.DataFrame(dados_fluxo)
        
        # Exibição dos resultados
        st.write("### Resumo do Fluxo de Caixa")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Mensal Entradas", f"R$ {total_entradas:,.2f}")
        with col2:
            st.metric("Total Mensal Saídas", f"R$ {total_saidas:,.2f}")
        with col3:
            st.metric("Fluxo Líquido Mensal", f"R$ {fluxo_mensal:,.2f}", 
                     delta=f"R$ {saldo_atual - saldo_inicial:,.2f}")
        
        # Tabela detalhada
        st.write("### Projeção Detalhada")
        st.dataframe(df_fluxo.style.format({
            "Entradas": "R$ {:,.2f}",
            "Saídas": "R$ {:,.2f}",
            "Fluxo Líquido": "R$ {:,.2f}",
            "Saldo Final": "R$ {:,.2f}"
        }))
        
        # Gráfico de evolução
        st.write("### Evolução do Saldo")
        st.line_chart(df_fluxo.set_index("Mês")["Saldo Final"])
        
        # Análise automática
        st.write("### Análise do Fluxo")
        if fluxo_mensal > 0:
            st.success(f"✅ Fluxo de caixa positivo de R$ {fluxo_mensal:,.2f} por mês")
        else:
            st.error(f"⚠️ Fluxo de caixa negativo de R$ {abs(fluxo_mensal):,.2f} por mês")
        
        if saldo_atual > saldo_inicial:
            st.success(f"✅ Projeção de aumento no saldo de R$ {saldo_atual - saldo_inicial:,.2f}")
        else:
            st.warning(f"⚠️ Projeção de redução no saldo de R$ {abs(saldo_atual - saldo_inicial):,.2f}")

elif opcao == "Análise DRE":
    st.header("Análise da Demonstração do Resultado do Exercício")
    
    # Receitas
    st.subheader("Receitas")
    receita_bruta = st.number_input("Receita Bruta (R$)", min_value=0.0)
    deducoes = st.number_input("Deduções da Receita (R$)", min_value=0.0)
    
    # Custos
    st.subheader("Custos")
    custo_produtos = st.number_input("Custo dos Produtos Vendidos (R$)", min_value=0.0)
    
    # Despesas
    st.subheader("Despesas Operacionais")
    despesas_vendas = st.number_input("Despesas com Vendas (R$)", min_value=0.0)
    despesas_administrativas = st.number_input("Despesas Administrativas (R$)", min_value=0.0)
    despesas_financeiras = st.number_input("Despesas Financeiras (R$)", min_value=0.0)
    
    if st.button("Analisar DRE"):
        # Cálculos
        receita_liquida = receita_bruta - deducoes
        lucro_bruto = receita_liquida - custo_produtos
        total_despesas = despesas_vendas + despesas_administrativas + despesas_financeiras
        lucro_operacional = lucro_bruto - total_despesas
        
        # Cálculo de margens
        margem_bruta = (lucro_bruto / receita_liquida * 100) if receita_liquida != 0 else 0
        margem_operacional = (lucro_operacional / receita_liquida * 100) if receita_liquida != 0 else 0
        
        # Exibição dos resultados
        st.write("### Demonstração do Resultado")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Receita Bruta:** R$ {:,.2f}".format(receita_bruta))
            st.write("(-) **Deduções:** R$ {:,.2f}".format(deducoes))
            st.write("**Receita Líquida:** R$ {:,.2f}".format(receita_liquida))
            st.write("(-) **CPV:** R$ {:,.2f}".format(custo_produtos))
            st.write("**Lucro Bruto:** R$ {:,.2f}".format(lucro_bruto))
            st.write("(-) **Despesas Operacionais:** R$ {:,.2f}".format(total_despesas))
            st.write("**Lucro Operacional:** R$ {:,.2f}".format(lucro_operacional))
        
        with col2:
            st.metric("Margem Bruta", f"{margem_bruta:.2f}%")
            st.metric("Margem Operacional", f"{margem_operacional:.2f}%")
        
        # Análise vertical
        st.write("### Análise Vertical")
        dados_analise = {
            "Componente": ["Deduções", "CPV", "Despesas Operacionais", "Lucro Operacional"],
            "Valor": [deducoes, custo_produtos, total_despesas, lucro_operacional],
            "% da Receita": [
                (deducoes/receita_bruta*100) if receita_bruta != 0 else 0,
                (custo_produtos/receita_bruta*100) if receita_bruta != 0 else 0,
                (total_despesas/receita_bruta*100) if receita_bruta != 0 else 0,
                (lucro_operacional/receita_bruta*100) if receita_bruta != 0 else 0
            ]
        }
        
        df_analise = pd.DataFrame(dados_analise)
        st.dataframe(df_analise.style.format({
            "Valor": "R$ {:,.2f}",
            "% da Receita": "{:.2f}%"
        }))
        
        # Gráfico de composição
        st.write("### Composição do Resultado")
        st.bar_chart(df_analise.set_index("Componente")["Valor"])
        
        # Análise automática
        st.write("### Análise dos Indicadores")
        if margem_bruta > 30:
            st.success("✅ Boa margem bruta (>30%)")
        else:
            st.warning("⚠️ Margem bruta abaixo do ideal")
            
        if margem_operacional > 15:
            st.success("✅ Boa margem operacional (>15%)")
        else:
            st.warning("⚠️ Margem operacional precisa de atenção")
            
        if total_despesas > lucro_bruto:
            st.error("⚠️ Despesas operacionais superiores ao lucro bruto")

elif opcao == "Análise de Indicadores":
    st.header("Análise de Indicadores Financeiros")
    
    # Dados financeiros
    st.subheader("Dados do Período")
    faturamento = st.number_input("Faturamento (R$)", min_value=0.0)
    lucro_liquido = st.number_input("Lucro Líquido (R$)", min_value=0.0)
    ativo_total = st.number_input("Ativo Total (R$)", min_value=0.0)
    patrimonio_liquido = st.number_input("Patrimônio Líquido (R$)", min_value=0.0)
    
    # Dados operacionais
    st.subheader("Dados Operacionais")
    prazo_medio_recebimento = st.number_input("Prazo Médio de Recebimento (dias)", min_value=0)
    prazo_medio_pagamento = st.number_input("Prazo Médio de Pagamento (dias)", min_value=0)
    giro_estoque = st.number_input("Giro do Estoque (vezes/ano)", min_value=0.0)
    
    if st.button("Calcular Indicadores"):
        # Cálculos dos indicadores
        rentabilidade_vendas = (lucro_liquido / faturamento * 100) if faturamento != 0 else 0
        rentabilidade_ativo = (lucro_liquido / ativo_total * 100) if ativo_total != 0 else 0
        rentabilidade_pl = (lucro_liquido / patrimonio_liquido * 100) if patrimonio_liquido != 0 else 0
        ciclo_operacional = prazo_medio_recebimento + (365/giro_estoque if giro_estoque != 0 else 0)
        ciclo_financeiro = ciclo_operacional - prazo_medio_pagamento
        
        # Exibição dos resultados
        st.write("### Indicadores de Rentabilidade")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rentabilidade das Vendas", f"{rentabilidade_vendas:.2f}%")
        with col2:
            st.metric("Rentabilidade do Ativo", f"{rentabilidade_ativo:.2f}%")
        with col3:
            st.metric("Rentabilidade do PL", f"{rentabilidade_pl:.2f}%")
        
        st.write("### Indicadores de Ciclo")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Ciclo Operacional", f"{ciclo_operacional:.0f} dias")
        with col2:
            st.metric("Ciclo Financeiro", f"{ciclo_financeiro:.0f} dias")
        
        # Análise dos indicadores
        st.write("### Análise dos Indicadores")
        analises = []
        
        # Análise de rentabilidade
        if rentabilidade_vendas > 15:
            analises.append("✅ Excelente rentabilidade das vendas")
        elif rentabilidade_vendas > 10:
            analises.append("✓ Boa rentabilidade das vendas")
        else:
            analises.append("⚠️ Rentabilidade das vendas precisa de atenção")
        
        # Análise do ciclo
        if ciclo_financeiro < 30:
            analises.append("✅ Ciclo financeiro eficiente")
        elif ciclo_financeiro < 45:
            analises.append("✓ Ciclo financeiro adequado")
        else:
            analises.append("⚠️ Ciclo financeiro extenso - considere otimização")
        
        # Exibição das análises
        for analise in analises:
            st.write(analise)
        
        # Gráfico comparativo de ciclos
        dados_ciclo = pd.DataFrame({
            'Ciclo': ['Prazo Recebimento', 'Prazo Pagamento', 'Ciclo Operacional', 'Ciclo Financeiro'],
            'Dias': [prazo_medio_recebimento, prazo_medio_pagamento, ciclo_operacional, ciclo_financeiro]
        })
        
        st.write("### Comparativo de Ciclos")
        st.bar_chart(dados_ciclo.set_index('Ciclo'))
        
        # Recomendações
        st.write("### Recomendações")
        if ciclo_financeiro > prazo_medio_pagamento:
            st.info("💡 Considere negociar prazos maiores com fornecedores")
        if prazo_medio_recebimento > 45:
            st.info("💡 Avalie políticas de redução no prazo de recebimento")
        if rentabilidade_vendas < 10:
            st.info("💡 Analise a estrutura de custos e política de preços")

else:
    st.header("Dúvidas Contábeis")
    
    pergunta = st.text_area("Digite sua dúvida contábil:")
    
    if st.button("Enviar Pergunta"):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um especialista contábil."},
                {"role": "user", "content": pergunta}
            ]
        )
        
        st.write("### Resposta:")
        st.write(response.choices[0].message.content)