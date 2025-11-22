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
            ("auto", "Auto"),
            ("light_mode", "Light Mode"),
            ("dark_mode", "Dark Mode"),
            ("forest", "Forest"),
            ("hacker", "Hacker"),
            ("vice", "Vice"),
            ("suffering", "Suffering"),
            ("unstyled", "Unstyled HTML"),
            ("dignified", "Dignified (70s-80s)"),
            ("geocities", "Geocities"),
            ("cyberpunk", "Cyberpunk"),
            ("fantasy", "Fantasy"),
            ("seapunk", "Seapunk"),
            ("modern_light", "Modern Light"),
            ("modern_dark", "Modern Dark"),
            ("helvetica_light", "Helvetica Light"),
            ("helvetica_dark", "Helvetica Dark"),
            ("low_contrast", "Low Contrast"),
            ("terminal", "Terminal"),
            ("sunset", "Sunset"),
            ("ocean", "Ocean"),
            ("lavender", "Lavender"),
            ("chocolate", "Chocolate"),
            ("neon", "Neon"),
            ("pastel", "Pastel"),
            ("high_contrast", "High Contrast"),
            ("solarized", "Solarized"),
            ("nord", "Nord"),
        ],
        label="Site theme:",
        required=True
    )