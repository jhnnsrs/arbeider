class Widget:
    base_template: None;


class SliderWidget(Widget):

    def __init__(self, lower, upper, step) -> None:
        self.lower = lower
        self.to = upper
        self.step = step
        super().__init__()    


class QueryWidget(Widget):

    def __init__(self, query):
        super().__init__()
    