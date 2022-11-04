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
    'oltName': "OLT Huawei - YouNet"
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


def OrgnnizePonName(tn):
    tn.write(b"display ont info 0 all | include port 0\n")
    time.sleep(5)

    return_pon_informartion = tn.read_until(
        'Control flag'.encode('utf-8'), 3).decode('utf-8').splitlines()

    for linha in return_pon_informartion:
        if "In port " in linha:
            pon = linha.split(',')[0].replace('In port', '').replace(' ', '')
            pons.append(pon)


def GetOntSignal(PonInfo, pon):
    sinais = []
    sinais_Bons = []
    sinais_Otimos = []
    sinais_Ruins = []
    for linha in PonInfo:

        if re.search(r'.*-[0-9]+\.[0-9]+', linha):
            try:
                sinal = float(linha.split('-')[2].split(' ')[0])*(-1)
                sinais.append(sinal)
                if sinal < -27.00:
                    id_onu = linha.split('-')[0].replace(' ', '')
                    sinais_Ruins.append(sinal)
                    SinaisRuins[pon].append({"idOnu": id_onu, "sinal": sinal})
                if sinal < -22.00 and sinal > -27.00:
                    sinais_Bons.append(sinal)
                if sinal < -9.00 and sinal > -22.00:
                    sinais_Otimos.append(sinal)
            except:
                continue
    

    if len(sinais) > 0:
        media = round(statistics.median_grouped(sinais),2)
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

                f = pon.split('/')[0]
                s = pon.split('/')[1]
                p = pon.split('/')[2]

                tn.write(
                    f'display ont info {f} {s} {p} {onu["idOnu"]}\n'.encode('utf-8'))
                time.sleep(.5)
                return_onuInformation = tn.read_until(
                    'Control flag'.encode('utf-8'), 3).decode('utf-8').splitlines()

                for linha in return_onuInformation:
                    if re.search(r'SN.+:', linha):
                        serial = linha.split(':')[1].split(
                            '(')[0].replace(' ', '')
                    if "Description" in linha:
                        description = linha.split(':')[1].replace(' ', '')
                        relatorioPons[pon]['onuComSinalRuim'].append(
                            {"idOnu": onu["idOnu"], "sinal": onu["sinal"], "description": description, "serial": serial})
    print(relatorioPons)


def GetOntProvisionedAndOntOnline(tn, pon):

    f = pon.split('/')[0]
    s = pon.split('/')[1]
    p = pon.split('/')[2]

    tn.write(
        f'display ont info {f} {s} {p} all | include port 0\n'.encode('utf-8'))
    time.sleep(1)
    PonInfo = tn.read_until(
        'Control flag'.encode('utf-8'), 3).decode('utf-8').splitlines()

    for linha in PonInfo:
        if "port 0/" in linha:
            srt_pon = linha.split(',')
            onuProvisioned = int(srt_pon[1].split(':')[
                                 1].lstrip().rstrip('\r'))
            onuOnline = int(srt_pon[2].split(':')[1].lstrip().rstrip('\r'))
            relatorioPons[pon] = {'online': onuOnline, 'provisionada': onuProvisioned, 'offline': (
                onuProvisioned-onuOnline)}


def ConnectOnOLTWithTelnet(ip, user, password, port):

    try:
        tn = telnetlib.Telnet(ip, port, 10)
    except Exception as e:
        print(e)
        return

    # tn.set_debuglevel(100)

    tn.read_until(b"name:")
    tn.write(user.encode('utf-8') + b"\n")
    time.sleep(.3)
    tn.read_until(b"password:")
    tn.write(password.encode('utf-8') + b"\n")
    time.sleep(.3)

    tn.write(b"enable\n")
    time.sleep(.3)
    tn.write(b"config\n")
    time.sleep(.3)
    tn.write(b"undo smart\n")
    time.sleep(.3)
    tn.write(b"scroll\n")
    time.sleep(.3)

    OrgnnizePonName(tn)

    for pon in pons:
        
        f = pon.split('/')[0]
        s = pon.split('/')[1]
        p = pon.split('/')[2]

        tn.write(f'interface gpon {f}/{s}\n'.encode('utf-8'))
        time.sleep(.3)
        tn.write(f'display ont optical-info {p} all\n'.encode('utf-8'))
        time.sleep(15)
        return_interfaceList = tn.read_until(
            'Control flag'.encode('utf-8'), 3).decode('utf-8').splitlines()

        tn.write(f'quit\n'.encode('utf-8'))
        time.sleep(.3)
        print(pon)
        SinaisRuins[pon] = []
        relatorioPons[pon] = {}
        GetOntProvisionedAndOntOnline(tn, pon)
        GetOntSignal(return_interfaceList, pon)

    GetDescriptionOfOnu(tn)

    with open('dados.js', 'w') as f:
        f.write(
            f'const relatorioPons={relatorioPons}\n\nconst dadosDoRelatorio={dadosDoRelatorio}\n\n')
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
