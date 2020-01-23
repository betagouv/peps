from django.core.files.storage import FileSystemStorage

class PepsFileStorage(FileSystemStorage):
    """
    Prevents Django creating multiple identical files
    """

    def get_available_name(self, name, max_length=None):
        if max_length and len(name) > max_length:
            raise Exception("name's length is greater than max_length")
        return name

    def _save(self, name, content):
        if self.exists(name):
            return name
        return super(PepsFileStorage, self)._save(name, content)
