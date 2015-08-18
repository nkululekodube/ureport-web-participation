ureport web-participation
=======

A web-based application to facilitate registration for potential ureport users and participation in polls by registered ureporters on the ureport platform.


###Setup:

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
- `cp env_vars.txt env_vars && chmod 755 env_vars`
- edit `env_vars` with your own values
- `source ./env_vars`
- `psql postgres`
  - `create database webparticipation`
- `python manage.py createsuperuser`
- `python manage.py migrate`
- `python manage.py celery worker`


#### Set up reverse proxy

- install nginx and start with sudo `sudo nginx`
- add this line to your hosts file (`/etc/hosts`):
  - `127.0.0.1 ureport.dev`
- add the following server block to `nginx.conf`:
```
    # ureport
    server {
        listen       80;
        server_name  ureport.dev;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout              60s;
        proxy_pass_request_headers      on;

        location /login/ {
            proxy_pass http://localhost:8200/login/;
        }

        location ~* ^/poll/(\d+)/respond/$ {
            proxy_pass http://localhost:8200/poll/$1/respond/;
        }

        location ~* ^/ureporter/([\d\w-]+)$ {
            proxy_pass http://localhost:8200/ureporter/$1/;
        }

        location ~* ^/(home|register|logout|forgot-password|password-reset|ureporter|rapidpro-receptor|send-token|confirm-token)/?$ {
            proxy_pass http://localhost:8200/$1/;
        }

        location /static {
            proxy_pass http://localhost:8200/static/;
        }

        # fallback to ureport.in main site
        location / {
            proxy_pass http://localhost:8100;
        }
    }
```
- and reload nginx: `sudo nginx -s reload`

You will now have an app on ureport.dev that serves from both ureport and ureport-web-participation


###Technologies:

- Django>=1.7.7,<=1.8.0
- PostgreSQL (9.4.1)


###Troubleshooting:
If application is hanging, verify that:
- RapidPro settings for web-participation
- - https://rapidpro.ngrok.com/api/v1/external/received/{web-channel}
- RapidPro channel is posting responses to the correct web-participation url
- The organisation unit in RapidPro has credit, otherwise top up more credit.

If the app hangs on submitting email for verification
- Verify the email settings,
- Verify that the flow in rapidPro update
