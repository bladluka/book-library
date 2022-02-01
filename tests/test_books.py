def test_get_books_no_records(client):
    response = client.get("/api/v1/books")
    expected_result = {"data": [], "success": "true"}
    assert response.status_code == 200
    assert response.get_json() == expected_result


def test_get_books(client, sample_data):
    response = client.get("/api/v1/books")
    response_data = response.get_json()
    assert response.status_code == 200
    assert len(response_data["data"]) == 14


def test_get_books_with_params(client, sample_data):
    response = client.get(
        "/api/v1/books?title=game&language=pl"
        "&published_date[gte]=2015-01-01"
        "&published_date[lte]=2020-01-01"
    )
    response_data = response.get_json()
    assert response.status_code == 200
    assert len(response_data["data"]) == 1


def test_get_single_book(client, sample_data):
    response = client.get("/api/v1/books/1")
    response_data = response.get_json()
    assert response.status_code == 200
    assert response_data["success"] == "true"
    assert response_data["data"]["title"] == "Animal Farm"
    assert len(response_data["data"]) == 8


def test_add_book_with_existing_isbn_fail(client, sample_data):
    json_data = {
        "title": "Drakula",
        "isbn": 9780141036137,
        "number_of_pages": 112,
        "published_date": "2021-01-01",
        "language": "pl",
        "info_link": "link",
        "authors_book": ["Jan Kowalski"],
    }
    response = client.post("api/v1/books", json=json_data)
    status_code = response.status_code
    data = response.get_json()
    error_msg = data["message"]

    assert status_code == 409
    assert error_msg == "Book with ISBN 9780141036137 already exists"


def test_add_book_author_not_found_fail(client, sample_data):
    json_data = {
        "title": "Drakula",
        "isbn": 9780679417399,
        "number_of_pages": 112,
        "published_date": "2021-01-01",
        "language": "pl",
        "info_link": "link",
        "authors_book": ["Jan Kowalski"],
    }
    response = client.post("api/v1/books", json=json_data)
    status_code = response.status_code
    data = response.get_json()
    error_msg = data["message"]

    assert status_code == 404
    assert error_msg == "Author Jan Kowalski not found"


def test_add_book_pass(client, sample_data, book):
    response = client.post("/api/v1/books", json=book)
    response_data = response.get_json()
    expected_result = {
        "success": "true",
        "data": {
            "title": "Drakula",
            "isbn": 8780141036121,
            "number_of_pages": 112,
            "published_date": "2021-01-01",
            "language": "pl",
            "info_link": "link",
            "id": 15,
            "authors": ["Dan Brown"],
        },
    }
    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json"
    assert response_data == expected_result

    response = client.get("/api/v1/books/15")
    response_data = response.get_json()
    assert response.status_code == 200
    assert response_data["success"] == "true"
    assert response_data["data"]["title"] == "Drakula"
    assert len(response_data["data"]) == 8


def test_update_book_not_found(client, sample_data):
    json_data = {
        "title": "Animal Farm",
        "isbn": 9780141036137,
        "number_of_pages": 112,
        "published_date": "2021-01-01",
        "language": "pl",
        "info_link": "",
        "authors_book": ["George Orwell"],
    }
    response = client.put("api/v1/books/21", json=json_data)
    status_code = response.status_code
    data = response.get_json()
    error_msg = data["message"]

    assert status_code == 404
    assert error_msg == "Book with id 21 not found"


def test_update_book_author_not_found_fail(client, sample_data):
    json_data = {
        "title": "Animal Farm",
        "isbn": 9780141036137,
        "number_of_pages": 112,
        "published_date": "2021-01-01",
        "language": "pl",
        "info_link": "",
        "authors_book": ["Jan Kowalski"],
    }
    response = client.put("api/v1/books/1", json=json_data)
    status_code = response.status_code
    data = response.get_json()
    error_msg = data["message"]

    assert status_code == 404
    assert error_msg == "Author Jan Kowalski not found"


def test_update_book_with_existing_isbn_fail(client, sample_data):
    json_data = {
        "title": "Drakula",
        "isbn": 9780679417392,
        "number_of_pages": 112,
        "published_date": "2021-01-01",
        "language": "pl",
        "info_link": "link",
        "authors_book": ["Dan Brown"],
    }
    response = client.put("api/v1/books/1", json=json_data)
    status_code = response.status_code
    data = response.get_json()
    error_msg = data["message"]

    assert status_code == 409
    assert error_msg == "Book with ISBN 9780679417392 already exists"


def test_update_book_pass(client, sample_data):
    json_data = {
        "title": "Drakula",
        "isbn": 8780141036121,
        "number_of_pages": 112,
        "published_date": "2021-01-01",
        "language": "pl",
        "info_link": "link",
        "authors_book": ["Dan Brown"],
    }
    response_p = client.put("api/v1/books/1", json=json_data)
    status_code = response_p.status_code
    response_g = client.get("api/v1/books/1")
    data = response_g.get_json()
    book = data["data"]

    assert status_code == 200
    assert book["title"] == json_data["title"]
    assert book["isbn"] == json_data["isbn"]
    assert book["number_of_pages"] == json_data["number_of_pages"]
    assert book["published_date"] == json_data["published_date"]
    assert book["language"] == json_data["language"]
    assert book["info_link"] == json_data["info_link"]


def test_delete_book_not_found_fail(client, sample_data):
    response = client.delete("api/v1/books/21")
    status_code = response.status_code
    data = response.get_json()
    error_msg = data["message"]

    assert status_code == 404
    assert error_msg == "Book with id 21 not found"


def test_delete_book_pass(client, sample_data):
    response = client.delete("api/v1/books/1")
    status_code = response.status_code
    data = response.get_json()
    success_msg = data["data"]

    assert status_code == 200
    assert success_msg == "Book with id 1 has been deleted"
