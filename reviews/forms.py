from django import forms
from .models import Review, Comment, Image

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', ]

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image_files', ]
        
ImageFormSet = forms.inlineformset_factory(Review, Image, form=ImageForm, extra=3)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['opinion', ]

