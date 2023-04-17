# Backend ERP

Para instalar el proyecto debes seguir las siguientes instrucciones en la terminar

```sh
git clone
cd itrio
crear archivo itrioapp/itrioapp/bd.py
python3 -m venv venv
source venv/bin/activate
pip3 install -r requerimientos.txt
cd itrioapp
python3 manage.py runserver
# Migrar la base de datos -> Debe estar creada
python3 manage.py migrate --database=bd_seguridad
python3 manage.py migrate --database=bd_general

```