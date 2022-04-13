from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Quote, Source, ReviewQuote
from django.views.generic import TemplateView
from main_app.forms import AddReviewQuoteForm
from main_app.filter import QuoteFilter, SourceFilter


def home(request):
    quote = Quote.objects.last()
    return render(request, "home.html", {"quote": quote})


class AboutView(TemplateView):
    template_name = "about.html"


def sources_index(request):
    sources = Source.objects.all()
    s = SourceFilter(request.GET, queryset=Source.objects.all())
    return render(
        request, "sources/index.html", {"sources": sources, "sourcefilter": s}
    )


def source_details(request, source_id):
    source = Source.objects.get(id=source_id)
    quotes = Quote.objects.all()
    return render(request, "sources/details.html", {"source": source, "quotes": quotes})


class SourceCreate(CreateView, LoginRequiredMixin):
    model = Source
    fields = ["quoter", "origin", "note"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SourceUpdate(UpdateView, LoginRequiredMixin):
    model = Source
    fields = ["quoter", "origin", "note"]


class SourceDelete(DeleteView, LoginRequiredMixin):
    model = Source
    success_url = "/sources/"


def quotes_index(request):
    quotes = Quote.objects.all()
    q = QuoteFilter(request.GET, queryset=Quote.objects.all())
    return render(
        request,
        "quotes/index.html",
        {"quotes": quotes, "quotefilter": q},
    )


def quote_details(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    sources_quote_does_not_have = Source.objects.exclude(
        id__in=quote.sources.all().values_list("id")
    )
    s = SourceFilter(request.GET, queryset=sources_quote_does_not_have)
    add_quote_review_form = AddReviewQuoteForm()
    return render(
        request,
        "quotes/details.html",
        {
            "quote": quote,
            "add_quote_review_form": add_quote_review_form,
            "sources": sources_quote_does_not_have,
            "sourcefilter": s,
        },
    )


class QuoteCreate(CreateView, LoginRequiredMixin):
    model = Quote
    fields = ["content", "note"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class QuoteUpdate(UpdateView, LoginRequiredMixin):
    model = Quote
    fields = ["content", "note"]


class QuoteDelete(DeleteView, LoginRequiredMixin):
    model = Quote
    success_url = "/quotes/"


@login_required
def quotes_personal(request):
    user = request.user
    quotes = user.quote_set.all()
    q = QuoteFilter(request.GET, queryset=user.quote_set.all())
    return render(request, "quotes/personal.html", {"quotes": quotes, "quotefilter": q})


@login_required
def add_quote_review(request, quote_id):
    form = AddReviewQuoteForm(request.POST)
    if form.is_valid():
        new_review_quote = form.save(commit=False)
        new_review_quote.quote_id = quote_id
        new_review_quote.user_id = request.user.id
        new_review_quote.save()
    return redirect("quote_details", quote_id=quote_id)


@login_required
def delete_quote_review(request, quote_id, review_id):
    q = Quote.objects.get(id=quote_id)
    review = ReviewQuote.objects.get(id=review_id)
    q.reviewquote_set.remove(review)
    return redirect("quote_details", quote_id=quote_id)


@login_required
def assoc_source(request, quote_id, source_id):
    Quote.objects.get(id=quote_id).sources.add(source_id)
    return redirect("quote_details", quote_id=quote_id)


@login_required
def unassoc_source(request, quote_id, source_id):
    Quote.objects.get(id=quote_id).sources.remove(source_id)
    return redirect("quote_details", quote_id=quote_id)


def signup(request):
    error_message = ""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        else:
            error_message = "Invalid signup - try again"
    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "registration/signup.html", context)
