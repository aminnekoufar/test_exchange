FROM python:3.11.3
# Author A.Nekofar@ipaam.ir

ENV PYTHONDOWNWIRTEBYCODE 1
ENV PYTHONBUFFRED 1

RUN mkdir -p /var/log/celeryd/ && \
    mkdir -p /var/log/django/ && \
    mkdir app ;



WORKDIR /app


COPY volumes/app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD while ! python3 manage.py sqlflush > /dev/null 2>&1 ; do sleep 1; done && \
    python manage.py collectstatic --noinput ;\
    python manage.py migrate --noinput && \
    python manage.py createsuperuser --noinput ;\
    gunicorn -b 0.0.0.0:8000 aban_challenge.wsgi --reload