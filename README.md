# Sensor Measurement Quality Analysis

More and more analytics are done on sensor data. This strengthens the need of ensuring the quality of sensor gathered data.

This project aims to answer the need for reliable sensor data. We add confidence to sensor data by statistically analyzing it and setting a quality attribute for that data. The quality, together with the original measurement are written to a Predix Time Series. Predix currently has native support for a quality attribute for each measurement.

The statistical model we used to measure the qualit of the data is the ARMA (auto regressive moving average). The model we use is configurable and can be extended to use more elaborate models.

In order to visualize the quality of the data, the project contains a web interface that displays a graph of the measurements. When our system recognizes low quality data it shows a red indication of low quality points. The web interface also displays a graph of the features computed for each measurement. When there is a change in the features between consecutive measurements there is a clear visual indication on the screen.

In order to demonstrate the solution in real-time, we developed a simulator using Intel's Predix developer kit. The simulator represents a sensor with valid measurements from the data set provided by ESB (the data set is the load measurement from ESB's substations). This dataset already has occasional data corruption due to Gaussian noise. In order to control when data corruption happens we connected a physical button to the kit. When the button is pressed by the user - further noise is injected into the measurement.

Overall our system's architecture is as follows: 
- The simulator ingests the data (valid or corrupted) into a Predix time series. 
- The analyzer component, which runs as a Predix app, analyzes the measurements in the time series, and outputs them, with a quality attribute for each measurement, to another Predix time series.
- The web interface requests a measurement, quality measure, and the feature vector from the analyzer and displays in visually. 

See more info about the project in the presentation available in GitHub.
