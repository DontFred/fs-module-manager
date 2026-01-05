# FS Module Manager

Deutsche version siehe unten.

A full-stack application for managing university modules, designed to handle complex workflows, versioning, translations, and role-based access control.

## Project Structure

This is a monorepo containing:

* **Frontend**: A Next.js 16 application using React 19, Tailwind CSS v4, and TypeScript.
* **Backend**: A FastAPI application using Python 3.14+, SQLAlchemy, and Pydantic.
* **Infrastructure**: Docker Compose configuration for the PostgreSQL database and service orchestration.

## Features

* **Module Management**: Create, update, and manage university modules and their versions.
* **Workflow System**: Structured status workflow (Draft → In Review → Validation → Approval → Released).
* **Role-Based Access**: Specialized roles for Module Owners, Program Coordinators, Examination Office, Deanery, and Admins.
* **Versioning & Auditing**: Comprehensive version control for modules and audit logs for all actions.
* **Internationalization**: Support for module translations.

## Prerequisites

Ensure you have the following installed:

* **[Docker](https://www.docker.com/)** & **Docker Compose**: For running the database.
* **[Bun](https://bun.sh/)**: Used as the package manager and script runner.
* **[uv](https://github.com/astral-sh/uv)**: A fast Python package and project manager.

## Getting Started in development

### 1. Clone the Repository
```bash
git clone https://github.com/DontFred/fs-module-manager
cd fs-module-manager

```

### 2. Environment Setup

Create a `.env` file in the root directory. Based on the configuration, it should include:

```ini
# PORTS
NEXT_PUBLIC_BACKEND_PORT=8000
FRONTEND_PORT=3000

# DATABASE
DB_USERNAME="admin"
DB_PASSWORD="please_change_me"
DB_DATABASE="modules"

# JWT
JWT_SECRET_KEY="please1change1me"
JWT_ALGORITHM="HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=240

# ARGON2
ARGON_TIME_COST=3
ARGON_MEMORY_COST=65536
ARGON_PARALLELISM=4
ARGON_HASH_LENGTH=32
ARGON_SALT_LENGTH=16

# ENVIRONMENTS
ENVIRONMENT="development"

# SERVER URL
NEXT_PUBLIC_SERVER_URL="http://127.0.0.1"

```

### 3. Install Dependencies

Install dependencies for the frontend and backend, and clean the workspace:

```bash
bun run install

```


### 4. Run the Application

Start the database, backend, and frontend concurrently:

```bash
bun run dev

```

### Available Scripts

* `bun run dev`: Starts the full stack (Docker DB, Backend, Frontend).
* `bun run dev:db`: Starts only the database container.
* `bun run dev:backend`: Starts only the backend service.
* `bun run dev:frontend`: Starts only the frontend application.
* `bun run lint`: Runs linters for both frontend (`eslint`) and backend (`ruff`).
* `bun run test`: Runs backend tests (`pytest`).
* `bun run clean`: Removes `node_modules` and lockfiles.
  
## Getting Started hosting

### 1. Clone the Repository
```bash
git clone https://github.com/DontFred/fs-module-manager
cd fs-module-manager

```

### 2. Environment Setup

Create a `.env` file in the root directory. Based on the configuration, it should include:

```ini
# PORTS
NEXT_PUBLIC_BACKEND_PORT=8000
FRONTEND_PORT=3000

# DATABASE
DB_USERNAME="admin"
DB_PASSWORD="please_change_me"
DB_DATABASE="modules"

# JWT
JWT_SECRET_KEY="please1change1me"
JWT_ALGORITHM="HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=240

# ARGON2
ARGON_TIME_COST=3
ARGON_MEMORY_COST=65536
ARGON_PARALLELISM=4
ARGON_HASH_LENGTH=32
ARGON_SALT_LENGTH=16

# ENVIRONMENTS
ENVIRONMENT="production"

# SERVER URL
NEXT_PUBLIC_SERVER_URL="http://127.0.0.1"

```

### 3. Build and run the application

Run docker compose to build and run the application

```bash
docker compose --build -d
```


## License

This software is licensed under **CC BY-NC-SA 4.0**. Usage is restricted to non-commercial purposes only. Any modifications or derivative works must also be open-source and non-commercial.

# FS Modul-Manager - DEU

Eine Full-Stack-Anwendung zur Verwaltung von Universitätsmodulen, entwickelt für die Handhabung komplexer Workflows, Versionierung, Übersetzungen und rollenbasierter Zugriffskontrolle.

## Projektstruktur

Dies ist ein Monorepo, bestehend aus:

* **Frontend**: Eine Next.js 16 Anwendung mit React 19, Tailwind CSS v4 und TypeScript.
* **Backend**: Eine FastAPI Anwendung mit Python 3.14+, SQLAlchemy und Pydantic.
* **Infrastruktur**: Docker Compose Konfiguration für die PostgreSQL-Datenbank und die Orchestrierung der Dienste.

## Funktionen

* **Modulverwaltung**: Erstellen, Aktualisieren und Verwalten von Universitätsmodulen und deren Versionen.
* **Workflow-System**: Strukturierter Status-Workflow (Entwurf → In Prüfung → Validierung → Genehmigung → Veröffentlicht).
* **Rollenbasierter Zugriff**: Spezielle Rollen für Modulverantwortliche, Studiengangskoordinatoren, Prüfungsamt, Dekanat und Administratoren.
* **Versionierung & Auditierung**: Umfassende Versionskontrolle für Module und Audit-Logs für alle Aktionen.
* **Internationalisierung**: Unterstützung für Modulübersetzungen.

## Voraussetzungen

Stellen Sie sicher, dass Folgendes installiert ist:

* **[Docker](https://www.docker.com/)** & **Docker Compose**: Zum Ausführen der Datenbank.
* **[Bun](https://bun.sh/)**: Wird als Paketmanager und Skript-Runner verwendet.
* **[uv](https://github.com/astral-sh/uv)**: Ein schneller Python-Paket- und Projektmanager.

## Erste Schritte für development

### 1. Repository klonen
```bash
git clone https://github.com/DontFred/fs-module-manager
cd fs-module-manager

```

### 2. Umgebung einrichten

Erstellen Sie eine `.env`-Datei im Hauptverzeichnis. Basierend auf der Konfiguration sollte diese Folgendes enthalten:

```ini
# PORTS
NEXT_PUBLIC_BACKEND_PORT=8000
FRONTEND_PORT=3000

# DATABASE
DB_USERNAME="admin"
DB_PASSWORD="please_change_me"
DB_DATABASE="modules"

# JWT
JWT_SECRET_KEY="please1change1me"
JWT_ALGORITHM="HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=240

# ARGON2
ARGON_TIME_COST=3
ARGON_MEMORY_COST=65536
ARGON_PARALLELISM=4
ARGON_HASH_LENGTH=32
ARGON_SALT_LENGTH=16

# ENVIRONMENTS
ENVIRONMENT="development"

# SERVER URL
NEXT_PUBLIC_SERVER_URL="http://127.0.0.1"

```

### 3. Abhängigkeiten installieren

Installieren Sie die Abhängigkeiten für das Frontend und bereinigen Sie den Workspace:

```bash
bun run install

```


### 4. Anwendung starten

Starten Sie Datenbank, Backend und Frontend gleichzeitig:

```bash
bun run dev

```

### Verfügbare Skripte

* `bun run dev`: Startet den gesamten Stack (Docker DB, Backend, Frontend).
* `bun run dev:db`: Startet nur den Datenbank-Container.
* `bun run dev:backend`: Startet nur den Backend-Dienst.
* `bun run dev:frontend`: Startet nur die Frontend-Anwendung.
* `bun run lint`: Führt Linter für Frontend (`eslint`) und Backend (`ruff`) aus.
* `bun run test`: Führt Backend-Tests (`pytest`) aus.
* `bun run clean`: Entfernt `node_modules` und Lockfiles.

## Erste Schritte fürs hosten

### 1. Repository klonen
```bash
git clone https://github.com/DontFred/fs-module-manager
cd fs-module-manager

```

### 2. Umgebung einrichten

Erstellen Sie eine `.env`-Datei im Hauptverzeichnis. Basierend auf der Konfiguration sollte diese Folgendes enthalten:

```ini
# PORTS
NEXT_PUBLIC_BACKEND_PORT=8000
FRONTEND_PORT=3000

# DATABASE
DB_USERNAME="admin"
DB_PASSWORD="please_change_me"
DB_DATABASE="modules"

# JWT
JWT_SECRET_KEY="please1change1me"
JWT_ALGORITHM="HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=240

# ARGON2
ARGON_TIME_COST=3
ARGON_MEMORY_COST=65536
ARGON_PARALLELISM=4
ARGON_HASH_LENGTH=32
ARGON_SALT_LENGTH=16

# ENVIRONMENTS
ENVIRONMENT="production"

# SERVER URL
NEXT_PUBLIC_SERVER_URL="http://127.0.0.1"

```

### 3. Build und starte die Anwendung
Benutze docker compose um die Anwendung zu builden und zu starten

```bash
docker compose --build -d
```

## Lizenz

Diese Software ist unter **CC BY-NC-SA 4.0** lizenziert. Die Nutzung ist auf nicht-kommerzielle Zwecke beschränkt. Jegliche Modifikationen oder abgeleitete Werke müssen ebenfalls Open-Source und nicht-kommerziell sein.