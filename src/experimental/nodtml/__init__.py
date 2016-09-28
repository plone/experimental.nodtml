# -*- coding: utf-8 -*-
from DocumentTemplate.DT_HTML import HTML
from DocumentTemplate.DT_String import String

import logging
import os


logger = logging.getLogger('experimental.nodtml')
TRUE_VALUES = ('true', 't', '1', 'yes', 'y')

# Show original dtml text in the logs?  Default: false.
SHOW = os.environ.get('SHOW_ORIGINAL_DTML', 'false')
if SHOW and SHOW.lower() in TRUE_VALUES:
    SHOW = True
else:
    SHOW = False

# Value to use instead of the original dtml text.
# Note: this must be a string, not unicode.
# Otherwise you may get exceptions in Products.ResourceRegistries,
# at least if you have css in dtml files, for example
# plonetheme/sunburst/skins/sunburst_styles/ploneCustom.css.dtml
# even though everything there is commented out.
VALUE = os.environ.get('DEBUG_DTML_VALUE', '')

# Should we only warn, instead of returning a fixd value?  Default: false.
ONLY_WARN = os.environ.get('EXPERIMENTAL_NODTML_ONLY_WARN', 'false')
if ONLY_WARN and ONLY_WARN.lower() in TRUE_VALUES:
    ONLY_WARN = True
    logger.info('Will only warn about DTML usage, not replace the value.')
    if VALUE:
        logger.warn('Ignored DEBUG_DTML_VALUE '
                    'in favor of EXPERIMENTAL_NODTML_ONLY_WARN.')
        VALUE = ''
    if SHOW:
        logger.warn('Ignored SHOW_ORIGINAL_DTML '
                    'in favor of EXPERIMENTAL_NODTML_ONLY_WARN.')
        SHOW = False
else:
    ONLY_WARN = False
    if VALUE:
        logger.info('Patched DTML to show: %r.', VALUE)
    else:
        logger.info('Patched DTML to not show anything.')


def quotedHTML(self, *args, **kwargs):
    if SHOW or ONLY_WARN:
        logger.info(
            'Hacked quotedHTML for args %r and kwargs %r.', args, kwargs)
        original = self._orig_quotedHTML(*args, **kwargs)
        if SHOW:
            logger.info(original)
        if ONLY_WARN:
            return original
    return VALUE

HTML._orig_quotedHTML = HTML.quotedHTML
HTML._orig__str__ = HTML.quotedHTML
HTML.quotedHTML = quotedHTML


def __call__(self, *args, **kwargs):
    if SHOW or ONLY_WARN:
        logger.info(
            'Hacked string call for args %r and kwargs %r.', args, kwargs)
        original = self._orig__call__(*args, **kwargs)
        if SHOW:
            logger.info(original)
        if ONLY_WARN:
            return original
    return VALUE

String._orig__call__ = String.__call__
String.__call__ = __call__


def __str__(self, *args, **kwargs):
    if SHOW or ONLY_WARN:
        logger.info(
            'Hacked string str for args %r and kwargs %r.', args, kwargs)
        original = self._orig__str__(*args, **kwargs)
        if SHOW:
            logger.info(original)
        if ONLY_WARN:
            return original
    return VALUE

String._orig__str__ = String.__str__
String.__str__ = __str__
