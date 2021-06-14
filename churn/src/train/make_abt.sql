SELECT '{date}' AS dt_referencia,
       t4.*,
       COALESCE(t3.qtde_vda, 0) AS qtde_vda_futura,
       CASE WHEN COALESCE(t3.qtde_vda, 0) = 0 THEN 1 ELSE 0 END flag_churn
FROM pre_abt_train_churn AS t4
     LEFT JOIN ( SELECT t2.seller_id,
                        COUNT(DISTINCT t1.order_id) AS qtde_vda
                 FROM tb_orders AS t1
                      LEFT JOIN tb_order_items AS t2 ON t1.order_id = t2.order_id
                 WHERE t1.order_purchase_timestamp >= '{date}'
                       AND t1.order_purchase_timestamp < DATE ( '{date}', '+3 month' )
                       AND t2.seller_id NOT NULL
                 GROUP BY t2.seller_id ) AS t3 ON t3.seller_id = t4.seller_id
-- ORDER BY dt_ult_vda ASC
