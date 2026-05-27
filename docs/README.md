# Awesome Journal - Todo and Journal API

A Todo API that helps you manage your tasks and write journals in a fast and easy way.

## Table of Contents

- [About the Project](#about-the-project)
  - [Built With](#built-with)
    - [Tech Stack](#tech-stack)
    - [Key Features](#key-features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Setup and Install](#setup-and-install)
  - [Usage](#usage)
- [Contributing](#contributing)
- [Show Your Support](#show-your-support)
- [License](#license)

## About the Project

This repository contains a FastAPI project for managing todos and writing journals. You can build applications or website interfaces using this API. The project allows you to easily create, read, update, and delete your todos, with JWT authentication support.

### Built With

#### Tech Stack

- **Language**: Python
- **Framework**: FastAPI
- **Database**: PostgreSQL

#### Key Features

- Create, read, update, and delete todos
- JWT authentication
- Admin endpoints

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

Clone the repository to your desired folder:

```sh
# Clone the repository
git clone https://github.com/geekmanesh/awsome-journal.git
cd awsome-journal

# Build the Docker image
make build

# Run the Docker container
make up
```

### Usage

Once the application is running, open your browser and go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to see the interactive API documentation for all endpoints.

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](/docs/CONTRIBUTING.md) for more information.

## Show Your Support

If you find this project useful, please consider supporting it.

## Acknowledgements

*No acknowledgements at this time.*

## License

This project is licensed under the MIT License. See the [LICENSE](/LICENSE) file for details.