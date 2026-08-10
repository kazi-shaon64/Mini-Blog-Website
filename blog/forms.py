from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Profile


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email",
                "autocomplete": "email",
            }
        )
    )

    class Meta:

        model = User

        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

        widgets = {

            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Choose a username",
                    "autocomplete": "username",
                }
            ),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Create a password",
            "autocomplete": "new-password",
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirm your password",
            "autocomplete": "new-password",
        })


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title", "content"]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter post title"
                }
            ),

            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 10,
                    "placeholder": "Write your post..."
                }
            ),
        }

    def clean_title(self):

        title = self.cleaned_data["title"].strip()

        if len(title) < 5:

            raise forms.ValidationError(
                "Title must contain at least 5 characters."
            )

        return title

    def clean_content(self):

        content = self.cleaned_data["content"].strip()

        if len(content) < 20:

            raise forms.ValidationError(
                "Post content must contain at least 20 characters."
            )

        return content


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["content"]

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write your comment..."
                }
            ),
        }

class ProfileForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = [
            "bio",
            "profile_image",
        ]

        widgets = {

            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Tell us about yourself..."
                }
            ),

            "profile_image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),
        }