from pydantic import BaseModel


class MetaData(BaseModel):
    current_page: int
    page_size: int
    total_items: int
    total_pages: int

    @classmethod
    def create(
        cls, current_page: int, total_items: int, page_size: int = 30
    ) -> "MetaData":
        total_pages = max((total_items + page_size - 1) // page_size, 1)
        return cls(
            current_page=current_page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages,
        )

    @property
    def offset(self) -> int:
        return (self.current_page - 1) * self.page_size
