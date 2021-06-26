## Προηγμένες Τεχνικές Διαχείρισης Υπολογιστικών Υποδομών - ΠΜΣ Χαροκόπειο Πανεπιστήμιο - 2021

## Η εφαρμογή αναπτύχθηκε στα πλαίσια του παραπάνω μαθήματος και αφορά την καταγραφή ζημιών στη μελισσοκομία. Οδηγός για την εφαρμογή υπάρχει στον φάκελο QuickStart-App. Για την εγκατάσταση της εφαρμογής ακολούθησε τα παρακάτω βήματα. 
<br>
<br>

1. Ακολούθησε τις οδηγίες του README.md στο path ./vagrant για να στηθεί το εικονικό περιβάλλον που θα τρέξει η εφαρμογή

2. Τρέξε το playbooks/openssl_certificates.yml για να δημιουργηθούν τα πιστοποιητικά του web server

```bash
ansible-playbook playbooks/openssl_certificates.yml 
```

3. Τρέξε το playbooks/owncloud.yml για την εγκατάσταση και παραμετροποίηση του ownCloud

```bash
ansible-playbook playbooks/owncloud.yml
```

4. Τρέξε το playbooks/mailhog.yml για την εγκατάσταση και παραμετροποίηση του MailHog

```bash
ansible-playbook playbooks/mailhog.yml
```

5. Τρέξε το playbooks/beehives.yml για να παραμετροποιηθούν τα VMs για την εφαρμογή. Εγκατάσταση και παραμετροποίηση PostgreSQL, Beekeeper App και Nginx web server. Επειδή αυτό το playbook χρησιμοποιεί ρόλο, πρέπει να γίνει εγκατάσταση του geerlingguy.postgresql role. 

```bash
ansible-galaxy install geerlingguy.postgresql
ansible-playbook playbooks/beehives.yml
```

6. Πρόσβαση από browser στο παρακάτω URL

```bash
https://192.168.135.101/
# Default Admin Credentials
admin
Admin1
```