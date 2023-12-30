# watch-hf 🤗👀

A webhook server that automates the update and restart of Hugging Face Spaces.

## Introduction

This project was created to simplify the deployment and maintenance of Hugging Face Spaces. This webhook server does two things:

- When it receives a notification from Watchtower, a service that monitors the updates of Docker images, it updates a Hugging Face Space by performing a "factory reboot", which resets the Space and pulls the latest docker image.
- When it receives a notification from Uptime Kuma, a service that monitors the availability of websites, stating that the Hugging Face Space is down, it tries to reboot it every 2 minutes, until Uptime Kuma sends a notification stating it's back up.

This project is built with Python, Flask, and Docker.

## Installation and Usage

To install and run this project, you need to have Python 3.8 or higher, Docker, and Docker Compose installed on your machine. You also need to have a Hugging Face account and a Hugging Face Space that you want to automate.

Follow these steps to set up the project:

- Clone this repository and navigate to the project directory.
- Create a virtual environment and activate it.
- Install the required packages with `pip install -r requirements.txt`.
- Create a `.env` file and add the following environment variables:

  - `SERVER_PORT`: the port you want to use for the server. Default port is `5000`
  - `DEBUG`: Flask debug, true or false. Default is `false`
  - `IMAGE_NAME`: the docker image that Watchtower is watching
  - `USERNAME`: your Hugging Face username. You can find your username on your profile page [here](https://huggingface.co/settings/profile).
  - `TOKEN`: your Hugging Face token. Use a token with write access. You can generate a token from your settings page [here](https://huggingface.co/settings/tokens).
  - `OWNER`: the owner of the Hugging Face Space.
  - `NAME`: the name of the Hugging Face Space

- Run `docker-compose up -d` to start the webhook server and the services.
- Configure Watchtower and Uptime Kuma to send notifications to the webhook server, using the URLs `http://localhost:5000/webhook`.

## License

This project is licensed under the MIT License. See the [LICENSE] file for more details.

## Acknowledgements

This project uses the following resources and services:

- [Hugging Face](https://huggingface.co/), a platform for natural language processing and deep learning.
- [Watchtower](https://github.com/containrrr/watchtower), a service that monitors the updates of Docker images.
- [Uptime Kuma](https://github.com/louislam/uptime-kuma), a service that monitors the availability of websites.
- [Flask](https://flask.palletsprojects.com/en/3.0.x/), a micro web framework for Python.
- [Docker](https://www.docker.com/), a platform for building and running containerized applications.
- [Docker Compose](https://docs.docker.com/compose/), a tool for defining and running multi-container applications with Docker.
