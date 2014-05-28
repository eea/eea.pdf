""" Main product initializer
"""
def initialize(context):
    """Initializer called when used as a Zope 2 product.
    """
    from eea.pdf import content
    content.initialize(context)
