from django import forms


class MessageForm(forms.Form):
    anonymous = forms.BooleanField(label="Send anonymously", required=False)
    body = forms.CharField(label="Message:", max_length=10000, required=True)


class ChangeSettingsForm(forms.Form):
    email = forms.EmailField(
        label="Email:",
        max_length=254,
        required=False
    )
    theme = forms.ChoiceField(
        choices=[
            ("auto", "auto"),
            ("light_mode", "light mode"),
            ("dark_mode", "dark mode"),
            ("forest", "forest"),
            ("hacker", "hacker"),
            ("vice", "vice"),
            ("suffering", "suffering")
        ],
        label="Site theme:",
        required=True
    )