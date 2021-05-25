## Εγκατάσταση και Παραμετροποίηση OwnCloud

https://doc.owncloud.com/server/admin_manual/installation/manual_installation.html

1. Ακολούθησε τις οδηγίες του README.md στο path ./vagrant για να στηθεί το εικονικό περιβάλλον που θα τρέξει η εφαρμογή

2. Τρέξε το playbooks/owncloud.yml για την εγκατάσταση και παραμετροποίηση του owncloud. By default η εγκατάσταση γίνεται στο app02.

```bash
ansible-playbook playbooks/owncloud.yml 
```

3. Δημιουργία βάσης και χρήστη στην mariadb 

```bash
ssh app02
sudo mysql -u root
CREATE DATABASE owncloud;
GRANT ALL PRIVILEGES ON owncloud.* TO 'ownuser'@localhost IDENTIFIED BY 'ownpass';
FLUSH PRIVILEGES;
```

4. Αρχική σύνδεση στο owncloud και δημιουργία λογαριασμού διαχειριστή
* http://192.168.135.112/owncloud 
* Δημιουργία admin account της επιλογής σου
* Σύνδεση στη βάση
```bash
Database user: ownuser
Database password: ownpass
Database name: owncloud
```