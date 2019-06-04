wsk -i action update reduce-dataset ./src/actions/reduce_dataset.py -P config.local.json --docker dacat/openwhisk-python2action-mantid:latest

wsk -i action update mantid-reduce ./src/actions/mantid_reduce.py -m 1024 --docker dacat/openwhisk-python2action-mantid:latest
