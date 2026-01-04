# Backend - Module Manager

The RESTful API service for the Module Manager, providing data persistence, business logic, and authentication.

Deutsche version siehe unten.

## Tech Stack

* **Language**: Python (>=3.14)
* **Framework**: FastAPI
* **Database ORM**: SQLAlchemy
* **Validation**: Pydantic
* **Dependency Manager**: uv
* **Testing**: Pytest
* **Linting/Formatting**: Ruff

## Architecture

* **API**: REST endpoints versioned (e.g., `/v0/`) and organized by resource (Auth, Modules, Users, Health).
* **Database**: PostgreSQL connection handled via `psycopg2-binary` and SQLAlchemy.
* **Authentication**: JWT-based auth using `pyjwt` and `argon2-cffi` for password hashing.

## Development

### Running the Server
To run the backend independently (ensure your database is running via Docker first):
```bash
uv run ./main.py

```

The server typically runs on port `8000` (configurable via `.env`).

### Testing

Run the test suite:

```bash
uv run pytest

```

### Linting and Formatting

The project uses `ruff` for both linting and formatting:

```bash
uv run ruff check --fix
uv run ruff format

```

## API Documentation

Once the server is running, you can access the interactive API documentation:

* **Swagger UI**: `http://localhost:8000/v0/docs`
* **OpenAPI JSON**: `http://localhost:8000/v0/openapi.json`

## License

This software is licensed under **CC BY-NC-SA 4.0**. Usage is restricted to non-commercial purposes only. Any modifications or derivative works must also be open-source and non-commercial.

# Backend - Modul-Manager - DEU

Der RESTful API-Dienst für den Modul-Manager, der Datenpersistenz, Geschäftslogik und Authentifizierung bereitstellt.

## Technologie-Stack

* **Sprache**: Python (>=3.14)
* **Framework**: FastAPI
* **Datenbank ORM**: SQLAlchemy
* **Validierung**: Pydantic
* **Dependency Manager**: uv
* **Testing**: Pytest
* **Linting/Formatierung**: Ruff

## Architektur

* **API**: REST-Endpunkte versioniert (z.B. `/v0/`) und nach Ressourcen organisiert (Auth, Module, Benutzer, Health).
* **Datenbank**: PostgreSQL-Verbindung, gehandhabt über `psycopg2-binary` und SQLAlchemy.
* **Authentifizierung**: JWT-basierte Authentifizierung unter Verwendung von `pyjwt` und `argon2-cffi` für das Passwort-Hashing.

## Entwicklung

### Server starten
Um das Backend unabhängig auszuführen (stellen Sie sicher, dass Ihre Datenbank zuerst via Docker läuft):
```bash
uv run ./main.py

```

Der Server läuft typischerweise auf Port `8000` (konfigurierbar über `.env`).

### Testen

Führen Sie die Test-Suite aus:

```bash
uv run pytest

```

### Linting und Formatierung

Das Projekt verwendet `ruff` sowohl für Linting als auch für Formatierung:

```bash
uv run ruff check --fix
uv run ruff format

```

## API-Dokumentation

Sobald der Server läuft, können Sie auf die interaktive API-Dokumentation zugreifen:

* **Swagger UI**: `http://localhost:8000/v0/docs`
* **OpenAPI JSON**: `http://localhost:8000/v0/openapi.json`

## Lizenz

Diese Software ist unter **CC BY-NC-SA 4.0** lizenziert. Die Nutzung ist auf nicht-kommerzielle Zwecke beschränkt. Jegliche Modifikationen oder abgeleitete Werke müssen ebenfalls Open-Source und nicht-kommerziell sein.
