class Widget():
    base_template: None;
    description: None

    def __init__(self, **kwargs) -> None:
        assert(self.description is not None), "Please Provide a description for the Widget"
        self.dependencies = kwargs.get("dependencies", [])

    def serialize(self, field): 
        return { "type": self.type, "dependencies": self.dependencies, **self.params(field)}

    def types(self,):
        return { "type": str, **self.paramTypes()}

    def params(self, field):
        return {}

    def paramTypes(self):
        return {}

class ModelWidget(Widget):
    type="select"
    description = "The Slider widget is an Easy way to have a cool name"

class FloatWidget(Widget):
    type="float"
    description = "The Slider widget is an Easy way to have a cool name"

class ListWidget(Widget):
    type="float"
    description = "The Slider widget is an Easy way to have a cool name"

class FileWidget(Widget):
    type="file"
    description = "The Slider widget is an Easy way to have a cool name"

class MultiSelectWidget(Widget):
    type="multiselect"
    description = "The Slider widget is an Easy way to have a cool name"

class UUIDWidget(Widget):
    type="uuid"
    description = "The Slider widget is an Easy way to have a cool name"

class IntWidget(Widget):
    type="int"
    description = "The Slider widget is an Easy way to have a cool name"

class CharWidget(Widget):
    type="char"
    description = "The Slider widget is an Easy way to have a cool name"

class SwitchWidget(Widget):
    type="switch"
    description = "The Slider widget is an Easy way to have a cool name"


class ObjectWidget(Widget):
    type="object"
    description = "The Slider widget is an Easy way to have a cool name"


class SliderWidget(Widget):
    type= "slider"
    description = "The Slider widget is an Easy way to have a cool name"

    def __init__(self, lower=None, upper=None, step=None, **kwargs) -> None:
        self.lower = lower
        self.upper = upper
        self.step = step
        super().__init__(**kwargs)

    def params(self, field):
        return {
            "lower": self.lower or field.min_value ,
            "upper": self.upper or field.max_value,
            "step": self.step
        }  

    def paramTypes(self):
        return {
            "lower": int,
            "upper": int,
            "step": int
        }



class QueryMixin(Widget):
    

    def __init__(self, query=None, **kwargs):
        self.query = query
        super().__init__(**kwargs)

    def params(self, field):
        return { "query": self.query, **super().params(field)}


    def paramTypes(self):
        return {
            "query": str,
            **super().paramTypes()
        }


class QueryWidget(QueryMixin, Widget):
    type= "query"
    description = "The Slider widget is an Easy way to have a cool name"


class SliderQueryWidget(QueryMixin, Widget):
    type= "sliderquery"
    description = "The Slider widget is an Easy way to have a cool name"

    