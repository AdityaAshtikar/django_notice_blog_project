from django import forms

from pagedown.widgets import PagedownWidget

from posts.models import Post, Category

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget)
    publish_date = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = Post
        fields = ["title", "category", "content", "image", "draft", "publish_date"]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['topic']
