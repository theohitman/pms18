## Προηγμένες Τεχνικές Διαχείρισης Υπολογιστικών Υποδομών

1. Ακολούθησε τις οδηγίες του README.md στο path ./vagrant για να στηθεί το εικονικό περιβάλλον που θα τρέξει η εφαρμογή

2. Τρέξε το playbooks/openssl_certificates.yml για να δημιουργηθούν τα πιστοποιητικά του web server

```bash
ansible-playbook playbooks/openssl_certificates.yml 
```

3. Τρέξε το playbooks/owncloud.yml για την εγκατάσταση και παραμετροποίση του owncloud

```bash
ansible-playbook playbooks/owncloud.yml
```

4. Τρέξε το playbooks/mailhog.yml για την εγκατάσταση και παραμετροποίση του mailhog

```bash
ansible-playbook playbooks/mailhog.yml
```

5. Τρέξε το playbooks/beehives.yml για να παραμετροποιηθούν τα VMs για την εφαρμογή. Εγκατάσταση και παραμετροποίηση Postgresql, Beekeeper App και nginx web server. 

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