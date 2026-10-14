
from sqlalchemy import select

from database import SessionLocal
from models import Engineer, Issue, Project, Team


def seed_database():
    with SessionLocal() as session:
        # 1. Create a team if it doesn't already exist.
        team = session.scalar(
            select(Team).where(
                Team.name == "Payments Engineering"
            )
        )

        if team is None:
            team = Team(
                name="Payments Engineering",
                description="Builds and maintains payment services.",
            )
            session.add(team)
            session.flush()

        # 2. Create engineers if they don't already exist.
        maya = session.scalar(
            select(Engineer).where(
                Engineer.email == "maya@example.com"
            )
        )

        if maya is None:
            maya = Engineer(
                name="Maya Sharma",
                email="maya@example.com",
                role="Backend Engineer",
                team=team,
            )
            session.add(maya)

        arjun = session.scalar(
            select(Engineer).where(
                Engineer.email == "arjun@example.com"
            )
        )

        if arjun is None:
            arjun = Engineer(
                name="Arjun Mehta",
                email="arjun@example.com",
                role="DevOps Engineer",
                team=team,
            )
            session.add(arjun)

        # Flush saves pending records within the current transaction.
        # This makes generated IDs available before creating related data.
        session.flush()

        # 3. Create a project if it doesn't already exist.
        project = session.scalar(
            select(Project).where(
                Project.name == "Payments API"
            )
        )

        if project is None:
            project = Project(
                name="Payments API",
                description="Processes customer payment requests.",
                status="active",
                team=team,
            )
            session.add(project)
            session.flush()

        # 4. Create a sample issue if it doesn't already exist.
        issue = session.scalar(
            select(Issue).where(
                Issue.id == 142
            )
        )

        if issue is None:
            issue = Issue(
                id=142,
                title="Payment requests are failing intermittently",
                description=(
                    "Payment requests fail intermittently. "
                    "The team is investigating a deployment "
                    "configuration issue."
                ),
                status="blocked",
                priority="high",
                project=project,
                assignee=maya,
            )
            session.add(issue)

        # Commit all changes together.
        session.commit()

        print("OpsLens seed data created successfully!")
        print(f"Team: {team.name}")
        print(f"Project: {project.name}")
        print(f"Issue: #{issue.id} — {issue.title}")


if __name__ == "__main__":
    seed_database()
