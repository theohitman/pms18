## Προηγμένες Τεχνικές Διαχείρισης Υπολογιστικών Υποδομών

1. Ακολούθησε τις οδηγίες του README.md στο path ./vagrant για να στηθεί το εικονικό περιβάλλον που θα τρέξει η εφαρμογή

2. Τρέξε το playbooks/openssl_certificates.yml για να δημιουργηθούν τα πιστοποιητικά του web server

```bash
ansible-playbook playbooks/openssl_certificates.yml 
```

3. Τρέξε το playbooks/beehives.yml για να παραμετροποιηθούν τα VMs για την εφαρμογή

```bash
ansible-galaxy install geerlingguy.postgresql
ansible-playbook playbooks/beehives.yml
```

4. Πρόσβαση από browser στο παρακάτω URL

```bash
https://192.168.135.101/
# Default Admin Credentials
admin
Admin1
```