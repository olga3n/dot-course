#!/usr/bin/env bash

NAME=$1

PTH='/opt/spark-1.3.1'

$PTH/build/mvn package

if [[ $? == 0 ]]; then
	
	$PTH/bin/spark-submit \
		--driver-memory 2g \
		--class "TfIdf" \
		target/tf-idf-1.0.jar text text/${NAME}
fi
