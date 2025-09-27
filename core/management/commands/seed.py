from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Keyword, Organization, Profile, Project, Event
from django.utils import timezone
import datetime

class Command(BaseCommand):
    help = "Seed database with sample data"

    def handle(self, *args, **kwargs):
        # Keyword list (sample from slides)
        keywords = [
            ("ai", "Artificial Intelligence"),
            ("iot", "Internet of Things"),
            ("cloud", "Cloud Computing"),
            ("data", "Data Mining / Big Data"),
            ("health", "eHealth"),
            ("env", "Environment"),
            ("energy", "Energy Engineering"),
            ("bio", "Biotechnology"),
            ("robot", "Robotics"),
            ("sec", "Security / Cryptography"),
            ("net", "Computer Networks"),
            ("edu", "Online Education"),
            ("mobile", "Mobile Computing"),
            ("sat", "Satellite & Space"),
            ("nlp", "Natural Language Processing"),
            ("cv", "Computer Vision"),
            ("embedded", "Embedded Systems"),
            ("qa", "Quality Assurance"),
            ("iotsec", "IoT Security"),
            ("mlops", "MLOps"),
        ]
        for code, label in keywords:
            Keyword.objects.get_or_create(code=code, label=label)

        # Organizations
        org1, _ = Organization.objects.get_or_create(
            name="Université de Tunis", org_type="university", description="Main public university"
        )
        org2, _ = Organization.objects.get_or_create(
            name="Centre Technique Agroalimentaire", org_type="tech_center", description="Food research center"
        )
        org3, _ = Organization.objects.get_or_create(
            name="Technopole Elgazala", org_type="technopole", description="Tech park focused on ICT"
        )

        # Create users and profiles
        def create_user(username, email, password, user_type, org, specialization, kw_codes):
            user, created = User.objects.get_or_create(username=username, email=email)
            if created:
                user.set_password(password)
                user.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.user_type = user_type
            profile.organization = org
            profile.specialization = specialization
            profile.save()
            if kw_codes:
                kws = Keyword.objects.filter(code__in=kw_codes)
                profile.keywords.set(kws)
            return profile

        p_student = create_user("student1", "student1@example.com", "1234", "student", org1, "cs", ["ai", "data", "cloud"])
        p_researcher = create_user("researcher1", "res1@example.com", "1234", "researcher", org1, "ai", ["ai", "nlp", "cv"])
        p_company = create_user("company1", "comp1@example.com", "1234", "company", org3, "cs", ["iot", "embedded", "iotsec"])

        # Projects
        proj1, _ = Project.objects.get_or_create(
            title="Smart Agriculture IoT Sensors",
            description="Research project on IoT-based monitoring of crops",
            project_type="research",
            posted_by=p_researcher,
            specialization_needed="agri",
            duration="6 months",
        )
        proj1.keywords.set(Keyword.objects.filter(code__in=["iot", "embedded", "cloud"]))

        proj2, _ = Project.objects.get_or_create(
            title="AI for Medical Imaging",
            description="PFE project using deep learning for X-ray diagnosis",
            project_type="pfe",
            posted_by=p_researcher,
            specialization_needed="med",
            duration="5 months",
        )
        proj2.keywords.set(Keyword.objects.filter(code__in=["ai", "cv"]))

        proj3, _ = Project.objects.get_or_create(
            title="Secure IoT for Smart Buildings",
            description="Development of an IoT security framework for building management",
            project_type="engineering",
            posted_by=p_company,
            specialization_needed="cs",
            duration="8 months",
        )
        proj3.keywords.set(Keyword.objects.filter(code__in=["iot", "iotsec", "sec"]))

        # Events
        Event.objects.get_or_create(
            title="Innovation Workshop",
            description="Hands-on workshop for startups",
            organizer=org3,
            location="Technopole Elgazala",
            start=timezone.now() + datetime.timedelta(days=10),
            end=timezone.now() + datetime.timedelta(days=11),
        )

        self.stdout.write(self.style.SUCCESS("Seeded database with sample data."))
