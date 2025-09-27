import factory
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory
from faker import Faker
from core.models import Profile, Organization, Keyword, Project, Message, Document, Event

fake = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True


class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Faker('company')
    org_type = factory.Iterator(['university', 'public_research', 'association', 'tech_center', 'technopole'])
    description = factory.Faker('text', max_nb_chars=200)
    contact_email = factory.Faker('email')
    website = factory.Faker('url')


class KeywordFactory(DjangoModelFactory):
    class Meta:
        model = Keyword

    code = factory.Sequence(lambda n: f'keyword{n}')
    label = factory.Faker('word')


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    user_type = factory.Iterator(['student', 'researcher', 'university', 'company', 'association', 'medical'])
    specialization = factory.Iterator(['aero', 'agri', 'ai', 'bio', 'chem', 'cs', 'mech', 'other'])
    bio = factory.Faker('text', max_nb_chars=500)
    contact_email = factory.Faker('email')
    phone = factory.Faker('phone_number')


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    title = factory.Faker('sentence', nb_words=6)
    description = factory.Faker('text', max_nb_chars=1000)
    project_type = factory.Iterator(['mission', 'research', 'engineering', 'pfe'])
    posted_by = factory.SubFactory(ProfileFactory)
    specialization_needed = factory.Iterator(['aero', 'agri', 'ai', 'bio', 'chem', 'cs', 'mech', 'other'])
    status = 'open'
    budget = factory.Faker('random_int', min=1000, max=50000)


class MessageFactory(DjangoModelFactory):
    class Meta:
        model = Message

    sender = factory.SubFactory(ProfileFactory)
    recipient = factory.SubFactory(ProfileFactory)
    subject = factory.Faker('sentence', nb_words=4)
    body = factory.Faker('text', max_nb_chars=500)


class DocumentFactory(DjangoModelFactory):
    class Meta:
        model = Document

    owner = factory.SubFactory(ProfileFactory)
    title = factory.Faker('sentence', nb_words=3)
    file = factory.django.FileField(filename='test.pdf')


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event

    title = factory.Faker('sentence', nb_words=5)
    description = factory.Faker('text', max_nb_chars=300)
    organizer = factory.SubFactory(OrganizationFactory)
    location = factory.Faker('city')
    capacity = factory.Faker('random_int', min=10, max=200)
