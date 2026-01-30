from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from pyshorteners import Shortener
from PyQt5.QtCore import pyqtSlot
from os import path
import qrcode
import sys

def CREATE_SHORT_URL(url):
    link = Shortener()
    return link.tinyurl.short(url)

def CREATE_QRCODE(link):
    img = qrcode.make(link)
    img.save("qrcode.png")

def loadFile(file):
    base_path = getattr(sys, "_MEIPASS", path.dirname(path.abspath(__file__)))
    return path.join(base_path, file)
class QrCode(QMainWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        loadUi(loadFile("./qrcode-builder.ui"), self)
        self.show()

    def getUrl(self):
        return self.url1.text()
    
    def setShortUrl(self, url):
        return self.url2.setText(url)

    @pyqtSlot()
    def on_gerar_clicked(self):
        valor = self.getUrl()

        if valor == "":
            self.showMessage("Erro", "URL inválida!")
            return
        else:
            try:
                url = CREATE_SHORT_URL(valor)
                CREATE_QRCODE(url)
                self.setShortUrl(url)
                self.img.setPixmap(QPixmap("qrcode.png"))
                self.salvar.setEnabled(True)
            except:
                self.showMessage("Erro", "URL inválida!")

    @pyqtSlot()
    def on_salvar_clicked(self):
        self.salvarArquivo()
        
    def salvarArquivo(self):
        nomeArquivo, _ = QFileDialog.getSaveFileName(self, "Salvar Imagem")

        if nomeArquivo:
            caminho = path.dirname(nomeArquivo)
            nome = nomeArquivo.removeprefix(caminho)
            self.showMessage("Salvo", "Imagem salva com sucesso!")
            self.reset()

            with open("qrcode.png", "rb") as fotoQrcode:
                dadosQrcode = fotoQrcode.read()

            with open(caminho+f"{nome}.png", "wb") as foto:
                foto.write(dadosQrcode)

    def reset(self):
        self.url1.setText("")
        self.url2.setText("")
        self.img.clear()
        self.salvar.setDisabled(True)

    def showMessage(self, title, message):
        QMessageBox.information(self, title, message)


if __name__ == "__main__":
    app = QApplication([])
    tela = QrCode()
    app.exec_()