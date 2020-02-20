from django.conf.urls import url

from demo import views

urlpatterns = [
    url(
        r'^$',
        views.IndexPageView.as_view(),
        {'template_name': 'demo/index.html'},
        name='index',
    ),

    # PAGES
    url(
        r'^pages/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/pages/index.html',
            'site_section': 'pages',
        },
        name='pages',
    ),
    url(
        r'^pages/404/$',
        views.BasePageView.as_view(),
        {
            'template_name': '404.html',
            'site_section': 'pages',
            'site_subsection': '404',
        },
        name='404',
    ),
    url(
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
    url(
        r'^forms/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/forms/index.html',
            'site_section': 'forms',
        },
        name='forms',
    ),
    url(
        r'^forms/widgets/$',
        views.DemoFormView.as_view(),
        {
            'template_name': 'demo/forms/widgets.html',
            'site_section': 'forms',
            'site_subsection': 'widgets',
        },
        name='widgets',
    ),
    url(
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
    url(
        r'^atoms/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/atoms/index.html',
            'site_section': 'atoms',
        },
        name='atoms',
    ),
    url(
        r'^atoms/typography/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/atoms/typography.html',
            'site_section': 'atoms',
            'site_subsection': 'typography',
        },
        name='typography',
    ),
    url(
        r'^atoms/list/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/atoms/list.html',
            'site_section': 'atoms',
            'site_subsection': 'list',
        },
        name='list',
    ),
    url(
        r'^atoms/table/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/atoms/table.html',
            'site_section': 'atoms',
            'site_subsection': 'table',
        },
        name='table',
    ),
    url(
        r'^atoms/colour/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/atoms/colour.html',
            'site_section': 'atoms',
            'site_subsection': 'colour',
        },
        name='colour',
    ),
    url(
        r'^atoms/grid/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/atoms/grid.html',
            'site_section': 'atoms',
            'site_subsection': 'grid',
        },
        name='grid',
    ),
    url(
        r'^atoms/spacing/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/atoms/spacing.html',
            'site_section': 'atoms',
            'site_subsection': 'spacing',
        },
        name='spacing',
    ),
    url(
        r'^atoms/responsive/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/atoms/responsive.html',
            'site_section': 'atoms',
            'site_subsection': 'responsive',
        },
        name='responsive',
    ),
    url(
        r'^atoms/visually-hidden/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/atoms/visually-hidden.html',
            'site_section': 'atoms',
            'site_subsection': 'visually-hidden',
        },
        name='visually-hidden',
    ),
    url(
        r'^atoms/underline/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/atoms/underline.html',
            'site_section': 'atoms',
            'site_subsection': 'underline',
        },
        name='underline',
    ),
    url(
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
    url(
        r'^molecules/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/molecules/index.html',
            'site_section': 'molecules',
        },
        name='molecules',
    ),
    url(
        r'^molecules/details/$',
        views.DetailsView.as_view(),
        {
            'template_name': 'demo/molecules/details.html',
            'site_section': 'molecules',
            'site_subsection': 'details',
        },
        name='details',
    ),
    url(
        r'^molecules/panel/$',
        views.DetailsView.as_view(),
        {
            'template_name': 'demo/molecules/panel.html',
            'site_section': 'molecules',
            'site_subsection': 'panel',
        },
        name='panel',
    ),
    url(
        r'^molecules/banner/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/molecules/banner.html',
            'site_section': 'molecules',
            'site_subsection': 'banner',
        },
        name='banner',
    ),
    url(
        r'^molecules/message-box/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/molecules/message-box.html',
            'site_section': 'molecules',
            'site_subsection': 'message_box',
        },
        name='message-box',
    ),
    url(
        r'^molecules/breadcrumbs/$',
        views.BreadcrumbsDemoPageView.as_view(),
        {
            'template_name': 'demo/molecules/breadcrumbs.html',
            'site_section': 'molecules',
            'site_subsection': 'breadcrumbs',
        },
        name='breadcrumbs',
    ),
    url(
        r'^molecules/content-list/$',
        views.DetailsView.as_view(),
        {
            'template_name': 'demo/molecules/content-list.html',
            'site_section': 'molecules',
            'site_subsection': 'content-list',
        },
        name='content-list',
    ),
    url(
        r'^molecules/error-reporting/$',
        views.DetailsView.as_view(),
        {
            'template_name': 'demo/molecules/error-reporting.html',
            'site_section': 'molecules',
            'site_subsection': 'error-reporting',
        },
        name='error-reporting',
    ),
    url(
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
    url(
        r'^components/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/components/index.html',
            'site_section': 'components',
        },
        name='components',
    ),
    url(
        r'^components/card/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/components/card.html',
            'site_section': 'components',
            'site_subsection': 'card',
        },
        name='card',
    ),
    url(
        r'^components/hero/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/components/hero.html',
            'site_section': 'components',
            'site_subsection': 'hero',
        },
        name='hero',
    ),
    url(
        r'^components/statistics/$',
        views.DemoStatsView.as_view(),
        {
            'template_name': 'demo/components/statistics.html',
            'site_section': 'components',
            'site_subsection': 'statistics',
        },
        name='statistics',
    ),
    url(
        r'^components/pagination/$',
        views.DemoPaginationView.as_view(),
        {
            'template_name': 'demo/components/pagination.html',
            'site_section': 'components',
            'site_subsection': 'pagination',
        },
        name='pagination',
    ),
    url(
        r'^components/search/$',
        views.SearchPageComponentsDemoPageView.as_view(),
        {
            'template_name': 'demo/components/search.html',
            'site_section': 'components',
            'site_subsection': 'search',
        },
        name='search',
    ),
    url(
        r'^components/feature-list/$',
        views.FeatureListView.as_view(),
        {
            'template_name': 'demo/components/feature-list.html',
            'site_section': 'components',
            'site_subsection': 'feature-list',
        },
        name='feature-list',
    ),
    url(
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
    url(
        r'^header-footer/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/header-footer/index.html',
            'site_section': 'header-footer',
        },
        name='header-footer',
    ),
    url(
        r'^header-footer/domestic/$',
        views.DomesticHeaderFooterView.as_view(),
        {'template_name': 'demo/header-footer/domestic.html'},
        name='great-domestic-header-footer',
    ),
    url(
        r'^header-footer/international/$',
        views.InternationalHeaderView.as_view(),
        {'template_name': 'demo/header-footer/international.html'},
        name='great-international-header-footer',
    ),
    url(
        r'^header-footer/invest/$',
        views.InvestHeaderView.as_view(),
        {'template_name': 'demo/header-footer/invest.html'},
        name='invest-header',
    ),

    url(
        r'^analytics/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/analytics/index.html',
            'site_section': 'analytics'
        },
        name='analytics',
    ),
    url(
        r'^elements/$',
        views.BasePageView.as_view(),
        {
            'template_name': 'demo/elements.html',
            'site_section': 'atoms'
        },
        name='elements',
    ),
    url(
        r'^featured-articles/$',
        views.FeaturedArticlesView.as_view(),
        {
            'template_name': 'demo/featured-articles.html',
            'site_section': 'components'
        },
        name='featured-articles',
    ),
    url(
        r'^google-tag-manager/$',
        views.BasePageView.as_view(),
        {'template_name': 'demo/google-tag-manager.html'},
        name='google-tag-manager',
    ),
]

handler404 = 'great_components.views.handler404'

handler500 = 'great_components.views.handler500'
