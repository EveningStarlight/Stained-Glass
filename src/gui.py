import sys
import cv2 as cv
import mosaic

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class StainGlassGUI(QMainWindow):
    """
    Houses the GUI implementation of the Stained Glass Application
    """

    def __init__(self):
        super().__init__()

        self.mosaic = mosaic.Mosaic(self.updateCanvas)

        self.setWindowTitle('Stained Glass Maker')

        self.__initMenu()
        self.__initFrame()

        self.mosaic.setImage(cv.imread('img/bird.png'))

        self.show()

    def __initMenu(self):
        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu(' &File')
        editMenu = mainMenu.addMenu(' &Edit')
        viewMenu = mainMenu.addMenu(' &View')

        openImageButton = QAction('Open...', self)
        openImageButton.setShortcut('Ctrl+O')
        openImageButton.setStatusTip('Opens a new image')
        openImageButton.triggered.connect(self.__openImage)
        fileMenu.addAction(openImageButton)

        closeTabButton = QAction(QIcon('exit24.png'), 'Close', self)
        closeTabButton.setShortcut('Ctrl+W')
        closeTabButton.setStatusTip('Close active window')
        closeTabButton.triggered.connect(self.close)
        fileMenu.addAction(closeTabButton)

        exitButton = QAction(QIcon('exit24.png'), 'Exit StainGlass', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)


    def __initFrame(self):
        canvasHeight = 2

        frame = QWidget()
        frameLayout = QGridLayout()
        frameLayout.addWidget(self.__initcanvas(),0,0,canvasHeight,1)
        frameLayout.addWidget(self.__initInterface(),0,1,canvasHeight,1)
        frame.setLayout(frameLayout)
        self.setCentralWidget(frame)


    def __initcanvas(self):
        """
        Implements the canvas for the Application
        """
        self.canvas = QLabel()
        self.canvas.size = (500,500)
        self.canvas.resize(self.canvas.size[0],self.canvas.size[1])

        return self.canvas


    def __initInterface(self):
        """
        Implements the intereface of the Application,
        which is composed of several tabs for interaction
        """
        tabs = QTabWidget()
        tabs.addTab(self.__initTabGrouping(), "Groupings")
        tabs.addTab(self.__initTabColour(), "Colours")

        return tabs


    def __initTabGrouping(self):
        """
        Implements the first tab
        usage is TODO
        """
        tab = QWidget()
        layout = QGridLayout()

        button1 = QPushButton('Button 1')
        button1.setToolTip("Test Button")
        button1.clicked.connect(self.__testButton)
        layout.addWidget(button1,0,0)

        layout.addWidget(QPushButton('Button 2'), 1,0)

        vboxK = QVBoxLayout()

        labelK = QLabel(str(self.mosaic.get("K")), self)
        labelK.setAlignment(Qt.AlignCenter)
        labelK.setMinimumWidth(40)
        labelK.setMaximumHeight(40)

        sliderK = QSlider(Qt.Horizontal)
        sliderK.setFocusPolicy(Qt.StrongFocus)
        sliderK.setTickPosition(QSlider.TicksBothSides)
        sliderK.setRange(1,20)
        sliderK.setSingleStep(1)
        sliderK.setTickInterval(5)
        sliderK.setValue(self.mosaic.get("K"))
        sliderK.valueChanged.connect(lambda value: self.mosaic.set("K", value))
        sliderK.valueChanged.connect(lambda value: labelK.setText(str(value)))

        vboxK.addWidget(labelK)
        vboxK.addWidget(sliderK)
        layout.addLayout(vboxK, 2,0, alignment=Qt.AlignTop)

        vboxA = QVBoxLayout()

        labelA = QLabel(str(self.mosaic.get("Area")), self)
        labelA.setAlignment(Qt.AlignCenter)
        labelA.setMinimumWidth(40)
        labelA.setMaximumHeight(40)

        sliderA = QSlider(Qt.Horizontal)
        sliderA.setFocusPolicy(Qt.StrongFocus)
        sliderA.setTickPosition(QSlider.TicksBothSides)
        sliderA.setRange(0,20)
        sliderA.setSingleStep(1)
        sliderA.setTickInterval(5)
        sliderA.setValue(self.mosaic.get("Area"))
        sliderA.valueChanged.connect(lambda value: self.mosaic.set("Area", value))
        sliderA.valueChanged.connect(lambda value: labelA.setText(str(value)))

        vboxA.addWidget(labelA)
        vboxA.addWidget(sliderA)
        layout.addLayout(vboxA, 3,0, alignment=Qt.AlignTop)

        tab.setLayout(layout)

        return tab

    def __initTabColour(self):
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


    def __testButton(self):
        print("test")

    def __openImage(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "./img", "Images (*.png *.xpm *.jpg)", options=options)
        if fileName:
            img = cv.imread(fileName)
            self.mosaic.setImage(img)

    def updateCanvas(self, img):
        img = cv.resize(img, self.canvas.size)
        cv.cvtColor(img, cv.COLOR_BGR2RGB, img)
        img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
        self.canvas.setPixmap(QPixmap.fromImage(img))


if __name__ == "__main__":
    app = QApplication([])
    ex = StainGlassGUI()
    sys.exit(app.exec_())
