""" Caching
"""
def cacheKey(method, self, *args, **kwargs):
    """ Generate unique cache id
    """
    name = getattr(self, '__name__', '')
    return ':'.join((self.context.absolute_url(1), name))
