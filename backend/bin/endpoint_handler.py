import splunk.admin as admin

'''
Copyright (C) 2005 - 2010 Splunk Inc. All Rights Reserved.
Description:  This skeleton python script handles the parameters in the configuration page.

Adapted from anjo-hsr

      handleList method: lists configurable parameters in the configuration page
      corresponds to handleractions = list in restmap.conf

      handleEdit method: controls the parameters and saves the values 
      corresponds to handleractions = edit in restmap.conf

'''


class ConfigApp(admin.MConfigHandler):
    '''
    Set up supported arguments
    '''

    def setup(self) -> None:
        if self.requestedAction == admin.ACTION_EDIT:
            for arg in ['safe_browsing_api_key', 'pcap_location']:
                self.supportedArgs.addOptArg(arg)

    '''
    Read the initial values of the parameters from the custom file
        myappsetup.conf, and write them to the setup page. 
  
    If the app has never been set up,
        uses .../app_name/default/myappsetup.conf. 
  
    If app has been set up, looks at 
        .../local/myappsetup.conf first, then looks at 
    .../default/myappsetup.conf only if there is no value for a field in
        .../local/myappsetup.conf
  
    For boolean fields, may need to switch the true/false setting.
  
    For text fields, if the conf file says None, set to the empty string.
    '''

    def handleList(self, configuration_information) -> None:
        configuration_dictionary = self.readConf("traffic-analyzer")
        field_name_list = ["safe_browsing_api_key", "pcap_location"]
        if configuration_dictionary is not None:
            for stanza, settings in configuration_dictionary.items():
                for key, value in settings.items():
                    if self.is_tuple_empty(key, value, field_name_list):
                        value = ""

                    configuration_information[stanza].append(key, value)

    def is_tuple_empty(self, key, value, field_name_list) -> bool:
        return key in field_name_list and self.is_empty(value)

    '''
    After user clicks Save on setup page, take updated parameters,
    normalize them, and save them somewhere
    '''

    def handleEdit(self, _) -> None:
        args = self.callerArgs

        self.check_field_value("safe_browsing_api_key")
        self.check_field_value("pcap_location")

        '''
        Since we are using a conf file to store parameters, write them to the [setupentity]
        stanza in app_name/local/myappsetup.conf  
        '''

        self.writeConf("traffic-analyzer", "Custom Configuration", args.data)

    def check_field_value(self, field) -> None:
        if self.is_empty(self.callerArgs.data[field][0]):
            self.callerArgs.data[field][0] = ""

    @staticmethod
    def is_empty(value) -> bool:
        return value in [None, ""]


# initialize the handler
admin.init(ConfigApp, admin.CONTEXT_NONE)
