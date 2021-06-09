## Εγκατάσταση MailHog

https://github.com/mailhog/MailHog 

1. Ακολούθησε τις οδηγίες του README.md στο path ./vagrant για να στηθεί το εικονικό περιβάλλον που θα τρέξει η εφαρμογή

2. Τρέξε το playbooks/mailhog.yml για την εγκατάσταση του MailHog. By default η εγκατάσταση γίνεται στο app02.

```bash
ansible-playbook playbooks/mailhog.yml 
```

3. Σύνδεση στο Web UI του MailHog

http://192.168.135.112:8025

## Αποστολή mail με mhsendmail

Από οποιοδήποτε VM της υποδομής μας εγκαθιστούμε το mhsendmail και μπορούμε να στείλουμε δοκιμαστικό mail

### 1. Install mdsendmail 

```bash
wget https://github.com/mailhog/mhsendmail/releases/download/v0.2.0/mhsendmail_linux_amd64
sudo chmod +x mhsendmail_linux_amd64
sudo mv mhsendmail_linux_amd64 /usr/local/bin/mhsendmail
```

### 2. Send test mail

```bash
mhsendmail --smtp-addr="192.168.135.112:1025" test@mailhog.local <<EOF
From: Theo <theo@mailhog.local>
To: HUA <hua@mailhog.local>
Subject: Hello, HUA!

Hi

EOF
```
