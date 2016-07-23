import sys
import os
import urllib.request
import urllib.parse
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from urllib.parse import urlparse

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

        self.details_label = QLabel('')

        url_label = QLabel('Url')
        self.url_textField = QLineEdit()
        self.url_textField.setPlaceholderText('ex: http://www.google.com')

        folder_label = QLabel('Folder')
        self.folder_textField = QLineEdit()
        self.folder_textField.setPlaceholderText('ex: c:/tempFiles')

        filename_label = QLabel('File Name')
        self.filename_textField = QLineEdit()
        self.filename_textField.setPlaceholderText('ex: Test.txt')

        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        self.progressBar.setAlignment(Qt.AlignHCenter)

        close_button = QPushButton('Close')
        download_button = QPushButton('Download')
        browse_button = QPushButton('Browse')
        reset_button = QPushButton('Reset')

        self.getInfoFromUrl_checkbox = QCheckBox('Get Filename from Url')
        self.getInfoFromUrl_combobox = QComboBox()
        self.getInfoFromUrl_combobox.addItems(
            ['GetFileNameFromPath', 'GetFileNameFromUrl', 'GetFileNameFromPathAndTime', 'GetFileNameFromUrlAndTime'])

        layout.addWidget(url_label, 0, 0)
        layout.addWidget(self.url_textField, 0, 1)
        layout.addWidget(self.getInfoFromUrl_checkbox, 0, 2)

        layout.addWidget(folder_label, 1, 0)
        layout.addWidget(self.folder_textField, 1, 1)
        layout.addWidget(self.getInfoFromUrl_combobox, 1, 2)

        layout.addWidget(filename_label, 2, 0)
        layout.addWidget(self.filename_textField, 2, 1)

        layout.addWidget(self.details_label, 3, 0)
        layout.addWidget(browse_button, 3, 1)

        layout.addWidget(self.progressBar, 4, 0)
        layout.addWidget(download_button, 4, 1)

        layout.addWidget(reset_button, 5, 0)
        layout.addWidget(close_button, 5, 1)

        self.setLayout(layout)
        self.setWindowTitle('test Python')
        self.setFocus()

        close_button.clicked.connect(self.close)
        download_button.clicked.connect(self.download)
        browse_button.clicked.connect(self.browse_file)
        reset_button.clicked.connect(self.resetInputs)

        self.getInfoFromUrl_checkbox.stateChanged.connect(self.getInfoFromUrlChanged)
        self.url_textField.textChanged.connect(self.getInfoFromUrlChanged)
        self.getInfoFromUrl_combobox.currentIndexChanged.connect(self.getInfoFromUrlChanged)

    def current_milli_time(self):
        current_time = round(time.time() * 1000)
        return str(current_time)

    def getInfoFromUrlChanged(self):

        url = self.url_textField.text()
        combobox_currentIndex = self.getInfoFromUrl_combobox.currentIndex()

        if url:
            if self.getInfoFromUrl_checkbox.isChecked():

                parsed_url = urlparse(url)
                url_path = parsed_url[2]
                filename_time = self.current_milli_time()
                filename = filename_time;
                filename_temp = ''

                if combobox_currentIndex == 0:
                    filename_temp = url_path.split('/')[-1]
                    if filename_temp:
                        filename = filename_temp

                if combobox_currentIndex == 1:

                    filename_temp = url_path.replace('/', '_')
                    if filename_temp:
                        filename = filename_temp

                if combobox_currentIndex == 2:
                    filename_temp = url_path.split('/')[-1]
                    file_extention = filename_temp.split('.')[-1]

                    if file_extention:
                        file_extention = "." + file_extention;

                    filename_temp_array = filename_temp.split('.')
                    filename_temp_array.remove(filename_temp_array[-1])
                    filename_temp = "_".join(filename_temp_array)

                    if filename_temp:
                        filename = filename_temp + filename_time + file_extention

                if combobox_currentIndex == 3:
                    filename_temp = url_path.replace('/', '_')
                    file_extention = filename_temp.split('.')[-1]

                    if file_extention:
                        file_extention = "." + file_extention;

                    filename_temp_array = filename_temp.split('.')
                    filename_temp_array.remove(filename_temp_array[-1])
                    filename_temp = "_".join(filename_temp_array)

                    if filename_temp:
                        filename = filename_temp + filename_time + file_extention

                self.filename_textField.setText(filename)

    def browse_file(self):
        save_file = QFileDialog.getSaveFileName(self, caption="Save File As", directory=".", filter="All Files (*.*)")
        save_file_string = QDir.toNativeSeparators(save_file[0]);
        save_file_array = save_file_string.split(os.sep)
        self.filename_textField.setText(save_file_array[-1])
        save_file_array.remove(save_file_array[-1])
        self.folder_textField.setText(os.sep.join(save_file_array))

    def download(self):
        url = self.url_textField.text()

        if not (url and self.folder_textField.text() and self.filename_textField.text()):
            self.details_label.setText('Invalid field')
            return

        saveLocation = self.folder_textField.text().replace('/', os.sep).replace('\\\\', os.sep)
        saveFileName = self.filename_textField.text().replace('/', '').replace('\\', '')

        if os.path.isdir(saveLocation):
            if saveLocation[:-1].endswith(os.sep):
                saveLocation += saveFileName
            else:
                saveLocation += os.sep + saveFileName

            if os.path.exists(saveLocation):
                if self.showConfirmationDialog("File exist", "Override it?") == QMessageBox.Cancel:
                    return

            self.details_label.setText('')
            try:
                download = DownloadProcess(saveFileName, url, saveLocation)

                urllib.request.urlretrieve(url, saveLocation, self.progress_report)
                self.progressBar.setValue(100)
                QMessageBox.information(self, "Information", "Download completed.")
            except Exception:
                self.url_textField.setText('')
                QMessageBox.warning(self, "Download Error", "Download failed.")
                return
        else:
            self.details_label.setText('Folder not exist')

    def showConfirmationDialog(self, title, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        return msg.exec_()

    def progress_report(self, blockNum, blocksize, totalSize):
        readSoFar = blockNum * blocksize
        if totalSize > 0:
            percent = readSoFar * 100 / totalSize
            self.progressBar.setValue(int(percent))

    def resetInputs(self):
        self.url_textField.setText('')
        self.filename_textField.setText('')
        self.folder_textField.setText('')
        self.details_label.setText('')
        self.progressBar.setValue(0)


class DownloadProcess():
    def __init__(self, name, url, saveLocation):
        self._url = url
        self._saveLocation = saveLocation
        self._name = name

    def start_download(self):
        urllib.request.urlretrieve(self._url, self._saveLocation, self.progress_report)

    def progress_report(self, blockNum, blocksize, totalSize):
        self._blockNum = blockNum
        self._blocksize = blocksize
        self._totalSize = totalSize

        self.readSoFar = blockNum * blocksize
        if totalSize > 0:
            self.percent = self.readSoFar * 100 / totalSize

    def getProgressReport(self):
        return self.percent


app = QApplication(sys.argv)
dialog = HelloWord()
dialog.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
