import sys
import os
from PyQt5.QtGui import QTextLength
import requests
import json
import getpass
from threading import Thread
from tqdm import tqdm
from pathvalidate import sanitize_filename
import zipfile


from main import *
from ui_functions import *

from PyQt5 import QtCore

# GLOBAL_VARIABLE
GLOBAL_WINDOW = None

downloadThreading = None
format_sizeof = tqdm.format_sizeof

pathGame = f"C:/Users/{getpass.getuser()}/AppData/Roaming/Bleach/client/otclient.exe"
url = "http://66.70.148.217/launcher"

class downloadFiles(QtCore.QObject):
    attBar = QtCore.pyqtSignal(int, str, str, str, str, str, bool)
    attClient = QtCore.pyqtSignal(int, str, str, str, str, str, bool)
    attFiles = QtCore.pyqtSignal(int, str, str, str, str, str, bool)


    @QtCore.pyqtSlot()
    def download(self):
        vers = f"C:/Users/{getpass.getuser()}/AppData/Roaming/Bleach/launcher/Version.json"
        arq_json = ler_json(vers)
        archives = arq_json['archives']
        temp = 0
        stats = ""
        count = 0
        for archive in archives:
            temp += 1
            baseFolder = archive["folder"]
            filename = archive["archive"]
            link = baseFolder+filename
            print(f"Link: {link}")
            req = requests.get(f"{url}{link}", stream = True)
            total_size = int(req.headers['content-length'])
            folderPathFile = f"C:/Users/{getpass.getuser()}/AppData/Roaming/Bleach/client/{baseFolder}"
            fullPathFile = f"C:/Users/{getpass.getuser()}/AppData/Roaming/Bleach/client/{baseFolder}/{filename}"
            if not os.path.exists(folderPathFile):
                os.makedirs(folderPathFile, True)

            #if not os.path.isfile(fullPathFile):
            try:
                progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
                with open(fullPathFile, 'wb') as f:
                    for data in req.iter_content(chunk_size = 4096):
                        if data:
                            progress_bar.update(len(data))
                            f.write(data)
                            current_size = os.path.getsize(fullPathFile)
                            percentg = round((int(current_size)/int(total_size))*100)
                            rate = progress_bar.format_dict['rate']
                            unit = progress_bar.format_dict['unit']
                            rate_noinv_fmt = ((format_sizeof(rate) if progress_bar.unit_scale else
                                            '{0:5.2f}'.format(rate)) if rate else '?') + unit + '/s'
                            currentSize = getStandartSize(current_size)     
                            totalSize = f"/{getStandartSize(total_size)}"     
                            count = len(archives)
                            count = f"{temp}/{count}"
                            stats = "Atualizando Arquivos."
                            self.attBar.emit(percentg, rate_noinv_fmt, currentSize, totalSize, str(count), stats, False)

            except Exception as Erro:
                print(f"Erro no download. {Erro}")
                self.attBar.emit(0, "", "", "", str(count), "Erro no download.", False)

        self.attBar.emit(100, "", "", "", "", "Client Atualizado.", True)
        info = 'http://66.70.148.217/launcher/info.txt'
        req = requests.get(info, stream = True)
        text = req.text
        text = text.split('\r\n')
        newVersion = text[1]
        vers = f"C:/Users/{getpass.getuser()}/AppData/Roaming/Bleach/launcher/version.txt"
        VersionTXT = open(vers, 'w+')
        VersionTXT.write(newVersion)
        VersionTXT.close()
        checkAttArchives(GLOBAL_WINDOW)

    @QtCore.pyqtSlot()
    def downloadClient(self):
        url = 'http://66.70.148.217/launcher/info.txt'
        req = requests.get(url, stream = True)
        text = req.text
        text = text.split('\r\n')
        url = text[0]
        #url = "http://66.70.148.217/launcher/Bleach.zip"
        fullPathFile = f"C:/Users/{getpass.getuser()}/AppData/Roaming/Bleach/Bleach.zip"
        stats = ""
        print(f"Link: {url}")
        req = requests.get(url, stream = True)
        total_size = int(req.headers['content-length'])
        try:
            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
            with open(fullPathFile, 'wb') as f:
                for data in req.iter_content(chunk_size = 4096):
                    if data:
                        progress_bar.update(len(data))
                        f.write(data)
                        current_size = os.path.getsize(fullPathFile)
                        percentg = round((int(current_size)/int(total_size))*100)
                        rate = progress_bar.format_dict['rate']
                        unit = progress_bar.format_dict['unit']
                        rate_noinv_fmt = ((format_sizeof(rate) if progress_bar.unit_scale else
                            '{0:5.2f}'.format(rate)) if rate else '?') + unit + '/s'
                        currentSize = getStandartSize(current_size)     
                        totalSize = f"/{getStandartSize(total_size)}"
                        count = "1/1"
                        stats = "Atualizando Arquivos."
                        self.attClient.emit(percentg, rate_noinv_fmt, currentSize, totalSize, count, stats, False)
            data = zipfile.ZipFile(fullPathFile)
            os.makedirs(f"C:/Users/{getpass.getuser()}/AppData/Roaming/Bleach/client/", True)
            data.extractall(f"C:/Users/{getpass.getuser()}/AppData/Roaming/Bleach/client/")
            data.close()
            os.remove(fullPathFile)
                        

        except Exception as Erro:
            print(f"Erro no download. {Erro}")
            self.attClient.emit(0, "", "", "", "", "Erro no download.", False)

        self.attClient.emit(100, "", "", "", "", "Client Atualizado.", True)


    @QtCore.pyqtSlot()
    def checkAttFiles(self):
        att = f"C:/Users/{getpass.getuser()}/AppData/Roaming/Bleach/launcher/Att.json"
        try:
            if not os.path.isfile(att):
                getAttJson("http://66.70.148.217/launcher/Att.json")
            
            try:
                with open(att) as f:
                    Json = json.load(f)
            except:
                getAttJson("http://66.70.148.217/launcher/Att.json")
                with open(att) as f:
                    Json = json.load(f)

            temp = 0
            archives = Json['archives']
            countArq = 0
            countTotal = 0
            newArchives = []
            for arq in archives:
                folderName = arq["folder"]
                fileName = arq["archive"]
                countTotal += 1
                folderPathFile = f"C:/Users/{getpass.getuser()}/AppData/Roaming/Bleach/client/{folderName}"
                fullPathFile = f"C:/Users/{getpass.getuser()}/AppData/Roaming/Bleach/client/{folderName}/{fileName}"
                if not os.path.exists(folderPathFile):
                    os.makedirs(folderPathFile, True)

                if not os.path.isfile(fullPathFile):
                    countArq += 1
                    newArchives.append({'folder': folderName, 'archive': fileName})

            for archive in newArchives:
                temp += 1
                folderName = archive["folder"]
                fileName = archive["archive"]
                fullPathFile = f"C:/Users/{getpass.getuser()}/AppData/Roaming/Bleach/client/{folderName}/{fileName}"
                folderPathFile = f"C:/Users/{getpass.getuser()}/AppData/Roaming/Bleach/client/{folderName}"
                if not os.path.exists(folderPathFile):
                    os.makedirs(folderPathFile, True)

                if not os.path.isfile(fullPathFile):
                    req = requests.get(f"{url}{folderName}/{fileName}", stream = True)
                    total_size = int(req.headers['content-length'])
                    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
                    with open(fullPathFile, 'wb') as f:
                        for data in req.iter_content(chunk_size = 4096):
                            if data:
                                progress_bar.update(len(data))
                                f.write(data)
                                current_size = os.path.getsize(fullPathFile)
                                percentg = round((int(temp)/int(countArq))*100)
                                rate = progress_bar.format_dict['rate']
                                unit = progress_bar.format_dict['unit']
                                rate_noinv_fmt = ((format_sizeof(rate) if progress_bar.unit_scale else
                                    '{0:5.2f}'.format(rate)) if rate else '?') + unit + '/s'
                                currentSize = getStandartSize(current_size)     
                                totalSize = f"/{getStandartSize(total_size)}"
                                count = f"{temp}/{countArq}"
                                stats = f"Atualizando Arquivos."
                                self.attFiles.emit(percentg, rate_noinv_fmt, currentSize, totalSize, str(count), stats, False)
            
            self.attFiles.emit(100, "", "", "", "", "Client Atualizado.", True)
            

        except Exception as Error:
            print(f"Erro no download. Erro: {Error}")

# obter tamanho atual do arquivo
def getStandartSize(size):
    itme = ['bytes', 'KB', 'MB', 'GB', 'TB']
    for x in itme:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size/=1024.0
    return size


def getVersionJson(url):
    vers = f"C:/Users/{getpass.getuser()}/AppData/Roaming/Bleach/launcher/Version.json"
    req = requests.get(url, stream = True)
    with open(vers, 'wb') as f:
        for chunk in req.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)


def getAttJson(url):
    att = f"C:/Users/{getpass.getuser()}/AppData/Roaming/Bleach/launcher/Att.json"
    req = requests.get(url, stream = True)
    with open(att, 'wb') as f:
        for chunk in req.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

def getNotices(url):
    req = requests.get(url, stream = True)
    folderPathFile = f"C:/Users/{getpass.getuser()}/AppData/Roaming/Bleach/launcher/news"
    fullPathFile = f"C:/Users/{getpass.getuser()}/AppData/Roaming/Bleach/launcher/news/path_notes.json"
    if not os.path.exists(folderPathFile):
        os.makedirs(folderPathFile, True)

    with open(fullPathFile, 'wb') as f:
        for chunk in req.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

def ler_json(arquivo):
    with open(arquivo, 'r', encoding='utf8') as f:
        return json.load(f)

def checkAttArchives(MainWindow):
    MainWindow.labelStats.setText("Calculando Atualizações.") # Envia mensagem para escrever na tela.
    MainWindow.archives = downloadFiles()
    MainWindow.thread = QtCore.QThread(MainWindow)
    MainWindow.archives.attFiles.connect(attInformation)
    MainWindow.archives.moveToThread(MainWindow.thread)
    MainWindow.thread.started.connect(MainWindow.archives.checkAttFiles)
    MainWindow.thread.start()


def checkCurrentVersion(MainWindow):
    global GLOBAL_WINDOW
    GLOBAL_WINDOW = MainWindow
    vers = f"C:/Users/{getpass.getuser()}/AppData/Roaming/Bleach/launcher/version.txt"

    try:
        with open(vers, 'r+') as VersionTXT:

            info = 'http://66.70.148.217/launcher/info.txt'
            req = requests.get(info, stream = True)
            text = req.text
            text = text.split('\r\n')
            newVersion = text[1]
            currentVersion = VersionTXT.read()
            try:
                if currentVersion != newVersion:
                    getVersionJson("http://66.70.148.217/launcher/version.json")
                    checkNotices(MainWindow, True)
                    MainWindow.labelStats.setText("Calculando Atualizações.") # Envia mensagem para escrever na tela.
                    MainWindow.info = downloadFiles()
                    MainWindow.thread = QtCore.QThread(MainWindow)
                    MainWindow.info.attBar.connect(attInformation)
                    MainWindow.info.moveToThread(MainWindow.thread)
                    MainWindow.thread.started.connect(MainWindow.info.download)
                    MainWindow.thread.start()
                    return False
                else:
                    MainWindow.progressBar.setProperty("value", 100)
                    MainWindow.labelStats.setText("O client esta atualizado") # Envia mensagem para escrever na tela.
                    VersionTXT.close()
            except:
                print(f"Ocorreu algum erro: {Exception}")
                MainWindow.labelStats.setText(f"Ocorreu algum erro: {Exception}")

            finally:
                VersionTXT.close()

    except Exception as erro:
        arq = open(vers, 'w+')
        arq.close()
        checkCurrentVersion(MainWindow)
        print(f"Erro: {erro}")
    
    return True


@QtCore.pyqtSlot(int, str, str, str, str, bool)
def attInformation(percent, rate, current_size, total_size, count, status, enable=False):
    global GLOBAL_WINDOW
    GLOBAL_WINDOW.progressBar.setProperty("value", percent)
    #GLOBAL_WINDOW.labelStats.setText(f'{str(percent)}%')
    if rate != "?B/s":
        GLOBAL_WINDOW.labelRate.setText(str(rate))
    if current_size != "0.0 bytes" and current_size != None:
        GLOBAL_WINDOW.labelSize.setText(f"{current_size}{total_size}")

    if not count == "":
        GLOBAL_WINDOW.labelCount.setText(count)

    if status != None:
        GLOBAL_WINDOW.labelStats.setText(f"{status}")

    if enable:
        GLOBAL_WINDOW.button_play.setEnabled(True)
    else: 
        GLOBAL_WINDOW.button_play.setEnabled(False)


def checkNotices(self, forceAtt = False):
    fullPathFile = f"C:/Users/{getpass.getuser()}/AppData/Roaming/Bleach/launcher/news/path_notes.json"
    self.labelStats.setText("Carregando noticias")

    # confere se foi forcado a baixar o arquivo path_notes.json
    if forceAtt:
        t = Thread(target=lambda: getNotices("http://66.70.148.217/launcher/path_notes.json"))
        t.daemon = True
        t.start()

    # Confere se o arquivo path_notes.json existe.
    if not os.path.isfile(fullPathFile):
        t = Thread(target=lambda: getNotices("http://66.70.148.217/launcher/path_notes.json"))
        t.daemon = True
        t.start()

    # tenta abrir o arquivo
    try:
        with open(fullPathFile) as f:
            arq_json = json.load(f)
        select = False
        self.listWidget.clear()
        for atts in arq_json['atts']:
            self.listWidget.addItem(atts['title'])
            if not select:
                select = True
                self.listWidget.setCurrentRow(0)
                self.labelAtts.setText(atts['content'])
                self.labelTittleAtts.setText(atts['title'])
    except: # caso nao consiga, entao inicia o download do arquivo e chama a funcao novamente
        t = Thread(target=lambda: getNotices("http://66.70.148.217/launcher/path_notes.json"))
        t.daemon = True
        t.start()
        checkNotices(self)

    print("Carregando noticias")

def attInformationInLabelAtt(self, item):
    fullPathFile = f"C:/Users/{getpass.getuser()}/AppData/Roaming/Bleach/launcher/news/path_notes.json"
    try:
        with open(fullPathFile) as f:
            arq_json = json.load(f)
        for atts in arq_json['atts']:
            if atts['title'] == item:
                self.labelAtts.setText(atts['content'])
                self.labelTittleAtts.setText(atts['title'])
    except: # caso nao consiga, entao inicia o download do arquivo e chama a funcao novamente
        t = Thread(target=lambda: getNotices("http://66.70.148.217/launcher/path_notes.json"))
        t.daemon = True
        t.start()
        attInformationInLabelAtt(self, item)


def openGame(self):
    self.close()
    os.startfile(pathGame)

def checkBaseDirectory(MainWindow):
    global GLOBAL_WINDOW
    GLOBAL_WINDOW = MainWindow
    folderPathFile = f"C:/Users/{getpass.getuser()}/AppData/Roaming/Bleach/client/"
    if not os.path.exists(folderPathFile):
        MainWindow.labelStats.setText("Calculando Atualizações.") # Envia mensagem para escrever na tela.
        MainWindow.client = downloadFiles()
        MainWindow.thread = QtCore.QThread(MainWindow)
        MainWindow.client.attClient.connect(attInformation)
        MainWindow.client.moveToThread(MainWindow.thread)
        MainWindow.thread.started.connect(MainWindow.client.downloadClient)
        MainWindow.thread.start()
        return False

    return True