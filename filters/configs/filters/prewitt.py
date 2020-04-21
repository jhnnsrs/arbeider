from delt.params import IntField, CharField
from .base import BaseFilterOutputs, BaseFilterConfig, BaseFilterInputs


class PrewittFilterInputs(BaseFilterInputs):
    sigma = IntField(allow_null=True, help_text="The Upper Index / The Upper Limit for the Slice", default=5)
    title = CharField(allow_null=True, help_text=" The title for thisSlice", default=5)

class PrewittFilterConfig(BaseFilterConfig):
    """
    The **Prewitt operator** is used in [image processing](/wiki/Image_processing "Image processing"), particularly within [edge detection](/wiki/Edge_detection "Edge detection") algorithms. Technically, it is a [discrete differentiation operator](/wiki/Difference_operator "Difference operator"), computing an approximation of the [gradient](/wiki/Image_gradient "Image gradient") of the image intensity function. At each point in the image, the result of the Prewitt operator is either the corresponding gradient vector or the norm of this vector. The Prewitt operator is based on convolving the image with a small, separable, and integer valued filter in horizontal and vertical directions and is therefore relatively inexpensive in terms of computations like [Sobel](/wiki/Sobel_operator "Sobel operator") and Kayyali<sup id="cite_ref-1" class="reference">[[1]](#cite_note-1)</sup> operators. On the other hand, the gradient approximation which it produces is relatively crude, in particular for high frequency variations in the image. The Prewitt operator was developed by Judith M. S. Prewitt<sup id="cite_ref-2" class="reference">[[2]](#cite_note-2)</sup>. """
    name = "Prewitt"
    interface = "prewitt"
    inputs = PrewittFilterInputs
    outputs = BaseFilterOutputs