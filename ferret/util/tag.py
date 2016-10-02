def get_ids_and_classes(tag):
    attrs = tag.attrs
    if 'id' in attrs:
        ids = attrs['id']
        if isinstance(ids, list):
            for subitem in ids:
                yield subitem
        else:
            yield ids

    if 'class' in attrs:
        classes = attrs['class']
        if isinstance(classes, list):
            for subitem in classes:
                yield subitem
        else:
            yield classes
