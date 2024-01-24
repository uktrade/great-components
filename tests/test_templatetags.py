import pytest
from bs4 import BeautifulSoup

from django.core.paginator import Paginator
from django.template import Context, Template

from great_components import forms
from great_components.templatetags import great_components
from great_components.templatetags.great_components import international_header

REQUIRED_MESSAGE = forms.PaddedCharField.default_error_messages['required']


class PaddedTestForm(forms.Form):
    field = forms.PaddedCharField(fillchar='0', max_length=6)


def test_static_absolute(rf):
    template = Template(
        '{% load static_absolute from great_components %}'
        '{% static_absolute "great_components/images/favicon.ico" %}'
    )

    context = Context({'request': rf.get('/')})
    html = template.render(context)

    assert html == (
        'http://testserver/static/great_components/images/favicon.ico'
    )


def test_add_anchors():
    template = Template(
        '{% load add_anchors from great_components %}'
        '{{ html|add_anchors:"-section" }}'
    )

    context = Context({
        'html': '<br/><h2>Title one</h2><h2>Title two</h2><br/>'
    })
    html = template.render(context)

    assert html == (
        '<br/>'
        '<h2 id="title-one-section">Title one</h2>'
        '<h2 id="title-two-section">Title two</h2>'
        '<br/>'
    )


def test_add_anchors_empty():
    template = Template(
        '{% load add_anchors from great_components %}'
        '{{ html|add_anchors:"-section" }}'
    )

    context = Context({
        'html': '<br/>'
                '<h2><b></b></h2>'
                '<h2><b>Some title</b></h2>'
                '<h2></h2>'
                '<br/>'
    })
    html = template.render(context)

    assert html == (
        '<br/>'
        '<h2><b></b></h2>'
        '<h2 id="some-title-section"><b>Some title</b></h2>'
        '<h2></h2>'
        '<br/>'
    )


def test_add_href_target(rf):
    request = rf.get('/')
    request.META['HTTP_HOST'] = 'example.com'
    template = Template(
        '{% load add_href_target from great_components %}'
        '{{ html|add_href_target:request|safe }}'

    )
    context = Context({
        'request': request,
        'html': (
            '<a href="http://www.google.com"></a>'
            '<a href="https://www.google.com"></a>'
            '<a href="http://www.example.com"></a>'
            '<a href="http://example.com/selling-online-overseas"></a>'
            '<a href="http://example.com/export-opportunities"></a>'
            '<a href="/selling-online-overseas"></a>'
            '<a href="/export-opportunities"></a>'
        )
    })
    html = template.render(context)

    assert html == (
        '<a href="http://www.google.com" rel="noopener noreferrer" target="_blank" title="Opens in a new window"></a>'
        '<a href="https://www.google.com" rel="noopener noreferrer" target="_blank" title="Opens in a new window"></a>'
        '<a href="http://www.example.com"></a>'
        '<a href="http://example.com/selling-online-overseas"></a>'
        '<a href="http://example.com/export-opportunities"></a>'
        '<a href="/selling-online-overseas"></a>'
        '<a href="/export-opportunities"></a>'
    )


def test_add_anchors_no_suffix():
    template = Template(
        '{% load add_anchors from great_components %}'
        '{{ html|add_anchors }}'
    )

    context = Context({
        'html': '<br/><h2>Title one</h2><h2>Title two</h2><br/>'
    })
    html = template.render(context)

    assert html == (
        '<br/>'
        '<h2 id="title-one">Title one</h2>'
        '<h2 id="title-two">Title two</h2>'
        '<br/>'
    )


def test_add_anchors_to_all_headings():
    template = Template(
        '{% load add_anchors_to_all_headings from great_components %}'
        '{{ html|add_anchors_to_all_headings:"-section" }}'
    )

    context = Context({
        'html': '<br/>'
                '<h1>Title one</h1>'
                '<h2>Title two</h2>'
                '<h3>Title: with punctuation!</h3>'
                '<br/>'
    })
    html = template.render(context)

    assert html == (
        '<br/>'
        '<h1 id="title-one-section">Title one</h1>'
        '<h2 id="title-two-section">Title two</h2>'
        '<h3 id="title-with-punctuation-section">Title: with punctuation!</h3>'
        '<br/>'
    )


def test_add_anchors_to_all_headings_empty():
    template = Template(
        '{% load add_anchors_to_all_headings from great_components %}'
        '{{ html|add_anchors_to_all_headings:"-section" }}'
    )

    context = Context({
        'html': '<br/>'
                '<h1><b></b></h1>'
                '<h2></h2>'
                '<h3>Title</h3>'
                '<br/>'
    })
    html = template.render(context)

    assert html == (
        '<br/>'
        '<h1><b></b></h1>'
        '<h2></h2>'
        '<h3 id="title-section">Title</h3>'
        '<br/>'
    )


def test_add_anchors_to_all_headings_no_suffix():
    template = Template(
        '{% load add_anchors_to_all_headings from great_components %}'
        '{{ html|add_anchors_to_all_headings }}'
    )

    context = Context({
        'html': '<br/>'
                '<h1>Title one</h1>'
                '<h2>Title two</h2>'
                '<h3>Title: with punctuation!</h3>'
                '<br/>'
    })
    html = template.render(context)

    assert html == (
        '<br/>'
        '<h1 id="title-one">Title one</h1>'
        '<h2 id="title-two">Title two</h2>'
        '<h3 id="title-with-punctuation">Title: with punctuation!</h3>'
        '<br/>'
    )


@pytest.mark.parametrize('input_html,expected_html', (
    ('<h1>content</h1>', '<h1 class="h-xl">content</h1>'),
    ('<h2>content</h2>', '<h2 class="h-l">content</h2>'),
    ('<h3>content</h3>', '<h3 class="h-m">content</h3>'),
    ('<h4>content</h4>', '<h4 class="h-s">content</h4>'),
    ('<ul>content</ul>', '<ul class="list list-bullet">content</ul>'),
    ('<ol>content</ul>', '<ol class="list list-number">content</ol>'),
    ('<p>content</p>', '<p>content</p>'),
    ('<a>content</a>', '<a class="link">content</a>'),
    ('<blockquote>a</blockquote>', '<blockquote class="quote">a</blockquote>')
))
def test_add_export_elements_classes(input_html, expected_html):
    template = Template(
        '{% load add_export_elements_classes from great_components %}'
        '{{ html|add_export_elements_classes }}'

    )
    context = Context({'html': input_html})

    html = template.render(context)
    assert html == expected_html


def test_card():
    card_content = {
        'title': 'title',
        'url': 'url',
        'description': 'description',
        'image': 'image',
        'img_alt': 'img_alt',
    }
    string = (
        "{{% load card from great_components %}}"
        "{{% card title='{title}' url='{url}' description='{description}' "
        "image='{image}' img_alt='{img_alt}' %}}"
        ).format(**card_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)
    soup = BeautifulSoup(html, 'html.parser')

    card_link = soup.select('.g-card-link')[0]
    assert 'url' in card_link['href']

    card_image = soup.select('.g-card-image')[0]
    assert 'image' in card_image['src']
    assert card_image['alt'] == 'img_alt'

    card_heading = soup.select('h3')[0]
    assert card_heading.string == 'title'

    card_description = soup.select('p.description')[0]
    assert card_description.string == 'description'


def test_card_html():
    html_content = '<p>Test</p>'
    card_content = {
        'html_content': html_content,
    }
    string = (
        "{{% load card from great_components %}}"
        "{{% card html_content='{html_content}' %}}"
        ).format(**card_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)

    assert html_content in html


def test_card_with_external_link():
    card_content = {
        'external_link': True,
        'url': 'url',
    }
    string = (
        "{{% load card from great_components %}}"
        "{{% card external_link='{external_link}' url='{url}' %}}"
        ).format(**card_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)
    soup = BeautifulSoup(html, 'html.parser')

    card_link = soup.select('.g-card-link')[0]

    assert card_link['target'] == '_blank'
    assert card_link['rel'] == ['noopener', 'noreferrer']
    assert card_link['title'] == 'Opens in a new window'


def test_card_no_padding_transparent():
    card_content = {
        'title': 'title',
        'url': 'url',
        'no_padding': True,
        'transparent': True
    }
    string = (
        "{{% load card from great_components %}}"
        "{{% card no_padding='{no_padding}' transparent='{transparent}' %}}"
        ).format(**card_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)

    assert 'g-card bg-transparent' in html
    assert 'p-0' in html


def test_message_box_default():
    box_content = {
        'heading': 'heading',
        'description': 'description',
    }
    string = (
        "{{% load message_box from great_components %}}"
        "{{% message_box heading='{heading}' "
        "description='{description}' %}}"
        ).format(**box_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)
    soup = BeautifulSoup(html, 'html.parser')

    box_heading = soup.select('h3.h-m')[0]
    assert box_heading.string == 'heading'

    box_description = soup.select('p.box-description')[0]
    assert box_description.string == 'description'


def test_message_box_custom():
    box_content = {
        'heading': 'heading',
        'heading_level': 'h4',
        'heading_class': 'text-great-red',
        'description': 'description',
        'box_class': 'border-great-red bg-offwhite',
    }
    string = (
        "{{% load message_box from great_components %}}"
        "{{% message_box heading='{heading}' heading_level='{heading_level}' "
        "heading_class='{heading_class}' description='{description}' "
        "box_class='{box_class}' %}}"
        ).format(**box_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)
    soup = BeautifulSoup(html, 'html.parser')

    box_heading = soup.select('h4.text-great-red')[0]
    assert box_heading.string == 'heading'

    box = soup.select('.g-message-box')[0]
    assert 'border-great-red' in box['class']
    assert 'bg-offwhite' in box['class']

    box_description = soup.select('p.box-description')[0]
    assert box_description.string == 'description'


def test_error_box():
    box_content = {
        'heading': 'heading',
        'description': 'description',
    }
    string = (
        "{{% load error_box from great_components %}}"
        "{{% error_box heading='{heading}' "
        "description='{description}' %}}"
        ).format(**box_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)
    soup = BeautifulSoup(html, 'html.parser')

    box_heading = soup.select('h3.text-flag-red')[0]
    assert box_heading.string == 'heading'

    box = soup.select('.g-message-box-with-icon')[0]
    assert 'border-flag-red' in box['class']
    assert 'bg-white' in box['class']

    box_description = soup.select('p.box-description')[0]
    assert box_description.string == 'description'


def test_success_box():
    box_content = {
        'heading': 'heading',
        'description': 'description',
    }
    string = (
        "{{% load success_box from great_components %}}"
        "{{% success_box heading='{heading}' "
        "description='{description}' %}}"
        ).format(**box_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)
    soup = BeautifulSoup(html, 'html.parser')

    box_heading = soup.select('h3.text-teal')[0]
    assert box_heading.string == 'heading'

    box = soup.select('.g-message-box-with-icon')[0]
    assert 'border-teal' in box['class']
    assert 'bg-white' in box['class']

    box_description = soup.select('p.box-description')[0]
    assert box_description.string == 'description'


def test_cta_box_default():
    box_content = {
        'box_id': 'box_id',
        'heading': 'heading',
        'description': 'description',
        'button_text': 'button_text',
        'button_url': 'button_url',
    }
    string = (
        "{{% load cta_box from great_components %}}"
        "{{% cta_box box_id='{box_id}' heading='{heading}' "
        "description='{description}' "
        "button_text='{button_text}' button_url='{button_url}' %}}"
        ).format(**box_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)
    soup = BeautifulSoup(html, 'html.parser')

    box_id = soup.find(id='box_id')
    assert box_id['id'] == 'box_id'

    box_heading = soup.select('h3.h-m')[0]
    assert box_heading.string == 'heading'

    box_description = soup.select('p.box-description')[0]
    assert box_description.string == 'description'

    box_button = soup.select('a.g-button')[0]
    assert box_button.string == 'button_text'
    assert box_button['href'] == 'button_url'


def test_cta_box_custom():
    box_content = {
        'box_id': 'box_id',
        'box_class': 'bg-great-blue text-white',
        'heading': 'heading',
        'heading_level': 'h4',
        'heading_class': 'h-s',
        'description': 'description',
        'button_text': 'button_text',
        'button_url': 'button_url',
    }
    string = (
        "{{% load cta_box from great_components %}}"
        "{{% cta_box box_id='{box_id}' heading='{heading}' "
        "box_class='{box_class}' heading_level='{heading_level}' "
        "heading_class='{heading_class}' description='{description}' "
        "button_text='{button_text}' button_url='{button_url}' %}}"
        ).format(**box_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)
    soup = BeautifulSoup(html, 'html.parser')

    box = soup.select('.g-cta-box')[0]
    assert box['id'] == 'box_id'

    assert 'bg-great-blue' in box['class']
    assert 'text-white' in box['class']

    box_heading = soup.select('h4.h-s')[0]
    assert box_heading.string == 'heading'

    box_description = soup.select('p.box-description')[0]
    assert box_description.string == 'description'

    box_button = soup.select('a.g-button')[0]
    assert box_button.string == 'button_text'
    assert box_button['href'] == 'button_url'
    assert box_button['id'] == 'box_id-button'


def test_hero():
    hero_content = {
        'background_image_url': 'image.png',
        'hero_text': 'hero_text',
        'description': 'description',
    }
    string = (
        "{{% load hero from great_components %}}"
        "{{% hero background_image_url='{background_image_url}' "
        "hero_text='{hero_text}' description='{description}' %}}"
        ).format(**hero_content)

    template = Template(string)
    context = Context({})

    html = template.render(context)
    soup = BeautifulSoup(html, 'html.parser')

    banner = soup.find(id='hero-heading')
    assert 'hero_text' in banner.string
    assert 'h-l' in banner['class']

    assert 'g-hero-title' in html


@pytest.mark.parametrize('template_tag', (
    great_components.cta_box,
    great_components.message_box,
    great_components.message_box_with_icon,
    great_components.hero,
    great_components.card,
    great_components.image_with_caption,
    great_components.cta_card,
    great_components.cta_link,
    great_components.statistics_card_grid,
    great_components.hero_with_cta,
    great_components.case_study,
    great_components.informative_banner,
    great_components.search_page_selected_filters,
    great_components.search_page_expandable_options,
    great_components.feature_list,
    great_components.accordion_list,
))
def test_template_tag_kwargs(template_tag):
    test_kwargs = {
        'foo': 'foo',
        'bar': 'bar',
    }
    actual = template_tag(**test_kwargs)
    assert actual == test_kwargs


@pytest.mark.parametrize('heading', ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
def test_convert_headings_to(heading):
    actual = great_components.convert_headings_to(
        '<' + heading + '></' + heading + '>',
        'figure'
    )
    expected = '<figure></figure>'
    assert actual == expected


def test_convert_headings_to_does_not_convert_non_headings():
    actual = great_components.convert_headings_to(
        '<span></span>', 'figure'
    )
    expected = '<span></span>'
    assert actual == expected


def test_override_elements_css_class():
    actual = great_components.override_elements_css_class(
        '<h2 class="existing-class"></h2>',
        'h2,test-class'
    )
    expected = '<h2 class="test-class"></h2>'
    assert actual == expected


def test_override_elements_css_class_does_not_override_non_targets():
    actual = great_components.override_elements_css_class(
        '<h4 class="existing-class"></h4>',
        'h2,test-class'
    )
    expected = '<h4 class="existing-class"></h4>'
    assert actual == expected


def test_lazyload():
    template = Template(
        '{% load lazyload from great_components %}'
        '{% lazyload %}'
        '<img class="foo" src="/bar"/>'
        '{% endlazyload %}'
    )

    rendered_html = template.render(Context())

    expected_html = (
        '<img class="foo" src="/bar"/>'
    )
    assert rendered_html.replace('\n', '') == expected_html


def test_lazyload_no_img_class():
    template = Template(
        '{% load lazyload from great_components %}'
        '{% lazyload %}'
        '<img src="/bar"/>'
        '{% endlazyload %}'
    )

    rendered_html = template.render(Context())

    expected_html = (
        '<img src="/bar"/>'
    )
    assert rendered_html.replace('\n', '') == expected_html


def test_lazyload_no_img_src():
    template = Template(
        '{% load lazyload from great_components %}'
        '{% lazyload %}'
        '<img class="foo"/>'
        '{% endlazyload %}'
    )

    rendered_html = template.render(Context())

    expected_html = (
        '<img class="foo"/>'
    )
    assert rendered_html.replace('\n', '') == expected_html


def test_lazyload_context_variables():
    template = Template(
        '{% load lazyload from great_components %}'
        '{% lazyload %}'
        '<img class="{{ foo.class }}" src="{{ foo.src }}"/>'
        '{% endlazyload %}'
    )

    context = {
        'foo': {'class': 'foo-class', 'src': '/foo'}
    }

    rendered_html = template.render(Context(context))

    expected_html = (
        '<img class="foo-class" src="/foo"/>'
    )
    assert rendered_html.replace('\n', '') == expected_html


def test_breadcrumbs():
    template = Template(
        '{% load breadcrumbs from great_components %}'
        '{% breadcrumbs "Current Page" %}'
        '<a href="/foo"></a>'
        '<a href="/bar"></a>'
        '<a href="/baz"></a>'
        '{% endbreadcrumbs %}'
    )

    rendered_html = template.render(Context())

    expected_html = (
        '<nav aria-label="Breadcrumb" class="g-breadcrumbs">'
        '<ol>'
        '<li><a href="/foo"></a></li>'
        '<li><a href="/bar"></a></li>'
        '<li><a href="/baz"></a></li>'
        '</ol>'
        '</nav>'
    )
    assert rendered_html.replace('\n', '') == expected_html


def test_breadcrumbs_context_variables():
    template = Template(
        '{% load breadcrumbs from great_components %}'
        '{% breadcrumbs "Current Page" %}'
        '<a href="{{ foo.url }}">{{ foo.title }}</a>'
        '<a href="{{ bar.url }}">{{ bar.title }}</a>'
        '<a href="{{ baz.url }}">{{ baz.title }}</a>'
        '{% endbreadcrumbs %}'
    )

    context = {
        'foo': {'title': 'Foo', 'url': '/foo'},
        'bar': {'title': 'Bar', 'url': '/bar'},
        'baz': {'title': 'Baz', 'url': '/baz'},
    }

    rendered_html = template.render(Context(context))

    expected_html = (
        '<nav aria-label="Breadcrumb" class="g-breadcrumbs">'
        '<ol>'
        '<li><a href="/foo">Foo</a></li>'
        '<li><a href="/bar">Bar</a></li>'
        '<li><a href="/baz">Baz</a></li>'
        '</ol>'
        '</nav>'
    )
    assert rendered_html.replace('\n', '') == expected_html


def test_breadcrumbs_empty_href():
    template = Template(
        '{% load breadcrumbs from great_components %}'
        '{% breadcrumbs "Current Page" %}'
        '<a href=""></a>'
        '{% endbreadcrumbs %}'
    )
    with pytest.raises(ValueError):
        template.render(Context())


def test_breadcrumbs_missing_href():
    template = Template(
        '{% load breadcrumbs from great_components %}'
        '{% breadcrumbs "Current Page" %}'
        '<a></a>'
        '{% endbreadcrumbs %}'
    )
    with pytest.raises(ValueError):
        template.render(Context())


def test_breadcrumbs_missing_links():
    template = Template(
        '{% load breadcrumbs from great_components %}'
        '{% breadcrumbs "Current Page" %}'
        '{% endbreadcrumbs %}'
    )
    with pytest.raises(ValueError):
        template.render(Context())


def test_breadcrumbs_missing_current_page():
    with pytest.raises(ValueError):
        Template(
            '{% load breadcrumbs from great_components %}'
            '{% breadcrumbs %}'
            '<a href="/foo"></a>'
            '{% endbreadcrumbs %}'
        )


def test_ga360_data_with_no_optional_parameters():
    template = Template(
        '{% load ga360_data from great_components %}'
        '{% ga360_data "a" %}'
        '<div>'
        '    <a href="example.com">Click Me</a>'
        '</div>'
        '{% end_ga360_data %}'
    )

    rendered_html = template.render(Context())

    expected_html = \
        '<div>' \
        ' <a href="example.com">Click Me</a>' \
        '</div>'
    assert rendered_html == expected_html


def test_ga360_data_with_all_optional_parameters():
    template = Template(
        '{% load ga360_data from great_components %}'
        '{% ga360_data "a" action="link" type="CTA" element="pageSection" value="Click Me" include_form_data="True" %}'  # noqa
        '<div>'
        '    <a href="example.com">Click Me</a>'
        '</div>'
        '{% end_ga360_data %}'
    )

    rendered_html = template.render(Context())

    expected_html = \
        '<div>' \
        ' <a data-ga-action="link" data-ga-element="pageSection" ' \
        'data-ga-include-form-data="True" ' \
        'data-ga-type="CTA" data-ga-value="Click Me" ' \
        'href="example.com">Click Me</a>' \
        '</div>'
    assert rendered_html == expected_html


@pytest.mark.parametrize('count,current,expected', (
    (21, 1, '[1] 2 3 4 5 N'),
    (21, 2, 'P 1 [2] 3 4 5 N'),
    (21, 3, 'P 1 2 [3] 4 5 N'),
    (21, 4, 'P 1 2 3 [4] 5 N'),
    (21, 5, 'P 1 2 3 4 [5]'),
    (30, 1, '[1] 2 3 4 5 6 N'),
    (40, 1, '[1] 2 3 4 ... 8 N'),
    (40, 2, 'P 1 [2] 3 4 ... 8 N'),
    (40, 3, 'P 1 2 [3] 4 ... 8 N'),
    (40, 4, 'P 1 2 3 [4] ... 8 N'),
    (40, 5, 'P 1 ... [5] 6 7 8 N'),
    (40, 6, 'P 1 ... 5 [6] 7 8 N'),
    (40, 7, 'P 1 ... 5 6 [7] 8 N'),
    (40, 8, 'P 1 ... 5 6 7 [8]'),
    (60, 1, '[1] 2 3 4 ... 12 N'),
    (60, 2, 'P 1 [2] 3 4 ... 12 N'),
    (60, 3, 'P 1 2 [3] 4 ... 12 N'),
    (60, 4, 'P 1 2 3 [4] ... 12 N'),
    (60, 5, 'P 1 ... 4 [5] 6 ... 12 N'),
    (60, 6, 'P 1 ... 5 [6] 7 ... 12 N'),
    (60, 7, 'P 1 ... 6 [7] 8 ... 12 N'),
    (60, 8, 'P 1 ... 7 [8] 9 ... 12 N'),
    (60, 9, 'P 1 ... [9] 10 11 12 N'),
    (60, 10, 'P 1 ... 9 [10] 11 12 N'),
    (60, 11, 'P 1 ... 9 10 [11] 12 N'),
    (60, 12, 'P 1 ... 9 10 11 [12]'),
))
def test_pagination(count, current, expected, rf):
    template = Template(
        '{% load pagination from great_components %}'
        '{% pagination pagination_page=pagination_page %}'
    )

    page_size = 5
    objects = [item for item in range(count)]

    paginator = Paginator(objects, page_size)
    pagination_page = paginator.page(current)
    context = {
        'request': rf.get('/'),
        'pagination_page': pagination_page
    }

    html = template.render(Context(context))

    soup = BeautifulSoup(html, 'html.parser')

    items = []
    if soup.findAll('a', {'class': 'g-pagination-previous'}):
        items.append('P')
    for element in soup.find_all('li'):
        if element.find('span'):
            items.append('...')
        else:
            button = element.find('a')
            if 'g-button' in button['class']:
                items.append(f'[{button.string}]')
            else:
                items.append(button.string)
    if soup.findAll('a', {'class': 'g-pagination-next'}):
        items.append('N')
    assert ' '.join(items) == expected


class NavNode:
    def __init__(self, tier_one_item, tier_two_items):
        self.tier_one_item = tier_one_item
        self.tier_two_items = tier_two_items


class NavItem:
    def __init__(self, title, name):
        self.title = title
        self.name = name
        self.url = "/{0}/".format(name)


SAMPLE_NAVIGATION_TREE = [
    NavNode(
        tier_one_item=NavItem('Root 1', 'root-1'),
        tier_two_items=[
            NavItem('Sub Page 1', 'sub-page-1'),
        ]
    ),
    NavNode(
        tier_one_item=NavItem('Root 2', 'root-2'),
        tier_two_items=[]
    ),
]


@pytest.mark.parametrize('section,subsection', [
    ('', ''),
    ('incorrect-section', ''),
    ('', 'incorrect-subsection'),
    ('', 'sub-page-one'),
])
def test_international_header_no_active_sections(section, subsection):
    navigation = international_header(Context({}), SAMPLE_NAVIGATION_TREE, '', '')

    assert len(navigation['tier_one_items']) == 2
    assert navigation['tier_one_items'][0].title == 'Root 1'
    assert navigation['tier_one_items'][0].is_active is False
    assert navigation['tier_one_items'][1].title == 'Root 2'
    assert navigation['tier_one_items'][1].is_active is False

    assert len(navigation['tier_two_items']) == 0

    assert navigation['navigation_tree'] == SAMPLE_NAVIGATION_TREE


def test_international_header_active_section():
    navigation = international_header(Context({}), SAMPLE_NAVIGATION_TREE, 'root-1', '')

    assert len(navigation['tier_one_items']) == 2
    assert navigation['tier_one_items'][0].is_active is True
    assert navigation['tier_one_items'][1].is_active is False

    assert len(navigation['tier_two_items']) == 1
    assert navigation['tier_two_items'][0].title == 'Sub Page 1'
    assert not navigation['tier_two_items'][0].is_active


def test_international_header_active_section_and_subsection():
    navigation = international_header(Context({}), SAMPLE_NAVIGATION_TREE, 'root-1', 'sub-page-1')

    assert len(navigation['tier_one_items']) == 2
    assert navigation['tier_one_items'][0].is_active is True
    assert navigation['tier_one_items'][1].is_active is False

    assert len(navigation['tier_two_items']) == 1
    assert navigation['tier_two_items'][0].title == 'Sub Page 1'
    assert navigation['tier_two_items'][0].is_active


def test_international_header_tag():
    template = Template(
        '{% load international_header from great_components %}'
        '{% international_header navigation_tree=tree site_section=section site_sub_section=sub_section %}'
    )
    context = {
        'tree': SAMPLE_NAVIGATION_TREE,
        'section': '',
        'sub_section': '',
    }

    html = template.render(Context(context))

    soup = BeautifulSoup(html, 'html.parser')
    assert soup.find('a', {'href': '/root-1/'}) is not None


def test_invest_header_tag():
    template = Template(
        '{% load invest_header from great_components %}'
        '{% invest_header navigation_tree=tree site_section=section site_sub_section=sub_section %}'
    )
    context = {
        'tree': SAMPLE_NAVIGATION_TREE,
        'section': '',
        'sub_section': '',
    }

    html = template.render(Context(context))

    soup = BeautifulSoup(html, 'html.parser')
    assert soup.find('a', {'href': '/root-1/'}) is not None
