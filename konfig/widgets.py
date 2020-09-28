class Widget():
    base_template: None;

    def __init__(self, **kwargs) -> None:
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

class FloatWidget(Widget):
    type="float"

class ListWidget(Widget):
    type="float"

class FileWidget(Widget):
    type="file"

class MultiSelectWidget(Widget):
    type="multiselect"

class UUIDWidget(Widget):
    type="uuid"

class IntWidget(Widget):
    type="int"

class CharWidget(Widget):
    type="char"

class SwitchWidget(Widget):
    type="switch"


class ObjectWidget(Widget):
    type="object"



class SliderWidget(Widget):
    type= "slider"

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


class QueryWidget(Widget):
    type= "query"
    
    def __init__(self, query=None, **kwargs):
        self.query = query
        super().__init__(**kwargs)

    def params(self, field):
        return { "query": self.query}


    def paramTypes(self):
        return {
            "query": str
        }

    