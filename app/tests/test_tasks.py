import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# Use an in-memory SQLite DB for tests - no Postgres needed
SQLITE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLITE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def test_create_task():
    response = client.post(
        "/api/v1/tasks", json={"title": "Write Terraform modules", "priority": "high"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Write Terraform modules"
    assert data["priority"] == "high"
    assert data["status"] == "pending"
    assert "id" in data


def test_list_tasks_empty():
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    data = response.json()
    assert data["tasks"] == []
    assert data["total"] == 0


def test_list_tasks_pagination():
    for i in range(5):
        client.post("/api/v1/tasks", json={"title": f"Task {i}"})
    response = client.get("/api/v1/tasks?page=1&page_size=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data["tasks"]) == 3
    assert data["total"] == 5


def test_get_task():
    created = client.post("/api/v1/tasks", json={"title": "Deploy to K8s"}).json()
    response = client.get(f"/api/v1/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Deploy to K8s"


def test_get_task_not_found():
    response = client.get("/api/v1/tasks/999")
    assert response.status_code == 404


def test_update_task():
    created = client.post("/api/v1/tasks", json={"title": "Setup CI"}).json()
    response = client.put(
        f"/api/v1/tasks/{created['id']}",
        json={"status": "completed"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    assert response.json()["title"] == "Setup CI"


def test_update_task_not_found():
    response = client.put("/api/v1/tasks/999", json={"status": "completed"})
    assert response.status_code == 404


def test_delete_task():
    created = client.post("/api/v1/tasks", json={"title": "Old task"}).json()
    response = client.delete(f"/api/v1/tasks/{created['id']}")
    assert response.status_code == 204
    # Confirm it's gone
    assert client.get(f"/api/v1/tasks/{created['id']}").status_code == 404


def test_create_task_invalid_title():
    response = client.post("/api/v1/tasks", json={"title": ""})
    assert response.status_code == 422
