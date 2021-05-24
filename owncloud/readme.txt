sudo add-apt-repository ppa:ondrej/php
sudo apt-get update
sudo apt install apache2 mariadb-server mariadb-client
sudo apt install php7.3 libapache2-mod-php7.3 php7.3-{mysql,intl,curl,json,gd,xml,mb,zip}
wget https://download.owncloud.org/community/owncloud-complete-20210326.tar.bz2
tar -xjf owncloud-complete-20210326.tar.bz2
sudo cp -r owncloud /var/www

-----Configure Apache----
sudo vim /etc/apache2/sites-available/owncloud.conf

######################################
Alias /owncloud "/var/www/owncloud/"

<Directory /var/www/owncloud/>
  Options +FollowSymlinks
  AllowOverride All

 <IfModule mod_dav.c>
  Dav off
 </IfModule>
</Directory>
######################################

sudo ln -s /etc/apache2/sites-available/owncloud.conf /etc/apache2/sites-enabled/owncloud.conf

sudo su -

a2enmod rewrite
a2enmod headers
a2enmod env
a2enmod dir
a2enmod mime
a2enmod unique_id

chown -R www-data:www-data /var/www/owncloud/
systemctl restart apache2


-----Enable SSL-----

a2enmod ssl
a2ensite default-ssl
systemctl restart apache2

----Create User in Mariadb----
sudo mysql -u root
CREATE DATABASE owncloud;
GRANT ALL PRIVILEGES ON ownuser.* TO 'owncloud_user'@localhost IDENTIFIED BY 'ownpass';
FLUSH PRIVILEGES;