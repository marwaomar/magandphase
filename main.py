from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ImageMixer import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from pyqtgraph.Qt import QtCore
from imageModel import ImageModel
from PIL import Image
from PyQt5.QtWidgets import QMessageBox
import logging
from modesEnum import Modes
logging.basicConfig(filename="logs.Log",level=logging.INFO)
logger = logging.getLogger()
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Assigning Data
        self.setupUi(self)
        self.show()
        self.percentages=[self.percentage1,self.percentage2]
        self.timer1 = QtCore.QTimer()
        self.timer2 = QtCore.QTimer()
        self.timer3 = QtCore.QTimer()
        self.timer4 = QtCore.QTimer()
        self.img1_comp = QPixmap()
        self.img2_comp= QPixmap()
        self.output_image = QPixmap()
        self.width_of_image  = self.img1.geometry().width()
        self.height_of_image = self.img1.geometry().height()
        self.timer = [self.timer1 , self.timer2,self.timer3,self.timer4]
        self.img1_active.clicked.connect(self.active_image1)
        self.img2_active.clicked.connect(self.active_image2)
        
       #Sliders Setup
        for percentage in self.percentages:
            percentage.setMaximum(100)
            percentage.setMinimum(0)
            percentage.setSingleStep(10)
            percentage.setValue(0)
            percentage.valueChanged.connect(self.component_choices)
        #Timers Setup
        for index in range(0,3):
            #self.timer[index] = QtCore.QTimer()
            self.timer[index].setInterval(50)
            self.timer[index].start()
            
            if  index == 0 :
                self.timer[index].timeout.connect(self.check_component)
            elif index == 1:
                self.timer[index].timeout.connect(self.control_comp_choices)
            elif index == 2 :
                self.timer[index].timeout.connect(self.output_selection)
            
            
    def open_image(self):
        imagePath = QFileDialog.getOpenFileName(None,'OpenFile','',"Image file(*.png); Img (*.jpg)")
        return imagePath
    def active_image1(self):

        imgpath = self.open_image()
        self.img1_active = True
        self.image1= ImageModel(imgpath[0])
        self.activation_of_image()

    def active_image2(self):
        
        imgpath = self.open_image()
        self.img1_active = False
        self.image2= ImageModel(imgpath[0])
        self.activation_of_image()

    def activation_of_image(self):
        self.Display()
        self.timer4.start()
        self.timer4.timeout.connect(self.Display)

    def Display(self):
        
        if self.img1_active:
            image1=self.image1.Display_original_img()
            self.size1 = image1.size()
            image1= image1.scaled(self.width_of_image,self.height_of_image,Qt.KeepAspectRatio,Qt.FastTransformation)
            self.img1_comp=self.img1_comp.scaled(self.width_of_image,self.height_of_image,Qt.KeepAspectRatio,Qt.FastTransformation)
            self.img1.setPixmap(image1)
            self.img1_modified.setPixmap(self.img1_comp)
            logger.info('displaying image 1 and its chosen components')
        else : 
            
            image2=self.image2.Display_original_img()
            self.size2=image2.size()
            if self.size1 != self.size2 :
                self.show_error()
                self.active_image2()
            image2= image2.scaled(self.width_of_image,self.height_of_image,Qt.KeepAspectRatio,Qt.FastTransformation)
            self.img2_comp=self.img2_comp.scaled(self.width_of_image,self.height_of_image,Qt.KeepAspectRatio,Qt.FastTransformation)
            self.img2.setPixmap(image2)
            self.img2_modified.setPixmap(self.img2_comp)
            logger.info('displaying image 2 and its chosen components')

    # Displaying Output

    def output_selection(self):
        if self.output_choice.currentText() == "Output1":
            self.output_image = self.output_image.scaled(self.width_of_image,self.height_of_image,Qt.KeepAspectRatio,Qt.FastTransformation)
            self.output1.setPixmap(self.output_image)
            logging.info('Displaying outputs in Output1 of Mixer')

        if self.output_choice.currentText() == "Output2":
            #image_output2 = self.ImageModel.Display_mixed_image()
            self.output_image = self.output_image.scaled(self.width_of_image,self.height_of_image,Qt.KeepAspectRatio,Qt.FastTransformation)

            #self.ImageModel.active_output2()
            self.output2.setPixmap(self.output_image)
            logger.info('Displaying outputs in Output2 of Mixer')

    def show_error(self):
        msg = QMessageBox()
        msg.setWindowTitle("ERROR")
        msg.setText("Not same Size , Please choose two pictures of the same size")
        msg.setIcon(QMessageBox.Critical) 
        logger.warning('Two Images are not the same size')
        execute = msg.exec_()
        

    def component_selection(self,comp1,comp2):

        if self.choose_comp1.currentText() == "Image1" and self.choose_comp2.currentText() == "Image1":
            if comp1 == "Magnitude" or comp2 == "Magnitude":
                self.output_image = self.image1.mix(self.image1,self.percentages[0].value(),self.percentages[1].value(),Modes.magnitudeAndPhase)
            if comp1 == "Real" or comp2 == "Real":
                self.output_image = self.image1.mix(self.image1,self.percentages[0].value(),self.percentages[1].value(),Modes.realAndImaginary)
            if (comp1 == "Unimagnitude" or comp2 == "Unimagnitude") and (comp1 == "Uniphase" or comp2 == "Uniphase"):
                self.output_image = self.image1.mix(self.image1,self.percentages[0].value(),self.percentages[1].value(),Modes.UniMagnitudeAndUniphase)
            if (comp1 == "Unimagnitude" or comp2 == "Unimagnitude") and (comp1 == "Phase" or comp2 == "Phase"):
                self.output_image = self.image1.mix(self.image1,self.percentages[0].value(),self.percentages[1].value(),Modes.UniMagnitudeAndPhase)
            if (comp1 == "Uniphase" or comp2 == "Uniphase") and (comp1 == "Magnitude" or comp2 == "Magnitude"):
                self.output_image = self.image1.mix(self.image1,self.percentages[0].value(),self.percentages[1].value(),Modes.magnitudeAndUniphase)
            logger.info('Selecting which Image1 and Image1 to mix')
        if self.choose_comp1.currentText() == "Image1" and self.choose_comp2.currentText() == "Image2":
            if comp1 == "Magnitude":
                self.output_image = self.image1.mix(self.image2,self.percentages[0].value(),self.percentages[1].value(),Modes.magnitudeAndPhase)
            if comp2 == "Magnitude":
                self.output_image = self.image2.mix(self.image1,self.percentages[0].value(),self.percentages[1].value(),Modes.magnitudeAndPhase)
            if comp1 == "Real" :
                self.output_image = self.image1.mix(self.image2,self.percentages[0].value(),self.percentages[1].value(),Modes.realAndImaginary)
            if comp2 == "Real":
                self.output_image = self.image2.mix(self.image1,self.percentages[0].value(),self.percentages[1].value(),Modes.realAndImaginary)
            if comp1 == "Unimagnitude" and comp2 == "Uniphase":
                self.output_image = self.image1.mix(self.image2,self.percentages[0].value(),self.percentages[1].value(),Modes.UniMagnitudeAndUniphase)
            if comp1 == "Unimagnitude" and comp2 == "Phase":
                self.output_image = self.image1.mix(self.image2,self.percentages[0].value(),self.percentages[1].value(),Modes.UniMagnitudeAndPhase)
            if comp1 == "Magnitude" and comp2 == "Uniphase":
                self.output_image = self.image1.mix(self.image2,self.percentages[0].value(),self.percentages[1].value(),Modes.magnitudeAndUniphase)
            if comp1 == "Uniphase" and comp2 == "Unimagnitude":
                self.output_image = self.image2.mix(self.image1,self.percentages[0].value(),self.percentages[1].value(),Modes.UniMagnitudeAndUniphase)
            if comp1 == "Phase" and comp2 == "Unimagnitude":
                self.output_image = self.image2.mix(self.image1,self.percentages[0].value(),self.percentages[1].value(),Modes.UniMagnitudeAndPhase)
            if comp1 == "Uniphase" and comp2 == "Magnitude":
                self.output_image = self.image2.mix(self.image1,self.percentages[0].value(),self.percentages[1].value(),Modes.magnitudeAndUniphase)
            logger.info('Selecting which Image1 and Image2 to mix')
        
        if self.choose_comp1.currentText() == "Image2" and self.choose_comp2.currentText() == "Image1":
            if comp1 == "Magnitude":
                self.output_image = self.image2.mix(self.image1,self.percentages[0].value(),self.percentages[1].value(),Modes.magnitudeAndPhase)
            if comp2 == "Magnitude":
                self.output_image = self.image1.mix(self.image2,self.percentages[0].value(),self.percentages[1].value(),Modes.magnitudeAndPhase)
            if comp1 == "Real" :
                self.output_image = self.image2.mix(self.image1,self.percentages[0].value(),self.percentages[1].value(),Modes.realAndImaginary)
            if comp2 == "Real":
                self.output_image = self.image1.mix(self.image2,self.percentages[0].value(),self.percentages[1].value(),Modes.realAndImaginary)
            
            if comp1 == "Unimagnitude" and comp2 == "Uniphase":
                self.output_image = self.image2.mix(self.image1,self.percentages[0].value(),self.percentages[1].value(),Modes.UniMagnitudeAndUniphase)
            if comp1 == "Unimagnitude" and comp2 == "Phase":
                self.output_image = self.image2.mix(self.image1,self.percentages[0].value(),self.percentages[1].value(),Modes.UniMagnitudeAndPhase)
            if comp1 == "Magnitude" and comp2 == "Uniphase":
                self.output_image = self.image2.mix(self.image1,self.percentages[0].value(),self.percentages[1].value(),Modes.magnitudeAndUniphase)
            if comp1 == "Uniphase" and comp2 == "Unimagnitude":
                self.output_image = self.image1.mix(self.image2,self.percentages[0].value(),self.percentages[1].value(),Modes.UniMagnitudeAndUniphase)
            if comp1 == "Phase" and comp2 == "Unimagnitude":
                self.output_image = self.image1.mix(self.image2,self.percentages[0].value(),self.percentages[1].value(),Modes.UniMagnitudeAndPhase)
            if comp1 == "Uniphase" and comp2 == "Magnitude":
                self.output_image = self.image1.mix(self.image2,self.percentages[0].value(),self.percentages[1].value(),Modes.magnitudeAndUniphase)
            logger.info('Selecting which Image2 and Image1 to mix')

        if self.choose_comp1.currentText() == "Image2" and self.choose_comp2.currentText() == "Image2": 
            if comp1 == "Magnitude" or comp2 == "Magnitude":
                self.output_image = self.image2.mix(self.image2,self.percentages[0].value(),self.percentages[1].value(),Modes.magnitudeAndPhase)
            if comp1 == "Real" or comp2 == "Real":
                self.output_image = self.image2.mix(self.image2,self.percentages[0].value(),self.percentages[1].value(),Modes.realAndImaginary)
            if comp1 == "Unimagnitude" or comp2 == "Unimagnitude" and comp1 == "Uniphase" or comp2 == "Uniphase":
                self.output_image = self.image2.mix(self.image2,self.percentages[0].value(),self.percentages[1].value(),Modes.UniMagnitudeAndUniphase)
            if comp1 == "Unimagnitude" or comp2 == "Unimagnitude" and comp1 == "Phase" or comp2 == "Phase":
                self.output_image = self.image2.mix(self.image2,self.percentages[0].value(),self.percentages[1].value(),Modes.UniMagnitudeAndPhase)
            if comp1 == "Uniphase" or comp2 == "Uniphase" and comp1 == "Magnitude" or comp2 == "Magnitude":
                self.output_image = self.image2.mix(self.image2,self.percentages[0].value(),self.percentages[1].value(),Modes.magnitudeAndUniphase)
            logger.info('Selecting which Image2 and Image2 to mix')
        
        
    def show_combobox(self):
        for index in range(1,7):
                self.comp2_effect.view().setRowHidden(index,False)
                self.comp1_effect.view().setRowHidden(index,False)

            
    def control_comp_choices(self):
        if self.comp1_effect.currentText() == "Magnitude" or self.comp1_effect.currentText() == "Unimagnitude":
            self.show_combobox()
            self.comp2_effect.view().setRowHidden(1,True)
            for index in range(4,8):
                self.comp2_effect.view().setRowHidden(index,True)
        logger.info('choosing Magnitude as comp1')
        if self.comp1_effect.currentText() == "Phase" or self.comp1_effect.currentText() == "Uniphase" :
            
            self.show_combobox()

            for index in range(2,6):
                self.comp2_effect.view().setRowHidden(index,True)
            logger.info('Phase as comp1')
        if self.comp1_effect.currentText() == "Real"  :
            self.show_combobox()
            self.comp2_effect.view().setRowHidden(6,True)
            for index in range(1,5):
                self.comp2_effect.view().setRowHidden(index,True)
            logger.info('Real as comp1')
        if self.comp1_effect.currentText() == "Imaginary" :
            self.show_combobox()
            self.comp2_effect.view().setRowHidden(5,True)
            self.comp2_effect.view().setRowHidden(6,True)
            for index in range(1,4):
                self.comp2_effect.view().setRowHidden(index,True)
            logger.info('choosing Imaginary as comp1')
        if self.comp2_effect.currentText() == "Magnitude" or self.comp2_effect.currentText() == "Unimagnitude":
            self.show_combobox()
            self.comp1_effect.view().setRowHidden(1,True)
            for index in range(4,8):
                self.comp1_effect.view().setRowHidden(index,True)
            
        if self.comp2_effect.currentText() == "Phase" or self.comp2_effect.currentText() == "Uniphase" :
            self.show_combobox()
            for index in range(2,6):
                self.comp2_effect.view().setRowHidden(index,True)

        if self.comp2_effect.currentText() == "Real"  :
            self.show_combobox()
            self.comp1_effect.view().setRowHidden(6,True)
            for index in range(1,5):
                self.comp1_effect.view().setRowHidden(index,True)
                
        if self.comp2_effect.currentText() == "Imaginary" :
            self.show_combobox()
            self.comp1_effect.view().setRowHidden(5,True)
            self.comp1_effect.view().setRowHidden(6,True)
            for index in range(1,4):
                self.comp1_effect.view().setRowHidden(index,True)




    def component_choices(self):
        
        if self.comp1_effect.currentText() == "Magnitude" and self.comp2_effect.currentText() == "Phase":
            self.component_selection("Magnitude","Phase")
                
        if self.comp1_effect.currentText() == "Phase" and self.comp2_effect.currentText() == "Magnitude":
            self.component_selection("Phase","Magnitude")

        if self.comp1_effect.currentText() == "Real" and self.comp2_effect.currentText() == "Imaginary" :
            self.component_selection("Real","Imaginary")

        if self.comp1_effect.currentText() == "Imaginary" and self.comp2_effect.currentText() == "Real":
            self.component_selection("Imaginary","Real")
        
        if self.comp1_effect.currentText() == "Unimagnitude" and self.comp2_effect.currentText() == "Uniphase":
            self.component_selection("Unimagnitude","Uniphase")
        if self.comp2_effect.currentText() == "Unimagnitude" and self.comp1_effect.currentText() == "Uniphase":
            self.component_selection("Uniphase","Unimagnitude")
        if self.comp1_effect.currentText() == "Unimagnitude" and self.comp2_effect.currentText() == "Phase":
            self.component_selection("Unimagnitude","Phase")
        if self.comp2_effect.currentText() == "Unimagnitude" and self.comp1_effect.currentText() == "Phase":
            self.component_selection("Phase","Unimagnitude")
        if self.comp1_effect.currentText() == "Uniphase" and self.comp2_effect.currentText() == "Magnitude":
            self.component_selection("Uniphase","Magnitude")
        if self.comp2_effect.currentText() == "Uniphase" and self.comp1_effect.currentText() == "Magnitude":
            self.component_selection("Magnitude","Uniphase")
       
        
        logger.info('choosing component')



    def check_component(self):
        
        if self.components_img1.currentText() == "Magnitude" :
           self.img1_comp =  self.image1.component("Magnitude")
        if self.components_img1.currentText() == "Phase" :
           self.img1_comp = self.image1.component("Phase")
        if self.components_img1.currentText() == "Real" :
           self.img1_comp = self.image1.component("Real")
        if self.components_img1.currentText() == "Imaginary" :
           self.img1_comp = self.image1.component("Imaginary")
        logger.info('Displaying components of Image1')
    #image 2
        if self.components_img2.currentText() == "Magnitude" :
           self.img2_comp =self.image2.component("Magnitude")
        if self.components_img2.currentText() == "Phase" :
           self.img2_comp =self.image2.component("Phase")
        if self.components_img2.currentText() == "Real" :
           self.img2_comp =self.image2.component("Real")
        if self.components_img2.currentText() == "Imaginary" :
           self.img2_comp = self.image2.component("Imaginary")
        logger.info('Displaying components of Image2')
        
    
            

if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("Failamp")
    app.setStyle("Fusion")

    # Fusion dark palette from https://gist.github.com/QuantumCD/6245215.
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

    window = MainWindow()
    #ImageModel=ImageModel()
    app.exec_()