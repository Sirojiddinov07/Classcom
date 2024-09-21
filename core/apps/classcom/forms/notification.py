from django import forms

from unfold.widgets import UnfoldAdminTextInputWidget


class NotificationForm(forms.Form):
    message_uz = forms.CharField(
        label="Matn UZ",
        widget=UnfoldAdminTextInputWidget(attrs={"placeholder": "Matn"}),
    )
    message_ru = forms.CharField(
        label="Текст RU",
        widget=UnfoldAdminTextInputWidget(attrs={"placeholder": "Текст"}),
    )
