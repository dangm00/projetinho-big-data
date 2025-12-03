Dashboard de Serviços e Streamlit & Plotly

Este projeto é um dashboard interativo em Python para visualizar informações sobre serviços realizados, ganhos e regiões de atuação. Ele utiliza Streamlit para a interface web e Plotly para gráficos dinâmicos.



FUNÇOES:
Filtros interativos por serviço e período de datas.

Gráficos dinâmicos:

Pizza: dias trabalhados x não trabalhados.

Linha: ganhos por dia.

Barra: serviços mais realizados.

Barra: ganhos por mês.

Barra: quantidade de serviços por região.

Padronização de textos e acentos automaticamente.




REGIÃO ATRIBUÍDA AUTOMATICAMENTE COM BASE NOP SERVIÇO:

INSTALACAO → BAIXADA

MANUTENCAO → ZONA NORTE

IMPRODUTIVA → ZONA OESTE

Outros → BAIXADA(tive que padronizar por que estava muito sujo)



 Estrutura do Projeto:
projetinho/
│
├─ planilha_de_servicos.xlsx   # Planilha com os dados
├─ dashboard.py                # Código principal do dashboard
└─ README.md                   # Este arquivo



REQUISITOS:

Python 3.9+

Bibliotecas Python:

pandas

streamlit

plotly



INSTALE AS DEPENDENCIAS COM:

pip install pandas streamlit plotly

COMO EXECUTAR:

Abra o terminal na pasta do projeto.



EXECUTE:

streamlit run dashboard.py

O navegador abrirá automaticamente o dashboard.



DETALHES DOS GRÁFICOS:

1. Pizza - Dias Trabalhados x Não Trabalhados

Mostra a proporção de dias em que houve serviço e dias sem serviço.

2. Linha - Ganhos por Dia

Exibe os ganhos totais de cada dia do período filtrado.

3. Barra - Serviços Mais Realizados

Mostra a quantidade de cada tipo de serviço realizado no período filtrado.

4. Barra - Ganhos por Mês

Mostra a soma dos ganhos por mês.

5. Barra - Quantidade de Serviços por Região

Exibe quantos serviços foram realizados em cada região, preenchendo automaticamente com base no serviço(alterado para rodar da melhor froma).

INSTALACAO → BAIXADA

MANUTENCAO → ZONA NORTE

IMPRODUTIVA → ZONA OESTE

PERSONALIZAÇOES

Para adicionar novos tipos de serviço ou regiões, edite a função definir_regiao no dashboard.py.

Para alterar filtros ou gráficos, modifique os blocos correspondentes no código.

O dashboard é dinâmico: qualquer alteração na planilha será refletida ao recarregar o Streamlit.
