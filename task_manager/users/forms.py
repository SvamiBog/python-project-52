from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        ]


class UserUpdateForm(UserCreateForm):
    class Meta(UserCreateForm.Meta):
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        ]

    def clean_username(self):
        if (
            self.get_initial_for_field(
                self.fields['username'], 'username'
            ).lower()
            != self.cleaned_data.get('username').lower()
        ):
            return super().clean_username()
        else:
            return self.cleaned_data.get('username')
