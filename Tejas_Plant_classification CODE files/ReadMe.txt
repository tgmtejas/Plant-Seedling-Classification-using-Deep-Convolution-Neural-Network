1) Libraries

Library       Version        Download Link             
Python        3.6.3     
Numpy         1.14.3         pip install numpy
Pandas        0.22.0         pip install pandas
CV2           3.4.0          https://opencv.org/releases.html
matplotlib    2.1.2          https://matplotlib.org/users/installing.html#install-from-source
OS          
scikit-learn  0.19.1         pip install -U scikit-learn
Keras         2.1.6          pip install Keras
Scipy         0.19.1         pip install scipy


2)Dataset :
Try to avoid using actual dataset.
I have already segmented and pre-processed the dataset,so download that one.
Even though you want to download actual dataset, use following link:
(Avoid)
Full Data set link: https://vision.eng.au.dk/plant-seedlings-dataset/
choose Non-segmented dataset
Use data_processing code to segment this data and save it to .mat format.
In this code you need to change input directory of original dataset and output directory for .mat segmented dataset as I pointed in comment section of code 

Or

Use Segmented dataset by me (Recommended):
https://drive.google.com/drive/folders/1uqv3yR9b0p6Ln8hNxapeRShAgxJEddc8?usp=sharing  

This will lead to google drive folder name Train and download file 'Image_Processed_1data.mat'
Download this dataset.
I am not including dataset in submission folder as it is 1.4Gbyte size. If you failed to download this file, please let me know.      


3) Code:

   i) Feature_Pyramid_Network_code.py and .ipynb
   ii)Base_code.py and .ipynb
   iii)Pyramid_unit_and_narrow_wide_model.py and .ipynb
   
  I want to highly recommend .ipynb using IPython notebooks as I have written code in .ipynb and downloaded as .py
  All these three are models used in this project and can be run individually.
  I have included PDF copy of .pynb notebook as well as Python notebooks from google colaboratory for all 3 files which has code as well as results.

Important Note:            
To execute this codes, first you need to change My_data directory which loads .mat dataset file.
Give the directory where you have saved Image_Processed_1data.mat file.
