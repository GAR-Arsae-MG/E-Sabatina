#! python3

# Authors:  Túlio Ferreira Horta - (TFH, Duke).
# Last modification: DUKE-11_nov_25

import flet, typing

class GenericWindow(flet.Window):
    def __init__(self, page: flet.Page, title: str, width: int, height: int, can_resize: bool = True):
        super().__init__(
            page=page,
            title=title,
            width=width,
            height=height,
            can_resize=can_resize,
            visible=False
        )
        # The first entry is the page on display -> array[0]
        self.page_cache: list[flet.Page] = []
    def update_window_view(self):
      self.page.clean()
      def create_updated_cache(cache: list[flet.Page]):
        aux = cache.copy()
        aux.reverse()
        aux.pop()
        aux.reverse()
        return aux.copy()
      self.page_cache = create_updated_cache(self.page_cache)
      self.page = self.page_cache[0]
      self.page.update()

    def insert_window_view(self, new_page: flet.Page):
      self.page_cache.append(new_page)

    def terminate_window(self):
      self.close()
