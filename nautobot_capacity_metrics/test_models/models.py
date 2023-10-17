"""Models for the testing plugin."""

from django.db.models import CharField
from nautobot.core.models import BaseModel


class TestModel(BaseModel):
    """This is a model solely used for the testing of the capacity metrics plugin."""

    name = CharField(max_length=20)
