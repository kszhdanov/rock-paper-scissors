from enum import Enum
from typing import Optional, List
from typing_extensions import Self


class MenuAffect(str, Enum):
    select = 'select'
    previous = 'previous'
    next = 'next'


class Menu:
    def __init__(
            self,
            title: str,
            tip: str,
            parent_menu: Optional[Self] = None,
            menu_items: Optional[List[Self]] = None,
            key_to_select: Optional[str] = None
    ):
        self.title: str = title
        self.tip: str = tip
        self.parent_menu: Self = parent_menu
        if menu_items is None:
            self.menu_items: List[Self] = []
        else:
            self.menu_items: List[Self] = menu_items
        if key_to_select:
            self.key_to_select = key_to_select
        else:
            self.key_to_select = title

    def add_menu_item(self, menu_item: Self):
        self.menu_items.append(menu_item)
