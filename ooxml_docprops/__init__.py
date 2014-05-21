SUPPORTED_MIME_TYPES = set(
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
)


def is_supported_mimetype(mime_type):
    return mime_type in SUPPORTED_MIME_TYPES