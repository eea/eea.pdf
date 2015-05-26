""" aysnc module - BBB
"""
def make_async_pdf(*args, **kwargs):
    """ BBB """
    import warnings
    warnings.warn("eea.pdf.async.make_async_pdf is deprecated. "
                  "Please use eea.converter.async.run_async_job instead",
                  DeprecationWarning)
