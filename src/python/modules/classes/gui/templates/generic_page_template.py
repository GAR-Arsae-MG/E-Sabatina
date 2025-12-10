#! python3

# Authors:  Túlio Ferreira Horta - (TFH, Duke).
# Last modification: DUKE-11_nov_25

from flet import *
import typing, enum

class WidgetTypes(enum.Enum):
    TEXT = Text
    TEXT_FIELD = TextField
    BUTTON = ElevatedButton
    CHECKBOX = Checkbox
    RADIO = Radio
    DROPDOWN = Dropdown
    SLIDER = Slider
    PROGRESS_BAR = ProgressBar
    IMAGE = Image
    ICON = Icon
    CONTAINER = Container
    ROW = Row
    COLUMN = Column
    STACK = Stack
    LIST_VIEW = ListView
    GRID_VIEW = GridView
    TABS = Tabs
    APP_BAR = AppBar
    NAVIGATION_BAR = NavigationBar
    DRAWER = NavigationDrawer
    SNACK_BAR = SnackBar
    ALERT_DIALOG = AlertDialog
    BOTTOM_SHEET = BottomSheet
    DATE_PICKER = DatePicker
    TIME_PICKER = TimePicker
    FILE_PICKER = FilePicker
    CIRCLE_AVATAR = CircleAvatar
    DIVIDER = Divider
    VERTICAL_DIVIDER = VerticalDivider
    EXPANSION_PANEL = ExpansionPanel
    DATA_TABLE = DataTable
    CHART = Chart
    WEB_VIEW = WebView
    GESTURE_DETECTOR = GestureDetector
    TOOLTIP = Tooltip
    DRAGGABLE = Draggable
    DRAG_TARGET = DragTarget
    CLIPRRECT = ClipRRect
    HERO = Hero
    INTERACTIVE_VIEWER = InteractiveViewer
    SHADER_MASK = ShaderMask
    BACKDROP_FILTER = BackdropFilter
    CUSTOM_PAINT = CustomPaint
    FLOW = Flow
    TABLE = Table
    FLEX = Flex
    WRAP = Wrap
    WIDGET = Control

class GenericPage(flet.Page):
    def __init__(self, title: str):
        super().__init__()
        self.page_title = title
        self.widget_cache: list[tuple[int, WidgetTypes]] = []
    def insert_widget(self, new_widget: WidgetTypes):
        self.widget_cache.append((len(self.widget_cache) + 1, new_widget()))
        self.add(new_widget)
        self.update()
    def remove_widget(self, widget_id: int):
        def filter_widget(id: int):
            for widget_container in self.widget_cache:
                for container in widget_container:
                    if(container[0] == id):
                        self.widget_cache.remove(widget_container)
        filter_widget(id)
        def update_page():
            self.clean()
            for widget_container in self.widget_cache:
                for container in widget_container:
                    page.add(container[1])
            self.update()
        update_page()
    def get_currently_loaded_widgets(self):
        return self.widget_cache
