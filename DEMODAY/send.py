#!/usr/bin/python -tt

import requests

TRAIN_ADDRESS = "/home/honeycomb/SparkService/data/sample_multiclass_classification_data.txt"
TEST_ADDRESS = "/home/honeycomb/SparkService/data/sample_multiclass_classification_data_test.txt"

def main():
	my_json = {'task_id':'101', 'train_address':TRAIN_ADDRESS, 'test_address':TEST_ADDRESS}
	r = requests.post('http://127.0.0.1:32768/', data=my_json)

if __name__ == '__main__':
  main()

