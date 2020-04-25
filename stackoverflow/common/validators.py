from django import forms


def max_three_tags(tags):
    if len(tags.split(",")) > 3:
        raise (forms.ValidationError("Maximum three tags requared"))


def like_dislike_validator(value):
    if value not in (-1, 1):
        raise (forms.ValidationError("-1 or 1 value expected"))

