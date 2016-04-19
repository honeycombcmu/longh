from flask import Flask, request
from subprocess import call
import json, requests, os.path
import commands
app = Flask(__name__)

PYSPARK_PATH = "/home/honeycomb/SparkService/src/PySpark.py"
HDFS_TRAIN = "/user/spark/input/sample_multiclass_classification_data.txt"
HDFS_TEST = "/user/spark/input/sample_multiclass_classification_data_test.txt"
MODEL1 = "LogisticRegression"
MODEL2 = "RandomForest"
PORT = 32768
BACK_URL = 'http://128.2.7.38:7124/task_finished/'
RESULT_ADDRESS = '/home/honeycomb/DEMODAY/'

@app.route("/", methods=['POST'])
def receive():
    task_id = str(request.form['task_id'])
    train_address = str(request.form['train_address'])
    test_address = str(request.form['test_address'])
    print "Received request: task_id: {}, train_address: {}, test_address: {}".format(task_id, train_address, test_address)
    call_Spark(task_id, train_address, test_address)
    back(task_id)
    return "Done."

@app.route("/status")
def test():
    return "Hello World!"

def call_Spark(task_id, train_address, test_address):
    #cmd = ["HADOOP_USER_NAME=hdfs", "hadoop", "fs", "-put", "-f", train_address, HDFS_TRAIN]
    cmd = "HADOOP_USER_NAME=hdfs hadoop fs -put -f {} {}".format(train_address, HDFS_TRAIN)
    print cmd
    #call(cmd, shell=True)
    print commands.getoutput(cmd)

    #cmd = ["HADOOP_USER_NAME=hdfs", "hadoop", "fs", "-copyFromLocal", "-f", test_address, HDFS_TEST]
    cmd = "HADOOP_USER_NAME=hdfs hadoop fs -put -f {} {}".format(test_address, HDFS_TEST)
    print cmd
    #call(cmd, shell=True)
    print commands.getoutput(cmd)

    #cmd = ["spark-submit", PYSPARK_PATH, HDFS_TRAIN, HDFS_TEST, task_id, MODEL1]
    cmd = "spark-submit {} {} {} {} {}".format(PYSPARK_PATH, HDFS_TRAIN, HDFS_TEST, task_id, MODEL1)
    print cmd
    #call(cmd)
    print commands.getoutput(cmd)

def back(task_id):
    path = RESULT_ADDRESS + str(task_id) + '.json'
    post_data = {'error': 1,  'task_id': task_id, 'result_address': path}
    if os.path.isfile(path):
        post_data['error'] = 0
    print post_data
    response = requests.post(BACK_URL, data=post_data)
    print response.content

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT, debug=True)