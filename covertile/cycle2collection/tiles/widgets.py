from z3c.form.widget import FieldWidget
from z3c.form.browser.textlines import TextLinesWidget
from z3c.form.interfaces import IFieldWidget, ITextLinesWidget
from zope.interface import implementer_only, implementer


class ITileTextLinesWidget(ITextLinesWidget):
    """ """


@implementer_only(ITileTextLinesWidget)
class TileTextLinesWidget(TextLinesWidget):
    """textlines widget implementation."""


@implementer(IFieldWidget)
def TileTextLinesFieldWidget(field, source, request=None):
    """IFieldWidget factory for SelectWidget."""
    # BBB: emulate our pre-2.0 signature (field, request)
    if request is None:
        real_request = source
    else:
        real_request = request
    return FieldWidget(field, TileTextLinesWidget(real_request))
