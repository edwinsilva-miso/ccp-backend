declare -A APIS=(
#  ["bodegas-api"]="warehouses-api"
  ["clientes-api"]="customers-api"
#  ["entregas-api"]="deliveries-api"
#  ["inventarios-api"]="inventory-api"
  ["pedidos-api"]="orders-api"
  ["productos-api"]="products-api"
  ["fabricantes-api"]="manufacturers-api"
#  ["reportes-api"]="reports-api"
  ["rutas-api"]="routes-api"
#  ["transportes-api"]="transport-api"
  ["usuarios-api"]="users-api"
#  ["ventas-api"]="sales-api"
)


declare -A BACKENDS_FOR_FRONTEDS=(
  ["web-bff"]="web-bff"
  ["mobile-bff"]="mobile-bff"
)
