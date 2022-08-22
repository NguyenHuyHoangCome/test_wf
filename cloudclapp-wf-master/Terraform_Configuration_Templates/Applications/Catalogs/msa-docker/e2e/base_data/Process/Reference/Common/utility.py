'''
Created on 28-Mar-2019

@author: prasadh
'''
from constants import *
import json


 # Prepare a Json response
 #
 # @param unknown $wo_status
 # @param unknown $wo_comment
 # @param unknown $wo_newparams
 # @param string $log_response
 # @return string
 
def prepare_json_response(wo_status, wo_comment, wo_newparams, log_response = False):
     if(type(wo_newparams) is not dict and (wo_newparams[0,1] == "{" or wo_newparams[0,1] == "[")):
         wo_newparams = json.loads(wo_newparams)
         
     response = { "wo_status" : wo_status, 
                "wo_comment" : wo_comment, 
                "wo_newparams" : wo_newparams }
     response = json.dumps(response)
     return response
 
 
 

