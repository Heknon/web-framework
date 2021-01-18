import os

from web_framework import MethodReturnContentType, HttpMethod, HttpRequest, RequestMappingMeta, RequestMapping, GetMapping, PostMapping, QueryParameter, HttpResponse, HttpClient, ConditionalHandler, HttpStatus


@RequestMapping(RequestMappingMeta("/", "/index.html", acceptable_methods={HttpMethod.GET}))
class Index:
    images = {}

    @staticmethod
    @GetMapping(content_type=MethodReturnContentType.TEXT)
    @ConditionalHandler(condition=lambda req: not os.path.exists("webroot" + req.url))
    def test(res: HttpResponse):
        res.status = HttpStatus.NOT_FOUND
        return "PATH DOES NOT EXIST"

    @staticmethod
    @GetMapping('calculate-area', content_type=MethodReturnContentType.TEXT)
    def handle_area_calc(height: QueryParameter(parameter_type=int), width: QueryParameter(parameter_type=int)):
        return height * width / 2

    @staticmethod
    @GetMapping('calculate-next', content_type=MethodReturnContentType.TEXT)
    def handle_next(num: QueryParameter(parameter_type=int)):
        return num + 1

    @staticmethod
    @PostMapping('upload', content_type=MethodReturnContentType.TEXT)
    def handle_post(file_name: QueryParameter(name="file-name", parameter_type=str), request: HttpRequest):
        Index.images[file_name] = request.body
        return 'Accepted file ' + file_name + '!'

    @staticmethod
    @PostMapping('image', content_type=MethodReturnContentType.TEXT)
    def get_image(image_name: QueryParameter(name="image-name", parameter_type=str)):
        return Index.images[image_name]
