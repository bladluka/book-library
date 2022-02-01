## Setup

- Clone repository
- Create database and user
- Rename .env.example to '.env' and set your values
```buildoutcfg
# SQLALCHEMY_DATABASE_URI MySQL template
SQLALCHEMY_DATABASE_URI=mysql+pymysql://<db_user>:<db_password>@<db_host>/<db_name>?charset=utf8mb4
```
- Create a virtual environment
```buildoutcfg
python -m venv venv
```
- Install packages from `requirements.txt`
```buildoutcfg
pip install -r requirements.txt
```
- Migrate database
```buildoutcfg
flask db upgrade
```
- Run command
```buildoutcfg
flask run
```
## Note
- Import/remove example data from\
`book-library/app/samples`
```buildoutcfg
# import
flask db-manage add-data

# remove
flask db-manage remove-data
```
- Import/remove books from Google API\
`https://www.googleapis.com/books/v1/volumes?q=Hobbit`
```buildoutcfg
# import
flask db-manage add-google-books
# remove
flask db-manage remove-data
```
## Tests
In order to execute tests located in `tests/` run the command
```buildoutcfg
python -m pytest --vv --cov --cov-report=html
```
