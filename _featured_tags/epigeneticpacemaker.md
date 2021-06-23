---
layout: page
type: tag
title: Epigenetic Pacemaker
slug: EpigeneticPacemaker
category: tools
sidebar: true
---

# Epigenetic Pacemaker

## A fast conditional expectation maximization algorithm for modeling epigenetic states

DNA methylation is widely used to model physiological phenotypes, such as 
aging[<sup>1</sup>](https://doi.org/10.1186/gb-2013-14-10-r115) and type II diabetes[<sup>2</sup>](https://doi.org/10.1093/hmg/ddy093). 
The Epigenetic Pacemaker, **EPM**, is an implementation of a fast conditional expectation maximization algorithm that models 
epigenetic states under and evolutionary framework[<sup>3</sup>](https://doi.org/10.2217/epi-2017-0130). The EPM was first introduced by Snir et al.
[<sup>4</sup>](https://doi.org/10.1371/journal.pcbi.1005183) as an extension of the Universal Pacemaker (UPM) model of genome evolution. In contrast to regression 
bases approaches, the EPM does not assume a linear relationship between the epigenetic state and a trait of interest.
As a result the EPM can model non-linear epigenetic trait associations directly without transformation of the phenotype of
interest[<sup>5</sup>](https://doi.org/10.1080/15592294.2019.1623634).
The software implementation of the Epigenetic Pacemaker is described our publication [*The Epigenetic Pacemaker - modeling epigenetic states under an evolutionary framework*](https://academic.oup.com/bioinformatics/article-abstract/doi/10.1093/bioinformatics/btaa585/5861533?redirectedFrom=fulltext)<sup>6</sup>.

## Installation

```shell
pip3 install EpigeneticPacemaker
```

## Documentation

[epigeneticpacemaker.readthedocs.io](https://epigeneticpacemaker.readthedocs.io/en/latest/)

## EPM Algorithm

### EPM Description

Given $i$ methylation sites and $j$ individuals a single methylation site can be described
as $\hat{m}_{ij} = m^0_i + r_is_j + \epsilon _{ij}$ where $\hat{m}_{ij}$ is the observed methylation value, $m^0_i$ is
the initial methylation values, $r_i$ is the rate of change, $s_j$ is the epigenetic state, and $\epsilon _{ij}$
is a normally distributed error term. Given an input matrix $\hat{M} = [\hat{m_{ij}}]$ the goal of the EPM is
find the optimal values of $m^0_i$, $r_i$, and $s_j$ to minimize the error between the predicted and
observed methylation values across a system of methylation sites. Under the EPM $m^0_i$ and $r_i$ are characteristic
of the site for all individuals and $s_j$ is shared by all sites within a system of methylation sites for every
individual.

The EPM optimization is accomplished through an implementation of a fast conditional expectation maximization algorithm
that maximizes the model likelihood by minimizing the residual sum of squares error. When fitting the EPM each
methylation site is assigned an independent rate of change and starting methylation value, while each individual is
assigned an epigenetic state. The initial epigenetic state is provided by the user and should represent a best guess.
The epigenetic state is then updated through each iteration of the EPM to  minimize the error across
the observed epigenetic landscape. Because the $s_j$ is updated while fitting the EPM the condition of linearity
between the methylation values and trait of interest is relaxed.

### EPM Implementation

The EPM algorithm is implemented as follows

1. fit $i$ site models using the user provided state predictions to get $r_i$ and $m_0$
2. update $s_j$ to minimize $\epsilon_{ij}^2$
      - $s_j = \frac{\sum_{i \leq n} r_i(\hat{m_{ij}} - m^0_i)}{\sum_{i \leq n} r^2_i}$
3. refit site models using $s_j$
4. repeat step 2 and 3 until model improvements $\leq$ specified threshold or maximum number of iterations reached

## References

1. [Horvath, S. DNA methylation age of human tissues and cell types. Genome Biol. 14, R115 (2013).](https://doi.org/10.1186/gb-2013-14-10-r115)
2. [Orozco, L. D. et al. Epigenome-wide association in adipose tissue from the METSIM cohort. Hum. Mol. Genet. 0, 223495 (2018).](https://doi.org/10.1093/hmg/ddy093)
3. [Snir, S. & Pellegrini, M. An epigenetic pacemaker is detected via a fast conditional expectation maximization algorithm. 10, 695–706 (2018).](https://doi.org/10.1371/journal.pcbi.1005183)
4. [Snir, S., vonHoldt, B. M. & Pellegrini, M. A Statistical Framework to Identify Deviation from Time Linearity in Epigenetic Aging. PLoS Comput. Biol. 12, 1–15 (2016).](https://doi.org/10.2217/epi-2017-0130)
5. [Snir, S., Farrell, C. & Pellegrini, M. Human epigenetic ageing is logarithmic with time across the entire lifespan. Epigenetics (2019). doi:10.1080/15592294.2019.1623634](https://doi.org/10.1080/15592294.2019.1623634
