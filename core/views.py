from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Exists, OuterRef, Prefetch
from django.views.decorators.cache import cache_page
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils import timezone
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from .models import Project, ProjectParticipant, Profile, Document, Message, Event, EventParticipant, Keyword, Organization
from .forms import ProjectForm, DocumentForm, MessageForm, RegisterForm, ProfileForm
from django.contrib.auth.forms import AuthenticationForm

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})

@login_required
def project_list(request):
    q = request.GET.get('q', '').strip()
    projects_qs = (
        Project.objects.all()
        .select_related('posted_by__user')
        .prefetch_related('keywords')
    )
    if q:
        projects_qs = projects_qs.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(keywords__label__icontains=q)
        ).distinct()
    if request.user.is_authenticated:
        projects_qs = projects_qs.annotate(
            user_has_applied=Exists(
                ProjectParticipant.objects.filter(
                    project=OuterRef('pk'),
                    profile=request.user.profile
                )
            )
        )
    projects = list(projects_qs)
    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required
def project_create(request):
    # Permission: only researchers and companies can create projects
    if getattr(request.user, 'profile', None) is None or request.user.profile.user_type not in ('researcher', 'company'):
        context = {
            'message': _("Only institutions and companies can create projects. Students and researchers can browse and apply."),
            'action_url': 'project_list',
            'action_text': _("Browse Projects"),
        }
        return render(request, 'projects/permission_denied.html', context)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.posted_by = request.user.profile
            project.save()
            form.save_m2m()
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'projects/project_detail.html', {'project': project})

@login_required
def project_apply(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        if request.user.profile.user_type not in ('student', 'researcher'):
            messages.warning(request, _("Only students and researchers can apply to projects."))
        elif project.status != 'open':
            messages.warning(request, _("This project is not open for applications."))
        else:
            exists = ProjectParticipant.objects.filter(project=project, profile=request.user.profile).exists()
            if exists:
                messages.info(request, _("You have already applied to this project."))
            else:
                ProjectParticipant.objects.create(
                    project=project,
                    profile=request.user.profile,
                    role='candidate',
                    accepted=False
                )
                messages.success(request, _("Application submitted successfully."))
    else:
        messages.error(request, _("Invalid request method."))
    return redirect('project_list')

@login_required
def project_withdraw(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        participant = ProjectParticipant.objects.filter(
            project=project, profile=request.user.profile
        ).first()
        if participant:
            participant.delete()
            messages.success(request, _("Your application has been withdrawn."))
        else:
            messages.info(request, _("You have no application for this project."))
    else:
        messages.error(request, _("Invalid request method."))
    return redirect('project_list')

@login_required
def suggestions_for_user(request):
    # Logic for suggestions
    return render(request, 'projects/suggestions.html')

@login_required
def dashboard(request):
    total_projects = Project.objects.count()
    open_projects = Project.objects.filter(status='open').count()
    total_users = Profile.objects.count()
    recent_projects = Project.objects.order_by('-created_at')[:5]

    # User-specific statistics
    projects_posted = Project.objects.filter(posted_by=request.user.profile).count()
    messages_sent = Message.objects.filter(sender=request.user.profile).count()
    messages_received = Message.objects.filter(recipient=request.user.profile).count()
    documents_uploaded = Document.objects.filter(owner=request.user.profile).count()

    context = {
        'total_projects': total_projects,
        'open_projects': open_projects,
        'total_users': total_users,
        'recent_projects': recent_projects,
        'projects_posted': projects_posted,
        'messages_sent': messages_sent,
        'messages_received': messages_received,
        'documents_uploaded': documents_uploaded,
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.owner = request.user.profile
            doc.save()
            return redirect('dashboard')
    else:
        form = DocumentForm()
    return render(request, 'documents/upload.html', {'form': form})

@login_required
def inbox(request):
    messages = (
        Message.objects
        .filter(recipient=request.user.profile)
        .select_related('sender__user', 'recipient__user')
        .order_by('-sent_at')
    )
    return render(request, 'messages/inbox.html', {'messages': messages})

@login_required
def send_message(request):
    recipient_profile = None
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user.profile
            msg.save()
            return redirect('inbox')
    else:
        form = MessageForm()
        recipient_id = request.GET.get('recipient')
        project_id = request.GET.get('project')
        if recipient_id:
            try:
                recipient_profile = Profile.objects.get(user__id=recipient_id)
                form = MessageForm(initial={'recipient': recipient_profile})
            except Profile.DoesNotExist:
                pass
    return render(request, 'messages/compose.html', {'form': form, 'recipient_profile': recipient_profile})

@login_required
def events_list(request):
    events_qs = (
        Event.objects.all()
        .select_related('organizer')
        .order_by('start')
    )
    if request.user.is_authenticated:
        events_qs = events_qs.annotate(
            user_is_registered=Exists(
                EventParticipant.objects.filter(
                    event=OuterRef('pk'),
                    profile=request.user.profile
                )
            )
        )
    events = list(events_qs)
    return render(request, 'events/events_list.html', {'events': events})

@login_required
def event_register(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    # Register current user to the event if not already registered
    if request.method != 'POST':
        messages.error(request, _("Invalid request method."))
        return redirect('events_list')

    already = EventParticipant.objects.filter(event=event, profile=request.user.profile).exists()
    if already:
        messages.info(request, _("You are already registered for this event."))
    else:
        EventParticipant.objects.create(event=event, profile=request.user.profile)
        messages.success(request, _("You have been registered for the event."))
    return redirect('events_list')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('about')

@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'auth/profile.html', {'profile': profile})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'auth/profile_edit.html', {'form': form})

@login_required
def user_projects(request):
    projects = (
        Project.objects
        .filter(posted_by=request.user.profile)
        .select_related('posted_by__user')
        .prefetch_related('keywords', 'participants')
        .order_by('-created_at')
    )
    return render(request, 'projects/user_projects.html', {'projects': projects})

@login_required
def my_applications(request):
    applications = (
        ProjectParticipant.objects
        .filter(profile=request.user.profile)
        .select_related('project', 'project__posted_by__user')
        .order_by('-applied_at')
    )
    return render(request, 'projects/my_applications.html', {'applications': applications})

@login_required
def manage_applications(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.posted_by.user != request.user:
        context = {
            'message': _("You don't have permission to manage applications for this project."),
            'action_url': 'project_list',
            'action_text': _("Browse Projects"),
        }
        return render(request, 'projects/permission_denied.html', context)
    applications = ProjectParticipant.objects.filter(project=project)
    return render(request, 'projects/manage_applications.html', {'applications': applications, 'project': project})

@login_required
def accept_application(request, application_id):
    application = get_object_or_404(ProjectParticipant, id=application_id)
    if application.project.posted_by.user == request.user:
        application.accepted = True
        application.joined_at = timezone.now()
        application.save()
    return redirect('manage_applications', project_id=application.project.id)

@login_required
def reject_application(request, application_id):
    application = get_object_or_404(ProjectParticipant, id=application_id)
    if application.project.posted_by.user == request.user:
        application.delete()
    return redirect('manage_applications', project_id=application.project.id)
