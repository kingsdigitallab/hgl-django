[
{% for result in page.object_list %}
{
  "type": "Feature",
  "geometry": {
    "type": "MultiPoint",
    "coordinates": [{% for coord in result.object.locus_coordinate.all %}[ {{ coord.point.x }}, {{ coord.point.y }}]{% if forloop.last %}{% else %},{% endif %}{% endfor %}]
  },
  "properties": {
    "name": "{{ result.object.name }}",
    "id": {{ result.object.id }}
  }
}{% if forloop.last %}{% else %},{% endif %}
{% endfor %}
]