## 1. Δημιουργία πιστοποιητικών για ασφαλή σύνδεση με τον server

Στο playbooks/openssl_certificates.yml τροποποιούμε αν θέλουμε κάποιες από τις μεταβλητές.

```bash
ansible-playbook playbooks/openssl_certificates.yml
```

Αφού τρέξουμε το playbook με την παραπάνω εντολή, δημιουργούνται τα certificates στο path ./files/certs/


## 2. Ρύθμιση και παραμετροποίση υπολογιστικών πόρων

```bash
ansible-playbook playbooks/project.yml
```

