from django.template import RequestContext
from django.shortcuts import (
    get_object_or_404,
    render,
    HttpResponse,
    render,
    HttpResponseRedirect,
)
from catalogue.models import Person, AlternativeName

"""Person detail page added as per 2021 Sow
done the old way because the django code is old...
"""
def person(request, id):
    context = {}
    person = Person.objects.get(pk=id)
    items = person.item.all()
    variant_names = AlternativeName.objects.filter(person=person)
    if variant_names.count() > 0:
        context["variant_names"] = items
    if items.count() > 0:
        context["archive_items"] = items
    context["person"] = person
    return render(
        request,
        "../templates/person.html",
        context
    )