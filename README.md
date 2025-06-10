# Todo-List Full-Stack Demo



## Stack

| Layer     | Details |
|-----------|---------|
| **Backend** | FastAPI • SQLAlchemy • Pydantic v2 • Celery (Redis broker) |
| **Database** | PostgreSQL 16 (local install) |
| **Frontend** | React • Vite • Tailwind CSS |
| **API** | `GET /`, `GET /​todos`, `POST /​todos`, `PUT /​todos/{id}`, `DELETE /​todos/{id}` |


### 1. Clone & create folders

```bash
git clone https://github.com/<your-username>/<repo>.git
cd todo-list
```
### 2. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install "uvicorn[standard]" fastapi sqlalchemy psycopg2-binary pydantic celery redis python-dotenv
```
#### Create backend/.env:
```bash
DATABASE_URL=postgresql://<db_user>:<db_password>@localhost:5432/tododb
REDIS_URL=redis://localhost:6379/0
```
##### Initialise DB
```bash
createdb tododb    
```
##### Run API

```bash
uvicorn main:app --reload
```
##### Run Celery worker (new terminal)

```bash
celery -A app.celery_worker.celery worker --loglevel=info

```
### 3. Frontend
```bash
cd ../frontend
npm install
npm run dev 
```