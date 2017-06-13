# Sensor Measurement Quality Analysis

As more and more analytics are done on sensors, ensuring the quality of the data gathered by the sensor is crucial.

This project aims to answer the need for a reliable data source. We do this by statistically analyzing the data sent by the sensor and setting a quality attribute for that data. The quality, together with the original measurement are written to a Predix Time Series, that natively supports a quality attribute for each measurement.

The statistical model used is the ARMA model, but is configurable and can be extended to additional models.

In order to visualize the quality of the data, the project contains a web frontend that displays a graph of the measurements, with a red indication of low quality points. The web inteface also displays a graph of the features computed for each measurement, visualizing the change in features between consecutive measurments.
