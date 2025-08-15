# 🐠 myNEMO

This software will help you set up NEMO and all its accessories (OASIS, XIOS, etc ...) for your experiment.
It will also generate a webpage gathering all the informations on your experiment : aureliealbertmeom.github.io/myNEMO

 - 1st step : Make sure you have a python environment with [these libraries](environment.yml) installed on your machine

 - 2nd step : Fill out the [lists.py](lists.py) with the specifics of your machine (take example of the irene one for instance), if some XIOS or NEMO versions are already installed, specify it and put their path

 - 3rd step : Modify the [current_experiment](current_experiment.yml) file to fit your needs (take a look at the [all_experiments](all_experiments.yml) file to be inspired)

 - last step : Follow the instructions given by the software by launching : ```python3 start.py```
