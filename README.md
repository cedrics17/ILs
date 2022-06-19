# ILs
Package Scripts to Submit Ionic Liquids studies in LAMMPS using the BU SCC machine and interface.
After running the replica exchange simulations and considering that LAMMPS dumps the coordinates following the trajectory and not the temperature, some additional processing has to be done using the reorder_remd_traj.py script available in lammps github replica package. 

#### This Package assumes that the replica exchange was done and processed such as the dump files are temperature based and not trajectory based. 


#####The pairs are: 

    AC4DCAsaltTFSI, AC4DCAneat, P111DCAneat, P101TFSIneat, AC4DCAsaltDCA, P111DCAsaltDCA, P101TFSIsaltDCA, AC4DCAsaltTFSI, AC4DCAsaltPF6, AC4DCAsaltDCAhalf, AC4DCAsaltTFSIhalf,AC4DCAsaltPF6half
# Procedure:
### 1)Load the required modules and packages in a fresh python 3 conda environment to prevent inconsistencies:
    numpy, os, argparse
### 2)Copy the python script correlate_gofr.py into your bin directory.
### 3)Get the edits
