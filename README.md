
# Installation

## Docker
- Install docker.io and docker-compose and git
- This commands for linux debian based os and apt package manager
- if you use another os dont worry docker worked for all os keep calm and search for install dependese in your os

```bash
sudo apt update && \
    sudo apt -y install docker.io && \
    docker-compose &&\
    git;
```

- Change directory to volumes and get clone of project
```bash
cd volumes
git clone 'SRC-git-django'
```

-
# Build

- Check your internet is connected and have accses to docker hub 
- download and build docker images
```bash
docker volume create --name=db_aban
docker-compose build
```

# RUN
- run container and wait for complete download and install requrments and config...
```bash
docker-compose up
```
- for run container in background can use -d opthion
```bash
docker-compose up -d
```


- open browser and check django admin and api
```text
- url admin : localhost/admin
- url apis  : localhost/api-auth/login/
- url get list of currency : localhost/api-exchange/
- url get list of wallets : localhost/api-balance OR /api-balance/?balance_currency=usd
- url get balance check of currency you want change: localhost/api-exchange/get-wallet/?balance_currency=usd&convert_currency=ABA
- url get list confirm change : localhost/api-exchange/confirm-change/?convert_currency=ABA
- url post confirm change : localhost/api-exchange/confirm-change/?convert_currency=ABA
example post data {
    "balance_currency": USD,
    "balance_amount": 100,
    "converted_currency": ABA,
    "confirm_converted": 1234
}

```

# Devloper Options
- in defualt makemigrations and restart container is manual
```bash
docker-compose exec app python3 manage.py makemigrations --noinput 
```
- reboot continer for run migrate and restart django
```bash
docker-compose restart app
```

- for automatic makemigrations 
```text
in app/Dockerfile CMD in line 2 write 
python3 manage.py makemigrations --noinput && \
```
- for reboot continer when you change and save SourceCod can set command 
```text
in docker-compose.yml/app/-volumes:
 - .:/code
```

- containers automatic check healthy of own servise you can check from this command
```bash
docker ps 
```


# Devops Options
```text
docker build --ssh github=~/.ssh/gitlab -t buildtest .
ssh-add ~/.ssh/id_rsa 
ssh-add -L
sudo docker buildx bake --set app.ssh=&{SSH_AUTH_SOCK} -f docker-compose.yml app
```
