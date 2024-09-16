# Website of the Ev.-Luth. Dreifaltigkeitskirchgemeinde Leipzig

This is the codebase of our website.

## Credits

This website uses

* a modified version of the template [Editorial](https://html5up.net/editorial) by [HTML5 UP | @ajlkn](https://html5up.net/) which is licensed under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/) including dependencies (see dreifaltigkeit/templates/README.txt),

* [FullCalendar v3.10.5](https://fullcalendar.io/) by [Adam Shaw](http://arshaw.com/) and others which is licensed under [MIT](https://github.com/fullcalendar/fullcalendar/blob/v3.10.5/LICENSE.txt) including dependencies (see [dreifaltigkeit/static/fullcalendar-3.10.5/lib](dreifaltigkeit/static/fullcalendar-3.10.5/lib)).


## Setup

Get [devenv](https://devenv.sh/) and then run:

    $ devenv up  # To install required packages and start PostgreSQL instance

Run in a second terminal:

    $ devenv shell  # To activate the developer environment

    $ export DREIFALTIGKEIT_SITE_ID=parish  # Or use kindergarden in other case

    $ export DJANGO_SECRET_KEY_FILE=django_secret_key.txt

    $ tr -dc [:alnum:] < /dev/urandom | head -c 50 > $DJANGO_SECRET_KEY_FILE  # Generate a secret key

    $ python manage.py migrate  # Setup database

    $ python manage.py createsuperuser  # Create a superuser for the admin panel

    $ python manage.py runserver

In case you changed urls.py or static file prefix, run:

    $ python manage.py generate_elm_file  # Some code generation for the elm client
