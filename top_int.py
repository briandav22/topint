import scrut_api

from scrut_api import ReportAPI, Requester, ScrutPrint
import json
import csv
import re
import petl as etl

#some of the data comes back with HTML tages, use this reg-ex to remove them. 
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)


# Update with your Scrutinizer Information
scrutinizer_requester = Requester(
    authToken="Your Auth TOken",
    hostname="Your Scrutinizer"
)
report_params = ReportAPI()

## you can pass in filters if you want. if you don't want filters just leave this blank. 
report_params.get_top_interfaces()

int_data = scrutinizer_requester.make_request(report_params)


#dictionary where all devices will be kept. 
dictionary_of_devices = {}


for interface in int_data['rows']:
    #parse JSON and assign variables
    device_name = interface[4]['label']
    time = interface[0]['title']
    device_ip = interface[4]['ip']
    interface_name = interface[5]['label']
    inbound_percent = interface[7]['label']
    try: 
        inbound_speed = remove_tags(interface[7]['oTip']['rows'][0]['ul'][3])
        inbound_bits = remove_tags(interface[7]['oTip']['rows'][0]['ul'][4])
    except: 
        inbound_speed = ''
        inbound_bits = ''
    try: 
        outbound_speed = remove_tags(interface[8]['oTip']['rows'][0]['ul'][3])
        outbound_bits = remove_tags(interface[8]['oTip']['rows'][0]['ul'][4])
    except: 
        outbound_speed = ''
        outbound_bits = ''
    outbound_percent= interface[8]['label']

    interface_direction = interface[8]['type']


    #set up device object
    device_to_add = { device_name : {
        'time':time,
        'device_ip':device_ip,
        'interfaces':[{
            "interface_name":interface_name,
            "inbound_int_speed":inbound_speed, 
            "inbound_percent": inbound_percent,
            "inbound_bits":inbound_bits,
            "outbound_int_speed":outbound_speed,
            "outbound_percent":  outbound_percent,
            "outbound_bits_second":outbound_bits


        }]
    }}
    
    #check if this device has been seen before, if it has, update interface values
    if device_name in dictionary_of_devices:
        dictionary_of_devices[device_name]['interfaces'].append(
            {
            "interface_name":interface_name,
            "inbound_int_speed":inbound_speed, 
            "inbound_percent": inbound_percent,
            "inbound_bits":inbound_bits,
            "outbound_int_speed":outbound_speed,
            "outbound_percent":  outbound_percent,
            "outbound_bits_second":outbound_bits


        }
        )
    #if device not seen yet, then add it to the dictionary. 
    else:
        dictionary_of_devices.update(device_to_add)

## converting the dictionary I create when iterating through returned JSON into a list of dictionaries that was a bit easier to parse in petl.


list_of_data = []
for item in dictionary_of_devices:
    for interface in dictionary_of_devices[item]['interfaces']:
        new_dict = {
            'exporter_name': item,
            'time': dictionary_of_devices[item]['time'],
            'device_ip': dictionary_of_devices[item]['device_ip'],
            'interface_name': interface['interface_name'],
            'inbound_int_speed': interface['inbound_int_speed'],
            'inbound_percent': interface['inbound_percent'],
            'inbound_bits': interface['inbound_bits'],
            'outbound_int_speed': interface['outbound_int_speed'],
            'outbound_percent': interface['outbound_percent'],
            'outbound_bits_second': interface['outbound_bits_second']}
        list_of_data.append(new_dict)

#creates the petl table
scrutinizer_table_petl = etl.fromdicts(list_of_data, header=['exporter_name', 'time', 'device_ip','interface_name','inbound_int_speed','inbound_percent',  'inbound_bits', 'outbound_int_speed',  'outbound_percent', 'outbound_bits_second' ])

print(scrutinizer_table_petl)