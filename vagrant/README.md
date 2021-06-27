# Vagrant Εγκατάσταση και Χρήση Vagrantfile

Σηκώνουμε σε εικονικό περιβάλλον 5 VMs με Ubuntu 18.04 για τις ανάγκες της εφαρμογής

## Εγκατάσταση Vagrant

```bash
sudo apt install virtualbox
wget https://releases.hashicorp.com/vagrant/2.2.14/vagrant_2.2.14_linux_amd64.zip
unzip vagrant_2.2.14_linux_amd64.zip
sudo mv vagrant /usr/local/bin
sudo apt install libarchive-tools
```

## Χρήση του Vagrantfile 

```bash
# Install plugin
vagrant plugin install vagrant-hostmanager

# Start the virtual machines
vagrant up

# Copy vagrant ssh configuration to host machine
vagrant ssh-config >> ~/.ssh/config
```

