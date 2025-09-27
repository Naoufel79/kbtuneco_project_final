import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from core.models import Profile, Organization, Keyword, Project, Message, Document, Event, ProjectParticipant


@pytest.mark.django_db
class TestEventModel:
    """Test cases for Event model."""

    def test_event_creation(self):
        """Test that an event can be created."""
        from django.utils import timezone
        event = Event.objects.create(
            title='Test Event',
            description='A test event',
            location='Test Location',
            start=timezone.now(),
            end=timezone.now()
        )
        assert event.title == 'Test Event'
        assert str(event) == 'Test Event'
class TestProfileModel:
    """Test cases for Profile model."""

    def test_profile_creation(self, user):
        """Test that a profile can be created."""
        profile = Profile.objects.create(
            user=user,
            user_type='student',
            specialization='cs'
        )
        assert profile.user == user
        assert profile.user_type == 'student'
        assert profile.specialization == 'cs'
        assert str(profile) == f"{user.username} (Student)"

    def test_profile_user_type_choices(self, user):
        """Test that user_type accepts valid choices."""
        for user_type in ['student', 'researcher', 'university', 'company', 'association', 'medical']:
            profile = Profile.objects.create(user=user, user_type=user_type)
            assert profile.user_type == user_type

    def test_profile_specialization_choices(self, user):
        """Test that specialization accepts valid choices."""
        specializations = ['aero', 'agri', 'ai', 'bio', 'chem', 'civ', 'cs', 'elec', 'env', 'mech', 'med', 'mgmt', 'math', 'phys', 'soc', 'other']
        for spec in specializations:
            profile = Profile.objects.create(user=user, specialization=spec)
            assert profile.specialization == spec

    def test_profile_get_user_type_display(self, user):
        """Test the get_user_type_display method."""
        profile = Profile.objects.create(user=user, user_type='student')
        assert profile.get_user_type_display() == 'Student'


@pytest.mark.django_db
class TestOrganizationModel:
    """Test cases for Organization model."""

    def test_organization_creation(self):
        """Test that an organization can be created."""
        org = Organization.objects.create(
            name='Test University',
            org_type='university',
            description='A test university'
        )
        assert org.name == 'Test University'
        assert org.org_type == 'university'
        assert str(org) == 'Test University'

    def test_organization_org_type_choices(self):
        """Test that org_type accepts valid choices."""
        for org_type in ['university', 'public_research', 'association', 'tech_center', 'technopole']:
            org = Organization.objects.create(name=f'Test {org_type}', org_type=org_type)
            assert org.org_type == org_type


@pytest.mark.django_db
class TestKeywordModel:
    """Test cases for Keyword model."""

    def test_keyword_creation(self):
        """Test that a keyword can be created."""
        keyword = Keyword.objects.create(
            code='python',
            label='Python Programming'
        )
        assert keyword.code == 'python'
        assert keyword.label == 'Python Programming'
        assert str(keyword) == 'Python Programming'

    def test_keyword_unique_code(self):
        """Test that keyword codes must be unique."""
        Keyword.objects.create(code='test', label='Test Keyword')
        with pytest.raises(IntegrityError):
            Keyword.objects.create(code='test', label='Another Test Keyword')


@pytest.mark.django_db
class TestProjectModel:
    """Test cases for Project model."""

    def test_project_creation(self, profile):
        """Test that a project can be created."""
        project = Project.objects.create(
            title='Test Project',
            description='A test project',
            project_type='research',
            posted_by=profile,
            specialization_needed='cs'
        )
        assert project.title == 'Test Project'
        assert project.posted_by == profile
        assert project.status == 'open'
        assert str(project) == 'Test Project'

    def test_project_keywords_relationship(self, profile, keyword):
        """Test many-to-many relationship with keywords."""
        project = Project.objects.create(
            title='Test Project',
            description='A test project',
            project_type='research',
            posted_by=profile
        )
        project.keywords.add(keyword)
        assert keyword in project.keywords.all()

    def test_project_participants_relationship(self, profile):
        """Test many-to-many relationship with participants."""
        project = Project.objects.create(
            title='Test Project',
            description='A test project',
            project_type='research',
            posted_by=profile
        )

        participant_profile = Profile.objects.create(
            user=User.objects.create_user('participant', 'part@example.com', 'pass'),
            user_type='student'
        )

        participant = ProjectParticipant.objects.create(
            project=project,
            profile=participant_profile,
            role='candidate'
        )

        assert participant_profile in project.participants.all()


@pytest.mark.django_db
class TestMessageModel:
    """Test cases for Message model."""

    def test_message_creation(self, profile):
        """Test that a message can be created."""
        recipient = Profile.objects.create(
            user=User.objects.create_user('recipient', 'rec@example.com', 'pass'),
            user_type='student'
        )

        message = Message.objects.create(
            sender=profile,
            recipient=recipient,
            subject='Test Subject',
            body='Test message body'
        )
        assert message.sender == profile
        assert message.recipient == recipient
        assert message.subject == 'Test Subject'
        assert not message.read
        assert str(message) == f"{profile.user.username} -> {recipient.user.username} [Test Subject]"


@pytest.mark.django_db
class TestDocumentModel:
    """Test cases for Document model."""

    def test_document_creation(self, profile):
        """Test that a document can be created."""
        document = Document.objects.create(
            owner=profile,
            title='Test Document',
            file='test.pdf'
        )
        assert document.owner == profile
        assert document.title == 'Test Document'
        assert str(document) == 'Test Document'
