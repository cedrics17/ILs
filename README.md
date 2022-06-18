# ILs
Package Scripts to Submit Ionic Liquids studies in LAMMPS using the BU SCC machine and interface.
After running the replica exchange simulations and considering that LAMMPS dumps the coordinates following the trajectory and not the temperature, some additional processing has to be done using the reorder_remd_traj.py script available in lammps github replica package. 

#### This Package assumes that the replica exchange was done and processed such as the dump files are temperature based and not trajectory based. 

# Procedure:
### 1)Load the required modules and packages in a fresh python 3 conda environment to prevent inconsistencies:
    a)numpy, os, argparse.
    b)Copy the python script correlate_gofr.py into your bin directory.
