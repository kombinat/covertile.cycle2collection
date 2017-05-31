from collective.cover.tiles.configuration_widgets.cssclasswidget import CSSClassWidget  # noqa
from z3c.form.browser import widget
from z3c.form.interfaces import ISelectWidget
from z3c.form.widget import FieldWidget
from zope.interface import implementer_only


class IColumnCSSClassWidget(ISelectWidget):
    """ marker for column_css_class field """


@implementer_only(IColumnCSSClassWidget)
class ColumnCSSClassWidget(CSSClassWidget):

    def update(self):
        """See z3c.form.interfaces.IWidget."""
        super(ColumnCSSClassWidget, self).update()
        widget.addFieldClass(self)
        # ugly value translation
        if isinstance(self.context.get('column_css_class'), dict):
            self.value = self.context.get('column_css_class').values()[0]


def ColumnCSSClassFieldWidget(field, request):
    return FieldWidget(field, ColumnCSSClassWidget(request))
