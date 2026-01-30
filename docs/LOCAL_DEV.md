# Local development (no Docker)

## Backend
```bash
cd backend
python -m venv .venv
# Windows Git Bash:
source .venv/Scripts/activate
pip install -r requirements.txt

cp .env.example .env
# edit DATABASE_URL + REDIS_URL as needed

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8000
```

## Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
