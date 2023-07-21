# datasets

## Instalation

To build the datasets, install the requirements with:
```bash
poetry shell
```

You can then build the datasets with:
```bash
python -m datasets.build
```

You may need to install the requirements of some drivers such as: https://pypi.org/project/mysqlclient/

## Test in an environment without docker

You can simulate this by trying to run this code inside a container:
`docker run --name test -d -i -t -v .:/datasets ubuntu:22.04`
Then run:
`docker exec -it test bash`

Then setup a `psql` as in https://colab.research.google.com/github/tensorflow/io/blob/master/docs/tutorials/postgresql.ipynb

```bash
# Inspred by https://colab.research.google.com/github/tensorflow/io/blob/master/docs/tutorials/postgresql.ipynb#scrollTo=YUj0878jPyz7
sudo apt-get -y -qq update
sudo apt-get -y -qq install postgresql
# Start postgresql server
sudo sed -i "s/#port = 5432/port = 5433/g" /etc/postgresql/14/main/postgresql.conf
sudo service postgresql start
# Set password
sudo -u postgres psql -U postgres -c "ALTER USER postgres PASSWORD 'pyqrlew-db'"
# Install python packages

```
