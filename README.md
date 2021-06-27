## Προηγμένες Τεχνικές Διαχείρισης Υπολογιστικών Υποδομών - ΠΜΣ Χαροκόπειο Πανεπιστήμιο - 2021

#### Η εφαρμογή αναπτύχθηκε στα πλαίσια του παραπάνω μαθήματος και αφορά την καταγραφή ζημιών στη μελισσοκομία. Οδηγός για τις λειτουργικότητες της εφαρμογής υπάρχει στον φάκελο QuickStart-App. Για την εγκατάσταση της εφαρμογής ακολούθησε τα παρακάτω βήματα. 


1. Αφού κάνεις git clone το project ακολούθησε τις οδηγίες του README.md στο path ./vagrant για να στήσεις το εικονικό περιβάλλον που θα τρέξει η εφαρμογή

```bash
git clone https://github.com/theohitman/pms18.git
```

2. Τρέξε το playbooks/openssl_certificates.yml για να δημιουργηθούν τα πιστοποιητικά του web server. Τα πιστοποιητικά αποθηκεύονται στο path ./ansible/files/certs

```bash
ansible-playbook playbooks/openssl_certificates.yml 
```
3. Τρέξε το playbooks/postgresql.yml για εγκατάσταση της PostgreSQL στον db01. Επειδή αυτό το playbook χρησιμοποιεί ρόλο, πρέπει να γίνει εγκατάσταση του geerlingguy.postgresql role στην ansible.

```bash
ansible-galaxy install geerlingguy.postgresql
ansible-playbook playbooks/postgresql.yml
```

4. Ακολούθησε τις οδηγίες του README.md στο path ./owncloud για την εγκατάσταση και παραμετροποίηση του ownCloud

```bash
# Σύνδεση στο ownCloud
http://192.168.135.112/owncloud 
```

5. Τρέξε το playbooks/mailhog.yml για την εγκατάσταση και παραμετροποίηση του MailHog

```bash
ansible-playbook playbooks/mailhog.yml
# Σύνδεση στο mailhog
http://192.168.135.112:8025
```

6. Τρέξε το playbooks/beehives.yml για εγκατάσταση και παραμετροποίηση της εφαρμογής Beekeeper App και Nginx Web Server. By default η εγκατάσταση του Beekeeper App γίνεται στο VM app01 και του Nginx Web Server στο VM lb01. Επίσης δημιουργεί βάση με όνομα beekeeper_db, χρήστη beekeeper_user με pass beekeeper_pass στο VM db01.

```bash
ansible-playbook playbooks/beehives.yml
```

7. Πρόσβαση στην εφαρμογή Beekeeper App από browser στο παρακάτω URL

```bash
https://192.168.135.101/
# Default Admin Credentials
admin
Admin1
```