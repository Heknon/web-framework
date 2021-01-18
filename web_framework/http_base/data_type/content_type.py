class ContentType:
    def __init__(self, content_type: str):
        self.__full_header = "Content-Type: " + self.__content_types[content_type.lower()]

    def __str__(self):
        return self.__full_header

    __content_types = {
        "html": "text/html; charset=utf-8",
        "htm": "text/html; charset=utf-8",
        "txt": "text/html; charset=utf-8",
        "text": "text/html; charset=utf-8",
        "js": "text/javascript; charset=utf-8",
        "css": "text/css",
        "jpg": "image/jpeg",
        'ico': "image/vnd.microsoft.icon",
        'gif': "image/gif",
        'json': 'application/json'
    }
