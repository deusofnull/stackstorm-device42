from lib.base_action import BaseAction
from st2client.client import Client 
from st2client.models import KeyValuePair 

import time, requests, json, random, string 

class LC_ObjCat_Updater(BaseAction):

    def put(self, url, payload, user, pw):
        try:  
            res = requests.put(
                url,
                auth=(user, pw),
                headers={'Accept': 'application/json'}, 
                data=payload,
                verify=False # https call to localhost requires skipping verification
            )
        except requests.exceptions.RequestsException as e:
            self.logger.error( e )
            sys.exit(1)
        self.logger.info("HTTP GET %s - status: %s " % (url, res.status_code) ) 
        
        return res 
         
    def run(self, identifier, identifier_type, lc_type_id, additional_changes):
        
        st2client = Client(base_url='http://localhost') 
        
        # search st2 datastore for value stored under the lifecycle event id
        # in the datastore, the IDs are stored under the format lc_{lc event id} so prepend 'lc_'
        key = "lc_%s" % lc_type_id 
        lc_type_name = st2client.keys.get_by_name(name=key) 
        
        # add device identifier to payload   
        payload = {identifier_type: identifier}  
        
        # change obj cat with the LC name (as a basic example) 
        changes = {
            "new_object_category": "%s_lc" % (lc_type_name.value), 
        }
        
        payload.update(changes) 
        
        payload.update(additional_changes)
         
        url = 'device/'
        response = self.putAPI(url, data=payload) 
        
        return response 

