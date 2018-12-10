
docker create -v /Users/williamclot/Documents/Etude/Eurecom/2019/Project/PrivacyRegression/garbled_circuit:/home --net network --name Evaluator --ip 172.18.0.22 -it aby
docker create -v /Users/williamclot/Documents/Etude/Eurecom/2019/Project/PrivacyRegression/garbled_circuit:/home --net network --name CSP --ip 172.18.0.23 -it aby
docker create -v /Users/williamclot/Documents/Etude/Eurecom/2019/Project/PrivacyRegression/garbled_circuit:/home --net network --name Users --ip 172.18.0.24 -it aby
