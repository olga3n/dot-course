#!/usr/bin/env bash

dr=`dirname $0`
file=${dr}/interface.proto 

protoc --python_out=. ${file}

