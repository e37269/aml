#!/usr/bin/python

"""
IP-Adresse oder DNS-Namen eures C4 MariaDB-Servers, sowie Nutzername und Passwort
"""
db_c4 = {'host': '***',
         'user': '***',
         'password': '***',
         'db': 'c4'}

"""
IP-Adresse oder DNS-Namen eures Servers, auf dem die Hilfsdatenbank 'leitstelle' läuft, sowie Nutzername und Passwort
"""
db_leitstelle = {'host': '***',
         'user': '***',
         'password': '***',
         'db': 'leitstelle'}

"""
Zugangsdaten für den AML-Server
"""
aml_server = {'user': 'lst_werra_meissner_kreis',
              'password': 'd5ae58df8dd1a0a46a57415cd70112ec',
              'url': 'https://auskunft.notrufdaten.de',
              'port': '50443'}
              
"""
Query C4 Anrufe (verarbeiet werden ROW_ID, telefonnummer, anrufzeit)
"""
query = "SELECT anrufe.ise_rowid, telefonnummer,  CONVERT_TZ(STR_TO_DATE(anrufe.eingabezeit, '%Y%m%d%H%i%s'), '+00:00', '+02:00') as anrufzeit\
            FROM c4.anrufe\
                WHERE (anrufe.telefonnummer LIKE '01%' OR anrufe.telefonnummer LIKE '+491%')\
                AND (CONVERT_TZ(STR_TO_DATE(anrufe.eingabezeit, '%Y%m%d%H%i%s'), '+00:00', '+02:00') > ADDTIME(NOW(),'-00:01:10'))\
                    ORDER BY anrufe.eingabezeit DESC\
                    LIMIT 50"