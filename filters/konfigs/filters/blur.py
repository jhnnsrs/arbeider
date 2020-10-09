from elements.models import Representation
from konfig.widgets import QueryWidget, SliderWidget
from konfig.params import IntPort, ModelPort
from .base import BaseFilterOutputs, BaseFilterKonfig, BaseFilterInputs

class BlurFilterInputs(BaseFilterInputs):
    sigma = IntPort(allow_null=True, label="Sigma", help_text="Sigma describes a helpful way to ", default=5, max_value=12, min_value=1, widget=SliderWidget())
    channel = IntPort(label="The parseable Channel", description="The channel that you want to parse", widget= QueryWidget(query="""
    query {
  data: channelsof(rep: {{rep}}) {
    value: index
    label: name
  }
}""", dependencies = ["rep"]))
    planes = IntPort(label="The planes that matter", description="The channel that you want to parse", widget= QueryWidget(query="""
    query {
  data: channelsof(rep: {{channel}}) {
    value: index
    label: name
  }
}""", dependencies = ["channel","rep"]))

class BlurFilterKonfig(BaseFilterKonfig):
    """
    In [image processing](/wiki/Image_processing "Image processing"), a **Gaussian blur** (also known as **Gaussian smoothing**) is the result of blurring an image by a [Gaussian function](/wiki/Gaussian_function "Gaussian function") (named after mathematician and scientist [Carl Friedrich Gauss](/wiki/Carl_Friedrich_Gauss "Carl Friedrich Gauss")). It is a widely used effect in graphics software, typically to reduce [image noise](/wiki/Image_noise "Image noise") and reduce detail. The visual effect of this blurring technique is a smooth blur resembling that of viewing the [image](/wiki/Image "Image") through a translucent screen, distinctly different from the [bokeh](/wiki/Bokeh "Bokeh") effect produced by an out-of-focus lens or the shadow of an object under usual illumination. Gaussian smoothing is also used as a pre-processing stage in [computer vision](/wiki/Computer_vision "Computer vision") algorithms in order to enhance image structures at different scales—see [scale space representation](/wiki/Scale_space_representation "Scale space representation") and [scale space implementation](/wiki/Scale_space_implementation "Scale space implementation").
    """
    name = "Gaussian Blur"
    variety = "filter"
    interface = "gaussian-blur"
    inputs = BlurFilterInputs
    outputs = BaseFilterOutputs