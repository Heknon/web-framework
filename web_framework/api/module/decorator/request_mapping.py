from ..decorator import RequestMappingMeta
from web_framework.utils import set_meta_attribute


class RequestMapping:
    """
    URL filtering
    Acceptable http methods
    Error handling
    """

    def __init__(self, meta: RequestMappingMeta):
        self.meta = meta

    def __call__(self, t):
        return set_meta_attribute(t, self.meta)
