---
layout: post
title: Launching a Jupyter Instance on the UCLA Hoffman2 Cluster
date: 2019-07-06
excerpt: "Guide to launching a remote jupyter instance for interactive data analysis"
project: True
tags: [Jupyter, Hoffman2]
comments: false
---

# Interactive Hoffman Programing Environment

[Jupyter](http://jupyter.org/) provides an interactive programming environment that streamlines reproducible analysis of data sets.
Jupyter notebooks allow users to compartmentalize code and objects, take notes with markdown, and quickly visualize results.
To effectively access data for analysis we want to work with a remote Jupyter instance that is running on the Hoffman2 cluster.

Using jupyter on Hoffman2 requires some light setup. The get jupyter working on Hoffman2 you first have to set a password 
by logging onto Hoffman2 and setting a jupyter password.

```bash
# connect to the cluster and enter your password
ssh username@hoffman2.idre.ucla.edu

# load your preferred versin of python
module load python/3.7.2

# generate a config file
jupyter lab --generate-config

# set a jupyter password
jupyter notebook password
Enter Password:
Verify Password:
```

You are now ready to work with a remote instance of jupyter. To automate the connection process we will use a a python script, [Hoffman2JupyterLauncher.py](https://github.com/NuttyLogic/Hoffman2JupyterLauncher), that
automates launching a remote jupyter notebook instance on the UCLA Hoffman2 cluster and forwarding the jupyter notebook port to your local machine.
My version of the script is a refactored version a [script](https://gitlab.idre.ucla.edu/dauria/jupyter-notebook)
provided by the UCLA [IDRE](https://idre.ucla.edu/). This script will fail if the port forwarded is in use.

```shell
usage: python3 Hoffman2JupyterLauncher -u sge_username -t time_in_hours -m memory_in_GB
                                -s cores -p port -d jupyter_directory
                               -c cluster_address -M module1 -M module2 ...

Script to launch remote jupyter instances on Hoffman2

optional arguments:
  -h, --help  show this help message and exit
  -u U        Hoffman2 username
  -t T        time in hours, default = 4
  -m M        memory in GB per slot, default = 4
  -s S        slots (cores), default = 2
  -p P        Port to output dictionary, default = 8790
  -d D        Hoffman2 directory to initialize jupyter, default = $HOME
  -c C        path to SGE cluster, default = idre.ucla.edu
  -M M        -M for each module you want to load, default python/3.6.1

```

To run the script without specifying inputs, change the default values in the argument parser.

```python
parser.add_argument('-u', type=str, default='sge user', help='hoffman2 username')
parser.add_argument('-t', type=int, default=8, help='time in hours, default = 4 ')
parser.add_argument('-m', type=int, default=8, help='memory in GB per slot, default = 4')
parser.add_argument('-s', type=int, default=2, help='slots (cores), default = 2 ')
parser.add_argument('-p', type=int, default=8790, help='Port to output dictionary, default = 8790, '
                                                       'if port is unavailable script will fail')
parser.add_argument('-d', type=str, default='$HOME', help='hoffman2 directory to initialize jupyter ')
parser.add_argument('-c', type=str, default='hoffman2.idre.ucla.edu', help='path to SGE cluster')
parser.add_argument('-M', type=str, default=['python/3.7.2'], action='append',
                    help='-M for each module you want to load')
```

## Setting Up and Extensible Jupyter Lab Environment on Hoffman2

By default the version of jupyter lab installed on the cluster is closed to jupyter lab extensions. To add extensions you 
have to add a nodejs and npm binary to your user path. Nodejs and npm are necessary for recompiling jupyter lab after 
installing extensions. Additionally, as of July 15th, 2019, Hoffman2 does not have the necessary SSL certificates to validate 
urls when updated jupyter lab extensions. The jupyter lab source can be modified to avoid this issue by overriding the SSL certificate 
checks, but this is an unsafe workaround.

```shell
# create local directory if it doesn't exist and add to path
mkdir -p local
cd local
echo 'export PATH=$HOME/local/bin:$PATH' >> ~/.bashrc

# pull and extract binary
wget https://nodejs.org/dist/v10.16.0/node-v10.16.0-linux-x64.tar.xz
tar -xf node-v10.16.0-linux-x64.tar.xz
mv node-v10.16.0-linux-x64/bin/* bin/

# install jupyter labs as user
pip3 install jupyterlab --user
```

To use an extensible version of jupyter lab you need to modify the launcher script as listed below.

```python
# change line 121 in the jupyter launcher to launch jupyter instance using local install

#old line
self.ssh_connection.stdin.write('jupyter lab --port=%s --no-browser\n' % self.port)
# new line
self.ssh_connection.stdin.write('${HOME}/.local/bin/jupyter lab --port=%s --no-browser\n' % self.port)
```

Open the juypter commands file (${HOME}/.local/lib/python3.7/site-packages/jupyterlab/commands.py) and edit accordingly.

```python
# import ssl library, add import command to test
import ssl

# modify the following line 
# in function def _fetch_package_metadata(registry, name, logger):

# change
with contextlib.closing(urlopen(req)) as response:
# to
with contextlib.closing(urlopen(req, context=ssl._create_unverified_context())) as response:
```
