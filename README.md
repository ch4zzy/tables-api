# Restaurant API
This API allows you to manage tables and orders for a restaurant.

## Endpoints

### Tables
```
GET /api/tables/: List all available tables.
POST /api/tables/: Create a new table.
```
### Orders
```
GET /api/orders/: List all orders.
POST /api/orders/: Create a new order.
```
### Available tables
```
GET /api/available_tables/?date=DD-MM-YYYY: List all available tables for a given date.
```
### Table reservations
```
GET /api/tables/<id>/reservations/: List all reservations for a table with ID <id>.
```
### Occupancy
```
GET /api/tables/occupancy/?date=DD-MM-YYYY: Occupancy for date
```