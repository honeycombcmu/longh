# path to the PySpark program
PYSPARK_PATH = "/home/honeycomb/SparkService/src/PySpark.py"

# name of the train data in HDFS
HDFS_TRAIN = "/user/spark/input/sample_multiclass_classification_data.txt"

# name of the test data in HDFS
HDFS_TEST = "/user/spark/input/sample_multiclass_classification_data_test.txt"

# candidate model 1
MODEL1 = "LogisticRegression"

# candidate model 2
MODEL2 = "RandomForest"

# the external port for receiving requests
PORT = 32768

# the call back URL
BACK_URL = 'http://128.2.7.38:7124/task_finished/'

# where to put the result files
RESULT_ADDRESS = '/home/honeycomb/DEMODAY/'



#Usage:
python receive.py or nohup python receive.py &

# URL for check the server status
http://128.2.7.38:32768/status

# check the status of a port
netstat -apn|grep <port number>
example:
netstat -apn|grep 32768

# kill the listener:
kill pid

