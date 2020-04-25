from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, FormView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.conf import settings
from django.db import transaction

from . import models, forms


class AskQuestionView(LoginRequiredMixin, CreateView):
    model = models.Question
    template_name = "qanda/ask_question.html"
    form_class = forms.AskQuestionForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AskQuestionView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("qanda:question", args=(self.object.id,))


class QuestionDetail(DetailView):
    model = models.Question
    template_name = "qanda/question.html"
    context_object_name = "question"

    def get(self, request, page=1, *args, **kwargs):
        self.page = page
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.AnswerForm()
        context["form"].fields["to_question"].initial = self.object.id

        question = context["question"]

        if self.request.user.is_authenticated:
            question.set_action_attrs(self.request.user)

        answers = []
        answer_paginator = Paginator(
            question.answers.order_by("-rating", "date"), settings.ANSWERS_PER_PAGE
        )
        answer_page = answer_paginator.page(self.page)

        for answ in answer_page:
            if self.request.user.is_authenticated:
                answ.set_action_attrs(self.request.user)
            answers.append(answ)

        context["answers"] = answers
        context["answer_page"] = answer_page

        return context


class QuestionListView(ListView):
    model = models.Question
    template_name = "qanda/question_list.html"
    paginate_by = settings.QUESTIONS_PER_PAGE
    ordering = ["rating", "date"]

    def get_ordering(self):
        ordering = self.request.GET.get("order_by", "rating")
        if ordering not in self.ordering:
            ordering = "rating"

        return ("-" + ordering,)

    def get_queryset(self):
        try:
            search_string = self.request.GET["search_string"].strip()
        except KeyError:
            self.header = "Questions"
            queryset = self.model.objects.all()
        else:
            if search_string.startswith("tag:"):
                tag_name = search_string.split("tag:")[1].strip()
                self.header = f'Tag "{tag_name}" result'
                queryset = self.model.objects.filter(tags__text=tag_name)
            else:
                self.header = "Search result"
                queryset = self.model.objects.filter(
                    title__icontains=search_string
                ) | self.model.objects.filter(text__icontains=search_string)

        ordering = self.get_ordering()
        return queryset.order_by(*ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["header"] = self.header
        return context


class CreateAnswerView(LoginRequiredMixin, CreateView):
    model = models.Answer
    form_class = forms.AnswerForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateAnswerView, self).form_valid(form)

    def get_success_url(self):
        question_uri = reverse("qanda:question", args=(self.object.to_question.id,))
        self.object.notify_question_owner(self.request.build_absolute_uri(question_uri))
        return question_uri


class VoteQuestionView(LoginRequiredMixin, View):
    template_name = "qanda/error.html"

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        question_id = kwargs.get("pk")
        action = kwargs.get("action")

        if action in ("like", "dislike"):
            models.QuestionVote.vote(question_id, request.user, action)
        elif action == "cancel":
            models.QuestionVote.cancel(question_id, request.user)

        page = request.POST.get("from_page", 1)
        return redirect(reverse("qanda:question_page", args=(question_id, page)))


class VoteAnswerView(LoginRequiredMixin, View):
    template_name = "qanda/error.html"

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        answer_id = kwargs.get("pk")
        action = kwargs.get("action")
        question_id = request.POST.get("question")


        if action in ("like", "dislike"):
            models.AnswerVote.vote(answer_id, request.user, action)
        elif action == "cancel":
            models.AnswerVote.cancel(answer_id, request.user)

        page = request.POST.get("from_page", 1)
        return redirect(reverse("qanda:question_page", args=(question_id, page)))



class CorrectAnswerView(LoginRequiredMixin, View):
    template_name = "qanda/error.html"

    def post(self, request, *args, **kwargs):
        question_id = kwargs.get("pk")
        answ_id = kwargs.get("answ_id")

        question = get_object_or_404(models.Question, pk=question_id)

        try:
            question.set_correct_answer(answ_id, request.user)
        except ValueError as e:
            return render(request, self.template_name, context={"msg": str(e)})
        except:
            return render(
                request,
                self.template_name,
                context={"msg": "Error while correct answer marking"},
            )

        page = request.POST.get("from_page", 1)

        return redirect(reverse("qanda:question_page", args=(question_id, page)))
