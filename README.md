# Map My World API

Map My World is a backend API for exploring and reviewing locations and categories worldwide. It includes a special recommendations feature to keep results fresh and relevant, as described in the technical challenge requirements.

---

## Technical decisions

- **Architecture:** FastAPI app structured into routers, CRUD services, models, and schemas.
- **Database:** SQLAlchemy ORM with Pydantic models for validation.
- **Recommendations:** Single SQL query with subquery + CROSS JOIN for efficiency.
- **Testing:** pytest suite with isolated in-memory SQLite database.
- **Data integrity:** Unique constraints on coordinates and category names, range validation for latitude/longitude.

---

## Requirements

- Python 3.11
- (Optional) Virtual environment
- Database (default: in-memory SQLite, configurable via `SQLALCHEMY_DATABASE_URL`)

---

## Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd map_my_world
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

- By default, the API uses in-memory SQLite.
- To use PostgreSQL or another database, set the environment variable:
  ```bash
    export SQLALCHEMY_DATABASE_URL="postgresql://user:pass@localhost/dbname"
  ```

---

## Running the API

```bash
  uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

---

## Docker

Build and run the API in a container:

1. Build the image:
   ```bash
   docker build -t map-my-world-api .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 map-my-world-api
   ```
The API is available at `http://localhost:8000`.

---

## Endpoints

### Locations

- **Create**  
  `POST /locations/`  
  Request body:
  ```json
  {
    "latitude": 4.6110,
    "longitude": -74.0809
  }
  ```
  - **201**: location created  
  - **409**: location with these coordinates already exists

- **List**  
  `GET /locations/`  
  Returns a list of all locations.

---

### Categories

- **Create**  
  `POST /categories/`  
  Request body:
  ```json
  {
    "name": "Nature"
  }
  ```
  - **201**: category created  
  - **409**: category already exists

- **List**  
  `GET /categories/`

---

### Reviews

- **Create**  
  `POST /reviews/`  
  Request body:
  ```json
  {
    "location_id": 1,
    "category_id": 2,
    "reviewed_at": "2025-08-01T12:00:00Z"
  }
  ```
  - **201**: review created  
  - **404**: location or category not found

- **List**  
  `GET /reviews/`

---

### Recommendations

- **List recommendations**  
  `GET /recommendations/?limit=10`  
  Returns a list of objects:
  ```json
  {
    "location_id": 1,
    "category_id": 3,
    "never_reviewed": true
  }
  ```
  - `never_reviewed: true` → never reviewed
  - Sorted with `never_reviewed=true` first

---

## Tests

This project includes a pytest suite. To run the tests:

```bash
  pytest -q
```

---

## Project Structure

```
.
├── app                             # Contains the main application files.
│   ├── __init__.py                 # this file makes "app" a "Python package"
│   ├── main.py                     # Entry point; exposes `app`
│   ├── api.py                      # Defines create_app(), lifespan & routers
│   ├── dependencies                # Defines dependencies used by the routers
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── session.py
│   ├── routers                     # API route definitions
│   │   ├── __init__.py
│   │   ├── categories.py
│   │   ├── locations.py
│   │   ├── recommendations.py
│   │   └── reviews.py
│   ├── crud                        # Defines CRUD operations
│   │   ├── __init__.py
│   │   ├── category.py
│   │   ├── location.py
│   │   ├── recommendation.py
│   │   └── review.py
│   ├── schemas                     # Defines schemas
│   │   ├── __init__.py
│   │   ├── category.py
│   │   ├── location.py
│   │   ├── recommendation.py
│   │   └── review.py
│   ├── models                      # Defines database models
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── category.py
│   │   ├── location.py
│   │   └── review.py
│   └── utils
│       ├── __init__.py
│       └── exceptions.py           # HTTPException helpers
├── tests                           # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   ├── fixtures                    # Auxiliary fixtures
│   │   ├── __init__.py
│   │   ├── categories.py
│   │   ├── common.py
│   │   ├── database.py
│   │   ├── locations.py
│   │   └── review.py
│   ├── test_categories.py
│   ├── test_locations.py
│   ├── test_recommendations.py
│   └── test_reviews.py
├── requirements.txt
├── .gitignore
└── README.md
```