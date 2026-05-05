SELECT DISTINCT maker
FROM product
JOIN pc ON product.model = pc.model
WHERE speed >= 450;