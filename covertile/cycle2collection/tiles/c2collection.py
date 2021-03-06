'''
Created on 16.6.2015

@author: peterm
'''
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.cover.interfaces import ITileEditForm
from collective.cover.tiles.collection import CollectionTile
from collective.cover.tiles.collection import ICollectionTile
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from plone.autoform import directives as form
from zope import schema
from zope.interface import implementer

try:
    from collective.contentleadimage.config import IMAGE_FIELD_NAME
except ImportError:
    IMAGE_FIELD_NAME = "image"


class ICycle2CollectionTile(ICollectionTile):
    """ the same fields as Carousel tile """

    form.omitted('columns')
    form.no_omit(ITileEditForm, 'columns')
    columns = schema.TextLine(
        title=u"No. Columns",
        description=u"How many items in one slide",
        required=False,
    )

    form.omitted('image_scale_dir')
    form.no_omit(ITileEditForm, 'image_scale_dir')
    image_scale_dir = schema.TextLine(
        title=u"Image scale crop direction",
        description=u"Can be 'thumbnail' (uncropped) or 'down' (cropped)",
        required=False,
        default=u'thumbnail',
    )

    form.omitted('timeout')
    form.no_omit(ITileEditForm, 'timeout')
    timeout = schema.TextLine(
        title=u"Timeout between slides",
        description=u"in milliseconds ... '0' means slider does not "
                    u"play automatically",
        required=False,
        default=u'0',
    )

    form.omitted('horz_centered')
    form.no_omit(ITileEditForm, 'horz_centered')
    horz_centered = schema.Bool(
        title=u"Horizontally centered",
        required=False,
    )

    form.omitted('fluid')
    form.no_omit(ITileEditForm, 'fluid')
    fluid = schema.Bool(
        title=u"Fluid support",
        required=False,
    )

    form.omitted('more_link')
    form.no_omit(IDefaultConfigureForm, 'more_link')
    more_link = schema.Text(
        title=u'More Link',
        required=False,
    )

    form.omitted('column_css_class')
    form.no_omit(IDefaultConfigureForm, 'column_css_class')
    form.widget(column_css_class='covertile.cycle2collection.tiles.widgets.ColumnCSSClassFieldWidget')  # noqa
    column_css_class = schema.Choice(
        title=u"Column CSS Class",
        required=False,
        vocabulary='collective.cover.TileStyles',
        default=u'tile-default',
    )


@implementer(ICycle2CollectionTile)
class Cycle2CollectionTile(CollectionTile):

    index = ViewPageTemplateFile('c2collection.pt')
    short_name = u'Cycle2 Collection'

    def thumbnail(self, item):
        """Return a thumbnail of an image if the item has an image field and
        the field is visible in the tile.

        :param item: [required]
        :type item: content object
        """
        if self._has_image_field(item) and self._field_is_visible('image'):
            tile_conf = self.get_tile_configuration()
            image_conf = tile_conf.get('image', None)
            if image_conf:
                scaleconf = image_conf['imgsize']
                # scale string is something like: 'mini 200:200'
                # we need the name only: 'mini'
                if scaleconf == '_original':
                    scale = None
                else:
                    scale = scaleconf.split(' ')[0]
                scales = item.restrictedTraverse('@@images')
                crop_dir = self.data.get('image_scale_dir', 'thumbnail')
                return scales.scale(
                    IMAGE_FIELD_NAME, scale, direction=crop_dir)

    @property
    def columns(self):
        try:
            return int(self.data.get('columns', 1))
        except:
            return 1

    @property
    def timeout(self):
        return self.data.get('timeout', '0')

    @property
    def column_css_class(self):
        tile_conf = self.get_tile_configuration()
        # ugly value translation
        return tile_conf.get('column_css_class', {}).values()[0][0]
