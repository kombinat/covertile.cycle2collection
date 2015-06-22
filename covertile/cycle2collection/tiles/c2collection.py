'''
Created on 16.6.2015

@author: peterm
'''
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.cover.interfaces import ITileEditForm
from collective.cover.tiles.collection import ICollectionTile, CollectionTile
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from plone.autoform import directives as form
from zope import schema
from zope.interface.declarations import implements


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
        description=u"in milliseconds ... '0' means slider does not " \
                    u"play automatically",
        required=False,
        default=u'0',
    )

    form.omitted('more_link')
    form.no_omit(IDefaultConfigureForm, 'more_link')
    form.order_after(more_link='image')
    more_link = schema.Text(
        title=u'More Link',
        required=False,
    )

    # form.widget(
    #    columns=TileTextLinesFieldWidget,
    #    image_scale_dir=TileTextLinesFieldWidget,
    #    timeout=TileTextLinesFieldWidget,
    # )


class Cycle2CollectionTile(CollectionTile):
    implements(ICycle2CollectionTile)
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
                return scales.scale('image', scale, direction=crop_dir)

    @property
    def columns(self):
        try:
            return int(self.data.get('columns', 1))
        except:
            return 1

    @property
    def timeout(self):
        return self.data.get('timeout', '0')
