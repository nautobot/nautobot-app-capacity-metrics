"""Models for the testing app."""

from django.db.models import CharField
from nautobot.core.models import BaseModel


class TestModel(BaseModel):
    """This is a model solely used for the testing of the capacity metrics app."""

    name = CharField(max_length=20)
