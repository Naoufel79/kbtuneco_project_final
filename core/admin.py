from django.contrib import admin
from .models import (
    Profile, Organization, Keyword, Project, ProjectParticipant,
    Document, Message, Event, SubscriptionPlan, CompanySubscription
)

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('label', 'code')
    search_fields = ('label', 'code')

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'org_type', 'contact_email')
    search_fields = ('name',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'organization', 'specialization')
    list_filter = ('user_type', 'specialization', 'institution_type')
    search_fields = ('user__username', 'user__email', 'organization__name')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'project_type', 'posted_by', 'status', 'created_at')
    list_filter = ('project_type', 'status', 'specialization_needed')
    search_fields = ('title', 'description', 'keywords__label')
    filter_horizontal = ('keywords',)

@admin.register(ProjectParticipant)
class ProjectParticipantAdmin(admin.ModelAdmin):
    list_display = ('project', 'profile', 'role', 'accepted', 'applied_at')
    list_filter = ('role', 'accepted')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'project', 'uploaded_at')
    search_fields = ('title', 'owner__user__username')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'sent_at', 'read')
    list_filter = ('read',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'start', 'end')
    search_fields = ('title',)

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_year')

@admin.register(CompanySubscription)
class CompanySubscriptionAdmin(admin.ModelAdmin):
    list_display = ('company', 'plan', 'started_at', 'expires_at')
