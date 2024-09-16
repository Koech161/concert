# concert
# dbdiagram
https://dbdiagram.io/d/concerts-66e540096dde7f4149172f1d

# Run the following commands in terminal
1. pipenv install
2. pipenv shell
3. pip install alembic sqlalchemy
4. alembic init
5. edit alembic.ini, sqlalchemy.url to = sqlite:///concert.db
6. alembic revision --autogenerate - m 'initial migration'
7. alembic upgrade head
8. python app.py