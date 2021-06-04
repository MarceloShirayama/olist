SELECT
    T2.seller_id,
    SUM(T2.price) AS receita_total,
    COUNT(DISTINCT T1.order_id) AS qtde_pedidos,
    COUNT(t2.product_id) AS qtde_prods,
    COUNT(DISTINCT t2.product_id) AS qtde_prods_dist,
    CAST((JulianDay('2018-06-01') - JulianDay(T1.order_approved_at)) As Integer) AS qtde_dias_ult_vda,
    MAX(T1.order_approved_at) AS dt_ult_vda

FROM tb_orders AS T1
LEFT JOIN tb_order_items AS T2
ON T1.order_id = T2.order_id
WHERE T1.order_approved_at BETWEEN '2017-06-01' AND '2018-06-01'
GROUP BY T2.seller_id
