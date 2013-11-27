#!/bin/bash

# Part 1: Installing nesc
apt-get install automake
apt-get install emacs 
apt-get install bison 
apt-get install flex 
apt-get install gperf 
apt-get install git 
apt-get install gcc 
apt-get install java-devl 
apt-get install gcc-c++ 

git clone git://github.com/tinyos/nesc.git

cd nesc
./Bootstrap
./configure
make
make install

# Part 2: Installing TinyOS
git clone git://github.com/tinyos/tinyos-main.git

cd tinyos-main/tools
./Bootstrap
./configure
make
make install

# Part 3: Set environment variables in ~/.bashrc file
echo "export TOSROOT=$HOME/tinyos-main" >> ~/.bashrc
echo "export TOSDIR=$TOSROOT/tos" >> ~/.bashrc
echo "export MAKERULES=$TOSROOT/support/make/Makerules" >> ~/.bashrc
echo "export CLASSPATH=$TOSROOT/support/sdk/java/tinyos.jar:." >> ~/.bashrc
echo "export PYTHONPATH=$TOSROOT/support/sdk/python:$PYTHONPATH" >> ~/.bashrc
echo "export PATH=$TOSROOT/support/sdk/c:$PATH" >> ~/.bashrc
