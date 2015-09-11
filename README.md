ureport web-participation
=======

A web-based application to facilitate registration of UReport users and participation in polls on the UReport platform.


### Setup:

You will need instances of:
- [ureport-web-participation](https://github.com/rapidpro/ureport-web-participation) (this app)
- [ureport](https://github.com/rapidpro/ureport)
- [rapidpro](https://github.com/rapidpro/rapidpro)

Install and get all instances up and running. Instructions for ureport and rapidpro are on their own sites. The following instructions relate to ureport-web-participation only.

It is recommended that you run:
- ureport-web-participation on `localhost:8200`
- ureport on `localhost:8100`
- rapidpro on `localhost:8000`

In RapidPro instance, `/temba/settings.py`:
- `SEND_WEBHOOKS = True`
- `SEND_MESSAGES = True` (careful: will send real emails!)

In project root:
- `virtualenv env`
- `pip install reqs/dev.txt`
- `cp env_vars.txt env_vars && chmod 755 env_vars`
- edit `env_vars` with your own values
- `source ./env_vars`
- `psql postgres`
  - `create database webparticipation`
- `python manage.py createsuperuser`
- `python manage.py migrate`
- `python manage.py celery worker`
- `python manage.py celery beat`


#### Set up nginx reverse proxy

- add this line to your hosts file (`/etc/hosts`):
  - `127.0.0.1 ureport.dev`
- install nginx and start with:
  - `sudo nginx -c /path/to/ureport-web-participation/nginx.conf`

You will now have an app on ureport.dev that serves from both ureport and ureport-web-participation


### Technologies:

- Django>=1.7.7,<=1.8.0
- PostgreSQL (9.4.1)


### Troubleshooting:
If application is hanging, verify:
- RapidPro settings for web-participation: https://rapidpro.ngrok.com/api/v1/external/received/{web-channel}
- RapidPro channel is posting responses to the correct web-participation URL
- The organisation unit in RapidPro has credit; otherwise top up with more credit.

If the app hangs on submitting email for verification
- Verify the email settings
- Verify that the flow in RapidPro


### Run tests with coverage

    pip install -r reqs/test
    python manage.py test_coverage --settings=webparticipation.settings.test
