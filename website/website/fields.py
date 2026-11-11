import re

from django_ckeditor_5.fields import CKEditor5Field

# CKEditor 5 adds a random data-list-item-id="..." to every <li> in the HTML it produces (new ids
# on every page load) and writes italics as <i>. Neither matters for display, but they would
# churn the stored data every time a record is re-saved, and existing content uses <em>.
_LIST_ITEM_ID = re.compile(r'\sdata-list-item-id="[^"]*"')
_ITALIC_TAG = re.compile(r"<(/?)i(?=[\s>])")


def clean_editor_html(value):
    value = _LIST_ITEM_ID.sub("", value)
    return _ITALIC_TAG.sub(r"<\1em", value)


class RichTextField(CKEditor5Field):
    """CKEditor 5 field that stores tidy HTML (a plain TextField column in the database)."""

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return clean_editor_html(value) if isinstance(value, str) else value
