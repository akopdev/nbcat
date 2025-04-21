from pydantic import BaseModel, model_validator


class Settings(BaseModel):
    """Validates cli arguments."""

    field: str | None = None
    list_field: list[str] = []
    bool_field: bool = False

    @model_validator(mode="before")
    def parse_list_field(values: dict):
        """You can pass multiple values as a comma separated string."""
        if isinstance(values.get("list_field"), str):
            values["list_field"] = values.get("list_field").split(",")
        return values
