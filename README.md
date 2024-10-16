# Open edX Platform

The [Open edX Platform](https://openedx.org) is a service-oriented platform for authoring and delivering online learning at any scale.  The platform is written in Python and JavaScript and makes extensive use of the Django framework. At the highest level, the platform is composed of a monolith, some independently deployable applications (IDAs), and micro-frontends (MFEs) based on the ReactJS.

This repository hosts the monolith at the center of the Open edX platform. Functionally, the edx-platform repository provides two services:

* CMS (Content Management Service), which powers Open edX Studio, the platform's learning content authoring environment;
* LMS (Learning Management Service), which delivers learning content.

## Documentation

Documentation can be found at https://docs.openedx.org/projects/edx-platform.

## Getting Started

### For Production

Installing and running an Open edX instance is not simple. We strongly recommend that you use a service provider to run the software for you. They have free trials that make it easy to get started: https://openedx.org/get-started/

However, if you have the time and expertise, then it is possible to self-manage a production Open edX instance. To help you build, customize, upgrade, and scale your instance, we recommend using `Tutor`, the community-supported, Docker-based Open edX distribution.

You can read more about getting up and running with a Tutor deployment at the [Site Ops home](https://docs.openedx.org).

### For Development

Tutor also features a `development mode` which will also help you modify, test, and extend edx-platform. We recommend this method for all Open edX developers.

### Bare Metal (Advanced)

It is also possible to spin up an Open edX platform directly on a Linux host. This method is less common and mostly undocumented. The Open edX community will only be able to provided limited support for it.

Running "bare metal" is only advisable for (a) developers seeking an adventure and (b) experienced system administrators who are willing to take the complexity of Open edX configuration and deployment into their own hands.

### System Dependencies

Interperters/Tools:
- Python 3.11 (preferred)
- Node 18

Services:
- MySQL 8.0
- Mongo 7.x
- Redis 7.x or Memcached _(optional)_
- ElasticSearch _(optional)_

Language Packages:

- Frontend:
  - `npm clean-install` (production)
  - `npm clean-install --dev` (development)
- Backend:
  - `uv sync` (production)
  - `uv sync --all-extras` (development)

### Build Steps

Create a MySQL database and a MySQL user with write permissions, and configure
Django to use them. Then, run migrations:
    ```bash
      ./manage.py lms migrate
      ./manage.py cms migrate
    ```

Build static assets (for more details, see `building static assets`):
    ```bash
      npm run build  # or, 'build-dev'
    ```

Download locales and collect static assets (can be skipped for development sites):
    ```bash
      make pull_translations
      ./manage.py lms collectstatic
      ./manage.py cms collectstatic
    ```

### Run the Platform

First, ensure `MySQL`, `Mongo`, and `Memcached/Redis` are running.

Start the LMS:
    ```bash
      ./manage.py lms runserver
    ```
Start the CMS:
    ```bash
      ./manage.py cms runserver
    ```
This will give you a mostly-headless Open edX platform. Most frontends have been migrated to "Micro-Frontends (MFEs)" which need to be installed and run separately. At a bare minimum, you will need to run the `Authentication MFE`,`Learner Home MFE`, and `Learning MFE` in order meaningfully navigate the UI.

- [Tutor](https://github.com/overhangio/tutor)
- [Site Ops home](https://docs.openedx.org/en/latest/site_ops/index.html)
- [Development mode](https://docs.tutor.edly.io/dev.html)
- [Building static assets](https://github.com/openedx/edx-platform/blob/open-release/redwood.master/docs/references/static-assets.rst)
- [Authentication MFE](https://github.com/openedx/frontend-app-authn/)
- [Learner Home MFE](https://github.com/openedx/frontend-app-learner-dashboard)
- [Learning MFE](https://github.com/openedx/frontend-app-learning/)

## More about Open edX

See the [Open edX site](https://openedx.org) to learn more about the Open edX world. You can find information about hosting, extending, and contributing to Open edX software. In addition, the Open edX site provides product announcements, the Open edX blog, and other rich community resources.
