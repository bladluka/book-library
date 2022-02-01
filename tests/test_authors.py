def test_get_authors_no_records(client):
    response = client.get("/api/v1/authors")
    expected_result = {"data": [], "success": "true"}
    assert response.status_code == 200
    assert response.get_json() == expected_result


def test_get_authors(client, sample_data):
    response = client.get("/api/v1/authors")
    response_data = response.get_json()
    assert response.status_code == 200
    assert len(response_data["data"]) == 10


def test_get_single_author(client, sample_data):
    response = client.get("/api/v1/authors/1")
    response_data = response.get_json()
    assert response.status_code == 200
    assert response_data["success"] == "true"
    assert response_data["data"]["first_and_last_name"] == "George Orwell"
    assert len(response_data["data"]) == 2


def test_add_author(client):
    response = client.post(
        "/api/v1/authors", json={"first_and_last_name": "Piotr Nowak"}
    )
    response_data = response.get_json()
    expected_result = {
        "success": "true",
        "data": {
            "first_and_last_name": "Piotr Nowak",
            "id": 1,
        },
    }
    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json"
    assert response_data == expected_result

    response = client.get("/api/v1/authors/1")
    response_data = response.get_json()
    assert response.status_code == 200
    assert response_data["success"] == "true"
    assert response_data["data"]["first_and_last_name"] == "Piotr Nowak"
    assert len(response_data["data"]) == 2


def test_update_author_not_found(client, sample_data):
    json_data = {
        "first_and_last_name": "Piotr Nowak",
    }
    response = client.put("api/v1/authors/21", json=json_data)
    status_code = response.status_code
    data = response.get_json()
    error_msg = data["message"]

    assert status_code == 404
    assert error_msg == "Author with id 21 not found"


def test_update_author_pass(client, sample_data):
    json_data = {
        "first_and_last_name": "Adam Sztaba",
    }
    response_p = client.put("api/v1/authors/1", json=json_data)
    status_code = response_p.status_code
    response_g = client.get("api/v1/authors/1")
    data = response_g.get_json()
    author = data["data"]

    assert status_code == 200
    assert author["first_and_last_name"] == json_data["first_and_last_name"]


def test_delete_author_pass(client, sample_data):
    response = client.delete("api/v1/authors/1")
    status_code = response.status_code
    data = response.get_json()
    success_msg = data["data"]

    assert status_code == 200
    assert success_msg == "Author with id 1 has been deleted"
