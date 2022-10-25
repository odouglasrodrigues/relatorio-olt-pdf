#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import telnetlib
import sys
import statistics
import json
import re


pons = []
SinaisRuins = {}
SinaisRuinsComNome = {}
relatorioSinal=[]


def OrgnnizePonName(dataPonsTotal):
    for linha in dataPonsTotal:
        if "gpon_" in linha:
            pon = linha.split(":")[1].replace('"', '').replace(" ", "")
            pons.append(pon)


def GetPonNameInfo():
    cmd = "snmpwalk -v2c -c public 190.123.65.230:65161 iso.3.6.1.2.1.31.1.1.1.1 | grep gpon_"
    shellcmd = os.popen(cmd)
    return shellcmd.read().splitlines()


def GetOntSignal(PonInfo, pon):
    sinais = []
    for linha in PonInfo:
        if "dbm" in linha:
            sinal = float(linha.replace(
                'gpon-onu', '').replace('(dbm)', '').split('-')[1].replace(' ', ''))*(-1)
            sinais.append(sinal)
            if sinal < (27.00*-1):
                id_onu = re.sub(r'-[0-9]+\.[0-9]+\(dbm\)',
                                '', linha).replace(' ', '')

                SinaisRuins[pon].append({"idOnu": id_onu, "sinal": sinal})
    

    if len(sinais) > 0:
        media = statistics.median_grouped(sinais)
        melhor = max(sinais)
        pior = min(sinais)

        relatorioSinal.append({"pon":pon,"melhor":melhor, "media":media, "pior":pior})


def GetDescriptionOfOnu(tn):
    listaDePonsComSinalRuim = SinaisRuins.keys()
    for pon in listaDePonsComSinalRuim:
        if len(SinaisRuins[pon])>0:
            SinaisRuinsComNome[pon] = []
            for onu in SinaisRuins[pon]:
                tn.write(
                    f'show gpon onu detail-info {onu["idOnu"]}\n'.encode('utf-8'))
                time.sleep(.5)
                return_onuInformation = tn.read_until(
                    'Control flag'.encode('utf-8'), 3).decode('utf-8').splitlines()
                for linha in return_onuInformation:
                    if "Name:" in linha:
                        description = linha.split(':')[1].replace(' ', '')
                        SinaisRuinsComNome[pon].append(
                            {"idOnu": onu["idOnu"], "sinal": onu["sinal"], "description": description})
    


def ConnectOnOLTWithTelnet(ip, user, password, port):
    OrgnnizePonName(GetPonNameInfo())

    try:
        tn = telnetlib.Telnet(ip, port, 10)
    except Exception as e:
        print(e)
        return

    # tn.set_debuglevel(100)

    tn.read_until(b"Username:")
    tn.write(user.encode('utf-8') + b"\n")
    time.sleep(.3)
    tn.read_until(b"Password:")
    tn.write(password.encode('utf-8') + b"\n")
    time.sleep(.3)
    tn.write(b'terminal length 0\n')
    time.sleep(.3)

    for pon in pons:
        if "_1/9" in pon:
            continue
        if "_1/12" in pon:
            continue
        if "_1/15" in pon:
            continue
        else:
            pon_olt = pon.replace("_", "-olt_")
            tn.write(f'show pon power olt-rx {pon_olt}\n'.encode('utf-8'))
            time.sleep(1)
            return_interfaceList = tn.read_until(
                'Control flag'.encode('utf-8'), 3).decode('utf-8').splitlines()
            print(pon)
            SinaisRuins[pon] = []
            GetOntSignal(return_interfaceList, pon)

    GetDescriptionOfOnu(tn)

    print(SinaisRuinsComNome)
    print("====\n====\n====\n")
    print(relatorioSinal)

    tn.write(b"exit\n")
    time.sleep(.3)
    tn.close()
    return


def main(ip, user, password, port):
    ConnectOnOLTWithTelnet(ip, user, password, port)


ip = sys.argv[1]
user = sys.argv[2]
password = sys.argv[3]
port = sys.argv[4]


if __name__ == "__main__":
    main(ip, user, password, port)
