# SalesInsight PY - Pipeline de Análise de Dados de Vendas

README.md

# Descrição
O SalesInsight PY é um projeto desenvolvido em Python para análise de vendas utilizando um dataset sintético gerado automaticamente pelo sistema.

# Integrante
Maria Cristina Cavasotto Botao

# Objetivos do Projeto
Gerar um dataset sintético de vendas.
Realizar a leitura do arquivo CSV.
Identificar registros incompletos.
Limpar e padronizar os dados.
Criar campos derivados para análise.
Calcular métricas de receita.
Segmentar clientes por volume de compras.
Exportar resultados para CSV e JSON.
Estrutura do Projeto
salesinsight_py/
│
├── main.py
├── modulo_vendas.py
├── vendas.csv
├── README.md
│
└── outputs/
    ├── estatisticas.json
    └── metricas_resumo.csv
# Arquivos
main.py
Arquivo principal responsável por executar todas as etapas do projeto:

# Geração do dataset.
Leitura dos dados.
Inspeção dos registros.
Limpeza e tratamento.
Criação de métricas.
Segmentação de clientes.
Exportação dos resultados.

# Funcionalidades Implementadas
1. Geração de Dados
O sistema gera automaticamente um conjunto de registros de vendas simuladas contendo.

2. Limpeza de Dados
Durante a etapa de limpeza:

Espaços extras são removidos.
Valores vazios são identificados.
Registros inválidos são descartados.
Tipos numéricos são convertidos corretamente.

3. Campos Derivados
É criado o campo:

receita_total

Também é criada uma classificação, de acordo com o valor da venda:

Baixo
Médio
Alto


4. Métricas de Negócio
O projeto calcula:

Receita total geral.
Receita por categoria.
Receita por região.

5. Segmentação de Clientes
Os clientes são classificados em:

Segmento	Critério
Bronze	até R$ 2.999,99
Prata	de R$ 3.000,00 a R$ 8.000,00
Ouro	acima de R$ 8.000,00

6. Exportação de Resultados
Ao final da execução são gerados:
estatisticas.json
metricas_resumo.csv
para armazenamento e consulta posterior.

==================================================

# Como Executar
Execute o arquivo principal:

python main.py
ou execute as células do notebook no Google Colab na ordem apresentada.

# Saída Esperada
Ao final da execução será exibido um resumo semelhante a:

==================================================
RESUMO EXECUTIVO
==================================================

Receita Total:
R$ 285.511,97

TOP 5 CLIENTES

Cliente_001 | R$ 12.540,50 | Ouro
Cliente_015 | R$ 10.845,20 | Ouro

Projeto executado com sucesso!
==================================================
