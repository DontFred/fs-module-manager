# Frontend - Module Manager

Deutsche version siehe unten.

The user interface for the Module Manager, offering a responsive and interactive dashboard for university staff.

## Tech Stack

* **Framework**: Next.js 16 (App Router)
* **Runtime**: React 19
* **Language**: TypeScript
* **Styling**: Tailwind CSS v4
* **Components**: shadcn/ui (Radix UI + Tailwind)
* **State Management**: TanStack Query (React Query)
* **Form Handling**: React Hook Form + Zod
* **API Client**: openapi-fetch (Type-safe fetch)

## Development

### Prerequisites
* **Bun** is required for running scripts and managing dependencies.

### Commands

* **Development Server**:
    ```bash
    bun run dev
    ```
    Starts the Next.js dev server on port `3000`.

* **Production Build**:
    ```bash
    bun run build
    bun run start
    ```

* **Linting**:
    ```bash
    bun run lint
    ```

### API Integration

The frontend uses a type-safe API client generated from the backend's OpenAPI specification.

To regenerate the SDK client (requires the backend to be running):
```bash
bun run sdk:generate

```

This command fetches `openapi.json` from the backend and generates TypeScript definitions in `api-sdk/schema.ts`.

## Project Structure

* `/app`: Next.js App Router pages and layouts.
* `/components/ui`: Reusable UI components (shadcn/ui).
* `/lib`: Utility functions, session management, and data access layer.
* `/api-sdk`: Generated API client and schemas.

## License

This software is licensed under **CC BY-NC-SA 4.0**. Usage is restricted to non-commercial purposes only. Any modifications or derivative works must also be open-source and non-commercial.

# Frontend - Modul-Manager - DEU

Die Benutzeroberfläche für den Modul-Manager, die ein responsives und interaktives Dashboard für Universitätsmitarbeiter bietet.

## Technologie-Stack

* **Framework**: Next.js 16 (App Router)
* **Runtime**: React 19
* **Sprache**: TypeScript
* **Styling**: Tailwind CSS v4
* **Komponenten**: shadcn/ui (Radix UI + Tailwind)
* **State Management**: TanStack Query (React Query)
* **Formularbehandlung**: React Hook Form + Zod
* **API Client**: openapi-fetch (Typsicherer Fetch)

## Entwicklung

### Voraussetzungen
* **Bun** ist erforderlich, um Skripte auszuführen und Abhängigkeiten zu verwalten.

### Befehle

* **Entwicklungsserver**:
    ```bash
    bun run dev
    ```
    Startet den Next.js Entwicklungsserver auf Port `3000`.

* **Produktions-Build**:
    ```bash
    bun run build
    bun run start
    ```

* **Linting**:
    ```bash
    bun run lint
    ```

### API-Integration

Das Frontend verwendet einen typsicheren API-Client, der aus der OpenAPI-Spezifikation des Backends generiert wird.

Um den SDK-Client neu zu generieren (erfordert, dass das Backend läuft):
```bash
bun run sdk:generate

```

Dieser Befehl ruft `openapi.json` vom Backend ab und generiert TypeScript-Definitionen in `api-sdk/schema.ts`.

## Projektstruktur

* `/app`: Next.js App Router Seiten und Layouts.
* `/components/ui`: Wiederverwendbare UI-Komponenten (shadcn/ui).
* `/lib`: Hilfsfunktionen, Sitzungsverwaltung und Datenzugriffsschicht (DAL).
* `/api-sdk`: Generierter API-Client und Schemata.

## Lizenz

Diese Software ist unter **CC BY-NC-SA 4.0** lizenziert. Die Nutzung ist auf nicht-kommerzielle Zwecke beschränkt. Jegliche Modifikationen oder abgeleitete Werke müssen ebenfalls Open-Source und nicht-kommerziell sein.