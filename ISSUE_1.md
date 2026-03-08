# Implement FIWARE Supermarkets Application

## Description

Build a Flask-based web UI for managing supermarket entities stored in Orion NGSIv2, featuring CRUD operations, real-time updates via Socket.IO, internationalization (Spanish/English), map integration with Leaflet, and external provider data for weather and tweets. The app ensures Orion as the single source of truth, with bootstrap logic for subscriptions and registrations, and operational workflows for inventory management and purchases.

## Steps
1. **Infrastructure Setup Phase**: Set up Docker Compose environment with Orion, MongoDB, and tutorial context providers. Implement and test `./services start/stop` scripts and `import-data` seeding script to initialize baseline entities (Stores, Shelves, Products, InventoryItems, Employees) without provider-managed attributes.
2. **Flask App Foundation**: Create Flask app factory (`run.py`, `app/__init__.py`) with Socket.IO initialization and async mode handling (default threading, auto-adjust for eventlet). Set up basic configuration (`app/config.py`) and extensions (Orion client placeholder, Flask-Babel for i18n).
3. **Orion Client and Bootstrap Logic**: Implement `app/fiware.py` with OrionClient class for NGSIv2 operations (CRUD in key-values mode, ID generation, entity serializers). Add bootstrap functions to ensure 8 registrations (weather/tweets for stores 001-004) and subscriptions (price changes, low stock per store).
4. **Core Routes and Templates**: Develop `app/routes.py` for UI handlers (home, CRUD pages for Store/Product/Employee, embedded Shelf/InventoryItem forms). Create base template (`app/templates/base.html`) with Socket.IO client, i18n setup, and static asset links. Build initial Jinja2 templates for navigation and basic forms.
5. **CRUD Functionality**: Implement full CRUD operations for Store, Product, Employee entities via Orion API calls. Add form validations (HTML constraints + JS blocking) and dynamic select APIs (`/api/stores/<store_id>/available-shelves`, `/api/shelves/<shelf_id>/available-products`) to enforce inventory uniqueness.
6. **Inventory and Business Logic**: Add embedded Shelf/InventoryItem creation/edit in Product/Store detail pages. Implement purchase endpoint (`/inventory/<id>/buy`) with Orion patches to decrement shelfCount/stockCount, blocking if shelfCount <= 0. Display shelf fill progress and inventory groupings.
7. **Real-Time Integration**: Set up subscription callback endpoints (`/subscription/price-change`, `/subscription/low-stock-storeXXX`) to normalize payloads and emit Socket.IO events. Update `app/static/js/main.js` for event listeners (price updates, low-stock toasts, store panel appends).
8. **Map and External Data Display**: Integrate Leaflet in `Stores Map` view with CDN fallbacks and error handling. Display provider-managed attributes (temperature, humidity, tweets) in Store detail pages, assuming data availability from registrations.
9. **Internationalization**: Implement `app/i18n.py` for locale resolution (query/session/cookie/Accept-Language). Populate `translations/` catalogs for Spanish/English. Add language switching (`POST /set-language`) and inject JS messages as `window.I18N`.
10. **UI Polish and Responsiveness**: Develop `app/static/css/styles.css` for layout, map styles, and responsive behavior. Add home dashboard with KPI counters (e.g., entity counts) and Mermaid class diagram. Ensure all UI text is translatable.
11. **Testing and Validation**: Run unit tests for Orion operations and business rules. Manually test CRUD flows, real-time events, form validations, map loading, and i18n switching. Validate purchase blocking and inventory constraints.
12. **Deployment Preparation**: Configure runtime notes (async modes, binding to 0.0.0.0:5000). Ensure compatibility with `python run.py` and infra scripts.

## Relevant files
- `run.py` — Flask app entry point and factory.
- `app/__init__.py` — App initialization with extensions.
- `app/config.py` — Environment-based configuration.
- `app/fiware.py` — Orion client and bootstrap logic.
- `app/routes.py` — All route handlers and APIs.
- `app/i18n.py` — Locale resolution and Babel setup.
- `app/templates/base.html` — Base template with Socket.IO and i18n.
- `app/templates/*` — Individual page templates (home, CRUD forms, map).
- `app/static/js/main.js` — Frontend JS for real-time and interactions.
- `app/static/css/styles.css` — Styles for layout and responsiveness.
- `translations/*/LC_MESSAGES/messages.po` — Translation catalogs.
- `docker-compose.yml` — Infrastructure services.
- `services` — Lifecycle scripts.
- `import-data` — Seeding script.

## Verification
1. Infrastructure: Run `./services start` and verify Orion/MongoDB/providers are up; execute `import-data` and check seeded entities in Orion via API.
2. App Startup: Launch with `python run.py` and confirm no errors; test bootstrap (registrations/subscriptions created if AUTO_BOOTSTRAP=true).
3. CRUD: Create/edit/delete entities via UI; verify Orion updates and form validations block invalid data.
4. Business Logic: Attempt purchases; confirm decrements and blocking at shelfCount=0; test dynamic selects for unique assignments.
5. Real-Time: Trigger price changes/low stock via Orion; observe UI updates and toasts without page refresh.
6. Map: Load Stores Map; check markers from coordinates, popups, and fallback error on CDN failure.
7. I18n: Switch languages via navbar; verify text changes and persistence.
8. External Data: Ensure Store details show temperature/humidity/tweets when providers supply data.
9. Responsiveness: Test UI on different screen sizes; validate KPI counts and diagram rendering.

## Decisions
- Async mode defaults to threading for compatibility; eventlet only if explicitly set and runtime supports.
- Provider data (temperature, humidity, tweets) is read-only and displayed as-is; no local caching or error handling for missing data beyond UI checks.
- Employee passwords stored plain text as demo-only; no auth layer implemented.
- Map uses Leaflet with fallbacks; no offline alternative.
- KPIs on home: total counts of each entity type; diagram: Mermaid representation of entity relationships.

## Further Considerations
1. Clarify external provider endpoints and data formats (e.g., tweets structure) to ensure proper display and error handling.
2. Determine update frequency for provider data and any polling mechanisms if push isn't sufficient.
3. Consider adding authentication for production, hashing passwords, and securing endpoints.
4. Evaluate performance for large entity sets; add pagination if needed for lists.