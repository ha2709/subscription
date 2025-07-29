# Subscription API

A Flask-based RESTful API for managing user subscriptions with performance-focused database optimizations.

---

##  Getting Started

###  Installation

```bash
git clone https://github.com/ha2709/subscription.git
cd subscription
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

###  Environment Setup

```
export PYTHONPATH=$(pwd)
export FLASK_APP=main.py
```

### Database Setup
 
This project uses PostgreSQL. Default connection:
 
`postgresql+psycopg2://postgres:postgres@localhost:5432/subscription`

### Steps

- Start PostgreSQL and create the database:

```bash
psql -U postgres
CREATE DATABASE subscription;
```

- Run migrations:
 
```bash
flask db migrate -m "Initial migration"
flask db upgrade
```

- Seed data:
 
`python scripts/seed_subscriptions.py`

### Run Application

`python main.py`

Server will run at: http://127.0.0.1:5000

## API Endpoints

### Register a New User

POST /api/auth/register

Body → raw → JSON:

```json
{
  "email": "testuser@example.com",
  "password": "securepassword"
}
```
 
## Optimization Highlights

### Query Optimizations

- Raw SQL used for performance-critical queries (avoids ORM overhead).

- Composite indexes on user_id, is_active, plan_id, and start_date.

- Pagination + Total Count Separation:

   - Read endpoints use two optimized queries:

   - One for paginated data (LIMIT, OFFSET)

   - One for total row count using COUNT(*)

   - This avoids full table scans and keeps pagination fast even on large datasets.

- Used LIMIT 1 where only one row is needed to minimize data scan.

- Bulk operations with batched inserts/updates for large data handling.

### Database Indexing Strategy

- Indexed user_id and is_active to accelerate active subscription lookups.

- Indexed end_date for fast retrieval of historical subscriptions.

- Composite indexes match WHERE and ORDER BY usage in queries.
 

## Performance Example

- Index: it takes 0.3 ms 

<img src="images/index.png" width="400"/> 

- Without Index , it takes 22 ms 

<img src="images/without-index.png" width="400"/>

Comparison of subscription query performance with and without proper indexing.

## Testing

Run tests with:

`pytest -v tests/`

Includes:

- Subscription logic tests.

- Performance and indexing tests.

## Tools & Stack

- Flask (RESTful API)

- SQLAlchemy Core + ORM

- PostgreSQL

- Flasgger (Swagger docs)

- Pytest (Unit testing)

## To Do

- Add pagination to other endpoints

- Enable rate-limiting or API key for production use

- Deploy to Docker/Kubernetes

- Enum Mapping for Plan ID

