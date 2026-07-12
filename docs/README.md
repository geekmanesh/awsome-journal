# Google Tasks API

A FastAPI backend inspired by Google Tasks, featuring lists, tasks, due dates, priorities, labels, authentication, and RESTful APIs.

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

This repository contains a FastAPI project inspired by Google Tasks. You can build applications or website interfaces using this API. The project allows you to easily create, read, update, and delete your lists and tasks, complete with due dates, priorities, and labels, with JWT authentication support.

### Built With

#### Tech Stack

- **Language**: Python
- **Framework**: FastAPI
- **Database**: PostgreSQL

#### Key Features

- Create, read, update, and delete lists and tasks
- Due dates, priorities, and labels
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
git clone https://github.com/geekmanesh/google-tasks-api.git
cd google-tasks-api

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