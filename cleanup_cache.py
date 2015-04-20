#!/usr/bin/python
"""
Created on Mon Apr 20 16:40:11 2015
@author: mints
"""
import os
import time

def cleanup_cache():
    for filename in os.listdir('./static/output_cache'):
        st = os.stat('static/output_cache/'+filename)
        age = time.time() - st.st_mtime
        print filename, age
        if age > 3600 and filename[0]!= '_':
            os.unlink('static/output_cache/'+filename)

if __name__ == '__main__':
    cleanup_cache()