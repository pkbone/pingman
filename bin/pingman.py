import xml.dom.minidom, xml.sax.saxutils
import logging
import splunk.entity as entity
import sys, time
from subprocess import call


#set up logging suitable for splunkd comsumption
logging.root
logging.root.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.root.addHandler(handler)


SCHEME = """<scheme>
    <title>Ping</title>
    <description>Monitor host by ping</description>
    <use_external_validation>true</use_external_validation>
    <streaming_mode>simple</streaming_mode>
    <use_single_instance>false</use_single_instance>
    <endpoint>
        <args>
            <arg name="name">
                <title>pingman input name</title>
                <description>Name of this ping input, such as an alias name</description>
             </arg>
            <arg name="hostname">
                <title>Ping hostname/IP</title>
                <description>the hostname or IP address to monitor </description>
                <data_type>string</data_type>
            </arg>
            <arg name="ping_interval">
                <title>Ping interval (seconds)</title>
                <description>How many seconds to wait between pings</description>
                <data_type>number</data_type>
            </arg>
        </args>
    </endpoint>
</scheme>
"""

def do_scheme():
	print SCHEME

# prints XML error data to be consumed by Splunk
def print_error(s):
    print "<error><message>%s</message></error>" % xml.sax.saxutils.escape(s)


def validate_conf(config, key):
    if key not in config:
        raise Exception, "Invalid configuration received from Splunk: key '%s' is missing." % key

#read XML configuration passed from splunkd
def get_config():
    config = {}
    
    try:
        # read everything from stdin
        config_str = sys.stdin.read()
        logging.info("config_str: %s" % config_str)
        # parse the config XML
        doc = xml.dom.minidom.parseString(config_str)
        root = doc.documentElement
        conf_node = root.getElementsByTagName("configuration")[0]
        if conf_node:
            logging.debug("XML: found configuration")
            stanza = conf_node.getElementsByTagName("stanza")[0]
            if stanza:
                stanza_name = stanza.getAttribute("name")
                if stanza_name:
                    logging.debug("XML: found stanza " + stanza_name)
                    config["hostname"] = stanza_name
                    
                    params = stanza.getElementsByTagName("param")
                    for param in params:
                        param_name = param.getAttribute("name")
                        logging.debug("XML: found param '%s'" % param_name)
                        if param_name and param.firstChild and \
                           param.firstChild.nodeType == param.firstChild.TEXT_NODE:
                            data = param.firstChild.data
                            config[param_name] = data
                            logging.debug("XML: '%s' -> '%s'" % (param_name, data))
        
        checkpnt_node = root.getElementsByTagName("checkpoint_dir")[0]
        if checkpnt_node and checkpnt_node.firstChild and \
           checkpnt_node.firstChild.nodeType == checkpnt_node.firstChild.TEXT_NODE:
            config["checkpoint_dir"] = checkpnt_node.firstChild.data
        
        if not config:
            raise Exception, "Invalid configuration received from Splunk."
        
        # just some validation: make sure these keys are present (required)
        validate_conf(config, "hostname")
        validate_conf(config, "checkpoint_dir")
    except Exception, e:
        raise Exception, "Error getting Splunk configuration via STDIN: %s" % str(e)
    
    return config

def get_validation_data():
    val_data = {}
    
    # read everything from stdin
    val_str = sys.stdin.read()
    
    # parse the validation XML
    doc = xml.dom.minidom.parseString(val_str)
    root = doc.documentElement
    
    logging.debug("XML: found items")
    item_node = root.getElementsByTagName("item")[0]
    if item_node:
        logging.debug("XML: found item")
        
        name = item_node.getAttribute("name")
        val_data["stanza"] = name
        
        params_node = item_node.getElementsByTagName("param")
        for param in params_node:
            name = param.getAttribute("name")
            logging.debug("Found param %s" % name)
            if name and param.firstChild and \
               param.firstChild.nodeType == param.firstChild.TEXT_NODE:
                val_data[name] = param.firstChild.data
    
    return val_data



def validate_config(name):
  try:
	pass
  except Exception,e:
	print_error("Invalid configuration specified: %s" % str(e))
	sys.exit(1)

def run():
    config =get_config()
    
    name=config["hostname"]
    interval = float(config["ping_interval"])
    if interval < 1:
        interval = 60
	
    validate_config(name)
    logging.info("Start to Ping %s" % name)
    while True:
        call(["date", "+%Y-%m-%d %H:%M:%S"])
        call(["ping","-c 1", name])
        time.sleep(interval )



if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "--scheme":
            do_scheme()
        elif sys.argv[1] == "--validate-arguments":
            if len(sys.argv)>2:
		validate_config(sys.argv[2])
	    else:
		print 'supply hostname/ip'
        elif sys.argv[1] == "--test":
            print 'No tests for the scheme present'
        else:
            print 'You giveth weird arguments'
    else:
        run()
    
    sys.exit(0)
