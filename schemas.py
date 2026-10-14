from pydantic import BaseModel, ConfigDict


class TeamRead(BaseModel):
    # Allow building this schema directly from SQLAlchemy objects.
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
