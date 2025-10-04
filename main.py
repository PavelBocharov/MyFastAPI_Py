from dicttoxml import dicttoxml
from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse, PlainTextResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

import logging
import functools

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
app.mount("/resources", StaticFiles(directory="resources"), name="resources")

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


@app.get("/file/{n}-{t}")
@api_logger
def download_file(n, t):
    return FileResponse("resources/for_download/ufo.jpeg",
                        filename=n + "." + t,
                        media_type="application/octet-stream")


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
