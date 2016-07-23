import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import urllib.request

sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook


class HelloWord(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        layout = QGridLayout()

        details_label = QLabel('')

        url_label = QLabel('Url')
        self.url_textField = QLineEdit()
        self.url_textField.setPlaceholderText('ex: http://www.google.com')

        location_label = QLabel('Location')
        self.location_textField = QLineEdit()
        self.location_textField.setPlaceholderText('ex: c:/tempFiles')

        filename_label = QLabel('File Name')
        self.filename_textField = QLineEdit()
        self.filename_textField.setPlaceholderText('ex: Test.txt')

        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        self.progressBar.setAlignment(Qt.AlignHCenter)

        close_button = QPushButton('Close')
        download_button = QPushButton('Download')

        layout.addWidget(filename_label, 0, 0)
        layout.addWidget(self.filename_textField, 0, 1)

        layout.addWidget(url_label, 1, 0)
        layout.addWidget(self.url_textField, 1, 1)

        layout.addWidget(location_label, 2, 0)
        layout.addWidget(self.location_textField, 2, 1)

        layout.addWidget(self.progressBar, 3, 0)
        layout.addWidget(download_button, 3, 1)

        layout.addWidget(details_label, 4, 0)
        layout.addWidget(close_button, 4, 1)

        self.setLayout(layout)
        self.setWindowTitle('test Python')
        self.setFocus()

        close_button.clicked.connect(self.close)
        download_button.clicked.connect(self.download)

        self.url_textField.textChanged.connect(details_label.setText)

    def download(self):
        url = self.url_textField.text()
        saveLocation = self.location_textField.text()
        urllib.request.urlretrieve(url, saveLocation, self.progress_report)
        self.progressBar.setValue(100)

    def progress_report(self, blockNum, blocksize, totalSize):
        readSoFar = blockNum * blocksize
        if totalSize > 0:
            percent = readSoFar * 100 / totalSize
            self.progressBar.setValue(int(percent))


app = QApplication(sys.argv)
dialog = HelloWord()
dialog.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
