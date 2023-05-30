from django import forms


class MessageForm(forms.Form):
    anonymous = forms.BooleanField(label="Send anonymously", required=False)
    body = forms.CharField(label="Message:", max_length=10000, required=True)