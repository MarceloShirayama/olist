-- SQLite
SELECT
    dt_sgmt AS dt_segmentacao,
    COUNT(DISTINCT seller_id) AS qtde_vendedores
FROM tb_seller_sgmt
GROUP BY dt_sgmt
;

SELECT
    MIN(T1.order_approved_at) AS prim_dt_base_dados,
    MAX(T1.order_approved_at) AS ult_dt_base_dados
FROM tb_orders AS T1
;
