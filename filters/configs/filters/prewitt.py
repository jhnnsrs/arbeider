from delt.params import IntField, CharField
from .base import BaseFilterOutputs, BaseFilterKonfig, BaseFilterInputs


class PrewittFilterInputs(BaseFilterInputs):
    sigma = IntField(allow_null=True, help_text="The Upper Index / The Upper Limit for the Slice", default=5)
    title = CharField(allow_null=True, help_text=" The title for thisSlice", default=5)

class PrewittFilterKonfig(BaseFilterKonfig):
    """## Prewitt operator
Der Prewitt-Operator ist ein Kantendetektions-Filter ähnlich dem Sobel-Operator und ist nach Judith M.S. Prewitt benannt. Es wird allerdings auf die Gewichtung der aktuellen Bildzeile bzw. -spalte verzichtet. Analog zum Sobel-Operator berechnet der Kantendetektors zwei Gradientenbilder.

---

### Image
![Prewitt](https://upload.wikimedia.org/wikipedia/commons/3/3e/Bikesgray_prewitt.JPG)"""
    name = "Prewitt"
    interface = "prewitt"
    inputs = PrewittFilterInputs
    outputs = BaseFilterOutputs