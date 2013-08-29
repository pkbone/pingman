from django.contrib.auth.decorators import login_required
from splunkdj.decorators.render import render_to
from splunklib.client import connect
from splunklib.client import Service
from django.http import Http404  
import datetime




@render_to('pingman:alert.html')
@login_required
def alert(request):
	#title=google&eventtype=pingloss&eventtime=08%2F27%2F2013+23%3A16%3A07&eventdesc=+host+cannot+be+reached+for++1+minute+&reportby=VMBA.local
	
	title = request.GET.get('title', '')
	eventtype = request.GET.get('eventtype', '')
	eventtime = request.GET.get('eventtime', '')
	eventdesc = request.GET.get('eventdesc', '')
	splunkserver = request.GET.get('reportby', '')
	related = request.GET.get('related', '')
	period = request.GET.get('period', '0')
	period = str(datetime.timedelta(seconds=int(period)))
	eventdesc = eventdesc.split("reach")
	if len(eventdesc) > 1 :
		eventdesc = eventdesc[0] + "reached"
	if eventtype=="pingsuccess":
		isok = True
	elif eventtype == "pingloss":
		isok = False
	else:
		raise Http404

	isweb = True
	return {
		"isok" : isok,
		"isweb" : isweb,
		"host" : title,
		"time" : eventtime,
		"desc"  : eventdesc,
		'related' : related,
		"reportby" : splunkserver,
		"period" : period,
		"app_name": "pingman"
    }



@render_to('pingman:dashboard.html')
@login_required
def dashboard(request):

	titleparam = request.GET.get('title', '')

	return {
		"message": titleparam  ,
		"app_name": "pingman"
    }


@render_to('pingman:home.html')
@login_required
def home(request):
	
	msg = ""
	#service = connect(
    #host=HOST,
 #    port=PORT,
 #    username=USERNAME,
 #    password=PASSWORD)
	# for item in service.inputs:
	# 	header =  "%s (%s)" % (item.name, item.kind)
	# 	msg = msg + header
	# 	msg = msg + '='*len(header)
	# 	content = item.content
	# 	for key in sorted(content.keys()):
	# 	 	value = content[key]
	# 		msg = msg + "%s: %s" % (key, value)
	# 	msg = msg + "\n"



	return {
		"message": msg  ,
		"app_name": "pingman"
    }

