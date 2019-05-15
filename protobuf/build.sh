#!/bin/bash

# This script will build the protobufs for this project. To compile the protobufs for
# other languages, you can add append arguments to ./build.sh. Python example:
# ./protobuf/build.sh --python_out=$HOME/stopwatch-analysis

# cd into script directory first to avoid extra folders in generated output.
# for example, running this from the project root makes the python output be
# a file in a folder called protobuf.
cd $(dirname $0)

protoc --swift_out=. --python_out=../scripts "$@" data.proto
