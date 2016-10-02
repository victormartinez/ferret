from bs4 import Comment


def remove_comments(body):
    comments = body.find_all(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()
    return body
