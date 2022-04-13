from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

RATE = ((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"))


class Source(models.Model):
    quoter = models.CharField(max_length=100)
    origin = models.CharField(max_length=100, blank=True)
    note = models.TextField(max_length=500, blank=True, default=(""))

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.quoter}, {self.origin}"

    def get_absolute_url(self):
        return reverse("source_details", kwargs={"source_id": self.id})


class Quote(models.Model):
    content = models.TextField(max_length=1000)
    note = models.TextField(max_length=500, blank=True, default=(""))
    sources = models.ManyToManyField(Source)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("quote_details", kwargs={"quote_id": self.id})


class ReviewQuote(models.Model):
    review = models.TextField(max_length=500)
    rating = models.IntegerField(default=RATE[0][0], choices=RATE)
    date = models.DateField(auto_now_add=True, blank=True)

    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["-date"]
