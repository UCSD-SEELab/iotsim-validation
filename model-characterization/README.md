# Model Characterization on Raspberry Pi 3B and Zero

This directory contains the scripts to model the power and execution time on Raspberry Pi 3B and Raspberry Pi Zero. More specifically, it builds up models for running Muiti-Layer Perceptrons (MLP) and Linear Regression (LR) on RPi3B as well as running LR on RPi Zero, according to number of MAC operations.

The script tries to fit the collected power and execution time traces to 4 different models in terms of the number of MAC operations:

* Linear Model. `power/exec_time = a*MAC_# + b`
* Polynomial Model. `power/exec_time = a*MAC_#^2 + b*MAC_# + c`
* Exponential Model. `power/exec_time = a*exp(b*MAC_#) + c`
* Log Model. `power/exec_time = a*log(b + MAC_#) + c`

[Environment Setup](#Environment-Setup)

[Run Instructions](#Run-Instructions)

[Results Organization](#Results-Organization)

## Environment Setup

### Dependencies

1. To run LR,  `matplotlib` and `numpy` are required.

   ```shell
   sudo pip3 install matplotlib
   sudo pip3 install numpy
   ```

2. To run MLP in this directory, `scikit-learn` module is a must.

   ```shell
   sudo apt-get install gfortran libgfortran3 libatlas-base-dev libopenblas-dev liblapack-dev -y
   sudo pip3 install scikit-learn
   ```

**Important:** For the ease of package management, try not to use `apt` to install Python packages, as we do not know the path for the installed packages. Sometimes the version of Python could cause problems. To avoid that, try to specify the Python version in the installation command:

`````` shell
sudo python3.7 -m pip install matplotlib numpy scikit-learn
``````

### Other preparation

Apart from installing necessary Python modules, there are the following preparations to be done:

* Enable `ssh` and setup ssh passwordless login following the tutorial [here](https://www.tecmint.com/ssh-passwordless-login-using-ssh-keygen-in-5-easy-steps/).
* Install the SeeLab powermeter module following its [Github page](https://github.com/UCSD-SEELab/powermeter).

## Run Instructions

To trigger the model building process, you need to pick a mode from `3b_mlp`, `3b_lr` and `0_lr`. Remember to change the IP of the target Pi in script `run.py`. Start the script with, taking mode `3b_mlp` as an example:

```shell
python3 run.py 3b_mlp
```

## Results Organization

After the program finishes, the following results will be generated:

* `result.txt`: detailed MAC operations, power and time traces. Parameters of the generated model. Logging.
* `img/`: the measured results and their regression models, with the Mean Absolute Percentage Error (MAPE) showing in the title.
* `pwr/`: detailed power traces for each case.