# Google Tasks API

A FastAPI backend for managing task lists and tasks, modeled on Google Tasks.

## Table of Contents

- [About the Project](#about-the-project)
  - [Tech Stack](#tech-stack)
  - [Key Features](#key-features)
  - [Entity Relationship Diagram](#entity-relationship-diagram)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Setup and Install](#setup-and-install)
  - [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## About the Project

This repository provides a JWT-authenticated REST API for organizing tasks into lists. Each task belongs
to exactly one list, carries a priority, and can optionally follow a recurrence rule (daily, weekly,
monthly, or yearly) with a defined start time and end condition. Admin users can manage tasks across all
accounts.

### Tech Stack

- **Language**: Python
- **Framework**: FastAPI
- **Database**: PostgreSQL, via SQLAlchemy and Alembic

### Key Features

- CRUD for lists and tasks, scoped to the authenticated user
- Task recurrence: repeat every N days, weeks, months, or years, with a start time and an end
  condition (never, on a fixed date, or after a set number of occurrences)
- Task and list priority levels
- JWT authentication
- Admin endpoints spanning every user's tasks

### Entity Relationship Diagram

See [ERD.md](/docs/ERD.md) for the current database schema (`users`, `lists`, `tasks`, `repeats`) and
which parts of the Google Tasks feature set are not yet modeled.

## Getting Started

Follow these steps to run the project locally.

### Prerequisites

```sh
git
python
docker
postgresql
```

### Setup and Install

Clone the repository:

```sh
git clone https://github.com/geekmanesh/google-tasks-api.git
cd google-tasks-api

# Build the Docker image
make build

# Start the containers
make up
```

### Usage

Once the containers are running, open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the
interactive API documentation.

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](/docs/CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License. See [LICENSE](/LICENSE) for details.
