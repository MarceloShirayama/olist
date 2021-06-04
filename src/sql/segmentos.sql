-- RFV (recência, frequência e valor):
-- BFBV - baixa frequência e baixo valor
-- AFAV - alta frequência e alto valor
-- AFBV - alta frequência e baixo valor
-- AFAV - alta frequência e alto valor
-- SP - super produtivo
DROP TABLE if EXISTS tb_seller_sgmt;
CREATE TABLE tb_seller_sgmt AS
    SELECT
        T5.*,
        CASE
            WHEN perc_receita <= 0.5 AND perc_pedidos <= 0.5 THEN "BFBV"
            WHEN perc_receita > 0.5 AND perc_pedidos <= 0.5 THEN "BFAV"
            WHEN perc_receita <= 0.5 AND perc_pedidos > 0.5 THEN "AFBV"
            WHEN perc_receita > 0.9 AND perc_pedidos > 0.9 THEN "SP"
            ELSE "AFAV"
        END AS segto_freq_valor,

        CASE
            WHEN qtde_dias_base <= 60 THEN "inicio"
            WHEN qtde_dias_base >= 300 THEN "retencao"
            ELSE "ativo"
        END AS segto_vida,

        '2018-06-01' AS dt_sgmt

    FROM (
        SELECT
            T4.*,
            PERCENT_RANK() OVER (ORDER BY receita_total ASC) AS perc_receita,
            PERCENT_RANK() OVER (ORDER BY qtde_pedidos ASC) AS perc_pedidos
        FROM (
            SELECT
                T2.seller_id,
                SUM(T2.price) AS receita_total,
                COUNT(DISTINCT T1.order_id) AS qtde_pedidos,
                COUNT(t2.product_id) AS qtde_prods,
                COUNT(DISTINCT t2.product_id) AS qtde_prods_dist,
                CAST((JulianDay('2018-06-01') - JulianDay(T1.order_approved_at)) As Integer) AS qtde_dias_ult_vda,
                MAX(T1.order_approved_at) AS dt_ult_vda,
                CAST((JulianDay('2018-06-01') - JulianDay(dt_ini)) As Integer) AS qtde_dias_base
            FROM tb_orders AS T1
            LEFT JOIN tb_order_items AS T2
            ON T1.order_id = T2.order_id
        LEFT JOIN (
            SELECT
                T2.seller_id,
                MIN(DATE(T1.order_approved_at)) AS dt_ini
            FROM tb_orders AS T1
            LEFT JOIN tb_order_items AS T2
            ON T1.order_id = T2.order_id
            GROUP BY T2.seller_id
        ) AS T3
    ON T2.seller_id = T3.seller_id
    WHERE T1.order_approved_at BETWEEN '2017-06-01' AND '2018-06-01'
    GROUP BY T2.seller_id
    ) AS T4
    ) AS T5
WHERE seller_id IS NOT NULL
;