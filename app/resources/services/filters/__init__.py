from resources.models.filters import Filters, FiltersQuery


class FilterService:
    def __init__(self) -> None:
        self.query = FiltersQuery()

    def getFilterById(self, id: str) -> Filters:
        return self.query.findOneById(id)
