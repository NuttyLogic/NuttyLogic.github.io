---
layout: post
title: Choosing Model Parameters
date: 2018-06-19
excerpt: "Performing a Grid Search to Select Regression Parameters"
teaching: True
tags: [Tutorial, Optimization]
comments: false
---
# Selecting Model Parameters
Selecting model parameters is a computationally expensive task, generally there is not an easy way to select the best parameters. As a result selecting the best model parameters comes down to testing all combinations of models parameters. To speed up this process we will run each combination of parameters in parallel across node in a cluster employed the sun/oracle grid engine (SGE).  
