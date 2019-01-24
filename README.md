# Privacy Preserving Ridge Regression

Semester Project - Eurecom 2018/2019

*William Clot & Camille Plays*

<hr>

## What is this project about?

This project is following this [paper](https://ieeexplore.ieee.org/document/6547119) written by Valeria Nikolaenko, Udi Weinsberg, Stratis Ioannidis, Marc Joye, Dan Boneh
& Nina Taft. This paper talks about a privacy preserving ridge regression which is using homomorphic encryption as well as garbled circuits between two parties.

This project is using their paper to implement this hybrid method of computation to evaluate the performance of such a solution.

## Motivations:

This repository is submitted as a semester project at EURECOM proposed by Melek Önen and Beyza Bozdemir.

## Code Structure:

Most of our work is based around the discovery of new methods like homomorphic encryption or garbled circuits. All the code that is related to the discovery of those methods can be found in `Modules/`. We can find in particular:
* [**ABY**](/Modules/ABY) which is all the examples of code that we wrote using the ABY framework. And the `Dockerfile` than can be used to build ABY in a virtual environment.
* [**Cholesky**](/Modules/cholesky) which is just a Python code that implements the cholesky decomposition of a matrix in a vector type array of values.
* [**Pailler**](/Modules/pailler) which is all the examples of python code which is done using `phe` (pailler homomorphic encryption).
* [**Regression**](/Modules/regression) which is a set of python scripts that implement in clair the ridge regression using pandas and numpy. 

A part from that the real code for the project can be found in the `/PrivacyRegression` folder which is basically combining examples and snippets of code from the `Modules/` folder in order to achieve the main goal of the paper (a privacy preserving ridge regression).

Finally all the meeting notes and datasets are stored in their relative folder as well.

## Library and dependencies:

To use our code you will need to compile ABY first:

#### Compiling ABY:

Compiling ABY clearly needs it's own section here. You will need ABY to be installed in one of the `include` folders during the linking phase of the compilation (we used `/usr/local/include`). ABY needs several libraries that are often not easy to find depending on your linux distribution. A easy solution we found to emulate an identical compilation environment is by using a Docker container.


##### Compiling ABY through a Docker container:

All the information related to build the docker container can be found in the [Dockerfile](Dockerfile). If Docker is installed on your machine you can easily compile ABY like so in the root of the repository:
```bash
$ sudo docker build . -t aby
```

If all goes well here you'll get ABY compiled within the docker image and all the python libraries needed to execute the code.

##### Compiling ABY on the machine:

This only worked for me using Ubuntu 18.10. But here are the steps we took to install ABY.

Firstly, install all the libraries needed to compile ABY:
```bash
$ sudo apt-get install make
$ sudo apt-get install g++
$ sudo apt-get install cmake
$ sudo apt-get install libgmp-dev
$ sudo apt-get install libssl-dev
$ sudo apt-get install libboost-all-dev
```

Then clone the ABY github repository: 
```bash
$ git clone https://github.com/encryptogroup/ABY
```

Then install ABY in a system PATH folder like so (here we install ABY in `/usr/local`):
```bash
$ mkdir build && cd build/
$ cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local
$ make 
$ make install
```

If you managed to get here: well done, ABY is installed on your machine.

To run our code you'll need python3 installed with a few libraries:
```bash
$ sudo apt-get install -q -y python3-pip
$ pip3 install pandas
$ pip3 install phe
$ pip3 install numpy
$ pip3 install xlrd
```

## How to use this code:

To use our code you will need to compile ABY first (See ABY compilation section if needed).


#### Using our code inside docker containers:

Now that you have built a docker image named aby you can launch a docker container simply like so: (enabling the current folder PWD to be access inside the container at /home).
```bash
$ sudo docker run -v /$PWD:/home -it aby
```

If you want to execute the privacy preserving code you will need to create three docker containers (CSP, Evaluator and Users) using separate IP addresses on the same network. You will first need to create a docker network as soo:
```bash
$ docker network create --subnet=172.18.0.0/16 mynetwork
```

Now we need to create the three different docker containers. Open un three different terminals and execute one of the commands in each one:
```
$ sudo docker run -v /$PWD:/home --net mynetwork --name Users --ip 172.18.0.24 -it --rm aby
$ sudo docker run -v /$PWD:/home --net mynetwork --name Evaluator --ip 172.18.0.22 -it --rm aby
$ sudo docker run -v /$PWD:/home --net mynetwork --name CSP --ip 172.18.0.23 -it --rm aby
```

The remaining instruction to use our code are then exactly the same then without docker.

#### Using our code without docker containers: 

You can compile the C++ code in PrivacyPreserving/garbled_circuit/ like so:
```bash
$ mkdir build && cd build
$ cmake ..
$ make
```

You should now get two binaries `Evaluator_Circuit` `CSP_Circuit` inside the build folder. To run the privacy preserving programm you'll need three terminals open and simply run the three python scripts: 
```
$ ./Users.py
$ ./Evaluator.py
$ ./CSP.py
```

##### Common errors:

- Don't forget to download the datasets by doing `./getDataset.sh` inside the Datasets folder.
- If you're running the code without docker you'll need to change the ip addresses of the differents members involded by going into /PrivacyRegression/classes/utils.py and putting `127.0.0.1` as ip address for the CSP, Evaluator and Users.
