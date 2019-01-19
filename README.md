# Diplomova praca

## Generovanie API key

```bash
server # echo `pwgen 80 1` "= ja@example.org" >> /etc/beeeon/server/apikeys.properties
```

## Rozsahy prikladov (examples)

* 0000 - priklad s funkciami, ktore sa spustaju a ponukaju prehlad toho, co je v systeme dosutupne

* 0100 - 0199 - priklady pre Klarku

* 0200 - 0299 - priklady pre Peta

## Import DB

### Full db

```bash
    mysql -u root -p statistiky  < measured_peto.sql; \
    mysql -u root -p statistiky  < measured_klarka.sql
```

### Reduced db

```bash
    mysql -u root -p statistiky  < measured_peto_reduced.sql; \
    mysql -u root -p statistiky  < measured_klarka_reduced.sql
```

## Export DB

### Full db

```bash
    mysqldump -uroot -p statistiky measured_peto  > measured_peto.sql; \
    mysqldump -uroot -p statistiky measured_klarka  > measured_klarka.sql
```

### Reduced db

```bash
    mysqldump -uroot -p statistiky measured_peto_reduced  > measured_peto_reduced.sql; \
    mysqldump -uroot -p statistiky measured_klarka_reduced  > measured_klarka_reduced.sql
```
