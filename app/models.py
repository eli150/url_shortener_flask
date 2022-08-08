from . import db
from dataclasses import dataclass


@dataclass
class Url(db.Model):
    id: int
    full_url: str
    short_url: str

    id = db.Column(db.Integer, primary_key=True)
    full_url = db.Column(db.String(2048), nullable=False)
    short_url = db.Column(db.String(20), nullable=False)

    def __init__(self, full_url, short_url) -> None:
        self.full_url = full_url
        self.short_url = short_url
