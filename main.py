from dicttoxml import dicttoxml
from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse, PlainTextResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

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


@app.get("/", response_class=FileResponse)
def return_index_page():
    return "src/index.html"  # file in {project_dir}/src/index.html
    # return "./public/index.html" # file in {project_dir}/src/index.html


@app.get("/file/{name}-{type}")
def download_file(name, type):
    return FileResponse("resources/for_download/31727044.jpg",
                        filename=name + "." + type,
                        media_type="application/octet-stream")


@app.get("/text", response_class=PlainTextResponse)  # декоратор
def read_root():
    # ERROR - нужно возвращать именно строку
    # return {
    #     'msg': 'Hello, Marolok!',
    #     'api type': 'GET',
    #     'content type': 'text'
    # }
    return ("<h2>TEXT + GET >>> Hello, Marolok!</h2><br>"
            "Message: Hello, Marolok!</br>"
            "API type: GET</br>"
            "Content type: text")


@app.get("/html")
def read_root():
    html_content = ("<h2>HTML + POST >>> Hello, Marolok!</h2><br>"
                    "Message: Hello, Marolok!</br>"
                    "API type: GET</br>"
                    "Content type: HTML")
    return HTMLResponse(content=html_content)


@app.get("/get/json")
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


@app.get("/get/xml")
def get_xml():
    xml_data = dicttoxml(data)
    xml_string = xml_data.decode('utf-8')
    return Response(content=xml_string, media_type="application/xml")
