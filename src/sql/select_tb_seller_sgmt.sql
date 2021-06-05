-- SQLite
SELECT
    seller_id,
    receita_total,
    qtde_pedidos,
    qtde_prods,
    qtde_prods_dist,
    qtde_dias_ult_vda,
    dt_ult_vda,
    qtde_dias_base,
    perc_receita,
    perc_pedidos,
    segto_freq_valor,
    segto_vida,
    dt_sgmt
FROM tb_seller_sgmt
LIMIT 10;
