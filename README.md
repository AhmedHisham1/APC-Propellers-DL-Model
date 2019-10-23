# APC-Propellers-DL-Model
A deep learning model for the regression problem of predicting the APC propellers thrust at various airspeed when given the propeller size and a certain rpm.

## Data Source

Data is downloaded from the official APC propellers  
Link: https://www.apcprop.com/technical-information/file-downloads/

## Usage and Files  

#### Files Info:  
- *'Data_Extraction.py'*: python script for extracting a cleaner data from the original data and store it in the 'all_props.csv' file.  
- *'Data Cleaning.ipynb'*: ipython notebook for additional cleaning of the 'all_props.csv' file by removing unwanted columns and saving to the 'all_props_cleaned_petite.csv' file.
- *'Fitting.ipynb'*: ipython notebook that contains the creation and training of the first deep learning model and saving the model into the 'Fitting_model.h5' file.
- *'Fitting_2.ipynb'*: ipython notebook that contains the creation and training of the second deep learning model and saving the model into the 'Fitting_2_model.h5' file.
- ***'Model UI.ipynb'***: ipython notebook. **the user-interface of the two models**

#### Usage:
The main interface with the two created models should be done through the "**Model UI**" notebook.  

## Example Output  
By changing the following values inside the "**Model UI**" notebook, the output will be as shown in the figure below.  
```python
diam = 16
pitch = 10
rpm = 13999
V_values = list(np.linspace(0,200,num=800))
```

![Imgur](https://i.imgur.com/Girh8bW.png)
