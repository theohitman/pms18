## 1. Δημιουργία πιστοποιητικών για ασφαλή σύνδεση με τον server

Στο playbooks/openssl_certificates.yml τροποποιούμε αν θέλουμε κάποιες από τις μεταβλητές και τρέχουμε την παρακάτω εντολή.

```bash
ansible-playbook playbooks/openssl_certificates.yml
```

Αφού τρέξει το playbook θα δημιουργηθούν τα certificates του server στο path files/certs/


## 2. Ρύθμιση και παραμετροποίση υπολογιστικών πόρων

```bash
ansible-playbook playbooks/project.yml
```

