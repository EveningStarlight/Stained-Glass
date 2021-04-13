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

        self.mosaic.setImage(cv.imread('img/landscape.png'))

        self.show()


    def __initMenu(self):
        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu(' &File')

        fileMenu.addAction(self.__initMenuItem(name='Open...', shortcut='Ctrl+O', status='Opens a new image', function=self.__openImage))
        fileMenu.addAction(self.__initMenuItem(name='Save...', shortcut='Ctrl+S', status='Saves the current image', function=self.__saveImage))
        fileMenu.addAction(self.__initMenuItem(name='Close', shortcut='Ctrl+W', status='Close active window', function=self.close))
        fileMenu.addAction(self.__initMenuItem(name='Exit StainGlass', shortcut='Ctrl+Q', status='Exit application', function=self.close))


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
        """
        tab = QWidget()
        layout = QGridLayout()
        yPos = 0

        vboxK = self.__initSlider(setting="K", preLabel="Colour Groups: ", min=1, max=6, tick=1)
        layout.addLayout(vboxK, yPos,0, alignment=Qt.AlignTop)
        yPos+=1

        vboxK = self.__initSlider(setting="Grid", preLabel="Grid Size: ", min=1, max=4, tick=1)
        layout.addLayout(vboxK, yPos,0, alignment=Qt.AlignTop)
        yPos+=1

        vboxK = self.__initSlider(setting="BlurSize", preLabel="Blur Size: ", min=0, max=8, tick=1, valFunction=(lambda v: 2*v+1), posFunction=(lambda v: int((v-1)/2)))
        layout.addLayout(vboxK, yPos,0, alignment=Qt.AlignTop)
        yPos+=1

        vboxK = self.__initSlider(setting="MinArea", preLabel="Minimum Area: ", postLabel="%", min=0, max=20, tick=5, valFunction=(lambda v: v/10), posFunction=(lambda v: int(v*10)))
        layout.addLayout(vboxK, yPos,0, alignment=Qt.AlignTop)
        yPos+=1

        vboxK = self.__initSlider(setting="MaxArea", preLabel="Minimum Area: ", postLabel="%", min=10, max=100, tick=10)
        layout.addLayout(vboxK, yPos,0, alignment=Qt.AlignTop)
        yPos+=1

        vboxThickness = self.__initSlider(setting="LineThickness", preLabel="Line Thickness: ", min=1, max=10, tick=2)
        layout.addLayout(vboxThickness, yPos,0, alignment=Qt.AlignTop)
        yPos+=1

        tab.setLayout(layout)

        return tab


    def __initTabColour(self):
        """
        Implements the second tab
        usage is TODO
        """
        tab = QWidget()
        layout = QGridLayout()
        yPos = 0

        vbox = QVBoxLayout()
        label = QLabel('Color Scheme: ', self)
        CB = QComboBox()
        CB.addItems(self.mosaic.colorSchemes)
        CB.currentIndexChanged.connect(lambda value: self.mosaic.set('colorScheme',value))

        vbox.addWidget(label)
        vbox.addWidget(CB)
        layout.addLayout(vbox, yPos, 0, alignment=Qt.AlignTop)
        yPos+=1

        vbox = self.__initSlider(setting="Saturation", preLabel="Saturation: ", min=0, max=20, tick=2, valFunction=(lambda v: v/10), posFunction=(lambda v: int(v*10)))
        layout.addLayout(vbox, yPos, 0, alignment=Qt.AlignTop)
        yPos+=1

        vbox = self.__initSlider(setting="Lightness", preLabel="Lightness: ", min=0, max=20, tick=2, valFunction=(lambda v: v/10), posFunction=(lambda v: int(v*10)))
        layout.addLayout(vbox, yPos, 0, alignment=Qt.AlignTop)
        yPos+=1

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


    def __saveImage(self):
        try:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self,"Save File", "./img/"+"mosaic.png", "Images (*.png *.xpm *.jpg)", options=options)
            if fileName != "":
                image = self.mosaic.mosaics[self.mosaic.getSettingHash()]
                cv.imwrite(fileName, image)
        except Exception as e:
            buttonReply = QMessageBox.question(self, 'Save Error', "File could not be saved:\n" +str(e), QMessageBox.Ok)


    def updateCanvas(self, img):
        img = cv.resize(img, self.canvas.size)
        cv.cvtColor(img, cv.COLOR_BGR2RGB, img)
        img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
        self.canvas.setPixmap(QPixmap.fromImage(img))


    def __initMenuItem(self, name, shortcut, status, function):
        menuItem = QAction(name, self)
        menuItem.setShortcut(shortcut)
        menuItem.setStatusTip(status)
        menuItem.triggered.connect(function)

        return menuItem


    def __initSlider(self, setting, preLabel="", postLabel="", min=0, max=10, tick=2, valFunction=(lambda v: v), posFunction=(lambda v: v)):
        vbox = QVBoxLayout()

        label = QLabel(preLabel + str(self.mosaic.get(setting)) + postLabel, self)
        label.setAlignment(Qt.AlignCenter)
        label.setMinimumWidth(80)
        label.setMaximumHeight(40)

        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setRange(min, max)
        slider.setTickInterval(tick)
        slider.setValue(posFunction(self.mosaic.get(setting)))
        slider.valueChanged.connect(lambda value: self.mosaic.set(setting, valFunction(value)))
        slider.valueChanged.connect(lambda value: label.setText(preLabel + str(valFunction(value)) + postLabel))

        vbox.addWidget(label)
        vbox.addWidget(slider)

        return vbox


if __name__ == "__main__":
    app = QApplication([])
    ex = StainGlassGUI()
    sys.exit(app.exec_())
