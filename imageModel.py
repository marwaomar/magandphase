from modesEnum import Modes
import numpy as np
from PIL import Image
from PyQt5.QtGui import QIcon, QPixmap
class ImageModel():

    """
    A class that represents the ImageModel"
    """
    def __init__(self, imgPath: str):
        #Assigning Data
        self.imgPath = imgPath
        self.image_asPixMap = QPixmap(imgPath)
        self.open_img=Image.open(imgPath)
        self.imgByte = np.asarray(self.open_img)
        if np.ndim(self.imgByte) == 3 :
            self.imgByte = np.asarray(self.open_img.convert('L'))
        self.dft = np.fft.fftn(self.imgByte)
        self.real = np.real(self.dft)
        self.imaginary = np.imag(self.dft)
        self.magnitude = np.abs(self.dft)
        self.dftShift = np.fft.fftshift(self.dft)
        self.magnitude_shift = (20*np.log(1+np.abs(self.dftShift)))
        self.phase = np.angle(self.dft)
        self.Unimagnitude=np.ones(self.imgByte.shape)
        self.Uniphase = np.zeros(self.imgByte.shape)
        self.mixed_output=QPixmap()
    #Displaying Original Image
    def Display_original_img(self):
        return self.image_asPixMap
        
    def reconstruct_image(self,img_data):
        Image.fromarray(img_data.astype(np.uint8)).save('component_img.png')
        self.reconstructed_img = QPixmap('component_img.png')
    #Chosen component applied and return reconstructed image
    def component(self,component):
        if component == "Magnitude" :
            self.reconstruct_image(self.magnitude_shift)
            return self.reconstructed_img
        if component == "Phase" :
            self.reconstruct_image(self.phase)
            return self.reconstructed_img
        if component == "Real" :
            self.reconstruct_image(self.real)
            return self.reconstructed_img
        if component == "Imaginary" :
            self.reconstruct_image(self.real)
            return self.reconstructed_img
    #reconstructing to complex then take inverse fouries
    def reconstruct_mag_phase(self,comp1,comp2):

        complex_comp=np.multiply(comp1,np.exp(1j*comp2))
        self.image_reconstruct = np.real(np.fft.ifftn(complex_comp))
        print("data unimagphase : ",self.image_reconstruct)
        Image.fromarray(self.image_reconstruct.astype(np.uint8)).save('mixedoutput.png')
        self.mixed_output = QPixmap('mixedoutput.png')
        return self.mixed_output

    def reconstruct_real_imag(self,comp1,comp2):
        complex_comp=comp1+(1j*comp2)
        self.image_reconstruct=np.real(np.fft.ifftn(complex_comp))
        
        Image.fromarray(self.image_reconstruct.astype(np.uint8)).save('mixedoutput.png')
        self.mixed_output = QPixmap('mixedoutput.png')
        return self.mixed_output
    #Calculating the results of the chosen percentages
    def calculations_of_percentages(self,measurand1_1,measurand1_2,percentage1_chosen,measurand2_1,measurand2_2 ,percentage2_chosen):
        data_to_calc1_part1 = measurand1_1*(percentage1_chosen/100)
        data_to_calc1_part2 = measurand1_2*(1-(percentage1_chosen/100))
        data_to_calc1 = data_to_calc1_part1  + data_to_calc1_part2
        data_to_calc2_part1 = measurand2_1*(percentage2_chosen/100)
        data_to_calc2_part2 = measurand2_2 *(1-(percentage2_chosen/100))
        data_to_calc2 = data_to_calc2_part1 + data_to_calc2_part2
        return data_to_calc1 , data_to_calc2
    # Mixing Function between two images
    def mix(self, imageToBeMixed: 'ImageModel', magnitudeOrRealRatio: float, phaesOrImaginaryRatio: float, mode: 'Modes') -> np.ndarray:

        percentage1_chosen = magnitudeOrRealRatio
        percentage2_chosen = phaesOrImaginaryRatio
        if mode == Modes.magnitudeAndPhase :
            mag_data , phase_data = self.calculations_of_percentages(self.magnitude,imageToBeMixed.magnitude,percentage1_chosen,imageToBeMixed.phase,self.phase,percentage2_chosen)
            return self.reconstruct_mag_phase(mag_data,phase_data) 
        if mode == Modes.realAndImaginary:
            real_data , imaginary_data =self.calculations_of_percentages(self.real,imageToBeMixed.real,percentage1_chosen,imageToBeMixed.imaginary,self.imaginary,percentage2_chosen)
            return self.reconstruct_real_imag(real_data,imaginary_data)

        if mode == Modes.magnitudeAndUniphase:
            mag_data , uniphase_data = self.calculations_of_percentages(self.magnitude,imageToBeMixed.magnitude,percentage1_chosen,imageToBeMixed.Uniphase,self.Uniphase,percentage2_chosen)
            return self.reconstruct_mag_phase(mag_data,uniphase_data)

        if mode == Modes.UniMagnitudeAndPhase:
            unimag_data , phase_data = self.calculations_of_percentages(self.Unimagnitude,imageToBeMixed.Unimagnitude,percentage1_chosen,imageToBeMixed.phase,self.phase,percentage2_chosen)
            
            return self.reconstruct_mag_phase(unimag_data,phase_data)
        
        if mode == Modes.UniMagnitudeAndUniphase:
            unimag_data , uniphase_data = self.calculations_of_percentages(self.Unimagnitude,imageToBeMixed.Unimagnitude,percentage1_chosen,imageToBeMixed.Uniphase,self.Uniphase,percentage2_chosen)
            return self.reconstruct_mag_phase(unimag_data,uniphase_data)
            



        