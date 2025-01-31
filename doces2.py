import streamlit as st
from ortools.linear_solver import pywraplp

# Título da aplicação
st.title("Otimização de Caixas para Doces")

# Entradas do usuário
st.header("Parâmetros de Entrada")
qtd_doces = st.number_input("Quantidade de Doces", min_value=1, value=500)

qtd_max_caixas = st.number_input("Quantidade Máxima de Tipos de Caixas", min_value=1, value=2)
tipo_caixas_input = st.text_input("Tipos de Caixas (separados por vírgula)", value="84, 70, 45, 35, 25")
custo_caixas_input = st.text_input("Custo de cada caixa (separados por vírgula)", value="5.00, 3.36, 4.60, 2.40, 1.90")

qtd_max_caixas_tipo = 1500

# Processar a entrada dos tipos de caixas e custos
tipo_caixas = [int(caixa.strip()) for caixa in tipo_caixas_input.split(",")]
custo_caixas = [float(custo.strip()) for custo in custo_caixas_input.split(",")]

# Botão para resolver o problema
if st.button("Otimizar"):
    # Criar o solver
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Definir as variáveis de decisão (quantidade de cada tipo de caixa)
    x = [solver.IntVar(0, qtd_max_caixas_tipo, f'x_{i}') for i in range(len(tipo_caixas))]
    y = [solver.BoolVar(f'y_{i}') for i in range(len(tipo_caixas))]
    z = solver.IntVar(0, qtd_doces, 'z')  # Excesso de doces

    # Função objetivo: minimizar o custo total das caixas
    solver.Minimize(solver.Sum(custo_caixas[i] * x[i] for i in range(len(tipo_caixas))))

    # Restrição: o total de doces embalados deve ser maior ou igual à quantidade necessária
    solver.Add(solver.Sum(tipo_caixas[i] * x[i] for i in range(len(tipo_caixas))) >= qtd_doces)

    # Garantir que o excesso de doces seja calculado corretamente
    solver.Add(solver.Sum(tipo_caixas[i] * x[i] for i in range(len(tipo_caixas))) - qtd_doces == z)

    # Garantir que x[i] só tenha valor positivo se y[i] for 1
    for i in range(len(tipo_caixas)):
        solver.Add(x[i] <= qtd_max_caixas_tipo * y[i])

    # Restrição: no máximo `qtd_max_caixas` tipos de caixas podem ser usados
    solver.Add(solver.Sum(y[i] for i in range(len(tipo_caixas))) <= qtd_max_caixas)

    # Resolver o problema
    status = solver.Solve()

    # Exibir resultados
    st.header("Resultados da Otimização")
    if status == pywraplp.Solver.OPTIMAL:
        st.success("Solução ótima encontrada!")
        custo_total = 0
        for i in range(len(tipo_caixas)):
            if int(x[i].solution_value()) > 0:
                quantidade = int(x[i].solution_value())
                custo_caixa = custo_caixas[i]
                custo_total += quantidade * custo_caixa
                st.write(f"Quantidade de caixas de tamanho {tipo_caixas[i]}: {quantidade} (Custo: R${quantidade * custo_caixa:.2f})")
        st.write(f"Custo total das caixas: R${custo_total:.2f}")
        st.write(f"Espaços vazios: {int(z.solution_value())}")
    else:
        st.error("Não foi encontrada uma solução ótima.")