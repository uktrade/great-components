from directory_constants import urls
from bs4 import BeautifulSoup
import pytest

from django.template.loader import render_to_string

from great_components import context_processors, forms, helpers


def test_google_tag_manager_project_id():
    context = {
        'great_components_analytics': {
            'GOOGLE_TAG_MANAGER_ID': '123456',
        }
    }
    head_html = render_to_string(
        'great_components/google_tag_manager_head.html', context
    )
    body_html = render_to_string(
        'great_components/google_tag_manager_body.html', context
    )

    assert '123456' in head_html
    assert 'https://www.googletagmanager.com/ns.html?id=123456' in body_html


def test_google_tag_manager():
    expected_head = render_to_string(
        'great_components/google_tag_manager_head.html', {}
    )
    expected_body = render_to_string(
        'great_components/google_tag_manager_body.html', {}
    )

    html = render_to_string('great_components/base.html', {'services_urls': {'feedback': None}})

    assert expected_head in html
    assert expected_body in html
    # sanity check
    assert 'www.googletagmanager.com' in expected_head
    assert 'www.googletagmanager.com' in expected_body


def test_google_tag_manager_env():

    context = {
        'great_components_analytics': {
            'GOOGLE_TAG_MANAGER_ID': '123456',
            'GOOGLE_TAG_MANAGER_ENV': '&gtm_auth=hello'
        }
    }
    head_html = render_to_string(
        'great_components/google_tag_manager_head.html', context
    )
    body_html = render_to_string(
        'great_components/google_tag_manager_body.html', context
    )

    assert '&gtm_auth=hello' in head_html
    assert '&gtm_auth=hello' in body_html


def test_base_page_links(settings):
    context = context_processors.urls_processor(None)
    html = render_to_string('great_components/base.html', context)

    assert urls.domestic.FEEDBACK in html


def test_404_links(settings):
    """Test 404 page has links to home and contact-us."""
    context = context_processors.urls_processor(None)
    html = render_to_string('404.html', context)

    assert urls.domestic.HOME in html
    assert urls.domestic.CONTACT_US in html


def test_404_content(settings):
    """Test 404 page has correct content."""
    context = context_processors.urls_processor(None)
    html = render_to_string('404.html', context)

    assert 'If you entered a web address please check it’s correct.' in html


def test_404_title_exists(settings):
    context = context_processors.urls_processor(None)
    html = render_to_string('404.html', context)
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string
    assert len(title) > 0


def test_social_share_links():
    social_links_builder = helpers.SocialLinkBuilder(
        url='https://testserver/',
        page_title='Do research first',
        app_title='Export Readiness',
    )
    template_name = 'great_components/social_share_links.html'
    context = {
        'social_links': social_links_builder.links
    }
    html = render_to_string(template_name, context)

    for url in social_links_builder.links.values():
        assert url in html


@pytest.mark.parametrize('title,expected', (
    ('Custom title', 'Custom title'),
    (None, 'Share'),
    ('', 'Share')
))
def test_social_share_title(title, expected):
    template_name = 'great_components/social_share_links.html'
    context = {
        'title': title
    }
    html = render_to_string(template_name, context)

    assert '<span class="visually-hidden">{title}</span>'.format(
        title=expected) in html


def test_robots_site_indexing():
    assert render_to_string('robots.txt', {})


def test_form_field_container():

    class Form(forms.Form):
        field = forms.CharField()

    form = Form()

    template_name = 'great_components/form_widgets/form_field.html'
    context = {
        'field': form['field']
    }
    html = render_to_string(template_name, context)

    assert 'id="id_field-container' in html


def test_image_with_caption_displays_caption():
    template_name = 'great_components/image_with_caption.html'
    context = {
            'main_caption': 'Hello'
        }

    html = render_to_string(template_name, context)

    assert 'figcaption class="caption"' in html
    assert 'class="main-caption"' in html


def test_image_with_caption_does_not_have_caption_without_caption_text():
    template_name = 'great_components/image_with_caption.html'
    context = {
            'main_caption': None
        }

    html = render_to_string(template_name, context)

    assert 'figcaption class="caption"' not in html
    assert 'class="main-caption"' not in html
