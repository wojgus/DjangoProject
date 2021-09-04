from django.forms import (
    ModelForm, CharField, IntegerField,
)
import re
from viewer.models import Movie
from django.core.exceptions import ValidationError
from viewer.validators import PastMonthField, capitalized_validator


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'
    title = CharField(validators=[capitalized_validator])
    rating = IntegerField(min_value=1, max_value=10)
    released = PastMonthField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_description(self):
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences)

    def clean(self):
        result = super().clean()
        if result['genre'].name == 'comedy' and result['rating'] > 7:
            self.add_error('genre', '')
            self.add_error('rating', '')
            raise ValidationError(
                'Commedies aren\'t so good to be over 7'

            )

        return result
