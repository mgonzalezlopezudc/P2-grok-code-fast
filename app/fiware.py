# app/fiware.py

import requests
import uuid
from flask import current_app

class OrionClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')

    def _get_headers(self):
        return {'Content-Type': 'application/json'}

    def list_entities(self, entity_type, options='keyValues'):
        url = f"{self.base_url}/v2/entities"
        params = {'type': entity_type, 'options': options}
        response = requests.get(url, params=params, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def get_entity(self, entity_id, options='keyValues'):
        url = f"{self.base_url}/v2/entities/{entity_id}"
        params = {'options': options}
        response = requests.get(url, params=params, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def upsert_entity(self, entity):
        url = f"{self.base_url}/v2/op/update"
        data = {
            "actionType": "APPEND",
            "entities": [entity]
        }
        response = requests.post(url, json=data, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def update_entity_attrs(self, entity_id, attrs):
        url = f"{self.base_url}/v2/entities/{entity_id}/attrs"
        response = requests.patch(url, json=attrs, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def delete_entity(self, entity_id):
        url = f"{self.base_url}/v2/entities/{entity_id}"
        response = requests.delete(url, headers=self._get_headers())
        response.raise_for_status()
        return response.status_code == 204

def generate_entity_id(entity_type, suffix=None):
    if suffix:
        return f"urn:ngsi-ld:{entity_type}:{suffix}"
    return f"urn:ngsi-ld:{entity_type}:{str(uuid.uuid4())}"

def serialize_store(data):
    return {
        "id": data.get('id') or generate_entity_id('Store', data.get('code')),
        "type": "Store",
        "name": {"type": "Text", "value": data['name']},
        "address": {
            "type": "PostalAddress",
            "value": {
                "streetAddress": data['streetAddress'],
                "addressRegion": data['addressRegion'],
                "addressLocality": data['addressLocality'],
                "postalCode": data['postalCode']
            }
        },
        "location": {
            "type": "geo:json",
            "value": {
                "type": "Point",
                "coordinates": [float(data['longitude']), float(data['latitude'])]
            }
        },
        "url": {"type": "Text", "value": data.get('url', '')},
        "telephone": {"type": "Text", "value": data.get('telephone', '')},
        "countryCode": {"type": "Text", "value": data.get('countryCode', 'DE')},
        "capacity": {"type": "Number", "value": int(data['capacity'])},
        "description": {"type": "Text", "value": data.get('description', '')},
        "image": {"type": "Text", "value": data.get('image', '')}
    }

def serialize_product(data):
    return {
        "id": data.get('id') or generate_entity_id('Product'),
        "type": "Product",
        "name": {"type": "Text", "value": data['name']},
        "price": {"type": "Number", "value": float(data['price'])},
        "size": {"type": "Text", "value": data['size']},
        "color": {"type": "Text", "value": data['color']},
        "image": {"type": "Text", "value": data.get('image', '')}
    }

def serialize_employee(data):
    return {
        "id": data.get('id') or generate_entity_id('Employee'),
        "type": "Employee",
        "name": {"type": "Text", "value": data['name']},
        "image": {"type": "Text", "value": data.get('image', '')},
        "salary": {"type": "Number", "value": float(data['salary'])},
        "role": {"type": "Text", "value": data['role']},
        "refStore": {"type": "Relationship", "value": data['refStore']},
        "email": {"type": "Text", "value": data['email']},
        "dateOfContract": {"type": "Date", "value": data['dateOfContract']},
        "skills": {"type": "StructuredValue", "value": data.get('skills', [])},
        "username": {"type": "Text", "value": data['username']},
        "password": {"type": "Text", "value": data['password']}
    }

def bootstrap_registrations(client):
    # Ensure registrations for stores 001-004
    for code in ['001', '002', '003', '004']:
        store_id = f"urn:ngsi-ld:Store:{code}"
        # Weather registration
        weather_reg = {
            "description": f"Store {code} weather provider",
            "dataProvided": {
                "entities": [{"id": store_id, "type": "Store"}],
                "attrs": ["temperature", "relativeHumidity"]
            },
            "provider": {
                "http": {"url": f"http://localhost:3000/random/weatherConditions"},
                "legacyForwarding": True
            },
            "status": "active"
        }
        try:
            requests.post(f"{client.base_url}/v2/registrations", json=weather_reg, headers=client._get_headers())
        except:
            pass  # Ignore if already exists

        # Tweets registration
        tweets_reg = {
            "description": f"Store {code} tweets provider",
            "dataProvided": {
                "entities": [{"id": store_id, "type": "Store"}],
                "attrs": ["tweets"]
            },
            "provider": {
                "http": {"url": f"http://localhost:3000/catfacts/tweets"},
                "legacyForwarding": True
            },
            "status": "active"
        }
        try:
            requests.post(f"{client.base_url}/v2/registrations", json=tweets_reg, headers=client._get_headers())
        except:
            pass

def bootstrap_subscriptions(client):
    # Product price change subscription
    price_sub = {
        "description": "Product price change",
        "subject": {
            "entities": [{"type": "Product"}],
            "condition": {"attrs": ["price"]}
        },
        "notification": {
            "http": {"url": "http://localhost:5000/subscription/price-change"},
            "attrs": ["price"]
        },
        "status": "active"
    }
    try:
        requests.post(f"{client.base_url}/v2/subscriptions", json=price_sub, headers=client._get_headers())
    except:
        pass

    # Low stock subscriptions for each store
    for code in ['001', '002', '003', '004']:
        low_stock_sub = {
            "description": f"Low stock store {code}",
            "subject": {
                "entities": [{"type": "InventoryItem"}],
                "condition": {
                    "attrs": ["shelfCount"],
                    "expression": {"q": f"shelfCount<10;refStore==urn:ngsi-ld:Store:{code}"}
                }
            },
            "notification": {
                "http": {"url": f"http://localhost:5000/subscription/low-stock-store{code}"},
                "attrs": ["shelfCount", "refProduct", "refStore", "refShelf"]
            },
            "status": "active"
        }
        try:
            requests.post(f"{client.base_url}/v2/subscriptions", json=low_stock_sub, headers=client._get_headers())
        except:
            pass

def bootstrap():
    client = OrionClient(current_app.config['ORION_BASE_URL'])
    bootstrap_registrations(client)
    bootstrap_subscriptions(client)