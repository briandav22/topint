import requests
import requests.packages.urllib3
import json

requests.packages.urllib3.disable_warnings()



class ReportAPI:
    def __init__(self):
        
        self.options = {

            "reportTypeLang": "conversationsApp",
            "reportDirections": {"selected": "inbound"},
            "dataGranularity": {"selected": "5"},
            "orderBy": "sum_octetdeltacount",
            "times": {"dateRange": "LastHour"},
            "filters": {
                        "sdfDips_0": "in_GROUP_ALL"
                    },
            "rateTotal": {"selected": "rate"},
            "dataFormat": {"selected": "normal"},
            "bbp": {"selected": "percent"},
            "view":"topInterfaces",
            "unit":"percent"
        }
        self.direction = {
            "inbound": {
                "graph": "all",
                "table": {
                    "query_limit": {
                        "offset": 0,
                        "max_num_rows": 10
                    }
                }
            }
        }
        self.params = None
    def report_options(self,
                    reportTypeLang="conversationsApp",
                    reportDirections= "inbound",
                    dataGranularity="5",
                    orderBy="sum_octetdeltacount",
                    times={"dateRange": "LastHour"},
                    filters={
                        "sdfDips_0": "in_GROUP_ALL"
                    },
                    rateTotal={"selected": "rate"},
                    dataFormat={"selected": "normal"},
                    bbp={"selected": "percent"},
                    view="topInterfaces",
                    unit="percent"):
        self.options = {

            "reportTypeLang": reportTypeLang,
            "reportDirections": {"selected": reportDirections},
            "dataGranularity": {"selected": dataGranularity},
            "orderBy": orderBy,
            "times": times,
            "filters": filters,
            "rateTotal": rateTotal,
            "dataFormat": dataFormat,
            "bbp": bbp
        }

    def report_direction(self, report_direction="inbound", max_rows=10):
        self.direction = {
            report_direction: {
                "graph": "all",
                "table": {
                    "query_limit": {
                        "offset": 0,
                        "max_num_rows": max_rows
                    }
                }
            }
        }

    def get_ipgroup_name(self):
        self.params = {
            "rm":"get_known_objects",
            "type":"ipgroups"
        }

    def make_object(self):
        self.params = {
            "rm":"report_api",
            "action":"get",
            "rpt_json":json.dumps(self.options),
            "data_requested":json.dumps(self.direction)
        }

    def get_groups(self):
        self.params = {
            "rm":"mappingConfiguration",
            "view":"mapping_configuration",
            "session_state": {"client_time_zone":"America/New_York","order_by":[],"search":[],"query_limit":{"offset":0,"max_num_rows":500},"hostDisplayType":"dns"}
        }

    def get_exporters(self, group_id):
        self.params = {
                "rm": "mappingConfiguration",
                "id": group_id,
                "action": "getObjectsInGroup"
        }

    def get_top_interfaces(self, search_type= '', search_value = '', comparison='like'):
        
        #make everything lower case
        search_type = search_type.lower()
        comparison = comparison.lower()

        if search_type == 'interface':
            search = [{
                "column":"interface_search",
                "value":"{}".format(search_value),
                "comparison":comparison,
                "data":{"filterType":"multi_string"},
                "_key":"interface_search_like_{}".format(search_value)}]
        elif search_type == 'group':
            search = [{
                "column":"groupFilter",
                "value":"{}".format(search_value),
                "comparison":comparison,
                "data":{"filterType":"string"},
                "_key":"groupFilter_like_{}".format(search_value),
                "custom":"groupFilter"
                }]

        elif search_type == 'device':
            search = [{
                "column":"exporter_search",
                "value":"{}".format(search_value),
                "comparison":comparison,
                "data":{"filterType":"multi_string"},
                "_key":"exporter_search_like_{}".format(search_value)
                }]
        else:
            search = []

        self.params = {
            "rm":"status",
            "view":"topInterfaces",
            "unit":"percent",
            "session_state": json.dumps({
                "client_time_zone":
                "America/New_York",
                "order_by":[],
                "search":search,
                "query_limit":{"offset":0,"max_num_rows":10000000000},"hostDisplayType":"dns"})
        }


        






class Requester:
    def __init__(self, authToken=None, hostname=None):
        self.authToken = authToken
        self.hostname = hostname

    def error_checker(self, json):
        # error handler
        if 'err' in json:
            error_msg = json['err']
            if 'details' in json:
                error_details = json['details']
                print("Looks like you API key may not be valid, I received this back\nError: {}\nDetails: {},\nAPI Key: {}".format(
                    error_msg, error_details, self.authToken))
                return
            else:
                print("Did you pass an API key? Recieved this Error\nError: {}\nAPI Key: {}".format(
                    error_msg, self.authToken))
                return

    def verify_https(self, response, params):
        # used so the user doesn't have to worry about the URL to Scrutinizer, only the hostname.
        print(response.history)
        try:
            if response.history[0].status_code == 302:

                r = requests.get(
                    "https://{}/fcgi/scrut_fcgi.fcgi?".format(self.hostname), params=params, verify=False)
                return r
            elif response.status_code == 404:

                r = requests.get(
                    "https://{}/fcgi/scrut_fcgi.fcgi?".format(self.hostname), params=params, verify=False)
                return r
        except:
            print("Seems you are running Scrutinizer in HTTP, consider enabling SSL for more secure use of the API")
            return response

    def intiated_check(self):
        # checks to make sure the hostname and authtoken were passed
        if self.hostname == None or self.authToken == None:
            print("Did not receive either a Hostname or a Authoken when Class was initiated\nHere are the values I recieved: \nHostname:{} \nAuthtoken: {}".format(
                self.hostname, self.authToken))
            return True

    def make_request(self, report_object):

        # make sure user passed in hostname and authtoken
        params = report_object.params
        if self.intiated_check():
            return
        # add authToken to the Params
        params['authToken'] = self.authToken


        # make request to Scrutinizer
        data_back = requests.get(
            "https://{}/fcgi/scrut_fcgi.fcgi?".format(self.hostname), params=params, verify=False)


 

        # check to see if user is using HTTPS, if they are, make request to HTTPS address.
        # response = self.verify_https(data_back, params)

        # convert response to JSON.
        response = data_back.json()

        # check for any errors in the JSON response
        if self.error_checker(response):
            return

        # return the response

        return response



class ScrutPrint:
    '''Most used for error check and seeing the data Scrutinizer is returning. It prints the JSON data out in a nicely formatted way to make it easier to read.'''
    def __init__(self, data_to_print):
        self.scrut_class = data_to_print
        if isinstance(data_to_print, dict):
            print(json.dumps(data_to_print, indent=4, sort_keys=True))
        else:
            for attribute in self.scrut_class.__dict__:
                print(attribute + ' : ' +
                      str(self.scrut_class.__dict__[attribute]))
