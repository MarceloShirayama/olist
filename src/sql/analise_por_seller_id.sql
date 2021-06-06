SELECT seller_id,
       COUNT(DISTINCT dt_sgmt) AS qte_safras
FROM tb_seller_sgmt
GROUP BY seller_id
ORDER BY COUNT(DISTINCT dt_sgmt) DESC;
--
--
SELECT seller_id,
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
-- WHERE seller_id = 'fffd5413c0700ac820c7069d66d98c89'
WHERE seller_id = '001cca7ae9ae17fb1caed9dfb1094831'
ORDER BY dt_sgmt ASC;
