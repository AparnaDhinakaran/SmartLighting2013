SmartLighting2013
=================

Smart Lighting Fall 2013

1. Database.py: database code
    - Recreate the database (NOTE: you must delete any existing 'data.db' to use this command)
        python Database.py -recreate
    - Cluster table t from times t1 to t2
        python Database.py --cluster t t1 t2
    - Other commands exist (read Database.py) but are not programmed to be run from the command line

2. dayahead_prediction directory:
    - data.db: a copy of the database for the prediction files to use
    - gaussianPrediction.py: contains the gaussian prediction functions 
    (run python gaussianPrediction.py)
    - testPredictions.py: contains several algorithms that we previously tested

3. error directory: contains text files of several testing results

4. inverse_model: contains the scripts used for the inverse model
    - Refer to the README.txt in the inverse_model directory for further instructions
    on how to run the inverse model scripts from the command line

5. util directory:
    - generatePlots.py: a script used for generating png images of sensor readings
    for every day for each sensor

6. data.db: database containing CITRIS light sensor data and NASA light sensor data.

7. data_files directory: contains text files of sensor data (parsed and added to tables in Database.py)

8. dateTimeUtil.py: contains several helper functions used by Database.py

9. svm directory: contains initial svm code for dayahead prediction

Updated 06/16/14 by Elizabeth Cheng
