from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from .models import Project, Document, Message, Profile, Keyword

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=Profile.USER_TYPES, required=True, label="User Type")
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create profile with user_type
            Profile.objects.get_or_create(user=user, defaults={'user_type': self.cleaned_data['user_type']})
        return user

class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['keywords'].widget = forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'})
        self.fields['keywords'].widget.choices = self.fields['keywords'].choices

    class Meta:
        model = Project
        fields = ['title', 'description', 'project_type', 'specialization_needed', 'keywords', 'duration', 'prerequisites', 'budget']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file', 'project']

    def clean_file(self):
        f = self.cleaned_data.get('file')
        if not f:
            return f
        # Size check
        max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 10 * 1024 * 1024)
        if f.size > max_size:
            raise forms.ValidationError(f"File too large. Max size is {max_size // (1024 * 1024)} MB.")
        # Content type check (may be None for some storages; fallback to name)
        allowed = set(getattr(settings, 'ALLOWED_FILE_TYPES', []))
        content_type = getattr(f, 'content_type', None)
        if content_type and allowed and content_type not in allowed:
            raise forms.ValidationError("Unsupported file type.")
        # Simple extension fallback
        allowed_ext = {'.pdf', '.png', '.jpg', '.jpeg', '.doc', '.docx'}
        name = f.name.lower()
        if not any(name.endswith(ext) for ext in allowed_ext):
            raise forms.ValidationError("Unsupported file extension.")
        return f

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_type', 'organization', 'institution_type', 'specialization', 'keywords', 'bio', 'contact_email', 'phone', 'cv']
        widgets = {
            'keywords': forms.CheckboxSelectMultiple(),
        }
