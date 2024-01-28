from fastapi import FastAPI
from fastapi.responses import JSONResponse
from db.db import MongoManager

mm = MongoManager('', '')

app = FastAPI()

root = '/api'
app_list = [ "ad", "db", "dns", "file", "ftp", "fw", "ntp", "os", "proxy", "rep", "vpn", "web" ]

@app.get('%s/{collections}' % root)
async def get(collections):
    if collections in app_list:   
        mm.set_collections(collections)
        r = {'data': list(mm.find())}
        return JSONResponse(status_code=200, content=r)
    else:
        return JSONResponse(status_code=404, content={'data': f'Error: collections {collections} is not found'})
