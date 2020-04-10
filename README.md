# Title 

## Vi-Track 

# Description 

Vi-Track provides a way for people whose relatives are affected by the pandemic to check and monitor the health and status of the infected patient. This would be extremely helpful for people as confirmed COVID 19 patients are kept in complete isolation and are not allowed to have visitors throughout their course of treatment. The setup consists of a hardware module equipped with sensors that read the vital signs of the patient and send the data to an online server. The data can be viewed and accessed through this web application by family members of the patient, in real-time. To avoid breaching in the privacy of the patients, the user data is deleted after regular time intervals. This web application utilizes a machine learning algorithm (XGBoost) to read the data and detect any anomalies to notify the appropriate parties in case the patient's health starts to deteriorate abruptly. 

# Requirements 
* Software 
	* Python 
		* Pandas (not mandatory)
		* matplotlib (not mandatory)
		* numpy (to manage numerical data)
		* sklearn (to build the machine learning model)

	* Node Package Manager
	* Required node modules
* Hardware 
	* ARDUINO NANO 33 IOT (in video we have used NODE MCU, due to unavailability of the same) 
	* Pulse sensor 
	* Temperature sensor DS18B20 
	* Ecg Sensor AD8232 


# Process Flow 

The hardware module captures data from the patient and transmit it to a Google Sheet (to reduce cost). The data is read by a web application. The application can be used by close ones of the patient to monitor the affected person's health in real time, since COVID-19 patients are not allowed to have visitors and are in complete isolation. 
The data is deleted at regular intervals to avoid privacy breach. 

# Data Flow Diagram 

![Data Flow Diagram](https://raw.githubusercontent.com/ChetanMadan/ViTrack/master/dataflow.png)
