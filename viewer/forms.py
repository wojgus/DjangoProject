from django.forms import (
    Form, CharField, ModelChoiceField, IntegerField, DateField, Textarea
)
import re
from viewer.models import Genre
from django.core.exceptions import ValidationError
from viewer.validators import PastMonthField, capitalized_validator
from logging import getLogger

LOGGER = getLogger()


class MovieForm(Form):
    title = CharField(max_length=128)
    genre = ModelChoiceField(queryset=Genre.objects)
    rating = IntegerField(min_value=1, max_value=10)
    released = DateField()
    description = CharField(widget=Textarea, required=False)

    def clean_description(self):
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences)

    def clean(self):
        result = super().clean()
        LOGGER.warning('tu jestem')
        if result['genre'].name == 'comedy' and result['rating'] > 7:
            self.add_error('genre', '')
            self.add_error('rating', '')
            raise ValidationError(
                'Commedies aren\'t so good to be over 7'

            )

        return result
