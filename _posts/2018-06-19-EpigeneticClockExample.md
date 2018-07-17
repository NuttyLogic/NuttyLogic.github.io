---
layout: post
title: A Simple Epigenetic Clock Using Python and SciKit-Learn, BIG Summer Tutorial
date: 2018-06-19
excerpt: "Brief Tutorial on Fitting a DNA Methylation Based Epigenetic Clock for the Bruins In Genomics (BIG) Summer Program"
teaching: True
tags: [Tutorial, Biomarker, Methylation]
comments: false
---
# Epigentic Biomarker to Predict Age
DNA methylation has emerged as a useful proxy for measuring the physiological state of an organism. DNA methylation is dynamic, changing over time in response to environmental stimuli, yet can also be stable for relatively long periods of time[1](https://www.ncbi.nlm.nih.gov/pubmed/20395474). Thus, an individual who continuously lacked exercise and ate poorly for years would have an epigenetic profile that reflected this continued behavior. The dynamic yet stable nature of DNA methylation is extremely beneficial, maintaining information lost with more transitory signals, such as gene expression. This makes DNA methylation ideal for the development of biomarkers, which have already been developed to assess age [2](https://www.ncbi.nlm.nih.gov/pubmed/24138928),[3](https://www.ncbi.nlm.nih.gov/pubmed/23177740) and BMI [4]('Epigenome-wide association study of body mass index, and the adverse outcomes of adiposity.').  

In this example we will use publicly available data from [Aging effects on DNA methylation modules in human brain and blood tissue, 5](https://www.ncbi.nlm.nih.gov/pubmed/23034122) to fit an epigenetic clock using a penalized regression model.  The data from this paper can be accessed at [GSE41169](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE41169). We will be working with the [*series_matrix_file*](ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE41nnn/GSE41169/matrix/GSE41169_series_matrix.txt.gz) deposited in GEO repository. The complete workflow will utilize several tools:
1. [SciKit-Learn](http://scikit-learn.org/stable/index.html); Several modules from SciKit will be utilized in this example
    1. [Principal Component Analysis (PCA)](http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html), used during quality control to identify and sample outliers
    2. [Train Test Split](http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html), this provides a convenient way to split data into training and testing sets
    3. [Lasso, Cross Validated](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LassoCV.html), this is an implementation of a penalized regression model used to generate the epigentic age model
2. [Pandas](https://pandas.pydata.org/), this library will help us organize data for downstream analysis
3. Numerical Operation Libraries
    1. [Numpy](http://www.numpy.org/), used to perform efficient, vectorized mathematical operations and matrix handling
    2. [Scipy](https://www.scipy.org/), we will use the scipy statistics module to score our regression model
4. Visualization libraries, to visualize quality control and the model output
    1. [MatPlotLib](https://matplotlib.org/)
    2. [Seaborn](https://seaborn.pydata.org/)

## Workflow
This workflow should be tailored to the data set and phenotype of interest, but generally I follow the same general workflow. I start by setting up an analysis environment in [Jupyter](http://jupyterlab.readthedocs.io/en/stable/), this is followed by pre-processing the data and quality control. Finally, the model is fit and scored. In practice this process is also includes phenotype transformation and model tuning, both tasks aren't trivial and can be be time intensive. However, this basic workflow should highlight how some of the methylation biomarkers are fit.      

### Initialize an Analysis Environment
The first step to the analysis is setting directory paths, this is something I do for convenience, and importing external libraries.

```python
# set working directory where the series matrix data is stored
wd = 'path to working directory'

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.linear_model import LassoCV
from sklearn.model_selection import train_test_split

```
