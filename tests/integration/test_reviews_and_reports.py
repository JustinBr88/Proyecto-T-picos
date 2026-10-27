import pytest

from tests.support import CUSTOMER, LOCATION

pytestmark = pytest.mark.integration


def test_add_and_list_reviews(client):
    response = client.post("/api/review", json={
        "username": CUSTOMER["username"], "location": LOCATION, "comment": "Muy bien", "rating": "good"})
    assert response.status_code == 200

    reviews = client.get("/api/review", query_string={"location": LOCATION}).get_json()
    assert [(r["comment"], r["rating"]) for r in reviews] == [("Muy bien", "good")]


@pytest.mark.parametrize("path", ["/api/reports/reservation", "/api/reports/popularRoom", "/api/reports/revenue"])
def test_reports_respond(client, path):
    response = client.get(path)
    assert response.status_code == 200
    assert isinstance(response.get_json(), dict)


def test_seed_command_loads_data(app, db):
    result = app.test_cli_runner().invoke(args=["seed-db", "--months", "3"])
    assert result.exit_code == 0, result.output
    assert "Reservation:" in result.output
