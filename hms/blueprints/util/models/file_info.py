# -*- coding: utf-8 -*-
import os

import sys
from flask import app


class FileInfo:

    def __init__(self):
        print('fileInfo')

    @classmethod
    def get_file_list(cls, file_path):
        fn = getattr(sys.modules['__main__'], '__file__')
        root_path = os.path.abspath(os.path.dirname(fn))
        # print(root_path)
        # print(os.path.abspath(__file__))
        # print(os.path.basename(__file__))
        # print (os.listdir("/hms/hms" + static/images/marker/icon_64"))
        # print (os.listdir("/hms/hms" + file_path))
        # print (os.listdir())sss
        # print(app.static_folder)

        for (path, dir, files) in os.walk("/hms/hms" + file_path):
            print(path)
            print(dir)
            print(files)

            return files

            # for filename in files:
            #     ext = os.path.splitext(filename)[-1]
            #     if ext == '.py':
            #         print("%s/%s" % (path, filename))
