from django.forms import ModelForm
from .models import ReviewQuote

class AddReviewQuoteForm(ModelForm):
    class Meta:
        model = ReviewQuote
        fields = ['review', 'rating']