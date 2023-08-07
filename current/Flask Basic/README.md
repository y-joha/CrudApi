How to Set Virtual Environment for Python

https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-22-04-server


How to Create a Flask-SQL Server
https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application

in order to install python packages use the command
pip3 install <package_name> ===> package_name can refer to any Python package or library

In order to make sure python is insall to have a rubust environment use this command

sudo apt install -y build-essential libssl-dev libffi-dev python3-dev

To Set a Python Venv use this command
sudo apt install -y python3-venv

Once a folder is created we initialize the environment with the command
python3 -m venv flask_env

and to activate it we run the command
source flask_env/bin/activate