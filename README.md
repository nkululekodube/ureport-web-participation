ureport web-participation
=======

[![Build Status](https://snap-ci.com/_PXf2yTT7nzZ0jFfAayLXowazqyU6eW6OE21KP8VX50/build_image)](https://snap-ci.com/rapidpro/ureport-web-participation/branch/master)

A web-based application to facilitate registration for potential ureport users and participation in polls by registered ureporters on the ureport platform.


###Setup:

- `virtualenv env`
- `cp env_vars.txt env_vars && chmod 755 env_vars
- edit env_vars with your own values
- `source ./env_vars`
- `psql postgres`
  - `create database webparticipation`
- `python manage.py createsuperuser`
- `python manage.py migrate`

In RapidPro instance, /temba/settings.py:
- SEND_WEBHOOKS = True
- SEND_MESSAGES = True (careful: will send real emails!)

###Technologies:

- Django>=1.7.7,<=1.8.0

- PostgreSQL (9.4.1)


###Troubleshooting:
If the application is hanging, verify that:
- RapidPro setting for the web-participation
- - https://rapidpro.ngrok.com/api/v1/external/received/{web-channel}
- RapidPro channel is posting responses to the correct web-participation url
- The organisation unit in RapidPro has credit, otherwise top up more credit.

if the app hangs on submitting email for verification
- Verify the email settings,
- Verify that the flow in rapidPro update



