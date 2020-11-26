import sys
import warningsimport django.utils
import django.utils.encoding
import django.shortcutsclass Six:
    string_types = str,
    text_type = str
    next = nextdef _compact(cls):
    warnings.warn(f"Remove python_2_unicode_compatible() for {cls}")
    return clsdjango.utils.six = Six
django.utils.encoding.python_2_unicode_compatible = _compact
django.shortcuts.render_to_response = django.shortcuts.render
sys.modules['django.utils.six'] = Six