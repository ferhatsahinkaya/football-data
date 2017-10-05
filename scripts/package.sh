#!/usr/bin/env bash
lambda_name=$1
rm lambda/${lambda_name}.zip
cd src/aws && zip -r ../lambda/${lambda_name}.zip ${lambda_name}.py && cd -
cd lib/python3.6/site-packages && zip -r ../../../lambda/${lambda_name}.zip * && cd -