import os

from web_framework import MethodContentType, HttpMethod, HttpRequest, RequestMapping, GetMapping, PostMapping, \
    QueryParameter, HttpResponse, ConditionalHandler, HttpStatus, RequestBody, RequestMappingMeta, PathVariable


@GetMapping('calculate-next', content_type=MethodContentType.TEXT)
def handle_next(num: QueryParameter(parameter_type=int)):
    return num + 1


@GetMapping('test/{hi}/hfds', content_type=MethodContentType.JSON)
def request_body_test(hi: PathVariable()):
    return {"data": hi}


@GetMapping(content_type=MethodContentType.JSON)
@ConditionalHandler(condition=lambda req: not os.path.exists("webroot" + req.url))
def test(req: HttpRequest, res: HttpResponse, q: QueryParameter(parameter_type=int)):
    res.status = HttpStatus.NOT_FOUND
    return {"status": res.status, "url": req.url, "query_data": q}


@RequestMapping("/", "/index.html", acceptable_methods={HttpMethod.GET})
class Index:
    images = {}

    @staticmethod
    @GetMapping('calculate-area', content_type=MethodContentType.TEXT)
    def handle_area_calc(height: QueryParameter(parameter_type=int), width: QueryParameter(parameter_type=int)):
        return height * width / 2

    @staticmethod
    @PostMapping('upload', content_type=MethodContentType.TEXT)
    def handle_post(file_name: QueryParameter(name="file-name", parameter_type=str), request: HttpRequest):
        Index.images[file_name] = request.body
        return 'Accepted file ' + file_name + '!'

    @staticmethod
    @PostMapping('image', content_type=MethodContentType.TEXT)
    def get_image(image_name: QueryParameter(name="image-name", parameter_type=str)):
        return Index.images[image_name]
