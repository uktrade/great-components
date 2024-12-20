from unittest.mock import Mock, patch, MagicMock

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.utils import translation
from django.views.generic import TemplateView
from great_components import mixins
from unittest.mock import ANY


def test_language_display_mixin(rf, settings):
    class TestView(mixins.EnableTranslationsMixin, TemplateView):
        template_name = 'great_components/base.html'

    # Test with usual settings first
    request = rf.get('/')
    request.LANGUAGE_CODE = ''
    response = TestView.as_view()(request)
    assert response.context_data['language_switcher']['form']

    # Test when MIDDLWARE_CLASSES setting is being used instead of MIDDLEWARE
    settings.MIDDLEWARE_CLASSES = settings.MIDDLEWARE
    settings.MIDDLEWARE = []

    request = rf.get('/')
    request.LANGUAGE_CODE = ''
    response = TestView.as_view()(request)
    assert response.context_data['language_switcher']['form']


def test_cms_language_switcher_one_language(rf):
    class MyView(mixins.CMSLanguageSwitcherMixin, TemplateView):

        template_name = 'great_components/base.html'
        page = {
            'meta': {'languages': [('en-gb', 'English')]}
        }

    request = rf.get('/')
    request.LANGUAGE_CODE = ''
    with translation.override('de'):
        response = MyView.as_view()(request)

    assert response.status_code == 200
    assert response.context_data['language_switcher']['show'] is False


def test_cms_language_switcher_active_language_unavailable(rf):

    class MyView(mixins.CMSLanguageSwitcherMixin, TemplateView):

        template_name = 'great_components/base.html'

        page = {
            'meta': {
                'languages': [('en-gb', 'English'), ('de', 'German')]
            }
        }

    request = rf.get('/')
    request.LANGUAGE_CODE = 'fr'

    response = MyView.as_view()(request)

    assert response.status_code == 200
    assert response.context_data['language_switcher']['show'] is False


def test_cms_language_switcher_active_language_available(rf):

    class MyView(mixins.CMSLanguageSwitcherMixin, TemplateView):

        template_name = 'great_components/base.html'

        page = {
            'meta': {
                'languages': [('en-gb', 'English'), ('de', 'German')]
            }
        }

    request = rf.get('/')
    request.LANGUAGE_CODE = 'de'

    response = MyView.as_view()(request)

    assert response.status_code == 200
    context = response.context_data['language_switcher']
    assert context['show'] is True
    assert context['form'].initial['lang'] == 'de'


@patch('great_components.mixins.requests.post')
def test_ga360_mixin_for_logged_in_user_old_style(mock_post, rf):
    settings.GA4_API_URL = 'http://test'
    settings.GA4_API_SECRET = 'secret'
    settings.GA4_MEASUREMENT_ID = '12345'
    mock_post.return_value = MagicMock(status_code=200, json=lambda: {'success': True})

    class TestView(mixins.GA360Mixin, TemplateView):
        template_name = 'great_components/base.html'

        def __init__(self):
            super().__init__()
            self.set_ga360_payload(
                page_id='TestPageId',
                business_unit='Test App',
                site_section='Test Section',
                site_subsection='Test Page',
                referer_url='http://anyurl.com'
            )

    request = rf.get('/')
    request.sso_user = Mock(
        hashed_uuid='a9a8f733-6bbb-4dca-a682-e8a0a18439e9',
        spec_set=['hashed_uuid', 'is_superuser'],
        is_superuser=False,
    )

    with translation.override('de'):
        response = TestView.as_view()(request)

    assert response.context_data['ga360']
    ga360_data = response.context_data['ga360']
    assert ga360_data['page_id'] == 'TestPageId'
    assert ga360_data['business_unit'] == 'Test App'
    assert ga360_data['site_section'] == 'Test Section'
    assert ga360_data['site_subsection'] == 'Test Page'
    assert ga360_data['referer_url'] == 'http://anyurl.com'
    assert ga360_data['user_id'] == 'a9a8f733-6bbb-4dca-a682-e8a0a18439e9'
    assert ga360_data['login_status'] is True
    assert ga360_data['site_language'] == 'de'
    mock_post.assert_called_with(
        'http://test',
        params={
                'api_secret': 'secret',
                'measurement_id': '12345',
            },
        json={
                'client_id': ANY,
                'events': [{
                    'name': 'page_view',
                    'params': {
                        'page_id': 'TestPageId',
                        'business_unit': 'Test App',
                        'site_section': 'Test Section',
                        'site_subsection': 'Test Page',
                        'site_language': 'de',

                    }
                }],
            },
    )


@patch('great_components.mixins.requests.post')
def test_ga360_mixin_for_logged_in_user(mock_post, rf):
    settings.GA4_API_URL = 'http://test'
    settings.GA4_API_SECRET = 'secret'
    settings.GA4_MEASUREMENT_ID = '12345'
    mock_post.return_value = MagicMock(status_code=200, json=lambda: {'success': True})

    class TestView(mixins.GA360Mixin, TemplateView):
        template_name = 'great_components/base.html'

        def __init__(self):
            super().__init__()
            self.set_ga360_payload(
                page_id='TestPageId',
                business_unit='Test App',
                site_section='Test Section',
                site_subsection='Test Page',
                referer_url='http://anyurl.com'
            )

    request = rf.get('/')
    request.user = Mock(
        id=1,
        hashed_uuid='a9a8f733-6bbb-4dca-a682-e8a0a18439e9',
        is_authenticated=True,
        is_superuser=False,
    )

    with translation.override('de'):
        response = TestView.as_view()(request)

    assert response.context_data['ga360']
    ga360_data = response.context_data['ga360']
    assert ga360_data['page_id'] == 'TestPageId'
    assert ga360_data['business_unit'] == 'Test App'
    assert ga360_data['site_section'] == 'Test Section'
    assert ga360_data['site_subsection'] == 'Test Page'
    assert ga360_data['referer_url'] == 'http://anyurl.com'
    assert ga360_data['user_id'] == 'a9a8f733-6bbb-4dca-a682-e8a0a18439e9'
    assert ga360_data['login_status'] is True
    assert ga360_data['site_language'] == 'de'
    mock_post.assert_called_with(
        'http://test',
        params={
                'api_secret': 'secret',
                'measurement_id': '12345',
            },
        json={
                'client_id': ANY,
                'events': [{
                    'name': 'page_view',
                    'params': {
                        'page_id': 'TestPageId',
                        'business_unit': 'Test App',
                        'site_section': 'Test Section',
                        'site_subsection': 'Test Page',
                        'site_language': 'de',

                    }
                }],
            },
    )


@patch('great_components.mixins.requests.post')
def test_ga360_mixin_for_admin_user_old_style(mock_post, rf):
    settings.GA4_API_URL = 'http://test'
    settings.GA4_API_SECRET = 'secret'
    settings.GA4_MEASUREMENT_ID = '12345'
    mock_post.return_value = MagicMock(status_code=200, json=lambda: {'success': True})

    class TestView(mixins.GA360Mixin, TemplateView):
        template_name = 'great_components/base.html'

        def __init__(self):
            super().__init__()
            self.set_ga360_payload(
                page_id='TestPageId',
                business_unit='Test App',
                site_section='Test Section',
                site_subsection='Test Page',
                referer_url='http://anyurl.com'
            )

    request = rf.get('/')
    request.user = Mock(
        id=1,
        is_authenticated=True,
        is_superuser=True
    )

    with translation.override('de'):
        response = TestView.as_view()(request)

    assert response.context_data['ga360']
    ga360_data = response.context_data['ga360']
    assert ga360_data['user_id'] is None
    assert ga360_data['login_status'] is True
    mock_post.assert_called_with(
        'http://test',
        params={
                'api_secret': 'secret',
                'measurement_id': '12345',
            },
        json={
                'client_id': ANY,
                'events': [{
                    'name': 'page_view',
                    'params': {
                        'page_id': 'TestPageId',
                        'business_unit': 'Test App',
                        'site_section': 'Test Section',
                        'site_subsection': 'Test Page',
                        'site_language': 'de',

                    }
                }],
            },
    )


@patch('great_components.mixins.requests.post')
def test_ga360_mixin_for_anonymous_user_old_style(mock_post, rf):
    settings.GA4_API_URL = 'http://test'
    settings.GA4_API_SECRET = 'secret'
    settings.GA4_MEASUREMENT_ID = '12345'
    mock_post.return_value = MagicMock(status_code=200, json=lambda: {'success': True})

    class TestView(mixins.GA360Mixin, TemplateView):
        template_name = 'great_components/base.html'

        def __init__(self):
            super().__init__()
            self.set_ga360_payload(
                page_id='TestPageId',
                business_unit='Test App',
                site_section='Test Section',
                site_subsection='Test Page',
                referer_url='http://anyurl.com'
            )

    request = rf.get('/')
    request.sso_user = None

    with translation.override('de'):
        response = TestView.as_view()(request)

    assert response.context_data['ga360']
    ga360_data = response.context_data['ga360']
    assert ga360_data['user_id'] is None
    assert ga360_data['login_status'] is False
    mock_post.assert_called_with(
        'http://test',
        params={
                'api_secret': 'secret',
                'measurement_id': '12345',
            },
        json={
                'client_id': ANY,
                'events': [{
                    'name': 'page_view',
                    'params': {
                        'page_id': 'TestPageId',
                        'business_unit': 'Test App',
                        'site_section': 'Test Section',
                        'site_subsection': 'Test Page',
                        'site_language': 'de',

                    }
                }],
            },
    )


@patch('great_components.mixins.requests.post')
def test_ga360_mixin_for_anonymous_user(mock_post, rf):
    settings.GA4_API_URL = 'http://test'
    settings.GA4_API_SECRET = 'secret'
    settings.GA4_MEASUREMENT_ID = '12345'
    mock_post.return_value = MagicMock(status_code=200, json=lambda: {'success': True})

    class TestView(mixins.GA360Mixin, TemplateView):
        template_name = 'great_components/base.html'

        def __init__(self):
            super().__init__()
            self.set_ga360_payload(
                page_id='TestPageId',
                business_unit='Test App',
                site_section='Test Section',
                site_subsection='Test Page',
                referer_url='http://anyurl.com'
            )

    request = rf.get('/')
    request.user = AnonymousUser()

    with translation.override('de'):
        response = TestView.as_view()(request)

    assert response.context_data['ga360']
    ga360_data = response.context_data['ga360']
    assert ga360_data['user_id'] is None
    assert ga360_data['login_status'] is False
    mock_post.assert_called_with(
        'http://test',
        params={
                'api_secret': 'secret',
                'measurement_id': '12345',
            },
        json={
                'client_id': ANY,
                'events': [{
                    'name': 'page_view',
                    'params': {
                        'page_id': 'TestPageId',
                        'business_unit': 'Test App',
                        'site_section': 'Test Section',
                        'site_subsection': 'Test Page',
                        'site_language': 'de',

                    }
                }],
            },
    )


def test_ga360_mixin_does_not_share_data_between_instances():
    class TestView(mixins.GA360Mixin):
        pass

    view_one = TestView()
    view_one.ga360_payload['Test Key'] = "Test Value"

    view_two = TestView()

    assert 'Test Key' not in view_two.ga360_payload
