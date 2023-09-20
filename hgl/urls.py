# from ddhldapdjango.signal_handlers import register_signal_handlers as \
#     ddhldap_register_signal_handlers

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

# for autocomplete

from geo.views import (
    autocomplete,
    login_user,
    logout_user,
    recordview_simple
)

from wagtailbase import urls as ws_urls
from geofield.views import geofield_js

admin.autodiscover()
# ddhldap_register_signal_handlers()

urlpatterns = [
    url(r"^cat_search/", include("hgl.catalogueSearchUrls")),
    url(r"^person/", include("catalogue.person_urls")),
    url(r"^haystack_search/", include("hgl.haystackUrls")),
    url(r"^grappelli/", include("grappelli.urls")),
    url('^admin/', admin.site.urls),
    url(r"^irt_geo/", include("geo.urls")),
    url(r"^hypothesis/", include("catalogue.urls")),
    url(r"^cat_item/", include("catalogue.urls")),
    url(r"^browse/", include("catalogue.urls")),
    url(r"^login/", login_user),
    url(r"^logout/", logout_user),
    url(r"^add/", include("geo.add_urls")),
    url(r"^get/", include("geo.get_urls")),
    url(r"^export/", include("geo.export_urls")),
    url(r"^geofield/(\w+)/geofield.js", geofield_js),
    url(r"^autocomplete/$", autocomplete.as_view(),
        name="location-autocomplete"),
    url(r"^(\d+)/", recordview_simple),
    url(r"^data/", include("geo.pelagiosUrls")),
]

# ------------------------------------------------------------------
# Django Debug Toolbar URLS
# -----------------------------------------------------------------------------
try:
    if settings.DEBUG:
        import debug_toolbar

        urlpatterns += [
            "",
            url(r"^__debug__/", include(debug_toolbar.urls)),
        ]

except ImportError:
    pass

# -----------------------------------------------------------------------------
# Wagtail CMS
# -----------------------------------------------------------------------------

urlpatterns += ws_urls.urlpatterns

# ------------------------------------------------------------------------
# Static file DEBUGGING
# -----------------------------------------------------------------------------
# if settings.DEBUG:
#     from django.conf.urls.static import static
#     from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#     import os.path
#
#     urlpatterns += staticfiles_urlpatterns()
#     urlpatterns += static(
#         settings.MEDIA_URL + "images/",
#         document_root=os.path.join(settings.MEDIA_ROOT, "images"),
#     )
