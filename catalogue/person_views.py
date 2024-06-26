from django.template import RequestContext
from django.shortcuts import (
    get_object_or_404,
    render,
    HttpResponse,
    render,
    HttpResponseRedirect,
)
from catalogue.models import Person, AlternativeName, Reference

"""Person detail page added as per 2021 Sow
done the old way because the django code is old...
"""
def person(request, id):
    context = {}
    person = Person.objects.get(pk=id)
    items = person.item.all()
    variant_names = AlternativeName.objects.filter(person=person)
    references = Reference.objects.filter(person=person)
    if variant_names.count() > 0:
        context["variant_names"] = variant_names
    if items.count() > 0:
        context["archive_items"] = items
    if references.count() > 0:
        context['references'] = references
    context["person"] = person
    # Get a unique set of dates
    dates = []
    for item in items:
        dates.append(item.unitstart_date)
        dates.append(item.unitend_date)
    date_set = set(dates)
    dates = list(date_set)
    dates.sort()
    context["dates"] = str(dates)
    return render(
        request,
        "../templates/person.html",
        context
    )