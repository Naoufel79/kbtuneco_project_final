import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.test.client import Client
from core.models import Profile, Organization, Keyword, Project


@pytest.fixture
def rf():
    """RequestFactory fixture for testing views."""
    return RequestFactory()


@pytest.fixture
def client():
    """Django test client fixture."""
    return Client()


@pytest.fixture
def user():
    """Create a test user."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def profile(user):
    """Create a test profile."""
    return Profile.objects.create(
        user=user,
        user_type='student',
        specialization='cs'
    )


@pytest.fixture
def organization():
    """Create a test organization."""
    return Organization.objects.create(
        name='Test University',
        org_type='university',
        description='A test university'
    )


@pytest.fixture
def keyword():
    """Create a test keyword."""
    return Keyword.objects.create(
        code='python',
        label='Python Programming'
    )


@pytest.fixture
def project(profile, keyword):
    """Create a test project."""
    project = Project.objects.create(
        title='Test Project',
        description='A test project description',
        project_type='research',
        posted_by=profile,
        specialization='cs'
    )
    project.keywords.add(keyword)
    return project


@pytest.fixture
def authenticated_client(client, user):
    """Create an authenticated test client."""
    client.login(username='testuser', password='testpass123')
    return client
