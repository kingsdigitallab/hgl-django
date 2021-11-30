from django.conf.urls import include, url
import geo

urlpatterns = [
    url(r"^kml", geo.views.kml),
    url(r"^convex-hull/$", geo.views.convex_hull),
    url(r"^line/$", geo.views.line),
    url(r"^popupcontent/$", geo.views.popupcontent),
    url(r"^recordview/$", geo.views.recordview),
    url(r"^geojson/$", geo.views.geojson),
]
