---
layout: post
title: A Quick Introduction to Interactive Data Analysis in Python
date: 2018-06-19
excerpt: "A Quick Introduction to Interactive Data Analysis in Python with Jupyter"
teaching: True
tags: [Tutorial, Optimization]
comments: false
---

# Interactive Programing Environment for Analysis of Genomic Data

[Jupyter](http://jupyter.org/) provides an interactive programming environment that streamlines reproducible analysis of genomic datasets.
Jupyter notebooks allow the user compartmentalize code and objects, take notes with markdown, and quickly visualize datasets.
To effectively access data for analysis we want to work on a remote Jupyter instance that is running on the Hoffman2 cluster. Launching a jupyter instance is accomplished using the [Hoffman2Jupyter](https://github.com/NuttyLogic/NuttyLogic.github.io/blob/master/posts/post_assets/interactive_data_analysis/Hoffman2Jupyter.py) script. Hoffman2Jupyter has a command line interface to change settings or the initial script lines (below) can be
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
