"""
ARQUIVO PRINCIPAL - SalesInsight PY
====================================
Ponto de entrada do pipeline. Importa as funções de modulo_vendas.py
e orquestra a execução de ponta a ponta (RF08).
"""

import os
import modulo_vendas as mv   # importa nosso módulo com as funções


def formatar_moeda(valor):
    """
    Converte um número no formato monetário brasileiro:
    1265714.21 -> 'R$ 1.265.714,21'

    Como funciona:
    1. f"{valor:,.2f}" gera '1,265,714.21' (padrão americano)
    2. .replace(",", "X") troca vírgulas por X temporariamente -> '1X265X714.21'
    3. .replace(".", ",") troca o ponto decimal por vírgula -> '1X265X714,21'
    4. .replace("X", ".") troca o X de volta por ponto -> '1.265.714,21'
    5. Prefixa com 'R$ '
    """

    return "R$ " + f"{valor:,.2f}".replace(",", ".")



def main():
    print("=" * 60)
    print(" SALESINSIGHT PY - Pipeline de Processamento com Python Nativo")
    print("=" * 60)

    arquivo_dados = "vendas.csv"

    # ---------- 1. Gerar dataset sintético se não existir ----------

    if not os.path.exists(arquivo_dados):
        mv.gerar_dataset_sintetico(arquivo_dados, n_registros=150)
    else:
        print(f"[INFO] Dataset já existe: {arquivo_dados}")

    # ---------- 2. Leitura + inspeção ----------

    dados_brutos = mv.carregar_csv(arquivo_dados)
    mv.inspecionar_dados(dados_brutos)

    # ---------- 3. Limpeza + campos derivados ----------

    dados_limpos        = mv.limpar_dados(dados_brutos)
    dados_transformados = mv.criar_campos_derivados(dados_limpos)

    # ---------- 4. Função de ordem superior com lambda ----------

    # Adiciona uma flag "processado": True em cada registro
    dados_com_tag = mv.processar_transformacao(
        dados_transformados,
        lambda x: {**x, "processado": True}
    )

    # ---------- 5. Métricas + segmentação ----------

    metricas     = mv.calcular_metricas(dados_com_tag)
    segmentos    = mv.segmentar_clientes(dados_com_tag)
    top_clientes = mv.obter_top_clientes(segmentos, top_n=5)

    # ---------- 6. Exibição do resumo (formato BR) ----------

    print("=" * 60)
    print("\n=== RESUMO EXECUTIVO ===")
    print("=" * 60)

    print(f"Receita Total da Empresa: {formatar_moeda(metricas['total_geral'])}")

    print("\nReceita por Categoria:")
    for cat, val in metricas["por_categoria"].items():
        print(f"  - {cat}: {formatar_moeda(val)}")

    print("\nReceita por Região:")
    for reg, val in metricas["por_regiao"].items():
        print(f"  - {reg}: {formatar_moeda(val)}")

    print("\nTop 5 Clientes em Valor de Venda:")
    for cli, info in top_clientes:
        print(f"  - {cli}: {formatar_moeda(info['total_gasto'])} ({info['segmento']})")


    # ---------- 7. Exportação ----------

    mv.exportar_resultados(metricas, segmentos)

    print("\n[CONCLUÍDO] Pipeline executado com sucesso!")


if __name__ == "__main__":
    main()
