import pytest
from app import create_app, db
from app.commands.db_manage_commands import add_data


@pytest.fixture()
def app():
    app = create_app("testing")

    with app.app_context():
        db.create_all()

    yield app

    app.config["DB_FILE_PATH"].unlink(missing_ok=True)


@pytest.fixture()
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture()
def sample_data(app):
    runner = app.test_cli_runner()
    runner.invoke(add_data)


@pytest.fixture()
def book():
    return {
        "title": "Drakula",
        "isbn": 8780141036121,
        "number_of_pages": 112,
        "published_date": "2021-01-01",
        "language": "pl",
        "info_link": "link",
        "authors_book": ["Dan Brown"],
    }
