# P2-grok-code-fast

FIWARE Supermarkets is a Flask web UI over Orion NGSIv2 to manage supermarket entities and monitor real-time updates.

## Features

- CRUD operations for Stores, Products, Shelves, InventoryItems, and Employees
- Real-time updates via Socket.IO for price changes and low stock alerts
- Internationalization support (Spanish/English)
- Interactive map with Leaflet for store locations
- Integration with external context providers for weather and tweets data
- Bootstrap logic for Orion subscriptions and registrations

## Setup

1. Start infrastructure: `./services start`
2. Seed data: `./import-data`
3. Run app: `python run.py`

## Requirements

- Docker and Docker Compose
- Python 3.x
- GitHub CLI (optional for remote operations)