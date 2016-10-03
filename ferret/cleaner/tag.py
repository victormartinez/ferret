import re

from ferret.util.tag import get_ids_and_classes

TAGS_TO_REMOVE = ['script', 'style', 'iframe', 'meta', 'link', 'form', 'noscript', 'object', 'source',
                  'svg', 'use', 'code', 'pre', 'input', 'textarea', 'option', 'select', 'fieldset', 'aside', 'menuitem',
                  'nav', 'footer', 'hr']

TAGS_TO_UNWRAP = ['font']

UNWANTED_ATTRS_REGEX = "sidebar|widget|social|facebook|comment|tweet|menu|footer|subscribe|foot|nav|google|share|search" \
                       "|form|contact|breadcrumb|banner|advertisement|lang|btn|tab|sitemap|instagram|flickr|print" \
                       "|button|pinterest|radio|bread|icon|dusqus|sponsor|popup|modal|pagination|promo" \
                       "|related|scroll|tool|login|sign|next|prev|old|new|shop|continue|fb-|messenger"


def remove_id_and_class(tag):
    for attr in ["class", "id", "name", "style", "align"]:
        if attr in tag.attrs.keys():
            del tag.attrs[attr]


def should_remove_tag(tag):
    should = False
    attrs = get_ids_and_classes(tag)
    for attr in attrs:
        if re.search(UNWANTED_ATTRS_REGEX, attr):
            should = True

    if re.search(UNWANTED_ATTRS_REGEX, tag.name):
        should = True

    return should


def remove_unwanted_tags(body):
    for elem in body.select(','.join(TAGS_TO_REMOVE)):
        elem.extract()
    return body


def unwrap_tags(body):
    for elem in body.select(','.join(TAGS_TO_UNWRAP)):
        elem.unwrap()
    return body


def contains_text(tag):
    return len(tag.text.strip()) != 0


def has_only_one_anchor(tag):
    return len(list(tag.children)) == 1 and tag.next.name == 'a'
