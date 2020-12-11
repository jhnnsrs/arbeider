class BaseWidgetMeta(type):
    # Register the widget in the widget registry
    #TODO: Register Widgets here
    pass




class BaseWidget(metaclass=BaseWidgetMeta):
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