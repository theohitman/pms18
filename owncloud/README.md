## Εγκατάσταση και Παραμετροποίηση ownCloud

https://doc.owncloud.com/server/admin_manual/installation/manual_installation.html


1. Τρέξε το playbooks/owncloud.yml για την εγκατάσταση και παραμετροποίηση του owncloud. By default η εγκατάσταση του owncloud γίνεται στο VM app02. Δημιουργεί βάση με όνομα owncloud, χρήστη ownuser με pass ownpass στο VM db01.

```bash
ansible-playbook playbooks/owncloud.yml 
```

2. Αρχική σύνδεση στο owncloud από τον παρακάτω σύνδεσμο και δημιουργία λογαριασμού διαχειριστή
* http://192.168.135.112/owncloud 
* Δημιουργία admin account (Πρέπει να ενημερώσεις το .env αρχείο αν χρησιμοποιήσεις διαφορετικά credentials)
```bash
admin
Admin1
```
* Σύνδεση στη βάση

```bash
Database user: ownuser
Database password: ownpass
Database name: owncloud
Database host: db01
```