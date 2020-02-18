# TekniBridge

[![GitLab pipeline](https://img.shields.io/gitlab/pipeline/ioteknikringen/teknibridge?style=for-the-badge)](https://gitlab.com/ioteknikringen/teknibridge/builds) [![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://img.shields.io/badge/Project%20Status-Active-brightgreen?style=for-the-badge)](https://www.repostatus.org/#active) [![Licence](https://img.shields.io/badge/Licence-BSD_2--Clause-black?style=for-the-badge)](./LICENCE)

## Table of Contents
+ [About](#about)
+ [Getting Started](#getting_started)
+ [Testing](#testing)
+ [Usage](#usage)

## About <a name = "about"></a>
This project is part of TekniIoT, a simple DIY IoT lighting project. Specifically, this is the bridge between [TekniFront](https://gitlab.com/ioteknikringen/teknifront) and the light controllers. Currently, two light controllers are supported: WS2811 LED strips and Yeelight WiFi bulbs.

## Getting Started <a name = "getting_started"></a>
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [usage](#usage) for notes on how to deploy the project on a Raspberry Pi.

### Prerequisites
This project requires Python 3, currently only 3.7 is actively supported and tested.

We will be using a virtual environment for our Python installation. Install either [`virtualenv`](https://virtualenv.pypa.io/en/stable/installation.html) or [`direnv`](https://direnv.net/docs/installation.html) if you haven't already.

### Installing<a name = "installing"></a>
Setup `virtualenv`:
```bash
# Create a virtual Python environment.
virtualenv venv

# Activate the virtual environment.
source venv/bin/activate
```

Or as an alternative to `virtualenv`, one can use `direnv`:
```bash
echo "layout_python3" > .envrc
direnv allow
```

Install all `pip` dependencies.
```bash
pip install -r requirements.txt

# Optional dev dependencies, e.g. needed for static code analysis tools
pip install -r requirements-dev.txt
```

Now the application can be started with:
```bash
python src/cli.py
```

Or if you want to have the simulator enabled:
```bash
SIMULATE=1 python src/cli.py
```
Which will look something like this:
![Screenrecording](./docs/img/screenrecording_visualizer.gif)


## Testing<a name = "testing"></a>
In order to run the tests, you have to have the optional development dependencies installed in [Installing](#installing)

Run `pyre` to check the type hinting, the CI will fail when this check won't pass:
```bash
pyre --source-directory src/ check
```

## Usage <a name = "usage"></a>
### Deploy to Raspberry Pi

If you want to use this project to control an LED strip using PWM, then you will need to disable the audio output first. Run the following command to prevent audio from being enabled at startup, afterwards reboot for the changes to take effect.

```bash
sudo mkdir  /etc/modprobe.d && echo "blacklist snd_bcm2835" > sudo tee -a /etc/modprobe.d/alsa-blacklist.conf

sudo reboot now
```

The default method of deploying to production environments is by using continious deployment, which can be found in [.gitlab-ci.yml](./.gitlab-ci.yml). To set this up:
  1. Fork this repository on Gitlab, either Gitlab.com any other instance works. Alternatively, you can use any Git remote and use [Gitlab's mirroring](https://docs.gitlab.com/ee/user/project/repository/repository_mirroring.html) to handle the contrinious deployment for you.
  2. [Install the Gitlab Runner](https://docs.gitlab.com/runner/install/linux-repository.html) on your Raspberry Pi.
  3. Make the `gitlab-runner` user root. This is necessary, as we will need elevated rights when deploying this codebase as a Unix service.
  4. Register the [Gitlab runner](https://docs.gitlab.com/runner/register/):
     1. `sudo gitlab-runner register`
     2. `Please enter the gitlab-ci coordinator URL (e.g. https://gitlab.com )` 
        Enter the hostname of your Gitlab instance, if you forked this project, then it will be `https://gitlab.com`.
     3. `Please enter the gitlab-ci token for this runner` :
        Go to the fork of this repository, under `Settings > CI/CD > Runners` you will find the registration token, add it here.
     4. `Please enter the gitlab-ci description for this runner`
        Give your runner a name, this can be whatever you like.
     5. `Please enter the gitlab-ci tags for this runner (comma separated):`
        Tag this instance, the pipeline will look for the `production` tag, hence this needs to be present to work. However, you're free to add other tags as well.
     6. `Please enter the executor: ssh, docker+machine, docker-ssh+machine, kubernetes, docker, parallels, virtualbox, docker-ssh, shell:`
        Enter `shell`.
  5. If no pipeline is automatically started, go to your fork and under "CI / CD" you can initiate a new pipeline, which should provision your Raspberry Pi and deploy the project.

### Prepare Yeelight

Use the Yeelight app to enable LAN Control of all lights you want the bridge to control. After deployment, all lights on the local network are automatically picked up and "bridged". This will take at least 10 seconds after the bridge is started.
