mapResult([
{% for result in page.object_list %}
{
  "type": "Feature",
  "geometry": {
    "type": "MultiPoint",
    "coordinates": [{% for coord in result.object.locus_coordinate.all %}[ {{ coord.point.x }}, {{ coord.point.y }}],{% endfor %}]
  },
  "properties": {
    "name": "null island"
  }
}{% if forloop.last %}{% else %},{% endif %}
{% endfor %}
])