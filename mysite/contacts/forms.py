from django import forms

from contacts.models import Tag, PhoneNumber, Contact, Record


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]


class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ["contact", "number"]

    def clean_number(self):
        number = self.cleaned_data.get("number")
        number = PhoneNumber().normalize_phone(number)  # нормалізуємо номер телефону
        if PhoneNumber.objects.filter(number=number).exists():
            raise forms.ValidationError("This phone number already exists.")
        return number


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["full_name", "address", "email", "birthday"]

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name")
        if Contact.objects.filter(full_name=full_name).exists():
            raise forms.ValidationError("This author is already exists.")
        return full_name


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ["contact", "note", "tags"]

    def clean(self):
        cleaned_data = super().clean()
        note = cleaned_data.get("note")
        contact = cleaned_data.get("contact")

        if note and contact:
            # Перевірка унікальності цитати для конкретного автора
            if Record.objects.filter(note=note, contact=contact).exists():
                raise forms.ValidationError("This note for the contact already exists.")
        return cleaned_data
