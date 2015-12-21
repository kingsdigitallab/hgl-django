# from ddhldapdjango.signal_handlers import register_signal_handlers as \
#     ddhldap_register_signal_handlers

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

import haystack

from wagtailbase import urls as ws_urls

admin.autodiscover()
# ddhldap_register_signal_handlers()

urlpatterns = patterns('',
                       url(r'^haystack_search/', include('hgl.haystackUrls')),
                       url(r'^grappelli/', include('grappelli.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^irt_geo/',include('geo.urls')),
                       url(r'^login/','geo.views.login_user'),
                       url(r'^logout/','geo.views.logout_user'),
                       url(r'^add/',include('geo.add_urls')),
                       url(r'^geofield/(\w+)/geofield.js','geofield.views.geofield_js'),
                       )



# ------------------------------------------------------------------
# Django Debug Toolbar URLS
# -----------------------------------------------------------------------------
try:
    if settings.DEBUG:
        import debug_toolbar
        urlpatterns += patterns('',
                                url(r'^__debug__/',
                                    include(debug_toolbar.urls)),
                                )

except ImportError:
    pass




# -----------------------------------------------------------------------------
# Wagtail CMS
# -----------------------------------------------------------------------------

urlpatterns += ws_urls.urlpatterns


# ------------------------------------------------------------------------
# Static file DEBUGGING
# -----------------------------------------------------------------------------
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    import os.path

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL + 'images/',
                          document_root=os.path.join(settings.MEDIA_ROOT,
                                                     'images'))
