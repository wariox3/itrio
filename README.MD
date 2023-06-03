# Backend ERP

Para instalar el proyecto debes seguir las siguientes instrucciones en la terminar

```sh
git clone
cd itrio
crear archivo al nivel de manage.py llamado .env con estas variables

DATABASE_USER='user'
DATABASE_CLAVE='clave'
DATABASE_HOST='localhost'
DATABASE_NAME='bdprueba'
DATABASE_PORT='5432'
KEY_SENDGRID='xx'

python3 -m venv venv
source venv/bin/activate
pip3 install -r requerimientos.txt
cd itrioapp
python3 manage.py runserver
# Migrar la base de datos -> Debe estar creada
python3 manage.py migrate
```