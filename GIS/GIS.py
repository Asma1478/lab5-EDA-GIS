import pandas as pd,os, sys, json, requests
import folium 
import csv
import webbrowser

def main():
    sensors = []
    with open('sensors.csv', 'r') as f:
        csv_file = csv.reader(f)
        next(csv_file)
        for row in csv_file:
            lat, lng, = float(row[1]), float(row[2])
            name = row[0]
            app_id = row[3]
            dev_id = row[4]
            status = row[10]
            details = row[11]
            sensors.append([lat, lng, name, app_id, dev_id, status, details])

    # sensors = []
    # # with open('sensors.csv', 'r') as f:
    # #     csv_file = csv.reader(f)
    # #     next(csv_file)
    # #     for row in csv_file:
    # #         lat, lng, sensor_name, status, additional_details = float(row[1]), float(row[2]), row[0],row[10], row[11], 
    # #         sensors.append([lat, lng, sensor_name, status, additional_details])

    m = folium.Map(location=[60.48746, 15.409658], zoom_start=14)

    for sensor in sensors:
        sensor_ids = 'app_id: {}, dev_id: {}'.format(sensor[3],sensor[4])
        sensor_info = 'Status: {}, Sensors: {} <a href="https://requestbin.com/r/end2o0vro9agd%22%3ELive data</a>'.format(sensor[5], sensor[6])


        if sensor[2] == 'Elsys ELT2': 
            blg_map = folium.Marker(location=sensor[:2], tooltip=sensor_ids, popup=sensor_info, icon=folium.Icon(icon='info-sign', color='blue')).add_to(m)
            blg_map.save('sensors_gateways.html')

        if sensor[2] == 'Elsys ERS CO2':
            blg_map = folium.Marker(location=sensor[:2], tooltip=sensor_ids, popup=sensor_info, icon=folium.Icon(icon='info-sign', color='red')).add_to(m)
            blg_map.save('sensors_gateways.html')

        if sensor[2] == 'ESP32':
            blg_map = folium.Marker(location=sensor[:2], tooltip=sensor_ids, popup=sensor_info, icon=folium.Icon(icon='info-sign', color='orange')).add_to(m) 
            blg_map.save('sensors_gateways.html')

        if sensor[2] == 'Arduino':
            blg_map = folium.Marker(location=sensor[:2], tooltip=sensor_ids, popup=sensor_info, icon=folium.Icon(icon='info-sign', color='purple')).add_to(m)
            blg_map.save('sensors_gateways.html')
   
    url = 'https://www.thethingsnetwork.org/gateway-data/location?latitude=60.48746&longitude=15.40965&distance=200000'
    response = requests.get(url)
    json_data = json.loads(response.text)
    gateway_ids = ['a84041ffff21b068', '3133303719004400', 'eui-b827ebfffedf20e3', 'gw-p07', 'indoor-labb-milesight', 'mechatronicscubicle-gw1', 'raboda', 'se-sto-bbt04',
                   'tcab-gateway-02', 'ttnind001', 'campus-borlange-gateway', 'creativeenabler05']

    for id in gateway_ids:

        dev_id = 'id: {}'.format(id)
        lat = json_data[id]['location']['latitude']
        lng = json_data[id]['location']['longitude']
        gateway_info = 'Latitude: {}, Longitude: {}'.format(lat, lng)
        location = [lat, lng]

        blg_map = folium.Marker(location=location, tooltip=dev_id, popup=gateway_info, icon=folium.Icon(icon='info_circle', color='darkblue')).add_to(m)
        blg_map.save('sensors_gateways.html')


    legend_html = '''
    <div style="position: fixed; 
    bottom: 50px; left: 50px; width: 180px; height: 180px; 
    border:2px solid grey; z-index:9999; font-size:14px;
    ">&nbsp; <b>Legend </b><br>
    &nbsp; Gateways &nbsp; <img src="gateway.png" width="18px" height="26px" align="top"></i><br>
    &nbsp; Elsys ELT2 &nbsp; <i class="fa fa-map-marker fa-2x" style="color:blue"></i><br>
    &nbsp; Elsys ERS CO2 &nbsp; <i class="fa fa-map-marker fa-2x" style="color:red"></i><br>
    &nbsp; ESP32 &nbsp; <i class="fa fa-map-marker fa-2x" style="color:orange"></i><br>
   &nbsp; Arduino &nbsp; <i class="fa fa-map-marker fa-2x" style="color:purple"></i><br>
    </div>
    ''' 
    m.get_root().html.add_child(folium.Element(legend_html))

    m.save('sensors_gateways.html')
    webbrowser.open_new_tab('sensors_gateways.html')


if __name__ =="__main__": 
    main()
    