# -*- coding: utf-8 -*-
from DocumentTemplate.DT_HTML import HTML
from DocumentTemplate.DT_String import String

import logging
import os


logger = logging.getLogger('experimental.nodtml')
# Show original dtml text in the logs?
SHOW = os.environ.get('SHOW_ORIGINAL_DTML')
# Value to use instead of the original dtml text.
# Note: this must be a string, not unicode.
# Otherwise you may get exceptions in Products.ResourceRegistries,
# at least if you have css in dtml files, for example
# plonetheme/sunburst/skins/sunburst_styles/ploneCustom.css.dtml
# even though everything there is commented out.
VALUE = os.environ.get('DEBUG_DTML_VALUE', '')


def quotedHTML(self, *args, **kwargs):
    if SHOW:
        logger.info('hacked quotedHTML')
        logger.info(self._orig_quotedHTML(*args, **kwargs))
    return VALUE

HTML._orig_quotedHTML = HTML.quotedHTML
HTML._orig__str__ = HTML.quotedHTML
HTML.quotedHTML = quotedHTML


def __call__(self, *args, **kwargs):
    if SHOW:
        logger.info('hacked string call')
        logger.info(self._orig__call__(*args, **kwargs))
    return VALUE

String._orig__call__ = String.__call__
String.__call__ = __call__


def __str__(self, *args, **kwargs):
    if SHOW:
        logger.info('hacked string str')
        logger.info(self._orig__str__(*args, **kwargs))
    return VALUE

String._orig__str__ = String.__str__
String.__str__ = __str__

if VALUE:
    logger.info('Patched DTML to show: %r.', VALUE)
else:
    logger.info('Patched DTML to not show anything.')
