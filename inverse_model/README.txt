SmartLighting2013
=================

Smart Lighting Fall 2013

The following section describes how to run inverse model scripts from the terminal command line.
Run the commands from inside this inverse_model directory.

1. Find the best regressors for testbed for validtimes v1-v2 and traintimes t1-t2 and output 
them (along with RMS percent/value errors) to the file <testbed>_bestreg.txt in the results 
directory.

    python inverse_pred_script.py testbed v1 v2 t1 t2

2. Plot the inverse model prediction versus the actual for each dependent sensor of testbed 
and save the plots in the plots directory using validtimes from v1-v2 and traintimes t1-t2.

    python inverse_pred_script.py testbed v1 v2 t1 t2 -plot

3. Plot the inverse model prediction versus the actual for the specified dependent sensor 
number depNum of testbed and using the regressors r1,...,rK. Use validtimes from v1-v2 
and traintimes t1-t2. Save the plot in the plots directory.

    python inverse_pred_script.py testbed v1 v2 t1 t2 -plotSingle depNum r1 r2 … rK

Updated on 05/13/14 by Elizabeth Cheng
