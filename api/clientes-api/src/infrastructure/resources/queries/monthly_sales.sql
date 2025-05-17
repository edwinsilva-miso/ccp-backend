SELECT
	o.id,
	o.created_at,
	o.quantity,
	o.subtotal,
	o.tax,
	o.total,
	o.currency,
	o.status
FROM
	orders o
WHERE
	date(o.created_at) BETWEEN :start_date AND :end_date
ORDER BY
    o.created_at