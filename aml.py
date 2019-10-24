#!/usr/bin/python

import requests
import os
import pathlib
import json
import time
import datetime
import mysql.connector as mariadb
import config as cfg

# aktuelles Verzeichnis
current_dir = pathlib.Path(__file__).parent
# Log-Verzeichnis erzeugen
if not os.path.exists(current_dir.joinpath('logs')):
    os.makedirs(current_dir.joinpath('logs'))
# PID für monit
with open(current_dir.joinpath('aml.pid'), 'w') as pid_file:
    pid_file.write(str(os.getpid()))

###
while True:
    # Verbindung mit C4-Datenbank aufnehmen
    try:
        c4_db = mariadb.connect(host = cfg.db_c4['host'], user = cfg.db_c4['user'], password = cfg.db_c4['password'], db = cfg.db_c4['db'])
    except mariadb.Error as err:
        if err.errno == mariadb.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Zugang verweigert. Nutzername und Passwort korrekt?")
            with open(current_dir.joinpath('logs', str(datetime.datetime.now().strftime('%Y_%m_%d.log'))), 'a') as log_file:
                log_file.write(datetime.datetime.now().strftime('*** %d.%m.%Y - %H:%M:%S ***: Zugang DB C4 verweigert. Nutzername und Passwort korrekt?' + '\n'))
        elif err.errno == mariadb.errorcode.ER_BAD_DB_ERROR:
            print("Datenbank existiert nicht")
            with open(current_dir.joinpath('logs', str(datetime.datetime.now().strftime('%Y_%m_%d.log'))), 'a') as log_file:
                log_file.write(datetime.datetime.now().strftime('*** %d.%m.%Y - %H:%M:%S ***: Datenbank existiert nicht' + '\n'))
        else:
            print(err)
            with open(current_dir.joinpath('logs', str(datetime.datetime.now().strftime('%Y_%m_%d.log'))), 'a') as log_file:
                log_file.write(datetime.datetime.now().strftime('*** %d.%m.%Y - %H:%M:%S ***: ' + err + '\n'))
        raise
    cursor_c4 = c4_db.cursor(buffered=True)

    """
    Die ise_rowid, telefonnumer und anrufzeit aus der Datenbank selektieren, falls ein passender Datensatz gefunden wird
    """
    cursor_c4.execute(cfg.query)
    #cursor_c4.execute("SELECT anrufe.ise_rowid, telefonnummer,  CONVERT_TZ(STR_TO_DATE(anrufe.eingabezeit, '%Y%m%d%H%i%s'), '+00:00', '+02:00') as anrufzeit, anrufrichtung FROM anrufe WHERE ise_rowid = 'ise1234sys00k231iwkj00'")
    # Pruefen ob Datensatz vorhanden              
    if (cursor_c4.rowcount > 0):
        for result in cursor_c4:
            ise_id = result[0]
            telefonnummer = result[1]
            anrufzeit = result[2]

            # AML-JSON-Daten vom Server abrufen. Parameter: telefonnummer
            params = (
                ('number', telefonnummer),
            )
            try:
                response = requests.get(cfg.aml_server['url'] + ':' + cfg.aml_server['port'] + '/v1/getdata', params=params, auth=(cfg.aml_server['user'], cfg.aml_server['password']), cert=(str(current_dir.joinpath('cert', 'cacert.pem'))))
            except requests.exceptions.RequestException as e:
                with open(current_dir.joinpath('logs', str(datetime.datetime.now().strftime('%Y_%m_%d.log'))), 'a') as log_file:
                    log_file.write(datetime.datetime.now().strftime('*** %d.%m.%Y - %H:%M:%S ***: ' + e + '\n'))
                    
            # Pruefen ob AML-Daten fuer telefonnummber vorhanden sind
            if (response.json()[0]['status']) == 'no aml data':
                result_no_aml = datetime.datetime.now().strftime('*** %d.%m.%Y - %H:%M:%S ***: ') + "Datensatz vorhanden (" + (telefonnummer) + "). Keine zugehoerigen AML-Daten"
                print(result_no_aml)
                with open(current_dir.joinpath('logs', str(datetime.datetime.now().strftime('%Y_%m_%d.log'))), 'a') as log_file:
                    log_file.write(result_no_aml + '\n')

            # AML-Daten vorhanden
            else:
                # Verbindung mit Hilfsdatenbank
                try:
                    leitstelle_db = mariadb.connect(host = cfg.db_leitstelle['host'], user = cfg.db_leitstelle['user'], password = cfg.db_leitstelle['password'], db = cfg.db_leitstelle['db'])
                except mariadb.Error as err:
                    if err.errno == mariadb.errorcode.ER_ACCESS_DENIED_ERROR:
                        print("Leistelle-DB: Zugang verweigert. Nutzername und Passwort korrekt?")
                        with open(current_dir.joinpath('logs', str(datetime.datetime.now().strftime('%Y_%m_%d.log'))), 'a') as log_file:
                            log_file.write(datetime.datetime.now().strftime('*** %d.%m.%Y - %H:%M:%S ***: Zugang DB Leitstelle verweigert. Nutzername und Passwort korrekt?' + '\n'))
                    elif err.errno == mariadb.errorcode.ER_BAD_DB_ERROR:
                        print("Leitstelle-DB: Datenbank existiert nicht")
                        with open(current_dir.joinpath('logs', str(datetime.datetime.now().strftime('%Y_%m_%d.log'))), 'a') as log_file:
                            log_file.write(datetime.datetime.now().strftime('*** %d.%m.%Y - %H:%M:%S ***: Datenbank existiert nicht' + '\n'))
                    else:
                        print(err)
                    raise
                
                
                
                   
                # AML-Daten sichern
                for r in response.json():
                        aml_location_accuracy           = float(r['location_accuracy'])
                        aml_json                        = json.dumps(r, indent=4)
                        aml_status                      = r['status']
                        aml_number                      = r['number']
                        aml_emergency_number            = r['emergency_number']
                        aml_location_latitude           = r['location_latitude']
                        aml_location_longitude          = r['location_longitude']
                        aml_location_time               = r['location_time']
                        aml_location_altitude           = r['location_altitude']
                        aml_location_floor              = r['location_floor']
                        aml_location_source             = r['location_source']
                        aml_location_vertical_accuracy  = r['location_vertical_accuracy']
                        aml_location_confidence         = r['location_confidence']
                        aml_location_bearing            = r['location_bearing']
                        aml_location_speed              = r['location_speed']
                    
                        # Genauigkeit abfragen
                        cursor_leitstelle_query = leitstelle_db.cursor(buffered=True)
                    
                        get_accuracy_ls = "SELECT location_accuracy FROM aml WHERE ise_id = %s"
                        cursor_leitstelle_query.execute(get_accuracy_ls, (ise_id,))
                        records = cursor_leitstelle_query.fetchall()
                        
                        
                        if not records:
                            # Daten in Leitstllen-Datenbank schreiben
                            print("hallo 1")
                            cursor_leitstelle_insert = leitstelle_db.cursor(buffered=True)
                            write_aml_ls = ('REPLACE INTO aml '
                                        '(ise_id, status, number, emergency_number, location_latitude, location_longitude, location_time, location_altitude, location_floor, location_source, location_accuracy, location_vertical_accuracy, location_confidence, location_bearing, location_speed, anrufzeit) '
                                        'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ')
                            try:
                                cursor_leitstelle_insert.execute(write_aml_ls, (ise_id, aml_status, aml_number, aml_emergency_number, aml_location_latitude, aml_location_longitude, aml_location_time, aml_location_altitude, aml_location_floor, aml_location_source, aml_location_accuracy, aml_location_vertical_accuracy, aml_location_confidence, aml_location_bearing, aml_location_speed, anrufzeit))
                                leitstelle_db.commit()
                            except mariadb.Error as err:
                                print(err)
                                # LOG
                                with open(current_dir.joinpath('logs', str(datetime.datetime.now().strftime('%Y_%m_%d.log'))), 'a') as log_file:
                                    log_file.write(err + '\n')
                            aml_result = datetime.datetime.now().strftime('*** %d.%m.%Y - %H:%M:%S ***: ')\
                            + "Datensatz vorhanden. (" + telefonnummer + "). "\
                            + "AML-Daten vorhanden."\
                            + " Genauigkeit in m: "\
                            + str(aml_location_accuracy)
                            print(aml_result)
                            print(aml_json)
                            # LOG
                            with open(str(current_dir) + datetime.datetime.now().strftime('/logs/%Y_%m_%d.log'), 'a') as log_file:
                                log_file.write(aml_result + '\n')
                                log_file.write(aml_json + '\n')

                            cursor_leitstelle_insert.close()

                        elif float(r['location_accuracy']) < float(records[0][0]):
                            cursor_leitstelle_insert = leitstelle_db.cursor(buffered=True)
                            write_aml_ls = ('REPLACE INTO aml '
                                        '(ise_id, status, number, emergency_number, location_latitude, location_longitude, location_time, location_altitude, location_floor, location_source, location_accuracy, location_vertical_accuracy, location_confidence, location_bearing, location_speed, anrufzeit) '
                                        'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ')
                            try:
                                cursor_leitstelle_insert.execute(write_aml_ls, (ise_id, aml_status, aml_number, aml_emergency_number, aml_location_latitude, aml_location_longitude, aml_location_time, aml_location_altitude, aml_location_floor, aml_location_source, aml_location_accuracy, aml_location_vertical_accuracy, aml_location_confidence, aml_location_bearing, aml_location_speed, anrufzeit))
                                leitstelle_db.commit()
                            except mariadb.Error as err:
                                print(err)
                                # LOG
                                with open(current_dir.joinpath('logs', str(datetime.datetime.now().strftime('%Y_%m_%d.log'))), 'a') as log_file:
                                    log_file.write(err + '\n')
                            aml_result = datetime.datetime.now().strftime('*** %d.%m.%Y - %H:%M:%S ***: ')\
                            + "Datensatz vorhanden. (" + telefonnummer + "). "\
                            + "AML-Daten vorhanden."\
                            + " Genauigkeit in m: "\
                            + str(aml_location_accuracy)
                            print(aml_result)
                            print(aml_json)
                            # LOG
                            with open(str(current_dir) + datetime.datetime.now().strftime('/logs/%Y_%m_%d.log'), 'a') as log_file:
                                log_file.write(aml_result + '\n')
                                log_file.write(aml_json + '\n')
                        
                            cursor_leitstelle_insert.close()
                        cursor_leitstelle_query.close()                        

                aml_location_accuracy = records[0][0]
                aml_result = datetime.datetime.now().strftime('*** %d.%m.%Y - %H:%M:%S ***: ')\
                + "Datensatz vorhanden. (" + telefonnummer + "). "\
                + "AML-Daten vorhanden."\
                + " Genauigkeit in m: "\
                + str(aml_location_accuracy)
                print(aml_result)
                # LOG
                with open(str(current_dir) + datetime.datetime.now().strftime('/logs/%Y_%m_%d.log'), 'a') as log_file:
                    log_file.write(aml_result + '\n')
                    log_file.write(aml_json + '\n')
                        
                        
                        
                        
                        #aml_result = datetime.datetime.now().strftime('*** %d.%m.%Y - %H:%M:%S ***: ')\
                        #    + "Datensatz vorhanden. (" + telefonnummer + "). "\
                        #    + "AML-Daten vorhanden."\
                        #    + " Genauigkeit in m: "\
                        #    + str(aml_location_accuracy)
                        #    # LOG
                        #with open(str(current_dir) + datetime.datetime.now().strftime('/logs/%Y_%m_%d.log'), 'a') as log_file:
                        #    log_file.write(aml_result + '\n')
                        #    log_file.write(aml_json + '\n')


    # Kein neuer Datensatz in C4-Datenbank vorhanden
    else:
        # LOG
        no_result = datetime.datetime.now().strftime('*** %d.%m.%Y - %H:%M:%S ***: ')\
            + "Kein neuer Datensatz vorhanden"
        print(no_result)
        with open(current_dir.joinpath('logs', str(datetime.datetime.now().strftime('%Y_%m_%d.log'))), 'a') as log_file:
            log_file.write(no_result + '\n')

    c4_db.close()
    time.sleep(10)