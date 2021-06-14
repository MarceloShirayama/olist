DROP TABLE IF EXISTS pre_abt_{stage}_churn;
CREATE TABLE pre_abt_{stage}_churn AS
    SELECT t5.seller_id,
        MAX(t5.dt_vda) AS dt_ult_vda,
        -- Totais
        ROUND(SUM(t5.price), 2) AS receita_total,
        ROUND(SUM(t5.freight_value), 2) AS frete_total,
        COUNT(DISTINCT t5.order_id) AS qtde_total_vdas,
        COUNT(t5.product_id) AS qtde_total_itens_vda,
        COUNT(DISTINCT t5.product_id) AS qtde_dist_itens_vda,
        -- Médias por pedido (venda)
        ROUND(SUM(t5.price) / COUNT(DISTINCT t5.order_id), 2) AS receita_por_vda,
        ROUND(SUM(t5.freight_value) / COUNT(DISTINCT t5.order_id), 2) AS frete_por_vda,
        COUNT(t5.product_id) / COUNT(DISTINCT t5.order_id) AS itens_por_vda,
        --
        COUNT(DISTINCT STRFTIME('%m', dt_vda)) AS qtde_dist_meses_com_vda,
        ROUND(( COUNT(DISTINCT STRFTIME('%m', dt_vda)) / 6. ) * 100, 2) AS porc_ativacao
    FROM ( SELECT t1.order_id,
                t1.order_purchase_timestamp AS dt_vda,
                CASE
                    WHEN t1.order_delivered_customer_date > t1.order_estimated_delivery_date
                    THEN 1
                    ELSE 0
                END AS flag_atraso,
                t2.seller_id,
                t2.product_id,
                t2.price,
                t2.freight_value,
                t3.seller_state,
                t4.product_category_name
        FROM tb_orders AS t1
            LEFT JOIN tb_order_items AS t2 ON t1.order_id = t2.order_id
            LEFT JOIN tb_sellers AS t3 ON t2.seller_id = t3.seller_id
            LEFT JOIN tb_products AS t4 ON t2.product_id = t4.product_id
        WHERE t1.order_purchase_timestamp >= DATE ( '{date}', '-6 month' )
                AND t1.order_purchase_timestamp < '{date}'
                AND order_status = 'delivered' ) AS t5
    GROUP BY t5.seller_id
    HAVING MAX(t5.dt_vda) >= DATE ( '{date}', '-3 month' )
;
