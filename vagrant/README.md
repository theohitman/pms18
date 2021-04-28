# Vagrant Installation and Usage

## Installation

```bash
sudo apt install virtualbox
wget https://releases.hashicorp.com/vagrant/2.2.14/vagrant_2.2.14_linux_amd64.zip
unzip vagrant_2.2.14_linux_amd64.zip
sudo mv vagrant /usr/local/bin
sudo apt install libarchive-tools
```

## Usage

```bash
# Start the virtual machine
vagrant up

# Copy vagrant ssh configuration to host machine
vagrant ssh-config >> ~/.ssh/config
```

