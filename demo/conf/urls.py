from django.urls import re_path

from demo import views

urlpatterns = [
    re_path(
        r'^$',
        views.IndexPageView.as_view(),
        {'template_name': 'demo/index.html'},
        name='index',
    ),

    # PAGES
    re_path(
        r'^pages/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/pages/index.html',
            'site_section': 'pages',
        },
        name='pages',
    ),
    re_path(
        r'^pages/404/$',
        views.BasePageView.as_view(),
        {
            'template_name': '404.html',
            'site_section': 'pages',
            'site_subsection': '404',
        },
        name='404',
    ),
    re_path(
        r'^pages/500/$',
        views.BasePageView.as_view(),
        {
            'template_name': '500.html',
            'site_section': 'pages',
            'site_subsection': '500',
        },
        name='500',
    ),

    # FORMS
    re_path(
        r'^forms/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/forms/index.html',
            'site_section': 'forms',
        },
        name='forms',
    ),
    re_path(
        r'^forms/widgets/$',
        views.DemoFormView.as_view(),
        {
            'template_name': 'demo/forms/widgets.html',
            'site_section': 'forms',
            'site_subsection': 'widgets',
        },
        name='widgets',
    ),
    re_path(
        r'^forms/errors/$',
        views.DemoFormErrorsView.as_view(),
        {
            'template_name': 'demo/forms/errors.html',
            'site_section': 'forms',
            'site_subsection': 'errors',
        },
        name='errors',
    ),

    # ATOMS
    re_path(
        r'^atoms/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/atoms/index.html',
            'site_section': 'atoms',
        },
        name='atoms',
    ),
    re_path(
        r'^atoms/typography/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/atoms/typography.html',
            'site_section': 'atoms',
            'site_subsection': 'typography',
        },
        name='typography',
    ),
    re_path(
        r'^atoms/list/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/atoms/list.html',
            'site_section': 'atoms',
            'site_subsection': 'list',
        },
        name='list',
    ),
    re_path(
        r'^atoms/table/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/atoms/table.html',
            'site_section': 'atoms',
            'site_subsection': 'table',
        },
        name='table',
    ),
    re_path(
        r'^atoms/colour/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/atoms/colour.html',
            'site_section': 'atoms',
            'site_subsection': 'colour',
        },
        name='colour',
    ),
    re_path(
        r'^atoms/grid/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/atoms/grid.html',
            'site_section': 'atoms',
            'site_subsection': 'grid',
        },
        name='grid',
    ),
    re_path(
        r'^atoms/spacing/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/atoms/spacing.html',
            'site_section': 'atoms',
            'site_subsection': 'spacing',
        },
        name='spacing',
    ),
    re_path(
        r'^atoms/responsive/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/atoms/responsive.html',
            'site_section': 'atoms',
            'site_subsection': 'responsive',
        },
        name='responsive',
    ),
    re_path(
        r'^atoms/visually-hidden/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/atoms/visually-hidden.html',
            'site_section': 'atoms',
            'site_subsection': 'visually-hidden',
        },
        name='visually-hidden',
    ),
    re_path(
        r'^atoms/underline/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/atoms/underline.html',
            'site_section': 'atoms',
            'site_subsection': 'underline',
        },
        name='underline',
    ),
    re_path(
        r'^atoms/button/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/atoms/button.html',
            'site_section': 'atoms',
            'site_subsection': 'button',
        },
        name='button',
    ),

    # MOLECULES
    re_path(
        r'^molecules/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/molecules/index.html',
            'site_section': 'molecules',
        },
        name='molecules',
    ),
    re_path(
        r'^molecules/details/$',
        views.DetailsView.as_view(),
        {
            'template_name': 'demo/molecules/details.html',
            'site_section': 'molecules',
            'site_subsection': 'details',
        },
        name='details',
    ),
    re_path(
        r'^molecules/panel/$',
        views.DetailsView.as_view(),
        {
            'template_name': 'demo/molecules/panel.html',
            'site_section': 'molecules',
            'site_subsection': 'panel',
        },
        name='panel',
    ),
    re_path(
        r'^molecules/banner/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/molecules/banner.html',
            'site_section': 'molecules',
            'site_subsection': 'banner',
        },
        name='banner',
    ),
    re_path(
        r'^molecules/message-box/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/molecules/message-box.html',
            'site_section': 'molecules',
            'site_subsection': 'message_box',
        },
        name='message-box',
    ),
    re_path(
        r'^molecules/breadcrumbs/$',
        views.BreadcrumbsDemoPageView.as_view(),
        {
            'template_name': 'demo/molecules/breadcrumbs.html',
            'site_section': 'molecules',
            'site_subsection': 'breadcrumbs',
        },
        name='breadcrumbs',
    ),
    re_path(
        r'^molecules/content-list/$',
        views.DetailsView.as_view(),
        {
            'template_name': 'demo/molecules/content-list.html',
            'site_section': 'molecules',
            'site_subsection': 'content-list',
        },
        name='content-list',
    ),
    re_path(
        r'^molecules/error-reporting/$',
        views.DetailsView.as_view(),
        {
            'template_name': 'demo/molecules/error-reporting.html',
            'site_section': 'molecules',
            'site_subsection': 'error-reporting',
        },
        name='error-reporting',
    ),
    re_path(
        r'^molecules/fact-sheet/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/molecules/fact-sheet.html',
            'site_section': 'molecules',
            'site_subsection': 'fact-sheet',
        },
        name='fact-sheet',
    ),

    # COMPONENTS
    re_path(
        r'^components/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/components/index.html',
            'site_section': 'components',
        },
        name='components',
    ),
    re_path(
        r'^components/card/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/components/card.html',
            'site_section': 'components',
            'site_subsection': 'card',
        },
        name='card',
    ),
    re_path(
        r'^components/hero/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/components/hero.html',
            'site_section': 'components',
            'site_subsection': 'hero',
        },
        name='hero',
    ),
    re_path(
        r'^components/statistics/$',
        views.DemoStatsView.as_view(),
        {
            'template_name': 'demo/components/statistics.html',
            'site_section': 'components',
            'site_subsection': 'statistics',
        },
        name='statistics',
    ),
    re_path(
        r'^components/pagination/$',
        views.DemoPaginationView.as_view(),
        {
            'template_name': 'demo/components/pagination.html',
            'site_section': 'components',
            'site_subsection': 'pagination',
        },
        name='pagination',
    ),
    re_path(
        r'^components/search/$',
        views.SearchPageComponentsDemoPageView.as_view(),
        {
            'template_name': 'demo/components/search.html',
            'site_section': 'components',
            'site_subsection': 'search',
        },
        name='search',
    ),
    re_path(
        r'^components/feature-list/$',
        views.FeatureListView.as_view(),
        {
            'template_name': 'demo/components/feature-list.html',
            'site_section': 'components',
            'site_subsection': 'feature-list',
        },
        name='feature-list',
    ),
    re_path(
        r'^components/case-study/$',
        views.FeatureListView.as_view(),
        {
            'template_name': 'demo/components/case-study.html',
            'site_section': 'components',
            'site_subsection': 'case-study',
        },
        name='case-study',
    ),

    # HEADER & FOOTER
    re_path(
        r'^header-footer/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/header-footer/index.html',
            'site_section': 'header-footer',
        },
        name='header-footer',
    ),
    re_path(
        r'^header-footer/domestic/$',
        views.DomesticHeaderFooterView.as_view(),
        {'template_name': 'demo/header-footer/domestic.html'},
        name='great-domestic-header-footer',
    ),
    re_path(
        r'^header-footer/international/$',
        views.InternationalHeaderView.as_view(),
        {'template_name': 'demo/header-footer/international.html'},
        name='great-international-header-footer',
    ),
    re_path(
        r'^header-footer/invest/$',
        views.InvestHeaderView.as_view(),
        {'template_name': 'demo/header-footer/invest.html'},
        name='invest-header',
    ),

    re_path(
        r'^analytics/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/analytics/index.html',
            'site_section': 'analytics'
        },
        name='analytics',
    ),
    re_path(
        r'^elements/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/elements.html',
            'site_section': 'atoms'
        },
        name='elements',
    ),
    re_path(
        r'^featured-articles/$',
        views.FeaturedArticlesView.as_view(),
        {
            'template_name': 'demo/featured-articles.html',
            'site_section': 'components'
        },
        name='featured-articles',
    ),
    re_path(
        r'^google-tag-manager/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/google-tag-manager.html'},
        name='google-tag-manager',
    ),
]

handler404 = 'great_components.views.handler404'

handler500 = 'great_components.views.handler500'
