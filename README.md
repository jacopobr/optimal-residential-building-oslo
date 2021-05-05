# Designing Optimal Residential Building in Oslo and Forecasting of Indoor Air-Temperature for Energy-Efficient Management
ICT in Building Desing Course - ICT4SS @politecnicoditorino - 2020/2021

##Abstract 
Buildings are one of the largest consumer of primary energy and attaining their efficiency is an important goal.
The energy consumed in buildings in developed countries comprises 20-40% of their total energy use and it is above that of industry and transport in the EU and US . Therefore knowing the characteristics of a building is necessary to manage and control its use. Moreover, knowing the energy use is important to promote demand analysis, energy feedback, Demand Response and Demand Side Management applications. In this project a residential building is modelled, varying all possible configurations of the construction parameters, in order to find the scenario that best optimizes the consumption. Once the optimal configuration has been found, some simulation will be ran in order to verify the behaviour of the internal temperature of the building over one year and analyze the energy signature. Finally, a model useful for Predictive Model Control will be implemented using two configurations of an Multi Layer Perceptron able to forecast the internal temperatures of the buildings.

:arrow_right:   [Full paper here](./Paper.pdf)

## Tools used
- [`DesignBuilder`](https://designbuilder.co.uk/): allows to build a model of the building in a really detailed way thanks to the huge number of options given such as materials choice, location, occupation and type of use (residential, office, schools...);
- [`EnergyPlus™ `](https://energyplus.net): is a whole building energy simulation program that engineers, architects, and researchers use to model both energy consumption—for heating, cooling, ventilation, lighting and plug and process loads—and water use in buildings;
- [`Pandas`](/https://pandas.pydata.org): open source data analysis and manipulation tool, built on top of the Python programming language;
- [`Keras`](https://keras.io): is a deep learning API written in Python, running on top of the machine learning platform TensorFlow;
- [`Scikit-learn`](https://scikit-learn.org/stable/): machine learning library build for Python.
