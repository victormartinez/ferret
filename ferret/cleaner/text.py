def remove_special_chars(body_str):
    result = body_str.replace('\n', '')
    result = result.replace('\t', '')
    return result.replace('\r', '')


def normalize_text(text):
    result = ' '.join([s for s in text.split(' ') if s != ''])
    result = result.replace('\n', '')
    result = result.replace('\t', '')
    result = result.replace('\r', '')
    return result.strip()
