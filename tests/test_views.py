import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Profile


@pytest.mark.django_db
class TestAuthenticationViews:
    """Test cases for authentication views."""

    def test_register_view_get(self, client):
        """Test that register page loads."""
        response = client.get(reverse('register'))
        assert response.status_code == 200
        assert 'Register - KBTuneco' in str(response.content)

    def test_login_view_get(self, client):
        """Test that login page loads."""
        response = client.get(reverse('login'))
        assert response.status_code == 200

    def test_logout_view(self, authenticated_client):
        """Test logout functionality."""
        response = authenticated_client.post(reverse('logout'))
        assert response.status_code == 302  # Redirect after logout


@pytest.mark.django_db
class TestProfileViews:
    """Test cases for profile views."""

    def test_profile_view_authenticated(self, authenticated_client, profile):
        """Test that authenticated user can view their profile."""
        response = authenticated_client.get(reverse('profile'))
        assert response.status_code == 200
        assert profile.user.username in str(response.content)

    def test_profile_view_unauthenticated(self, client):
        """Test that unauthenticated user is redirected."""
        response = client.get(reverse('profile'))
        assert response.status_code == 302  # Redirect to login

    def test_profile_edit_view_get(self, authenticated_client, profile):
        """Test that profile edit page loads."""
        response = authenticated_client.get(reverse('profile_edit'))
        assert response.status_code == 200
        assert 'Edit Your Profile' in str(response.content)

    def test_profile_edit_view_post(self, authenticated_client, profile):
        """Test profile editing functionality."""
        data = {
            'user_type': 'researcher',
            'specialization': 'ai',
            'bio': 'Updated bio',
            'contact_email': 'new@example.com',
            'phone': '+1234567890'
        }
        response = authenticated_client.post(reverse('profile_edit'), data)
        assert response.status_code == 302  # Redirect after successful edit

        # Refresh profile from database
        profile.refresh_from_db()
        assert profile.user_type == 'researcher'
        assert profile.specialization == 'ai'
        assert profile.bio == 'Updated bio'


@pytest.mark.django_db
class TestProjectViews:
    """Test cases for project views."""

    def test_project_list_view(self, client):
        """Test that project list page loads."""
        response = client.get(reverse('project_list'))
        assert response.status_code == 200

    def test_project_create_view_unauthenticated(self, client):
        """Test that unauthenticated users are redirected from project creation."""
        response = client.get(reverse('project_create'))
        assert response.status_code == 302

    def test_project_create_view_student(self, authenticated_client, profile):
        """Test that students cannot create projects."""
        profile.user_type = 'student'
        profile.save()

        response = authenticated_client.get(reverse('project_create'))
        assert response.status_code == 200
        assert 'cannot create projects' in str(response.content).lower()


@pytest.mark.django_db
class TestDashboardViews:
    """Test cases for dashboard views."""

    def test_dashboard_view_authenticated(self, authenticated_client):
        """Test that authenticated user can access dashboard."""
        response = authenticated_client.get(reverse('dashboard'))
        assert response.status_code == 200

    def test_dashboard_view_unauthenticated(self, client):
        """Test that unauthenticated user is redirected from dashboard."""
        response = client.get(reverse('dashboard'))
        assert response.status_code == 302


@pytest.mark.django_db
class TestMessageViews:
    """Test cases for message views."""

    def test_inbox_view_authenticated(self, authenticated_client):
        """Test that authenticated user can access inbox."""
        response = authenticated_client.get(reverse('inbox'))
        assert response.status_code == 200

    def test_inbox_view_unauthenticated(self, client):
        """Test that unauthenticated user is redirected from inbox."""
        response = client.get(reverse('inbox'))
        assert response.status_code == 302


@pytest.mark.django_db
class TestEventViews:
    """Test cases for event views."""

    def test_events_list_view(self, client):
        """Test that events list page loads."""
        response = client.get(reverse('events_list'))
        assert response.status_code == 200
        assert 'Events' in str(response.content)
