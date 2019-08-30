from sanic import Sanic
from sanic.response import json
import pydsb, pyuntis, requests

app = Sanic()
app.config.from_pyfile("config.py")

dsb = pydsb.PyDSB(app.config.DSB_USER, app.config.DSB_PASSWORD)
dsb.login()


@app.route("/")
async def api(request):
    urls = [file["url"] for file in dsb.get_plans() if file["is_html"]]
    result = []
    for url in urls:
        text = requests.get(url).text
        plan = pyuntis.PyUntis(text)
        result.append(plan.parse())

    return json(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
