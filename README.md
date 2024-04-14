# meduzzen-internship

Welcome to my Meduzzen internship practice work.

### Installation & Setup
1. Clone this repository:

````angular2html
git clone https://github.com/nataliia-petrushak/meduzzen-intership.git
````
2. Make migrations:
````angular2html
cd app/db
alembic revision --autogenerate -m "create user table"
````
3. Create a database structure:
````angular2html
alembic upgrade head
````
4. In root directory build and start a Docker:
````angular2html
docker-compose up --build
````
