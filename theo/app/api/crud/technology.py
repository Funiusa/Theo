from .base import CRUDBase
from app.api.models.technology import Technology
from app.api.schemas.technology import TechnologyCreate, TechnologyUpdate


class CRUDPost(CRUDBase[Technology, TechnologyCreate, TechnologyUpdate]):
    pass


technology = CRUDPost(Technology)
