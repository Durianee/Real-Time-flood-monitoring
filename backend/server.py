from flask import Flask, request, render_template_string, jsonify
import requests
from datetime import datetime, timedelta, timezone
from flask_caching import Cache

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 900  # 15 分钟缓存
cache = Cache(app)

API_BASE = "https://environment.data.gov.uk/flood-monitoring"
STATIONS_ENDPOINT = f"{API_BASE}/id/stations?_view=full"

@app.route("/", methods=["GET"])
def index():
    error_message = ""
    try:
        resp = requests.get(STATIONS_ENDPOINT, timeout=10)
        resp.raise_for_status()
        stations_json = resp.json()
        station_items = stations_json.get("items", [])
    except Exception as e:
        station_items = []
        error_message = f"获取监测站列表失败：{str(e)}"

    # 提取所有需要的字段
    stations = []
    for item in station_items:
        station_ref = item.get("stationReference")
        if station_ref:
            stations.append({
                "label": item.get("label", "无名称"),
                "stationReference": station_ref,
                "town": item.get("town", ""),
                "riverName": item.get("riverName", ""),
                "dateOpened": item.get("dateOpened", ""),
                "status": item.get("status", ""),
                "RLOIid": item.get("RLOIid", ""),
                "notation": item.get("notation", ""),
                "wiskiID": item.get("wiskiID", ""),
                "lat": item.get("lat"),
                "long": item.get("long"),
                "easting": item.get("easting"),
                "northing": item.get("northing"),
                "catchmentName": item.get("catchmentName", ""),
                "measures": item.get("measures", []),
                "stageScale": item.get("stageScale", {}),
                "downstageScale": item.get("downstageScale", {}),
                "statusReason": item.get("statusReason", ""),
                "statusDate": item.get("statusDate", "")
            })

    html_template = """
    <!doctype html>
    <html lang="zh">
    <head>
      <meta charset="UTF-8">
      <title>监测站列表 - 后端测试</title>
      <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        .station { margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid #ccc; }
        .field { margin: 2px 0; }
      </style>
    </head>
    <body>
      <h1>监测站列表</h1>
      {% if error_message %}
        <p style="color:red;">{{ error_message }}</p>
      {% endif %}
      {% for station in stations %}
        <div class="station">
          <div class="field"><strong>名称：</strong> {{ station.label }}</div>
          <div class="field"><strong>站点标识：</strong> {{ station.stationReference }}</div>
          <div class="field"><strong>城市：</strong> {{ station.town }}</div>
          <div class="field"><strong>河流：</strong> {{ station.riverName }}</div>
          <div class="field"><strong>开站日期：</strong> {{ station.dateOpened }}</div>
          <div class="field"><strong>状态：</strong> {{ station.status }}</div>
          <div class="field"><strong>RLOIid：</strong> {{ station.RLOIid }}</div>
          <div class="field"><strong>notation：</strong> {{ station.notation }}</div>
          <div class="field"><strong>wiskiID：</strong> {{ station.wiskiID }}</div>
          <div class="field"><strong>经纬度：</strong> {{ station.lat }}, {{ station.long }}</div>
          <div class="field"><strong>英国网格坐标：</strong> Easting: {{ station.easting }}, Northing: {{ station.northing }}</div>
          <div class="field"><strong>集水区：</strong> {{ station.catchmentName }}</div>
          <div class="field"><strong>测量指标：</strong>
            <ul>
              {% for measure in station.measures %}
                <li>
                  {{ measure.parameterName }} ({{ measure.parameter }}) - 周期: {{ measure.period }} 秒,
                  修饰: {{ measure.qualifier }}, 单位: {{ measure.unitName }}
                </li>
              {% endfor %}
            </ul>
          </div>
          <div class="field"><strong>阶段量程：</strong> {{ station.stageScale }}</div>
          <div class="field"><strong>下游量程：</strong> {{ station.downstageScale }}</div>
          <div class="field"><strong>状态原因：</strong> {{ station.statusReason }}</div>
          <div class="field"><strong>状态更新时间：</strong> {{ station.statusDate }}</div>
        </div>
      {% endfor %}
    </body>
    </html>
    """
    return render_template_string(html_template, error_message=error_message, stations=stations)

@app.route("/api/stations", methods=["GET"])
@cache.cached(timeout=900)
def api_stations():
    try:
        resp = requests.get(STATIONS_ENDPOINT, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("items", [])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(items)

@app.route("/api/station/<station_id>", methods=["GET"])
@cache.cached(timeout=900)
def api_station_detail(station_id):
    station_url = f"{API_BASE}/id/stations/{station_id}.json"
    try:
        resp = requests.get(station_url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(data)

@app.route("/api/readings/<station_id>", methods=["GET"])
@cache.cached(timeout=900, query_string=True)
def api_readings(station_id):
    period = request.args.get("period", "24h")
    if period == "24h":
        since_time = datetime.now(timezone.utc) - timedelta(hours=24)
    elif period in ["7d", "week", "7days"]:
        since_time = datetime.now(timezone.utc) - timedelta(days=7)
    else:
        since_time = datetime.now(timezone.utc) - timedelta(hours=24)
    since_str = since_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    readings_url = f"{API_BASE}/id/stations/{station_id}/readings?since={since_str}&_sorted"
    try:
        resp = requests.get(readings_url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("items", [])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(items)

if __name__ == "__main__":
    app.run(debug=True)
