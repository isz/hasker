import sys
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import reverse
from django.utils import timezone

import logging
from datetime import datetime, timedelta


class TagsManager(models.Manager):
    def queryset_from_list(self, tags):
        for tag in tags:
            if self.get_queryset().filter(text=tag).count() == 0:
                Tag.objects.create(text=tag)

        return self.get_queryset().filter(text__in=tags)


class Tag(models.Model):
    """
    Модель сущности Тэг
    """
    text = models.CharField(primary_key=True, verbose_name="text", max_length=32)

    objects = TagsManager()


class Entry(models.Model):
    """
    Абстрактная модель запией
    """
    vote_class_name = ""

    def __init__(self, *args, **kwargs):
        self.vote_class = getattr(sys.modules[__name__], self.vote_class_name)
        super().__init__(*args, **kwargs)

    class Meta:
        abstract = True

    date = models.DateField(verbose_name="Creation date", auto_now_add=True)
    rating = models.IntegerField(default=0, blank=True)

    def set_action_attrs(self, user):
        try:
            vote_val = self.votes.get(user=user).value
            if vote_val == 1:
                self.like = "cancel"
                self.dislike = "dislike"
            else:
                self.like = "like"
                self.dislike = "cancel"
        except self.votes.model.DoesNotExist:
            self.like = "like"
            self.dislike = "dislike"


class Question(Entry):
    """
    Модель сущности Вопрос
    """
    user = models.ForeignKey(User, related_name="questions", on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Title", max_length=255)
    text = models.TextField(verbose_name="Text")
    tags = models.ManyToManyField(Tag, verbose_name="Tags")
    correct_answer = models.ForeignKey(
        "Answer", default=None, null=True, blank=True, on_delete=models.SET_DEFAULT
    )
    date = models.DateTimeField(auto_now_add=True)

    vote_class_name = "QuestionVote"

    def get_absolute_url(self):
        return reverse("qanda:question", args=(self.id,))

    def set_correct_answer(self, answ_id, user):
        if self.correct_answer:
            raise ValueError("Correct answer exist")

        if user != self.user:
            raise ValueError("Only for question owner")

        try:
            answ = self.answers.get(pk=answ_id)
        except Answer.DoesNotExist:
            logging.error(f"The answer (id={answ_id}) does not match the question")
            raise ValueError("The answer does not match the question")

        self.correct_answer = answ
        self.save()

    def age(self):
        delta = timezone.now() - self.date

        val = delta.total_seconds()

        if delta < timedelta(minutes=1):
            text = "second"
        elif delta < timedelta(hours=1):
            val = val / 60
            text = "minute"
        elif delta < timedelta(days=1):
            val = val / (60 * 60)
            text = "hour"
        else:
            val = val / (60 * 60 * 24)
            text = "day"

        val = int(val)
        if val > 1:
            text += "s"
        return f"{val} {text}"


class Answer(Entry):
    """
    Модель сущности Ответ
    """
    user = models.ForeignKey(User, related_name="answers", on_delete=models.CASCADE)
    to_question = models.ForeignKey(
        Question, related_name="answers", on_delete=models.CASCADE
    )
    text = models.TextField(verbose_name="Answer")
    date = models.DateTimeField(auto_now_add=True)

    vote_class_name = "AnswerVote"

    def notify_question_owner(self, question_uri):
        question = self.to_question

        subject, from_email, to = (
            "Answer to your question",
            settings.EMAIL_FROM,
            question.user.email,
        )
        text_content = f'You received answer to your question "{question.title}".'
        html_content = f'You received answer to your question <a href="{question_uri}">"{question.title}"</a>.'

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class VoteModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField()

    class Meta:
        abstract = True

    @classmethod
    def vote(cls, obj_id, user, action):
        value = 1 if action == "like" else -1

        try:
            instance = cls.objects.select_related("to").get(to=obj_id, user=user)

            if instance.value != value:
                if instance.value == -1 and value == 1:
                    correction = 2
                else:
                    correction = -2

                instance.value = value

                to_instance = instance.to
                to_instance.rating += correction
                instance.to.save()

        except cls.DoesNotExist:
            to_instance = cls.to_model_class.objects.get(pk=obj_id)
            instance = cls(user=user, to=to_instance, value=value)
            to_instance.rating += value

        to_instance.save()
        instance.save()
        return instance

    @classmethod
    def cancel(cls, obj_id, user):
        try:
            instance = cls.objects.select_related("to").get(to=obj_id, user=user)

            instance.to.rating += instance.value * -1
            instance.to.save()
            instance.delete()
        except:
            pass


class QuestionVote(VoteModel):
    to_model_class = Question
    to = models.ForeignKey(Question, related_name="votes", on_delete=models.CASCADE)


class AnswerVote(VoteModel):
    to_model_class = Answer
    to = models.ForeignKey(Answer, related_name="votes", on_delete=models.CASCADE)
