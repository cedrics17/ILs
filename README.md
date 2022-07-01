# ILs
Package Scripts to Submit Ionic Liquids studies in LAMMPS using the BU SCC machine and interface.
After running the replica exchange simulations and considering that LAMMPS dumps the coordinates following the trajectory and not the temperature, some additional processing has to be done using the reorder_remd_traj.py script available in lammps github replica package. 

#### This Package assumes that the replica exchange was done and processed so that the dump files are temperature based and not trajectory based. 


##### The pairs are: 

    AC4DCAsaltTFSI, AC4DCAneat, P111DCAneat, P101TFSIneat, AC4DCAsaltDCA, P111DCAsaltDCA, P101TFSIsaltDCA, AC4DCAsaltTFSI, AC4DCAsaltPF6, AC4DCAsaltDCAhalf, AC4DCAsaltTFSIhalf,AC4DCAsaltPF6half
# Procedure:
#### 1)Load the required modules and packages in a fresh python 3 conda environment to prevent inconsistencies:
    numpy, os, argparse
#### 2)Copy the python script correlate_gofr.py into your bin directory.
#### 3)Depending on the pair you're running add in the heading of generate_full_SingleTrajRuns.py:
    the length of the run (copied from the end of the log file) to variable RunLength
    the name of the pair (copied from the list above) to variable pair
    the number of steps and snapshots (if the replex run ran for less than 30000000 steps) to the variables PostProcLength and snaps respectively
    you might also want to change the number of cores requested for every run in the variable core
#### 4)Run the script generate_full_SingleTrajRuns.py and submit the six array jobs for temperatures 300,323,349,376,405 and 436 K.
    You might find it useful to change the number of cores requested for each of the array but make sure to change the number of processes.
#### 5)Do the edits to the heading of check_SingleTraj.py (snaps if necessary and pair) and run it to check if all runs were properly terminated.Check the submission scripts generated (they start with the prefix reSub, and if there are inputs in the inputs line, submit the reSub scripts. 
#### 6)Generate the post-processing scripts by doing the edits of the heading of generate_general.py (the pair, your conda environment to the condaEnv variable and the number of cores to batch_count variable) and running the script. It will create a directory with the prefix bundles_ followed by the name of your pair within the SingleTraj directory. 
#### 7)Copy the functions get_gr.py and get_flux.py in your general directory before the Single Trajectries of every liquid and submit bundle0.sh the rest will submit itself automatically.
#### 8)Copy the scripts fromflux_correlateChoppedUp.py, from_chops_getAverage.py and avgr.py in your general directory before the SingleTraj directories. The correct liquid has to be added to the pair variable in all three scripts and the scripts have to run in this particular order. 
#### 9) Calculate the conductivity using the calc_conductivity.py script after doing the necessary edits related to the nature of the liquid. 
#### 10) Plot the data generated above: Charge flux correlation functions for every temperature, g(r) for every combination of center atoms and temperature as well as the conductivity vs temperature plots. 

### The end
