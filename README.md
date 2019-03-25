## Subway Emergency: Bridging the Gap in MTA Turnstile data
### Urban Sensing Course Project

Counting number of people exiting using the emergency exit in order to undertsand local transit demand.

Site: York Street Station (F Line)
Analysis done for Peak and Off Peak hours.

### Getting Started

The following instructions will help you to run and test the application on your local machine.

### Prerequisites

The application is built using Python 3.6.

You need to install the following libraries:

cv2  
numpy

### Running the code
The code can be run using Jupyter Notebook as well as command line. On running the code a separate window will pop up showing the video and bounding boxes.

1. Jupyter Notebook: 
You can download the jupyter notebook. You should see another window showing the video and the bounding boxes. The final count will be displayed after the video ends. 

2. Command Line
To run from command line. Download the MTA_counts.py file. run the code as follows:
```
python MTA_count.py
```
The final count will be displayed after the video ends. To see the count before the video ends, stop the video using Ctrl + C.
