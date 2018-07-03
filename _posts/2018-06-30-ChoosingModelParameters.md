---
layout: post
title: Selecting Model Parameters
date: 2018-07-03
excerpt: "Performing a Grid Search to Select Regression Parameters"
teaching: True
tags: [Tutorial, Optimization]
comments: false
---
# Selecting Model Parameters
Selecting model parameters is a computationally expensive task, generally there is not an easy way to select the best parameters. As a result selecting the best model parameters comes down to testing all possible combinations of models parameters. To speed up this process we will run each combination of parameters in parallel across nodes in a cluster with a job scheduler, sun/oracle grid engine (SGE), in place.

To choose parameters we will make use of custom code for parameter selection,[SciKitLearnModelSelection](https://github.com/NuttyLogic/SciKitLearnModelSelection). To import classes from this library include the library directory in your python path, then import as normal. We will make use of test data from from [Aging effects on DNA methylation modules in human brain and blood tissue, 5](https://www.ncbi.nlm.nih.gov/pubmed/23034122), data cleaning was performed in an earlier tutorial on fitting an [epigentic clock](https://nuttylogic.github.io/EpigeneticClockExample/).

### Data Import and Preprocessing

We first want to set paths our working directory and the save the file name as a variable.
```python
# Set working directory and input data path
wd = 'path to working directory'
geo_file = 'file name'
```

We want to modify the python system paths to import external files to process the data and wrap Sci-Kit Learn models.

```python
sklearn_model_wappers = 'path_to_/SciKitLearnModelSelction'
series_matrix_parsers = 'path_to_/matrix_parsers'
import sys
sys.path.append(sklearn_model_wappers)
sys.path.append(series_matrix_parsers)
```

With the python path modified, we now import all of the external libraries we will employ for the analysis.


```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
import math
import matplotlib.pyplot as plt
from ParameterRandomization import RandomizeParameters
from BatchJobGenerator import  LaunchOptimizationJob
from SeriesMatrixParser import SeriesMatrixParser
```

### Data Preprocessing
Data preprocessing will follow the same workflow as a previous tutorial on fitting an [epigenetic clock](https://nuttylogic.github.io/EpigeneticClockExample/).


```python
# import and parse the methylation data
example_matrix = SeriesMatrixParser(f'{wd}{geo_file}')
example_matrix.run(description_ids=['!Series_title', '!Series_geo_accession', '!Series_pubmed_id', '!Series_summary',
                             '!Series_overall_design', '!Series_sample_id', '!Series_relation'],
               sample_id='!Sample_geo_accession',
               phenotype_ids=['!Sample_characteristics_ch1'],
               matrix_start='!series_matrix_table_begin')
# initialize a pandas dataframe
example_matrix_df = pd.DataFrame(data=example_matrix.matrix[1:-1], columns=example_matrix.matrix[0])
example_matrix_df = example_matrix_df.set_index('"ID_REF"')
example_matrix_df = example_matrix_df.apply(pd.to_numeric, errors='coerce')
# drop row containing null values
example_matrix_df = example_matrix_df.dropna(axis=0)

# collect phenotype info
example_matrix_age = [int(x) for x in example_matrix.phenotype_matrix['age']]
```
As part of the preprocessing step we will perform PCA and remove outliers.

```python
# define a PCA object
qc_pca = PCA(n_components=4, whiten=False)
# fit the PCA object
qc_pca_values = qc_pca.fit_transform(example_matrix_df.values.T)

pc1 = qc_pca_values[:,0]
pc2 = qc_pca_values[:,1]

# scatter plot of first two PCs, and retrieve and sample outliers
# list to store sample outliers
non_outlier_list = []
non_outlier_age = []
# iterate through pc1, pc2, and sample labels to add labels to plotted points
for x, y, label, age in zip(pc1, pc2, list(example_matrix_df), example_matrix_age):
    # add outliers to list
    if x < 5:
        non_outlier_list.append(label)
        non_outlier_age.append(age)
```

## Split Data into a Testing and Validation Set

We want to split the data into a testing and training dataset. For downstream analysis we will drop all of the outlier samples.
```python
# want a list of sample names
sample_ids = list(example_matrix_df[non_outlier_list])

X_train, X_test, y_train, y_test = train_test_split(sample_ids, non_outlier_age, test_size=0.3)

# take dataframe values as a numpy array and transpose the array with .T
X_train_array = example_matrix_df[X_train].values.T
X_test_array = example_matrix_df[X_test].values.T
```

## Parameters Search
To search for parameters we will modify a dictionary of standard input arguments.  We will then pass a dictionary containing lists for different parameters we want to consider. All combination of parameters will be considered, so there is a practical limit to the number of parameters that can be feasibly searched. As a general strategy I first consider a few dramatic parameter changes then perform a more focused parameter search based on the results from the first search. In this example we will modify parameters for SKLearn [ElasticNetCV](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNetCV.html). The default argument for the ElasticNetCV are list below.


```python
# Create a dictionary with default arguments
elastic_net_default = {'l1_ratio':0.5,
                       'eps':0.001,
                       'n_alphas':100,
                       'alphas':None,
                       'fit_intercept':True,
                       'normalize':False,
                       'precompute':'auto',
                       'max_iter':1000,
                       'tol':0.0001,
                       'cv':None,
                       'copy_X':True,
                       'verbose':0,
                       'n_jobs':8,
                       'positive':False,
                       'random_state':None,
                       'selection':'cyclic'}
```

For this example we will consider model with different lasso penalty weights and the different path lengths. We initialize a dictionary with lists of values for the parameters we are interested in searching. We pass this dictionary along with the default arguments dictionary into the RandomizeParameters class, this class return a tuple of dictionaries that contain all combinations of the input arguments.


```python
parameter_dict = {'l1_ratio':[.1,.9], 'eps':[0.01, 0.0001]}
```


```python
en_kwargs_tuple = RandomizeParameters(input_dictionary=elastic_net_default, randomization_dictionary=parameter_dict).get_randomized_parameters()
print(en_kwargs_tuple)
```

    ({'l1_ratio': 0.1, 'eps': 0.01, 'n_alphas': 100, 'alphas': None, 'fit_intercept': True, 'normalize': False, 'precompute': 'auto', 'max_iter': 1000, 'tol': 0.0001, 'cv': None, 'copy_X': True, 'verbose': 0, 'n_jobs': 8, 'positive': False, 'random_state': None, 'selection': 'cyclic'}, {'l1_ratio': 0.1, 'eps': 0.0001, 'n_alphas': 100, 'alphas': None, 'fit_intercept': True, 'normalize': False, 'precompute': 'auto', 'max_iter': 1000, 'tol': 0.0001, 'cv': None, 'copy_X': True, 'verbose': 0, 'n_jobs': 8, 'positive': False, 'random_state': None, 'selection': 'cyclic'}, {'l1_ratio': 0.9, 'eps': 0.01, 'n_alphas': 100, 'alphas': None, 'fit_intercept': True, 'normalize': False, 'precompute': 'auto', 'max_iter': 1000, 'tol': 0.0001, 'cv': None, 'copy_X': True, 'verbose': 0, 'n_jobs': 8, 'positive': False, 'random_state': None, 'selection': 'cyclic'}, {'l1_ratio': 0.9, 'eps': 0.0001, 'n_alphas': 100, 'alphas': None, 'fit_intercept': True, 'normalize': False, 'precompute': 'auto', 'max_iter': 1000, 'tol': 0.0001, 'cv': None, 'copy_X': True, 'verbose': 0, 'n_jobs': 8, 'positive': False, 'random_state': None, 'selection': 'cyclic'})


Wth the model parameters set, we will now specify paths to data and data labels, and convert the list to a tuple to ensure immutability.


```python
regression_dict_list = []

for count, grid_search in enumerate(en_kwargs_tuple):
    regression_dict = {'x':X_train_array,
                       'y':y_train,
                       'sample_labels':X_train,
                       'sk_elastic_net_kwargs':grid_search,
                       'regression_site_labels':list(example_matrix_df.index),
                       'output_name':f'{count}_grid_search.txt',
                       'output_directory':wd,
                       'test_split':0}
    regression_dict_list.append(regression_dict)
regression_dict_tuple = tuple(regression_dict_list)
```

## Launch Gridsearch Job
To fit the model we input SGE specifications for the job. We will specify the number of cores, the memory required, the time required for the job, the user name, the SGE report output folder, and the number of simultaneous jobs. Finally we will have to speficy where the model interface is located on the server, this is necessary to call a job wihin python and parse the necessary information. When the class is initialized a serialized file containing all the input data is placed in the the output folder.  This serialized file is then loaded by the model interface when the resources become available to run the job.  


```python
grid_search =  LaunchOptimizationJob(dictionary_tuple=regression_dict_tuple,
                                    model_interface='/u/home/c/colinpat/SciKitLearnModelSelction/LaunchElasticNet.py',
                                     sge_cores=4,
                                     sge_mem=2,
                                     sge_time=1,
                                     simultaneous_jobs=4,
                                     optimization_batch_name='ex_age',
                                     optimization_batch_directory=wd,
                                     sge_output_folder='/u/home/c/colinpat/job_outputs/',
                                     sge_user='colinpatfarrell@g.ucla.edu')

```

## Import First Search Jobs
After running the jobs we would like to check the results. First we will define functions to parse the output information then we can launch additional jobs if necessary to further search the parameter space.


```python
def line_split(line):
    return line.replace('\n', '').split('\t')

def model_info_parser(file):
    parsed_file = []
    with open(file, 'r') as info:
        for line in info:
            l = line_split(line)
            parsed_file.append(l)
    return parsed_file

def model_f_dict(parsed_list):
    model = {}
    model['label'] = parsed_list[0][0].replace('.txt', '')
    model['score'] = float(parsed_list[1][0].split(' ')[-1])
    model['arguments'] = parsed_list[3][1:]
    model['test_samples'] = parsed_list[4][1:]
    model['test_predicted'] = [float(x) for x in parsed_list[5][1:]]
    model['test_actual'] = [float(x) for x in parsed_list[6][1:]]
    model['training_samples'] = parsed_list[7][1:]
    model['training_actual'] = [float(x) for x in parsed_list[8][1:]]
    model['regression_sites'] = parsed_list[9][1:]
    return model

def format_model_info(file):
    p_list = model_info_parser(file)
    p_dict = model_f_dict(p_list)
    return p_dict
```

Import model results, and look at performance.

```python
model_info_container = []

for model in regression_dict_tuple:
    name = model['output_name']
    info_path = f'{wd}{name}.model_info.txt'
    model_info_container.append(format_model_info(info_path))
```

Plot histogram of R^2 values.

```python
score_container = []

for model in model_info_container:
    score_container.append(model['score'])

ax, fig = plt.subplots(figsize=(12,12))
plt.hist(score_container)
plt.title('Model Performance')
plt.ylabel('Count')
plt.xlabel('R**2')
plt.show()
```
![](https://github.com/NuttyLogic/NuttyLogic.github.io/blob/master/posts/post_assets/parameter_optimization/model_score.png?raw=true)
