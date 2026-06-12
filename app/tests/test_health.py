from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_liveness():
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "cloudops-task-api"
    assert "version" in data


def test_health_check_db_unhealthy():
    """Health endpoint degrades gracefully when DB is unreachable."""
    with patch("app.routes.health.get_db") as mock_get_db:
        mock_db = MagicMock()
        mock_db.execute.side_effect = Exception("DB unreachable")
        mock_get_db.return_value = iter([mock_db])
        response = client.get("/health")
        # Should not 500 - it degrades gracefully
        assert response.status_code == 200
