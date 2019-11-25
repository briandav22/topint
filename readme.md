# API Script to get Interface Speed Information from Scrutinizer

In the top_int.py file you will need to update the scrutinizer_requester() with the hostname of your scrutinizer as well as a value auth token. 


## Filtering the Data  

*get_top_interfaces()* method on the ReportAPI() is responsible for setting up the params for the Requester(). This method takes some optional arguments incase you want to filter your request to the API. If you call this method without passing arguments to it, no filters will be applied (you will get all the interfaces back)

The arguments are: 

**search_type**

Options are 'interface', 'group', or 'device'. 

**search_value**

Specificies the value to be used in the search 

**comparison**

Specific the comparison you want, options are 'like' and 'notlike'. If you do not use the comparison option, it has a default value of 'like'. 


## Example Filters. 

All three of these would do the exact same thing. Specify the values in the method just makes it a little more careful that you are passing in the right order. 

*get_top_interfaces( search_type = 'interface' , search_value = 'mpls', comparison = 'like')*

*get_top_interfaces( search_type = 'interface' , search_value = 'mpls')*

*get_top_interfaces( 'interface' , 'mpls')*

## Data Returned 

There is a **dictionary_of_devices** that is set up in this file. That will hold all of that data, for now the script just prints that out at the end, but a flask app could be a potential endpoint that is hit at regular intervals to send the data back as JSON. 

## Data output
```json
{'PLXRCORE-R1.plxr.local': {
    'time': '2019-11-25 10:44', 
    'device_ip': '10.1.1.4', 
    'interfaces': [
        {'interface_name': '11 - Port Trunk 1 to Core Switch (Port-channel1)',
        'inbound_int_speed': 'Interface Speed: 10.00 Mb/s',
        'inbound_percent': '44.0755%',
        'inbound_bits': 'Rate: 4.41 Mb/s',
        'outbound_int_speed': 'Interface Speed: 20.00 Mb/s',
        'outbound_percent': '2.9969%',
        'outbound_bits_second': 'Rate: 599.38 kb/s'},
        {'interface_name': '12 - Port Trunk 2 TO Downstairs (Port-channel2)', 
        'inbound_int_speed': 'Interface Speed: 20.00 Mb/s', 
        'inbound_percent': '2.1079%', 
        'inbound_bits': 'Rate: 421.58 kb/s', 
        'outbound_int_speed': 'Interface Speed: 20.00 Mb/s', 
        'outbound_percent': '21.9042%', 
        'outbound_bits_second': 'Rate: 4.38 Mb/s'}]} 
```

