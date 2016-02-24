#!/usr/bin/env python

import sys, json
import tempfile
from urlparse import urlparse
from subprocess import call

APP_NAME = 'spark-submit'
DST = 'dst_file'

def get_local_copy(uri, local_path):
    parsed = urlparse(uri)
    if parsed.scheme == "s3":
        cmd = ["aws", "s3", "cp", uri, local_path]
    elif parsed.scheme == "https":
        cmd = ["wget", "-O", local_path, uri]
    else:
        cmd = ["cp", uri, local_path]

    call(cmd)

    return local_path

def process(source_uri, order, workspace_uri):
    # do something here
    local_path = get_local_copy(source_uri, DST)

    return local_path


if __name__ == '__main__':
    from pyspark import SparkConf, SparkContext

    request_uri = sys.argv[1]
    # hardcode for test
    request_uri = '{"files": ["src_file"], \
                    "workspace": "", \
                    "jobId": "test-job"}'
    request = json.loads(request_uri)

    source_uris = request["files"]
    workspace = request["workspace"]
    jobId = request["jobId"]

    conf = SparkConf().setAppName(APP_NAME)
    sc = SparkContext(conf=conf)

    uri_sets = sc.parallelize(enumerate(source_uris)).flatMap(lambda (o, i): process(i, o, workspace))
    source_tile_count = uri_sets.cache().count()

    print "Done."
