from django.conf import settings
from django.conf.urls import include, url
from catalogue.person_views import person
from hgl.catalogueSearchUrls import CustomTextSearchView, CustomSearchForm

urlpatterns = [
    url(r"(\d+)/$", person, name="person_detail"),
    url(
        r"^$",
        CustomTextSearchView(
            template="search/catalogue_text_search.html",
            form_class=CustomSearchForm,
            results_per_page=15,
            record_type="Person"
        ),
        name="person_search",
    ),
]
