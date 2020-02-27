# Validation for IoT Reliability Simulation

This repo holds the real-world experiment setup, scripts, data and result analysis for ReLIoT, a reliability simulating module on ns-3. The content in each directory is summarized in the following:

```
├── data                      // experiment scenarios, collected data and processing scripts
├── esp8266                   // code running on ESP8266s
├── model-characterization    // scripts and results of modeling power & execution time
|			  											// of RPi3 and RPi0
├── README.md                 // this file
├── rpi-broker                // scripts to fire the experiment on RPi3
├── rpi-mesh-setup            // scripts to setup mesh network with RPis
├── rpi-mqtt                  // scripts running on each RPi during experiment
├── script                    // handy scripts on RPi to change frequency and bandwidth
└── sensor                    // handy module to read power and temperature from external             
                              // sensors

```

Refer to the README in each directory for more details regarding each part.