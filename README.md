### Optimization Highlights
- Raw SQL for performance-critical subscription queries (avoids ORM overhead).
- Indexed `user_id` and `is_active` to speed up lookups.
- `LIMIT 1` to reduce scanned rows.
- Batched inserts and updates in SQL (atomic ops).


`python main.py`

flask db init
flask db migrate
flask db upgrade
export PYTHONPATH=$(pwd)
export FLASK_APP=main.py
flask db migrate -m "Initial migration"

http://127.0.0.1:5000/api/auth/register

Body → raw → JSON:
 
{
  "email": "testuser@example.com",
  "password": "securepassword"
}