# Privacy Preserving Ridge Regression

Semester Project - Eurecom 2018/2019

*William Clot & Camille Plays*

<hr>

## Code Structure:

Most of our work is based around the discovery of new methods like homomorphic encryption or garbled circuits. All the code that is related to the discovery of those methods can be found in `Modules/`. We can find in particular:
* [**ABY**](/Modules/ABY) which is all the examples of code that we wrote using the ABY framework. And the `Dockerfile` than can be used to build ABY in a virtual environment.
* [**Cholesky**](/Modules/cholesky) which is just a Python code that implements the cholesky decomposition of a matrix in a vector type array of values.
* [**Pailler**](/Modules/pailler) which is all the examples of python code which is done using `phe` (pailler homomorphic encryption).
* [**Regression**](/Modules/regression) which is a set of python scripts that implement in clair the ridge regression using pandas and numpy. 

A part from that the real code for the project can be found in the `/PrivacyRegression` folder which is basically combining examples and snippets of code from the `Modules/` folder in order to achieve the main goal of the paper (a privacy preserving ridge regression).

Finally all the meeting notes and datasets are stored in their relative folder as well.

## How to use this code:

For the moment the different section of the project are still not connected with each other. 

To execute the encryption with paillier homomorphic encryption you simply need python3 with a `phe` (pailler homomorphic encryption) that can be installed easily using:
```bash
pip3 install phe
```

### Compiling ABY:

Compiling ABY clearly needs it's own section here. You will need ABY to be installed in one of the `include` folders during the linking phase of the compilation (we used `/usr/local/include`). ABY needs several libraries that are often not easy to find depending on your linux distribution. A easy solution we found to emulate an identical compilation environment is by using a Docker container.

All the information related to build the docker container can be found in the [Dockerfile](/Modules/ABY/Dockerfile). If Docker is installed on your machine you can easily compile ABY like so:
```bash
$ cd /Modules/ABY
$ sudo docker build . -t aby
```

Then to launch the docker container simply type: (enabling the current folder PWD to be access inside the container at /home).
```bash
$ sudo docker run -v /$PWD:/home -it aby
```

Once inside the container, to compile the code simply type:
```bash
$ mkdir build && cd build
$ cmake ..
$ make
```

You can then launch the CSP and Evaluator binaries in separates windows (using tmux for example).