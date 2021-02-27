import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class StainGlassGUI():
    """
    Houses the GUI implementation of the Stained Glass Application
    """

    def __init__(self):
        canvasHeight = 2

        # Creates the base of the Application
        app = QApplication([])
        self.window = QWidget()
        self.window.setWindowTitle('Stained Glass Maker')

        # Defines the high level layout of the application
        topLevelLayout = QGridLayout()
        topLevelLayout.addWidget(self.__canvas(),0,0,canvasHeight,1)
        topLevelLayout.addWidget(self.__interface(),0,1,canvasHeight,1)
        self.window.setLayout(topLevelLayout)

        # Displays the Application
        self.window.show()
        sys.exit(app.exec_())

    def __canvas(self):
        """
        Implements the canvas for the Application
        """
        self.image = QImage('img/Geometry.png')
        label = QLabel()
        label.setPixmap(QPixmap(self.image))

        return label
        #QPushButton('Canvas')

    def __interface(self):
        """
        Implements the intereface of the Application,
        which is composed of several tabs for interaction
        """
        tabs = QTabWidget()
        tabs.addTab(self.__tab1(), "Tab1")
        tabs.addTab(self.__tab2(), "Tab2")

        return tabs

    def __tab1(self):
        """
        Implements the first tab
        usage is TODO
        """
        tab = QWidget()
        layout = QGridLayout()
        layout.addWidget(QPushButton('Button 1'))
        layout.addWidget(QPushButton('Button 2'))
        tab.setLayout(layout)

        return tab

    def __tab2(self):
        """
        Implements the second tab
        usage is TODO
        """
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QCheckBox("General Option 1"))
        layout.addWidget(QCheckBox("General Option 2"))
        tab.setLayout(layout)

        return tab



if __name__ == "__main__":
    app = StainGlassGUI()
