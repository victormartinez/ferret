def remove_special_chars(body_str):
    if body_str is None:
        return ''

    result = body_str.replace('\n', '')
    result = result.replace('\\n', '')
    result = result.replace('\t', '')
    result = result.replace('\\t', '')
    result = result.replace('\r', '')
    result = result.replace('\\r', '')
    return result


def normalize_text(text):
    if text is None:
        return ''
    result = ' '.join([s for s in text.split(' ') if s != ''])
    result = result.replace('\n', '')
    result = result.replace('\t', '')
    result = result.replace('\r', '')
    return result.strip()
