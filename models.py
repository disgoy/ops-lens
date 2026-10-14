
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    engineers: Mapped[list["Engineer"]] = relationship(
        back_populates="team"
    )
    projects: Mapped[list["Project"]] = relationship(
        back_populates="team"
    )


class Engineer(Base):
    __tablename__ = "engineers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True
    )
    role: Mapped[str] = mapped_column(String(100))

    team_id: Mapped[int | None] = mapped_column(
        ForeignKey("teams.id", ondelete="SET NULL"),
        nullable=True,
    )

    team: Mapped["Team | None"] = relationship(
        back_populates="engineers"
    )
    assigned_issues: Mapped[list["Issue"]] = relationship(
        back_populates="assignee"
    )


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="active")

    team_id: Mapped[int | None] = mapped_column(
        ForeignKey("teams.id", ondelete="SET NULL"),
        nullable=True,
    )

    team: Mapped["Team | None"] = relationship(
        back_populates="projects"
    )
    issues: Mapped[list["Issue"]] = relationship(
        back_populates="project"
    )


class Issue(Base):
    __tablename__ = "issues"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="open")
    priority: Mapped[str] = mapped_column(String(20), default="medium")

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE")
    )
    assignee_id: Mapped[int | None] = mapped_column(
        ForeignKey("engineers.id", ondelete="SET NULL"),
        nullable=True,
    )

    project: Mapped["Project"] = relationship(
        back_populates="issues"
    )
    assignee: Mapped["Engineer | None"] = relationship(
        back_populates="assigned_issues"
    )
