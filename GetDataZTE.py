#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import telnetlib
import sys
import statistics
import re
import matplotlib.pyplot as plt


pons = []
SinaisRuins = {}
SinaisRuinsComNome = {}
relatorioSinal = []
relatorioPons = {}
dadosDoRelatorio = {
    'data': "25/10/2022",
    'hora': "14:09",
    'oltName': "OLT Huawei"
}


def GeraGrafico(pon, onus):
    faixa = ['Ótimo', 'Bom', 'Ruim']
    # onus = [11, 20, 29]
    cor = ['#05F131', '#EAA706', '#F31616']
    # borda = ['255,255,0', '255,255,0', '255,255,0']
    explode = (0.09, 0.02, 0.02)

    plt.pie(onus, labels=faixa, colors=cor, autopct=lambda v: f"{sum(onus)*v/100:.0f} ONUs",
            explode=explode, wedgeprops={'edgecolor': 'black', 'linewidth': 1, 'antialiased': True})

    plt.legend(['-13 à -22', '-22 à -27', '-27 à -33'], loc=3)
    plt.title(
        f"Quantidade de ONU x Qualidade de sinal - PON {pon} ", fontsize=15)
    plt.axis('equal')

    # plt.show()
    arqName = f"{pon.replace('/','-')}.png"

    plt.savefig(arqName, format='png')
    plt.close()


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
    sinais_Bons = []
    sinais_Otimos = []
    sinais_Ruins = []
    for linha in PonInfo:
        if "dbm" in linha:
            sinal = float(linha.replace(
                'gpon-onu', '').replace('(dbm)', '').split('-')[1].replace(' ', ''))*(-1)
            sinais.append(sinal)
            if sinal < -27.00:
                id_onu = re.sub(r'-[0-9]+\.[0-9]+\(dbm\)',
                                '', linha).replace(' ', '')
                sinais_Ruins.append(sinal)
                SinaisRuins[pon].append({"idOnu": id_onu, "sinal": sinal})
            if sinal < -22.00 and sinal > -27.00:
                sinais_Bons.append(sinal)
            if sinal < -9.00 and sinal > -22.00:
                sinais_Otimos.append(sinal)

    if len(sinais) > 0:
        media = statistics.median_grouped(sinais)
        melhor = max(sinais)
        pior = min(sinais)

        qntOnu = [len(sinais_Otimos), len(sinais_Bons), len(sinais_Ruins)]

        GeraGrafico(pon, qntOnu)

        relatorioSinal.append(
            {"pon": pon, "melhor": melhor, "media": media, "pior": pior})
        relatorioPons[pon].update({'onusSinalBom': len(sinais_Bons), 'onusSinalOtimo': len(sinais_Otimos), 'onusSinalRuim': len(
            sinais_Ruins), 'melhorSinal': melhor, 'piorSinal': pior, 'mediaSinal': media, 'onuComSinalRuim': []})


def GetDescriptionOfOnu(tn):
    listaDePonsComSinalRuim = SinaisRuins.keys()
    for pon in listaDePonsComSinalRuim:
        if len(SinaisRuins[pon]) > 0:
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
                    if "Serial number:" in linha:
                        serial = linha.split(':')[1].replace(' ', '')
                        relatorioPons[pon]['onuComSinalRuim'].append(
                            {"idOnu": onu["idOnu"], "sinal": onu["sinal"], "description": description, "serial": serial})


def GetOntProvisionedAndOntOnline(tn, pon):
    pon_olt = pon.replace("_", "-olt_")
    tn.write(f'show gpon onu state {pon_olt}\n'.encode('utf-8'))
    time.sleep(1)
    PonInfo = tn.read_until(
        'Control flag'.encode('utf-8'), 3).decode('utf-8').splitlines()
    for linha in PonInfo:
        if "ONU Number" in linha:
            onuOnline = int(linha.split(':')[1].split('/')[0].replace(" ", ""))
            onuProvisioned = int(linha.split(
                ':')[1].split('/')[1].replace(" ", ""))
            relatorioPons[pon] = {'online': onuOnline, 'provisionada': onuProvisioned, 'offline': (
                onuProvisioned-onuOnline)}


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
            relatorioPons[pon] = {}
            GetOntProvisionedAndOntOnline(tn, pon)
            GetOntSignal(return_interfaceList, pon)

    GetDescriptionOfOnu(tn)

    
    with open('dados.js','w') as f:
        f.write(f'const relatorioPons={relatorioPons}\n\nconst dadosDoRelatorio={dadosDoRelatorio}\n\n')
    # print(relatorioPons)

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
