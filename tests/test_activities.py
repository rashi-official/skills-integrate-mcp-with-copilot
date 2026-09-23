import sys
from pathlib import Path

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.app import app, activities


client = TestClient(app)


def test_signup_rejects_full_activity(monkeypatch):
    monkeypatch.setitem(
        activities,
        "Test Club",
        {
            "description": "A test club",
            "schedule": "Mondays, 3:00 PM",
            "max_participants": 1,
            "participants": ["existing@mergington.edu"],
        },
    )

    response = client.post("/activities/Test Club/signup?email=new@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
    assert activities["Test Club"]["participants"] == ["existing@mergington.edu"]


def test_signup_allows_space_when_not_full(monkeypatch):
    monkeypatch.setitem(
        activities,
        "Another Test Club",
        {
            "description": "Another test club",
            "schedule": "Tuesdays, 3:30 PM",
            "max_participants": 2,
            "participants": ["existing@mergington.edu"],
        },
    )

    response = client.post("/activities/Another Test Club/signup?email=new@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up new@mergington.edu for Another Test Club"
    assert "new@mergington.edu" in activities["Another Test Club"]["participants"]
