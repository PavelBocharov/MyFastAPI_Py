import functools
import logging

from dicttoxml import dicttoxml
from fastapi import FastAPI, Path, Query, status, Body
from fastapi.responses import Response, JSONResponse, PlainTextResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s  [%(levelname)s] %(module)s [line: %(lineno)d] >> %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

app = FastAPI()
app.mount("/resources", StaticFiles(directory="resources"), name="resources") # https://metanit.com/python/fastapi/1.9.php

data = {
    'root': {
        'item1': 'value1',
        'item2': {
            'subitem1': 'subvalue1',
            'subitem2': 'subvalue2'
        },
        'item3': ['list_item1', 'list_item2']
    }
}


def api_logger(f):
    @functools.wraps(f)  # перенесет метаданные из недекорированной вызываемой функции в декорированную
    # def wrapper():
    def wrapper(*args, **kwargs):
        logger.debug(f"Start API: {f.__name__}. Args: {args}. KwArgs: {kwargs}")
        # rez = f()
        rez = f(*args, **kwargs)
        logger.debug(f"End API: {f.__name__}.")
        return rez

    return wrapper

@app.get("/", response_class=FileResponse)
@api_logger
def return_index_page():
    return "src/index.html"  # file in {project_dir}/src/index.html


@app.get("/search/{file_name}", status_code=status.HTTP_200_OK)
@api_logger
def search_file_by_name(response: Response, file_name: str = Path()):
    match file_name:
        case "ufo":
            return FileResponse("resources/for_download/ufo.jpeg", filename="ufo.jpeg",
                                media_type="application/octet-stream")
        case "cover":
            return FileResponse("resources/video1/cover.png", filename="cover.png",
                                media_type="application/octet-stream")
        case _:
            response.status_code = status.HTTP_204_NO_CONTENT
            # return JSONResponse(content={'msg': 'File not find.'}, status_code=status.HTTP_204_NO_CONTENT)
            # >>> h11._util.LocalProtocolError: Too much data for declared Content-Length
            return JSONResponse(content={'msg': f"File '{file_name}' not find."})


@app.get("/file")
@api_logger
def download_query_file(name: str | None = Query(pattern="([a-zA-Z0-9_-]+)", default=None, min_length=1),
                        extension: str | None = Query(pattern="jpg|jpeg|png|bmp", default=None, min_length=3,
                                                      max_length=4)):
    if name is None or extension is None:
        return FileResponse("resources/for_download/ufo.jpeg", filename="ufo.jpeg",
                            media_type="application/octet-stream")
    else:
        return FileResponse("resources/for_download/ufo.jpeg",
                            filename=name + "." + extension.lower(),
                            media_type="application/octet-stream")


@app.get("/file/{name}-{extension}")
@api_logger
def download_path_file(name: str = Path(pattern="([a-zA-Z0-9_-]+)", min_length=1),
                       extension: str = Path(pattern="jpg|jpeg|png|bmp", min_length=3, max_length=4)):
    return FileResponse("resources/for_download/ufo.jpeg",
                        filename=name + "." + extension.lower(),
                        media_type="application/octet-stream")


@app.get("/your/req/{test_p}")  # /your/req/my_req?test_q=12&test_q=awd
@api_logger
def pars_query(test_p: str = Path(),
               test_q: list[str] = Query()):
    json = {
        'path': test_p,
        'query': test_q
    }
    return JSONResponse(content=json)


@app.get("/text", response_class=PlainTextResponse)  # декоратор
@api_logger
def get_text():
    # ERROR - нужно возвращать именно строку
    # return {
    #     'msg': 'Hello, Marolok!',
    #     'api type': 'GET',
    #     'content type': 'text'
    # }
    return content("GET TEXT", "GET", "text")


@app.get("/html")
@api_logger
def get_html():
    html_content = content("GET HTML", "GET", "html")
    return HTMLResponse(content=html_content)


def content(header_text: str, api_type: str, content_type: str):
    return (f"<h2>{header_text}</h2></br>"
            "Message: Hello, Marolok!</br>"
            f"API type: {api_type.upper()}</br>"
            f"Content type: {content_type.upper()}")


@app.get("/json")
@api_logger
def get_json():
    # version 1
    # return data # dict -> JSON автоматом. + content-type:	application/json
    # ----------
    # version 2
    # data = {"message": "Hello METANIT.COM"}
    # json_data = jsonable_encoder(data)
    # return JSONResponse(content=json_data)
    # ----------
    # version 3
    return JSONResponse(content=data)


@app.get("/xml")
@api_logger
def get_xml():
    xml_data = dicttoxml(data)
    xml_string = xml_data.decode('utf-8')
    return Response(content=xml_string, media_type="application/xml")


@app.post("/hello")
# Version 1
# def hello(data = Body()):
#     name = data["name"]
#     age = data["age"]
#     return {"message": f"{name}, ваш возраст - {age}"}
# ---------
# Version 2 - get field
# @app.post("/hello")
# def hello(name = Body(embed=True), age = Body(embed=True)):
#     return {"message": f"{name}, ваш возраст - {age}"}
# ---------
# Version 3 - with rules
def hello(name:str  = Body(embed=True, min_length=3, max_length=20),
          age: int = Body(embed=True, ge=18, lt=111)):
    return {"message": f"{name}, ваш возраст - {age}"}

# TODO https://metanit.com/python/fastapi/1.11.php