## Fraud Detection System

> Fraud Detection System on PaySim dataset. Big Data course (CEDS841) at @ITA

## Objectives

In this work we simulate a small company which has a large dataset on banking transactions and want to create a new system to analyse and alert about possible frauds using Big data technologies. All the work was deployed and tested at **Amazon AWS**.

In the diagram bellow you can check the proposed architecture to solve this problem.

![alt text](https://github.com/Hguimaraes/bd-fraud/blob/master/assets/architecture.PNG)

*tl;dr*: The historical data from [PaySim](https://www.kaggle.com/ntnu-testimon/paysim1) was on a MySQL database at Amazon RDS. A small cluster with 3 nodes of m1.large machines (1 master and 2 nodes) was created at EMR. A Hive table was constructed with sqoop from RDS to the HDFS system and then connected to a spark module responsible to manage e delivery the product.

## Team

1. Anderson Carlos
2. Guilherme Cano
3. Heitor Guimarães
4. Rafael Barroso
5. Sostenes Gutembergue