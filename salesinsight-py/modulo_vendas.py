"""
MÓDULO DE VENDAS - SalesInsight PY
===================================
Este arquivo contém TODAS as funções do pipeline de análise de vendas.
Cada função tem uma responsabilidade única (modularização).

Conceitos usados:
- listas [] e dicionários {} (estruturas nativas)
- laços for e condicionais if/elif/else
- leitura/escrita de arquivos com csv e json (biblioteca padrão)
"""

import csv       # módulo nativo para ler/escrever CSV
import json      # módulo nativo para ler/escrever JSON
import os        # módulo nativo para manipular caminhos e pastas
import random    # módulo nativo para gerar dados aleatórios (dataset sintético)

# ============================================================
# UTILITÁRIO: formatar número como "R$ 437.722.41"
# ============================================================
def formatar_moeda(valor):
    """
    Converte 437722.41 -> 'R$ 437.722.41'
    - formata valor numérico para (R$) com duas casas decimais.
    - ponto no decimal (o mesmo '.', sem trocar por vírgula)
    """
    return "R$ " + f"{valor:,.2f}"


# ============================================================
# 01 GERA DATASET SINTÉTICO .csv
# ============================================================

"""
    Cria um arquivo CSV com dados fictícios de vendas.
    - seed=42 garante que os dados sejam SEMPRE os mesmos (reprodutibilidade)
    - Insere propositalmente ~5% de valores vazios para testar a limpeza (RF03)
    """

def gerar_dataset_sintetico(caminho_arquivo="vendas.csv", n_registros=150, seed=42):


    random.seed(seed)  # Fixa valores aleatórios gerados sejam sempre os mesmos

    # Lista de produtos possíveis
    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor", "Teclado", "Mouse"]

    # Dicionário que mapeia cada produto à sua categoria
    categorias = {
        "Notebook": "Eletrônicos",
        "Smartphone": "Celulares",
        "Tablet": "Celulares",
        "Monitor": "Eletrônicos",
        "Teclado": "Acessórios",
        "Mouse": "Acessórios"
    }

    # Regiões do Brasil
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]

    # Cabeçalho do CSV (lista nomes das colunas)
    cabecalho = ["id_venda", "data_venda", "cliente", "produto",
                 "categoria", "regiao", "quantidade", "preco_unitario"]

    dados = []  # lista que vai acumular todas as linhas

    # Gerar a quantidade de registros definida (150 +1) e seleciona um produto aleatório em cada venda

    for i in range(1, n_registros + 1):
        prod = random.choice(produtos)

        # Simula dado nulo 5% de chance de gerar quantidade vazia
        qtd = str(random.randint(1, 8)) if random.random() > 0.05 else ""

        # 5% de chance de gerar preço vazio
        preco = str(round(random.uniform(100, 3500), 2)) if random.random() > 0.05 else ""

        # 10% de chance de adicionar espaços extras ao nome do produto
        # (para testar o .strip() na limpeza)
        prod_nome = f"  {prod} " if random.random() < 0.1 else prod

        # Cria um registro de venda com dados aleatórios e adiciona ao dataset
        dados.append([
            i,
            f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}",  # data aleatoria 2024
            f"Cliente_{random.randint(1, 30):03d}",                          # cliente aleatorio de 30
            prod_nome,
            categorias.get(prod, "Outros"),
            random.choice(regioes),
            qtd,
            preco
        ])

    # Escreve o arquivo CSV
    with open(caminho_arquivo, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(cabecalho)   # primeira linha = cabeçalho
        writer.writerows(dados)      # cria demais linhas = dados

    print(f"[OK] Dataset gerado em: {caminho_arquivo}")


# ============================================================
# 01.1 - CARREGAR CSV COM csv.DictReader
# ============================================================
def carregar_csv(caminho_arquivo):
    """
    Lê o CSV e retorna uma LISTA DE DICIONÁRIOS.
    Cada linha do CSV vira um dicionário: {"coluna": "valor", ...}
    Isso é feito automaticamente pelo csv.DictReader.
    """
    dados = []
    with open(caminho_arquivo, mode="r", encoding="utf-8") as f:
        leitor = csv.DictReader(f)   # usa o cabeçalho como chave de cada dicionário
        for linha in leitor:
            dados.append(linha)
    return dados


# ============================================================
# 02 - INSPECIONAR E DESCREVER OS DADOS
# ============================================================
def inspecionar_dados(dados):
    """
    Exibe:
    - total de registros carregados
    - campos disponíveis
    - exemplo do primeiro registro
    - quantidade de linhas com dados incompletos/nulos
    """

    print("=" * 60)
    print("\n=== INSPEÇÃO INICIAL DOS DADOS ===")
    print("=" * 60)
    print(f"Total de registros carregados: {len(dados)}")

    if dados:
        print(f"Campos disponíveis: {list(dados[0].keys())}")
        print(f"Exemplo do primeiro registro: {dados[0]}")

    # Conta linhas com quantidade OU preço vazios
    incompletos = 0
    for lin in dados:
        if not lin.get("quantidade", "").strip() or not lin.get("preco_unitario", "").strip():
            incompletos += 1

    print(f"Registros com dados incompletos/nulos: {incompletos}")


# ============================================================
# 03 - LIMPAR E TRATAR OS DADOS
# ============================================================
def limpar_dados(dados_brutos):
    """
    Remove espaços extras, descarta registros inválidos
    e converte quantidade -> int e preco_unitario -> float.
    """
    dados_limpos = []
    removidos = 0

    for lin in dados_brutos:
        # .strip() remove espaços em branco do começo e fim
        prod = lin["produto"].strip()
        cat  = lin["categoria"].strip()
        reg  = lin["regiao"].strip()
        cli  = lin["cliente"].strip()

        # Descarta se quantidade ou preço estiverem vazios
        if not lin["quantidade"] or not lin["preco_unitario"]:
            removidos += 1
            continue

        try:
            # Converte tipos (pode gerar ValueError se o dado for inválido)
            qtd   = int(lin["quantidade"])
            preco = float(lin["preco_unitario"])

            dados_limpos.append({
                "id_venda":       int(lin["id_venda"]),
                "data_venda":     lin["data_venda"].strip(),
                "cliente":        cli,
                "produto":        prod,
                "categoria":      cat,
                "regiao":         reg,
                "quantidade":     qtd,
                "preco_unitario": preco
            })
        except ValueError:
            # Se int() ou float() falhar, descarta a linha
            removidos += 1

    print("=" * 60)
    print("\n=== RELATÓRIO DE LIMPEZA ===")
    print("=" * 60)
    print(f"Registros Válidos: {len(dados_limpos)} | Registros Removidos: {removidos}")
    return dados_limpos


# ============================================================
# 04 - CRIAR CAMPOS DERIVADOS
# ============================================================
def criar_campos_derivados(dados):
    """
    Adiciona a cada dicionário:
    - receita_total = quantidade * preco_unitario
    - faixa_preco: "Baixo" (<500), "Médio" (500 a 2000), "Alto" (>2000)
    """
    for item in dados:
        receita = round(item["quantidade"] * item["preco_unitario"], 2)
        item["receita_total"] = receita

        if receita < 500:
            item["faixa_preco"] = "Baixo"
        elif receita <= 2000:
            item["faixa_preco"] = "Médio"
        else:
            item["faixa_preco"] = "Alto"

    return dados


# ============================================================
# FUNÇÃO DE ORDEM SUPERIOR (usada no main.py com lambda)
# ============================================================
def processar_transformacao(dados, funcao):
    """
    Aplica uma função (passada como parâmetro) a cada item da lista.
    Exemplo de uso no main: mv.processar_transformacao(dados, lambda x: {...})
    """
    return [funcao(item) for item in dados]


# ============================================================
# 05 - CALCULAR MÉTRICAS AGREGADAS
# ============================================================
def calcular_metricas(dados):
    """
    Usa DICIONÁRIOS para agregar:
    - receita total por categoria
    - receita total por região
    - total geral da empresa
    """
    receita_categoria = {}
    receita_regiao    = {}
    total_geral       = 0.0

    for item in dados:
        cat = item["categoria"]
        reg = item["regiao"]
        rec = item["receita_total"]

        # .get(chave, 0.0) retorna 0.0 se a chave ainda não existir
        receita_categoria[cat] = round(receita_categoria.get(cat, 0.0) + rec, 2)
        receita_regiao[reg]    = round(receita_regiao.get(reg, 0.0) + rec, 2)
        total_geral += rec

    return {
        "total_geral":   round(total_geral, 2),
        "por_categoria": receita_categoria,
        "por_regiao":    receita_regiao
    }


# ============================================================
# 06 - SEGMENTAR CLIENTES POR NÍVEL DE GASTO
# ============================================================
def segmentar_clientes(dados):
    """
    Soma o gasto de cada cliente e classifica:
    - Abaixo de R$ 3.000  -> Bronze
    - R$ 3.000 a R$ 8.000 -> Prata
    - Acima de R$ 8.000   -> Ouro
    Retorna dicionário: {cliente: {"total_gasto": X, "segmento": Y}}
    """
    gastos_cliente = {}

    # Primeiro acumula o gasto de cada cliente
    for item in dados:
        cli = item["cliente"]
        gastos_cliente[cli] = gastos_cliente.get(cli, 0.0) + item["receita_total"]

    # Depois classifica cada um
    segmentos = {}
    for cli, total in gastos_cliente.items():
        if total > 8000:
            cat = "Ouro"
        elif total >= 3000:
            cat = "Prata"
        else:
            cat = "Bronze"

        segmentos[cli] = {"total_gasto": round(total, 2), "segmento": cat}

    return segmentos


# ============================================================
# FUNÇÃO EXTRA - TOP CLIENTES (usada no main.py)
# ============================================================
def obter_top_clientes(segmentos, top_n=5):
    """
    Retorna uma lista com os N clientes que mais gastaram,
    ordenada do maior para o menor.
    """
    # Transforma o dicionário em lista de tuplas (cliente, info)
    lista = list(segmentos.items())

    # Ordena pelo total_gasto em ordem decrescente
    lista.sort(key=lambda tupla: tupla[1]["total_gasto"], reverse=True)

    return lista[:top_n]


# ============================================================
# 07 (parte 2) - EXPORTAR RESULTADOS (CSV + JSON)
# ============================================================
def exportar_resultados(metricas, clientes, pasta_saida="outputs"):
    """
    Gera dois arquivos:
    - outputs/estatisticas.json (métricas + clientes)
    - outputs/metricas_resumo.csv (receita por categoria)
    """
    # Cria a pasta se não existir (exist_ok evita erro se já houver)
    os.makedirs(pasta_saida, exist_ok=True)

    # -------- JSON --------
    caminho_json = os.path.join(pasta_saida, "estatisticas.json")
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(
            {"metricas_gerais": metricas, "clientes": clientes},
            f,
            indent=4,              # formata bonito, com quebras de linha
            ensure_ascii=False     # mantém acentos legíveis (Médio, Região...)
        )
    print("=" * 60)
    print(f"[OK] Arquivo JSON exportado em: {caminho_json}")


    # -------- CSV --------
    caminho_csv = os.path.join(pasta_saida, "metricas_resumo.csv")
    with open(caminho_csv, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["Categoria", "Receita Total"])  # cabeçalho
        for cat, rec in metricas["por_categoria"].items():
          # Formata o número no padrão R$ 437.722.41
            valor_formatado = "R$ " + f"{rec:,.2f}".replace(",", ".")
            escritor.writerow([cat, rec])


    print(" ")
    print(f"[OK] Arquivo CSV exportado em: {caminho_csv}")
