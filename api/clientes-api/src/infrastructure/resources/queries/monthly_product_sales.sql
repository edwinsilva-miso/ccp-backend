SELECT 
    od.product_id, 
    sum(od.quantity) as total_quantity, 
    sum(od.total_price) as total_sales
FROM 
    order_details od
JOIN 
    orders o ON o.id = od.order_id
WHERE 
    date(o.created_at) BETWEEN :start_date AND :end_date
GROUP BY 
    od.product_id
ORDER BY 
    sum(od.quantity) DESC