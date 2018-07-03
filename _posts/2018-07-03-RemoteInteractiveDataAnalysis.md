---
layout: post
title: A Quick Introduction to Interactive Data Analysis in Python
date: 2018-07-03
excerpt: "A Quick Introduction to Interactive Data Analysis in Python with Jupyter"
teaching: True
tags: [Tutorial]
comments: false
---

# Interactive Programing Environment for Analysis of Genomic Data

[Jupyter](http://jupyter.org/) provides an interactive programming environment that streamlines reproducible analysis of genomic data sets.
Jupyter notebooks allow the users to compartmentalize code and objects, take notes with markdown, and quickly visualize results.
To effectively access data for analysis we want to work with a remote Jupyter instance that is running on the Hoffman2 cluster.

Using jupyter on Hoffman2 requires some initial setup before a notebook can be launched. To get started connect to hoffman2, request a computing node, and load python.  

```bash
# connect to the cluster and enter your password
ssh username@hoffman2.idre.ucla.edu

# request a computing node with minimal resources
qrsh

# load python
module load python/3.6.1
```

To work with a remote instance of jupyter we will have to generate a configuration file and then  set a password in the configuration file. Change the jupyter notebook password when prompted.

```python
jupyter notebook --generate-config
jupyter notebook password
Enter Password:
Verify Password:
```

With the password set you can now request a computing node running a jupyter notebook instance. Launching a jupyter instance is accomplished using the [Hoffman2Jupyter](https://github.com/NuttyLogic/BIG_Summer/blob/master/Hoffman2Jupyter.py) script. Hoffman2Jupyter has a command line interface to change settings or the initial script lines (below) can be
altered to change the resources requested and the username.

```python

username = ''
username = str(username)
timeinhours = 8
timeinhours = int(timeinhours)
memoryingb = 8
memoryingb = int(memoryingb)
numberofslots = 2
numberofslots = int(numberofslots)
port = 8789
port=int(port)
directory = ''
directory = str(directory)
opsys = platform.system()
opsys = str(opsys)
pythonver = '3.6.1'
pythonver = str(pythonver)

```

Once the setting have been changed launch the script and input your password when prompted.  

```bash
python2 Hoffman2Jupyter.py
```

A juypter instance running on a hoffman2 computing node will launch in your local browser.
