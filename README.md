# pyor
PyoR Experiment Lab - A plataform to manage experiments.

In datascience, specially when working with Deep Learning, it's common to run experiments that may take hours or even days. If you simply run it in your server, you don't know when it's done running unless you keep checking. And chances are that you will notice it's finished after quite some time. Even worse, you may notice that the experiment didn't work out and you should adjust the parameters and try again. Between each trial, you'll probably lose a lot of time. That's why we created PYOR. With it, you'll be able to enqueue lots of experiments and they will start one after the other or in parallel, depending on your configuration. Even better, when an experiment is done, you can be notified via Telegram.

# Features

- Create Tasks with name, script and auxiliar files. Both Python and R are compatible.
- Enqueue as many experiments as desired by selecting a registered Task and setting the parameters.
- Configure workers and the queues they will consume from. By default, there're two workers: sequential and parallel.
- Be notified when a experiment has been concluded

# How to use

## Prerequisites

You'll only need [Docker](https://docs.docker.com/engine/installation/) and [Docker Compose](https://docs.docker.com/compose/install/) installed in your computer. If you want to use GPU, you'll also need [nvidia-docker](https://github.com/NVIDIA/nvidia-docker/wiki/Installation) and [nvidia-docker-compose](https://github.com/eywalker/nvidia-docker-compose#installing).

This project use [dobi](https://dnephin.github.io/dobi) to configure the tasks like `run-dev`, `run-prod`, `refresh-backend-dependencies` and so on (`dobi.yaml` has all the tasks). You need to install dobi: [installation instructions](https://dnephin.github.io/dobi/install.html). If you're using linux, you can simply run `curl -L -o /usr/local/bin/dobi "https://github.com/dnephin/dobi/releases/download/v0.10/dobi-$(uname -s)"; chmod +x /usr/local/bin/dobi` to install it. Then, you just need to type `dobi <command>` to execute the available commands.

## Contributing

To contribute, clone the repository, run `dobi refresh-backend-dependencies` and open your IDE. For PyCharm, the Docker Compose Python Interpreter will be already defined. You just need to select it in `Settings > Project: pyor > Project Interpreter` and select the `Docker Compose`. Then, you should right click on the `backend` folder and `Mark directory as > Sources root`. After that, you're good to go. To run it in dev on the shell, run `dobi run-dev:attach`. It will run the backend in attached mode.

The frontend isn't running inside docker in development. So, you should have node installed and run `npm install` and `npm start` inside the `frontend` folder.
