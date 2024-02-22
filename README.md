# Team-Builder

## How To Run
1. Once you have cloned the repo, move into the team-builder folder and create a virtual environment, follow steps 1-3 to create the virtual environmnet. If not creating a virtual environment, skip to step 4.
2. Run ```python3 -m venv venv```
3. Run ```source venv/bin/activate``` 
4. Run ```pip install -r requirements```
5. Create an .env file with:
    DATABASE_HOSTNAME=
    DATABASE_PORT=
    DATABASE_PASSWORD=
    DATABASE_NAME=
    DATABASE_USERNAME=
6. If you need to create the database, if not skip to step 8, run ```alembic revision --autogenerate -m "creating tables"```
7. Run ```alembic upgrade head```
8. Run ```uvicorn app.main:app --port 3000```
