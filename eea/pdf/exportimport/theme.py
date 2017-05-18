""" XML Adapter
"""
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from Products.GenericSetup.utils import XMLAdapterBase
from eea.pdf.interfaces import IPDFTheme
from eea.pdf.content.theme import EditSchema


class PDFThemeXMLAdapter(XMLAdapterBase):
    """ Generic setup import/export xml adapter
    """
    __used_for__ = IPDFTheme

    def _exportNode(self):
        """Export the object as a DOM node.
        """
        node = self._getObjectNode('object')
        fields = ['title']
        fields.extend(field.getName() for field in EditSchema.fields())
        for prop in fields:
            child = self._doc.createElement('property')
            child.setAttribute('name', prop)
            field = self.context.getField(prop)
            if field.type == 'image':
                continue
            value = field.getAccessor(self.context)()
            if isinstance(value, (tuple, list)):
                for item in value:
                    if not item:
                        continue
                    element = self._doc.createElement('element')
                    element.setAttribute('value', item)
                    child.appendChild(element)
            else:
                if isinstance(value, (bool, int)):
                    value = repr(value)
                value = self._doc.createTextNode(str(value))
                child.appendChild(value)
            node.appendChild(child)

        for child in self.context.objectValues():
            element = self._doc.createElement('object')
            element.setAttribute('name', child.getId())
            element.setAttribute('meta_type', child.meta_type)
            node.appendChild(element)

        return node

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        for child in node.childNodes:
            # Properties
            if child.nodeName == 'property':
                name = child.getAttribute('name')
                purge = child.getAttribute('purge')
                purge = self._convertToBoolean(purge)

                elements = []
                field = self.context.getField(name)
                for element in child.childNodes:
                    if element.nodeName != 'element':
                        continue
                    elements.append(element.getAttribute('value'))
                if elements:
                    if not purge:
                        value = elements
                        oldValue = field.getAccessor(self.context)()
                        value.extend(x for x in oldValue if x not in value)
                    else:
                        value = []

                else:
                    value = self._getNodeText(child)
                    value = value.decode('utf-8')
                    value = value if not purge else u''

                field.getMutator(self.context)(value)
                notify(ObjectModifiedEvent(self.context))

        self.context.reindexObject()

    node = property(_exportNode, _importNode)
