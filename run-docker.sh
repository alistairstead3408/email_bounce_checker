#!/bin/bash

docker build -t ucamcldtg/email-bounce-checker . && docker run -p 5000:5000 -it ucamcldtg/email-bounce-checker
