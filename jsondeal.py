import json
import os



json_data={
    "citycode":'',
    "gaodeApikey":''
}

configFile = 'config.json'
ConfigData={}



def get_config():   #处理配置文件
    global ConfigData
    with open(configFile,"r")as file:
        ConfigData=json.load(file)
get_config()

def get_citycode():
    return ConfigData['citycode']

def get_gaodeApikey():
    return ConfigData['gaodeApikey']