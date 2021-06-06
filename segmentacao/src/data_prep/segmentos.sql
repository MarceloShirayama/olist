-- RFV (recência, frequência e valor):
-- BFBV - baixa frequência e baixo valor
-- AFAV - alta frequência e alto valor
-- AFBV - alta frequência e baixo valor
-- AFAV - alta frequência e alto valor
-- SP - super produtivo
SELECT t5.*,
       CASE
           WHEN perc_receita <= 0.5
                AND perc_pedidos <= 0.5
           THEN "BFBV"
           WHEN perc_receita > 0.5
                AND perc_pedidos <= 0.5
           THEN "BFAV"
           WHEN perc_receita <= 0.5
                AND perc_pedidos > 0.5
           THEN "AFBV"
           WHEN perc_receita > 0.9
                AND perc_pedidos > 0.9
           THEN "SP"
           ELSE "AFAV"
       END AS segto_freq_valor,
       CASE
           WHEN qtde_dias_base <= 60
           THEN "inicio"
           WHEN qtde_dias_ult_vda >= 300
           THEN "retencao"
           ELSE "ativo"
       END AS segto_vida,
       '{date_end}' AS dt_sgmt
FROM ( SELECT t4.*,
              PERCENT_RANK() OVER ( ORDER BY receita_total ASC ) AS perc_receita,
              PERCENT_RANK() OVER ( ORDER BY qtde_pedidos ASC ) AS perc_pedidos
       FROM ( SELECT t2.seller_id,
                     SUM(t2.price) AS receita_total,
                     COUNT(DISTINCT t1.order_id) AS qtde_pedidos,
                     COUNT(t2.product_id) AS qtde_prods,
                     COUNT(DISTINCT t2.product_id) AS qtde_prods_dist,
                     CAST(( JULIANDAY('{date_end}') - JULIANDAY(t1.order_approved_at) ) AS integer) AS qtde_dias_ult_vda,
                     MAX(t1.order_approved_at) AS dt_ult_vda,
                     CAST(( JULIANDAY('{date_end}') - JULIANDAY(dt_ini) ) AS integer) AS qtde_dias_base
              FROM tb_orders AS t1
                   LEFT JOIN tb_order_items AS t2 ON t1.order_id = t2.order_id
                   LEFT JOIN ( SELECT t2.seller_id,
                                      MIN(DATE( t1.order_approved_at )) AS dt_ini
                               FROM tb_orders AS t1
                                    LEFT JOIN tb_order_items AS t2 ON t1.order_id = t2.order_id
                               GROUP BY t2.seller_id ) AS t3 ON t2.seller_id = t3.seller_id
              WHERE t1.order_approved_at BETWEEN '{date_init}'
                    AND '{date_end}'
              GROUP BY t2.seller_id ) AS t4 ) AS t5
WHERE seller_id IS NOT NULL
