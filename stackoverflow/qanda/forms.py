from django import forms


from . import models


def max_three_tags(tags):
    if len(tags.split(',')) > 3:
        raise(forms.ValidationError('Maximum three tags requared'))


def like_dislike_validator(value):
    if value not in (-1, 1):
        raise(forms.ValidationError('-1 or 1 value expected'))


class TagsField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(max_three_tags)

    def clean(self, value):
        value = super().clean(value.lower())

        return [tag.strip() for tag in value.split(',')]


class AskQuestionForm(forms.ModelForm):
    tags = TagsField(max_length=128)

    class Meta:
        model = models.Question
        fields = [
            "title",
            "text",
        ]

    def save(self, commit=True, *args, **kwargs):
        instance = super().save(commit=False, *args, **kwargs)
        tags = self.cleaned_data.get('tags')
        print(tags)
        if commit:
            tags_qs = models.Tag.objects.queryset_from_list(tags)

            if not instance.id:
                instance.save()
            instance.tags.clear()
            instance.tags.add(*tags_qs)
            instance.save()
        return instance


class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = [
            'text',
            'to_question',
        ]
        widgets = {
            'to_question': forms.HiddenInput(),
        }
