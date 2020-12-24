"""
Author: Daryl.Xu
E-mail: xuziqiang@zyheal.com
"""
import logging
import os
import zipfile

from pdf_client_wrapper.rpc import pdf_pb2
from pdf_client_wrapper import app_config


def gen_stream(file_path: str):
    with open(file_path, 'rb') as f:
        chunk = f.read(app_config.CHUNK_SIZE)
        while chunk:
            logging.debug('the chunk, size: %d', len(chunk))
            # stub.uploadResource()
            yield pdf_pb2.Chunk(content=chunk)
            chunk = f.read(app_config.CHUNK_SIZE)


def zip_dir(source_dir: str, target_file: str):
    """
    将给定目录下的所有文件都添加到目标zip文件中

    Add all the files contained in the source_dir into the target_file(a zip file)
    """
    resources_path_length = len(source_dir)

    # TODO write to bytes instead of file
    with zipfile.ZipFile(target_file, 'w') as zip_file:
        path_iterator = os.walk(source_dir)
        for i in path_iterator:
            dirname = i[0]
            # print('iterator: ', i)
            for filename in i[2]:
                full_path = os.path.join(dirname, filename)
                arcname = full_path[resources_path_length:]
                print(f'related path: {arcname}')
                zip_file.write(full_path, arcname)
