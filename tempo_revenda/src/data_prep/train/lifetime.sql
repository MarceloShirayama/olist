SELECT *
FROM ( SELECT *,
              JULIANDAY(DATE( t4.order_approved_at )) - JULIANDAY(DATE( t4.last_sale )) AS qtde_dias,
              ROW_NUMBER() OVER ( partition BY t4.seller_id, t4.product_category_name ORDER BY RANDOM() ) AS random
       FROM ( SELECT t2.seller_id,
                     t3.product_category_name,
                     t1.order_approved_at,
                     LAG(t1.order_approved_at) OVER ( partition BY t2.seller_id,
                                                      t3.product_category_name
                                                      ORDER BY t1.order_approved_at ) AS last_sale
              FROM tb_orders AS t1
                   LEFT JOIN tb_order_items AS t2 ON t1.order_id = t2.order_id
                   LEFT JOIN tb_products AS t3 ON t2.product_id = t3.product_id
              WHERE t2.seller_id IS NOT NULL
                    AND t3.product_category_name IS NOT NULL
              ORDER BY t2.seller_id,
                       t1.order_approved_at ) AS t4
       WHERE t4.last_sale IS NOT NULL
             AND JULIANDAY(DATE( order_approved_at )) - JULIANDAY(DATE( last_sale )) > 0 ) AS t5
WHERE random = 1
