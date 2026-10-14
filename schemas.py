from pydantic import BaseModel, ConfigDict


class TeamRead(BaseModel):
    # Allow building this schema directly from SQLAlchemy objects.
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    status: str
    team_id: int | None = None


class IssueRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None = None
    status: str
    priority: str
    project_id: int
    assignee_id: int | None = None
