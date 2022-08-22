'''
Created on 28-Mar-2019

@author: prasadh
'''

import sys
import subprocess
import types
import json

var_defs = []

fct = sys.argv[1].replace("--","")

if fct != "execute":
    get_vars_definition()

try:
    phpParameterFile = sys.argv[2]
    proc = subprocess.Popen("php "+str(phpParameterFile)+"", shell=True, stdout=subprocess.PIPE)
    script_response = proc.stdout.read()
    response = script_response.decode('utf-8')
    context = json.loads(response)
except NameError:
    context = dict()

def get_vars_definition():
    if function_exists('list_args'):
        list_args()
    
    else:
        var_defs = []
        
    vars = json.dumps(var_defs)
    print(vars)

def create_var_def(name, type = 'String', values = '', default_value = ''):
    if values != '' or type(values) is not dict:
        values = dict()
        
    var_def = {"name" : name,
               "type" : type,
               "values" : values,
               "default_value" :default_value }
    var_defs.append(var_def)
    
def isset(variable):
    return variable in locals() or variable in globals()

def function_exists(fun):
  try:
    ret = type(eval(str(fun)))
    return ret in (types.FunctionType, types.BuiltinFunctionType)
  except NameError:
    return False
