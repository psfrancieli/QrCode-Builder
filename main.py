from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from pyshorteners import Shortener
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMessageBox

def CREATE_SHORT_URL(url):
    link = Shortener()
    return link.tinyurl.short(url)

class QrCode(QMainWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        loadUi("qrcode-builder.ui", self)
        self.show()

    def getUrl(self):
        return self.url1.text()
    
    def setShortUrl(self, url):
        return self.url2.setText(url)

    @pyqtSlot()
    def on_gerar_released(self):
        valor = self.getUrl()

        if self.getUrl() == "":
            self.showMessage("Erro", "URL inválida!")
        else:
            url = CREATE_SHORT_URL(valor)
            self.setShortUrl(url)

    def showMessage(self, title, message):
        QMessageBox.information(self, title, message)


if __name__ == "__main__":
    app = QApplication([])
    tela = QrCode()
    app.exec_()