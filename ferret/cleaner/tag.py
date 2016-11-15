def remove_unnecessary_attributes(tag):
    keys = list(tag.attrs.keys())
    for attr in keys:
        if attr not in ['src', 'href']:
            del tag.attrs[attr]


def has_only_one_anchor(tag):
    return len(list(tag.children)) == 1 and tag.next.name == 'a'
