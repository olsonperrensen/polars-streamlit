from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from great_tables import GT, md, html
from great_tables.data import islands

islands_mini = islands.head(10)

app = FastAPI()


@app.get("/",response_class=HTMLResponse)
async def html_table():
    gt_tbl = GT(islands_mini)
    return gt_tbl.as_raw_html()
