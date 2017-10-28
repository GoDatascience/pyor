import tempfile
import os
from shutil import copy
import hashlib

import pathlib
from flask import Flask
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from eve.io.media import MediaStorage

from pyor.models import FileSource

# BLOCKSIZE value to efficently calculate the MD5 of a file
BLOCKSIZE = 104857600

class FileWrapper(object):

    def __init__(self, file_source: FileSource):
        self.file_source = file_source
        fd = os.open(self.file_source.filepath, os.O_RDONLY)
        self._file = os.fdopen(fd, 'rb')

    def __getattr__(self, attr):
        if hasattr(self.file_source, attr):
            return getattr(self.file_source, attr)
        return getattr(self._file, attr)

    def __iter__(self):
        return self._file.__iter__()

    def close(self):
        self._file.close()


class PyorMediaStorage(MediaStorage):

    """The File System class stores files into disk.
    It uses the MEDIA_PATH configuration value.
    """

    def __init__(self, app=None):
        """Constructor.
        :param app: the flask application (eve itself). This can be used by
        the class to access, amongst other things, the app.config object to
        retrieve class-specific settings.
        """
        super(PyorMediaStorage, self).__init__(app)

        self.validate()
        self._fs_path = self.app.config['MEDIA_PATH']

    def validate(self):
        """Make sure that the application data layer is a eve.io.mongo.Mongo
        instance.
        """
        if self.app is None:
            raise TypeError('Application object cannot be None')

        if not isinstance(self.app, Flask):
            raise TypeError('Application object must be a Eve application')

        if not self.app.config.get('MEDIA_PATH'):
            raise KeyError('MEDIA_PATH is not configured on app settings')

    def get(self, id, resource=None):
        """Return a FileSource object given by unique id. Returns None if no
        file was found.
        """

        return FileWrapper(FileSource.objects.get(id=id))

    def put(self, content: FileStorage, filename:str=None, content_type:str=None, resource:str=None):
        """ Saves a new file in disk. Returns the unique id of the stored
        file. Also stores content type, length, md5, filename and upload date of
        the file.
        """
        fd, fp = tempfile.mkstemp()
        content.save(fp)

        file_source = FileSource(content_type=content_type or content.content_type,
                                 md5=get_md5(fp),
                                 length=os.path.getsize(fp),
                                 filename="null",
                                 filepath="null")

        try:
            file_source.original_filename = secure_filename(filename)
        except AttributeError:
            file_source.original_filename = secure_filename(content.filename)

        file_source.save()

        file_source.filename = '{oid}_{filename}'.format(oid=str(file_source.id),
                                               filename=file_source.original_filename)
        dirpath = os.path.join(self._fs_path, resource)
        file_source.filepath = os.path.join(dirpath, file_source.filename)
        file_source.save()

        pathlib.Path(dirpath).mkdir(parents=True, exist_ok=True)

        copy(fp, file_source.filepath)
        os.close(fd)
        os.remove(fp)

        return str(file_source.id)

    def delete(self, id, resource=None):
        FileSource.objects(id=id).delete()

    def exists(self, id, resource=None):
        return FileSource.objects(id__exists=id)


def get_md5(file_path):
    """Helper function to calculate MD5 value for a given file.
    :param file_path: File path.
    """
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(BLOCKSIZE)

    return hasher.hexdigest()