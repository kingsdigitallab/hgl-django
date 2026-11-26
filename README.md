# hgl-django

Heritage Gazetteer of Libya

This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).

## Development

### Requirements

- python 3.7
- gdal
- mysql8
- uv

### Setup

#### Prerequirements

Request access to:

- Secrets
- DB dump

#### From compose folder

Create env file

```bash
nvim .env
```

Initialise docker compose dev

```bash
docker compose -f docker-compose.dev.yml up -d
```

#### From hgl/settings/

Edit the base.py lines 338 and 352 from http://elasticsearch:9200/ to http://localhost:9200/

> [!NOTE]
> Don't commit this change as it will break the prod deployment.

#### From project root folder

Create env

```bash
uv venv --python 3.7
```

Install deps

```bash
uv pip install -r requirements-dev.txt
```

Rebuild index

```bash
uv python manage.py rebuild_index --noinput
```

> [!NOTE]
> If you bring the elasticsearch container down you'll have to rerun this command.

Run the server

```bash
uv run manage.py runserver --insecure 127.0.0.1:8000
```
