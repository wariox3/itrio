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
#Entorno
ENV='dev'
DOMINIO='reddoc.online'
#Credenciales sendgrid
KEY_SENDGRID='xyz'
#Credenciales S#
DO_CLAVE_ACCESO="xyz"
DO_CLAVE_SECRETA="xyz"
DO_REGION="xyz"
DO_BUCKET="xyz"

python3.10 -m venv ~/.venvs/itrio
source ~/.venvs/itrio/bin/activate
pip3 install -r requirements.txt
cd itrio
python3 manage.py runserver
# Migrar la base de datos -> Debe estar creada
python3 manage.py migrate
```