
sudo rm /etc/nginx/sites-enabled/default
sudo cp $PYTHONPATH/clientservice/conf/clientservice_nginx.conf /etc/nginx/sites-enabled/
pkill gunicorn
cd $PYTHONPATH/clientservice/conf
echo $PWD
gunicorn -c gunicorn.py service_app:app
sudo service nginx restart
