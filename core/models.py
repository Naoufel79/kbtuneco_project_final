from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

INSTITUTIONS = [
    ("university", "Université"),
    ("public_research", "Établissement public de recherche"),
    ("association", "Association scientifique"),
    ("tech_center", "Centre technique"),
    ("technopole", "Technopôle"),
]

SPECIALIZATIONS = [
    ("aero", "Aeronautical Engineering"),
    ("agri", "Agriculture"),
    ("ai", "Artificial Intelligence"),
    ("bio", "Biotechnology"),
    ("chem", "Chemistry / Chemical Engineering"),
    ("civ", "Civil Engineering"),
    ("cs", "Computer Science / ICT"),
    ("elec", "Electrical & Power Engineering"),
    ("env", "Environment"),
    ("mech", "Mechanical Engineering"),
    ("med", "Medicine / Biomedical"),
    ("mgmt", "Management Science"),
    ("math", "Mathematics"),
    ("phys", "Physics"),
    ("soc", "Social Sciences / Humanities"),
    ("other", "Other"),
]

class Keyword(models.Model):
    code = models.CharField(max_length=80, unique=True)
    label = models.CharField(max_length=200)

    def __str__(self):
        return self.label

class Organization(models.Model):
    name = models.CharField(max_length=255)
    org_type = models.CharField(max_length=50, choices=INSTITUTIONS)
    description = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    USER_TYPES = [
        ('student', 'Student'),
        ('researcher', 'Researcher'),
        ('university', 'University / Lab'),
        ('company', 'Company'),
        ('association', 'Association'),
        ('medical', 'Medical Staff'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=30, choices=USER_TYPES, default='student')
    institution_type = models.CharField(max_length=50, choices=INSTITUTIONS, blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, blank=True, null=True)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATIONS, default='other')
    keywords = models.ManyToManyField(Keyword, blank=True)
    bio = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_user_type_display()})"

class Project(models.Model):
    PROJECT_TYPES = [
        ('mission', 'Mission Courte'),
        ('research', 'Recherche'),
        ('engineering', 'Ingénierie'),
        ('pfe', 'PFE / Master / PhD'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=300)
    description = models.TextField()
    project_type = models.CharField(max_length=30, choices=PROJECT_TYPES)
    posted_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posted_projects')
    specialization_needed = models.CharField(max_length=50, choices=SPECIALIZATIONS, default='other')
    keywords = models.ManyToManyField(Keyword, blank=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    prerequisites = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='open')
    participants = models.ManyToManyField(Profile, through='ProjectParticipant', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.title

class ProjectParticipant(models.Model):
    ROLE_CHOICES = [
        ('candidate', 'Candidate'),
        ('member', 'Member'),
        ('supervisor', 'Supervisor'),
        ('company_contact', 'Company Contact'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='candidate')
    applied_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    joined_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('project', 'profile')

    def __str__(self):
        return f"{self.profile.user.username} -> {self.project.title} ({self.role})"

class Document(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='documents')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents', blank=True, null=True)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.user.username} -> {self.recipient.user.username} [{self.subject}]"

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    organizer = models.ForeignKey(Organization, on_delete=models.SET_NULL, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    capacity = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)

    class Meta:
        unique_together = ('event', 'profile')

    def __str__(self):
        return f"{self.profile.user.username} -> {self.event.title}"

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price_per_year = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField(blank=True)

    def __str__(self):
        return self.name

class CompanySubscription(models.Model):
    company = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'user_type': 'company'})
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    started_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.company.user.username} - {self.plan.name}"
