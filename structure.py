import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class HelloWord(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        layout = QVBoxLayout()

        label = QLabel('Hello World')
        line_edit = QLineEdit()
        button = QPushButton('Close')

        layout.addWidget(label)
        layout.addWidget(line_edit)
        layout.addWidget(button)

        self.setLayout(layout)

        button.clicked.connect(self.close)
        line_edit.textChanged.connect(label.setText)


app = QApplication(sys.argv)
dialog = HelloWord()
dialog.show()
app.exec_()
