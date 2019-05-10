import splunk.admin as admin
import splunk.entity as en

# import your required python modules

'''
Copyright (C) 2005 - 2010 Splunk Inc. All Rights Reserved.
Description:  This skeleton python script handles the parameters in the configuration page.

      handleList method: lists configurable parameters in the configuration page
      corresponds to handleractions = list in restmap.conf

      handleEdit method: controls the parameters and saves the values 
      corresponds to handleractions = edit in restmap.conf

'''


class ConfigApp(admin.MConfigHandler):
    '''
    Set up supported arguments
    '''

    def setup(self):
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

    def handleList(self, confInfo):
        confDict = self.readConf("traffic-analyzer")
        if None != confDict:
            for stanza, settings in confDict.items():
                for key, val in settings.items():
                    if key in ['safe_browsing_api_key'] and val in [None, '']:
                        val = ''
                    if key in ['pcap_location'] and val in [None, '']:
                        val = ''
                    confInfo[stanza].append(key, val)

    '''
    After user clicks Save on setup page, take updated parameters,
    normalize them, and save them somewhere
    '''

    # def handleEdit(self, confInfo):
    #     name = self.callerArgs.id
    #     args = self.callerArgs
    #
    #     self.check_stanza("Safe Browsing", "safe_browsing_api_key")
    #     self.check_stanza("Paths", "pcap_location")
    #
    #     '''
    #     Since we are using a conf file to store parameters,
    # write them to the [setupentity] stanza
    #     in app_name/local/myappsetup.conf
    #     '''
    #
    # def check_stanza(self, stanza, field):
    #     data = {}
    #     if self.callerArgs.data[field][0] in [None, '']:
    #         self.callerArgs.data[field][0] = ''
    #         data[field] = self.callerArgs.data[field]
    #
    #     config_name = "traffic-analyzer"
    #     self.write_conf(config_name, stanza, data)

    def handleEdit(self, confInfo):
        name = self.callerArgs.id
        args = self.callerArgs

        if args.data['safe_browsing_api_key'][0] in [None, '']:
            args.data['safe_browsing_api_key'][0] = ''

        if args.data['pcap_location'][0] in [None, '']:
            args.data['pcap_location'][0] = ''

        '''
        Since we are using a conf file to store parameters, 
    write them to the [setupentity] stanza
        in app_name/local/myappsetup.conf  
        '''

        self.writeConf('traffic-analyzer', 'Custom Configuration', args.data)

# initialize the handler
admin.init(ConfigApp, admin.CONTEXT_NONE)
