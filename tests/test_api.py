from models import Engineer, Issue, Project, Team


def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to OpsLens!",
        "status": "running",
    }


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_teams_empty(client):
    response = client.get("/teams")

    assert response.status_code == 200
    assert response.json() == []


def test_teams_returns_seeded_rows(client, db_session):
    # Insert out of order to prove the endpoint sorts by id.
    db_session.add_all(
        [
            Team(id=2, name="Platform", description=None),
            Team(id=1, name="Payments", description="Handles payments."),
        ]
    )
    db_session.commit()

    response = client.get("/teams")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Payments", "description": "Handles payments."},
        {"id": 2, "name": "Platform", "description": None},
    ]


def test_projects_empty(client):
    response = client.get("/projects")

    assert response.status_code == 200
    assert response.json() == []


def test_projects_returns_seeded_rows(client, db_session):
    team = Team(id=1, name="Payments")
    db_session.add(team)
    db_session.add_all(
        [
            Project(
                id=1,
                name="Payments API",
                description="Processes payments.",
                status="active",
                team=team,
            ),
            # A project with no team: team_id must come back as null.
            Project(id=2, name="Orphan Project", status="paused"),
        ]
    )
    db_session.commit()

    response = client.get("/projects")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "Payments API",
            "description": "Processes payments.",
            "status": "active",
            "team_id": 1,
        },
        {
            "id": 2,
            "name": "Orphan Project",
            "description": None,
            "status": "paused",
            "team_id": None,
        },
    ]


def test_issues_empty(client):
    response = client.get("/issues")

    assert response.status_code == 200
    assert response.json() == []


def test_issues_returns_seeded_rows(client, db_session):
    team = Team(id=1, name="Payments")
    project = Project(id=1, name="Payments API", team=team)
    engineer = Engineer(
        id=1,
        name="Maya Sharma",
        email="maya@example.com",
        role="Backend Engineer",
        team=team,
    )
    db_session.add_all(
        [
            team,
            project,
            engineer,
            Issue(
                id=142,
                title="Payment requests are failing intermittently",
                description="Fails intermittently.",
                status="blocked",
                priority="high",
                project=project,
                assignee=engineer,
            ),
            # An unassigned issue: assignee_id must come back as null.
            Issue(
                id=7,
                title="Add retry logging",
                status="open",
                priority="low",
                project=project,
            ),
        ]
    )
    db_session.commit()

    response = client.get("/issues")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 7,
            "title": "Add retry logging",
            "description": None,
            "status": "open",
            "priority": "low",
            "project_id": 1,
            "assignee_id": None,
        },
        {
            "id": 142,
            "title": "Payment requests are failing intermittently",
            "description": "Fails intermittently.",
            "status": "blocked",
            "priority": "high",
            "project_id": 1,
            "assignee_id": 1,
        },
    ]


def test_get_issue_found(client, db_session):
    team = Team(id=1, name="Payments")
    project = Project(id=1, name="Payments API", team=team)
    engineer = Engineer(
        id=1,
        name="Maya Sharma",
        email="maya@example.com",
        role="Backend Engineer",
        team=team,
    )
    db_session.add_all(
        [
            team,
            project,
            engineer,
            Issue(
                id=142,
                title="Payment requests are failing intermittently",
                description="Fails intermittently.",
                status="blocked",
                priority="high",
                project=project,
                assignee=engineer,
            ),
        ]
    )
    db_session.commit()

    response = client.get("/issues/142")

    assert response.status_code == 200
    assert response.json() == {
        "id": 142,
        "title": "Payment requests are failing intermittently",
        "description": "Fails intermittently.",
        "status": "blocked",
        "priority": "high",
        "project_id": 1,
        "assignee_id": 1,
    }


def test_get_issue_not_found(client):
    response = client.get("/issues/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Issue 999 not found"}
