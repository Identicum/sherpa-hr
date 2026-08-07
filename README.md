# sherpa-hr

Web module for HR CRUD operations in [Identicum Sherpa](https://identicum.com/iga/).

## What it is

`sherpa-hr` is a small, self-contained Flask application that simulates a company's **authoritative HR source** — the kind of system that, in a real deployment, would feed identity lifecycle events (joiners/movers/leavers) into an IGA/IDM platform such as MidPoint.

It is a **satellite component** of Sherpa, Identicum's internal suite of reusable building blocks and demo/PoC assets built around our open-source IAM stack (Keycloak, Evolveum MidPoint, Gluu/Janssen). It is not sold or deployed at customers as-is; its purpose is to give sales, delivery, and engineering a realistic, disposable "source of truth" to connect to during demos, PoCs, and internal testing of provisioning/de-provisioning flows.

## Data model

The app models a simple organization:

- **Department** — organizational unit (`name`, `description`).
- **Position** — a job title belonging to a Department.
- **Person** — an individual, uniquely identified by `id_number` and `tax_id`, with personal and (optional) organizational contact info (`personal_email`, `org_email`, `username`).
- **Employee** — a work relationship linking a Person to a Position, with `start_date`/`end_date` and an optional `manager` (another Person).
- **Contractor** — a work relationship linking a Person to a Department and an external `company_name`, also with `start_date`/`end_date` and an optional `manager`.

A Person can have at most one Employee and/or one Contractor relationship. Deleting a Person is blocked while related Employee or Contractor relationships exist.

Three read-only SQL views compute derived/aggregated data (see [db/01_structure.sql](db/01_structure.sql)):

- `vw_employee` / `vw_contractor` — join Person with their Employee/Contractor row and compute a `status` (`A`ctive / `I`nactive) from `start_date`/`end_date` against `CURRENT_DATE`.
- `vw_persondata` — one row per Person, unioning the Employee and Contractor views and picking the most recent relationship. Persons with no relationship at all still appear, with `status` defaulting to `'I'`. This view is the one exposed through the read-only `PersonData` API/model — the intended integration point for external systems that just need "who is this person, and what's their current status."

## Application structure

- **Flask + SQLAlchemy** ([app/main.py](app/main.py), [app/models.py](app/models.py)) — app factory registers one Blueprint per resource.
- **Marshmallow** ([app/schemas.py](app/schemas.py)) — serialization schemas, also used to auto-generate Swagger definitions.
- **Flasgger** — serves interactive API docs at `/apidocs/`.
- **Bootstrap 5** server-rendered templates ([app/templates/](app/templates/)) — a minimal nav bar with a page per resource (Persons, Departments, Positions, Employees, Contractors) plus a link to Swagger.
- **PostgreSQL** — schema and views ([db/01_structure.sql](db/01_structure.sql)) plus seed data (Beatles + a couple of contractors, [db/02_data.sql](db/02_data.sql)) loaded on first container start.

### Web UI (`/persons`, `/departments`, `/positions`, `/employees`, `/contractors`)

Full CRUD (list/add/edit/delete) via server-rendered HTML forms, one Blueprint per resource (see [app/blueprints/](app/blueprints/)).

### REST API

All endpoints are documented in a Swagger using Flasgger docstrings and browsable at `/apidocs/`.
