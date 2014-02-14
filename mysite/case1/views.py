from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response,render
from django.http import HttpResponseRedirect
from collections import Counter
WinList=[[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]]


def index(request):
	# Request the context of the request.
	# The context contains information such as the client's machine details, for example.
	context = RequestContext(request)
	# Construct a dictionary to pass to the template engine as its context.
	# Note the key boldmessage is the same as {{ boldmessage }} in the template!
	context_dict = {'boldmessage': "I am bold font from the context"}
	#print "beging"
	# if 1>0:
	
	if request.method=='POST':		
		request.session['st'] = 'T'
		if  'Igo' in request.POST:
			# # print "IG"
			request.session['first'] = 'I'
			#return render_to_response('case1/page1.html',{"C5":" "})
			return HttpResponseRedirect('page1/')
		if 'Cgo' in request.POST:
			request.session['first'] = 'C'
			return HttpResponseRedirect('page1/')
			# print "CG"
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
	return render_to_response('case1/index.html', context_dict, context)
	
	
def page1(request):	

	context = RequestContext(request)
	who=request.session['first']
	#for reset the web page
	if 'reset' in request.POST:
		request.session.flush()
		return HttpResponseRedirect('/case1/')
	
	if  'st' in request.session:
		del request.session['st']
		if who=='I':
			res_dic={}
			request.session['dic'] = res_dic
			request.session['PC']=[]
			return render_to_response('case1/page1.html',{},context)
		else:
			request.session['PC']=[5]
			res_dic={"C5":"O"}
			request.session['dic'] = res_dic
			return render_to_response('case1/page1.html',res_dic,context)
	newCome=getData(request)
	pcList=request.session['PC']
	if 'HM' in request.session:
		hmList=request.session['HM']
	else:
		hmList=[]	
	res_dic=request.session['dic'] 
	#if click exist button no action
	if newCome in pcList+hmList:
		return render_to_response('case1/page1.html',res_dic,context)
	hmList.append(newCome)
	request.session['HM']=hmList
	res_dic['C'+str(newCome)]='X'
	if len(pcList)+len(hmList)!=9:	
		pcmove=computerturn(hmList,pcList)
		pcList.append(pcmove)
		res_dic['C'+str(pcmove)]='O'
	
	win=whowin(hmList,pcList)
	
	res_dic['C'+str(newCome)]='X'
	if win==1:
		res_dic['who1']="You Win!"
		for ii in range(1,10):
			res_dic['C'+str(ii)]='X'
		return render_to_response('case1/page1.html',res_dic,context)
	if win==-1:
		res_dic['who1']="PC Win!"
		for ii in range(1,10):
			res_dic['C'+str(ii)]='O'
		return render_to_response('case1/page1.html',res_dic,context)
	if win==0:
		res_dic['who1']="We tie!"
		for ii in range(1,10):
			res_dic['C'+str(ii)]='@'
		return render_to_response('case1/page1.html',res_dic,context)
	
	res_dic['pcgo']=pcmove
	res_dic['pclist']=pcList
	res_dic['hmlist']=hmList
	return render_to_response('case1/page1.html',res_dic,context)
	
def whowin(hm,pc):
	for ii in WinList:
		if set(ii)<=set(hm):
			return 1
	for ii in WinList:
		if set(ii)<=set(pc):
			return -1	
	if len(hm)+len(pc)==9:
		return 0
	return 2
	
	
def computerturn(hm,pc):
	hp=hm+pc
	open=[]
	for ii in WinList:
		if  len(set(ii)&set(hm))==0:
			open.append(ii)
	for ii in open:
		if len(set(ii)&set(pc))==2:
			return sum(set(ii)-(set(ii)&set(pc)))
	for ii in WinList:
		if  len(set(ii)&set(hm))==2 and len(set(ii)&set(pc))==0:
			return sum(set(ii)-(set(ii)&set(hm)))
	openel=[]
	for ii in open:
		openel.extend(set(ii)-(set(ii)&set(hp)))
	ecommon=[ii for ii,it in Counter(openel).most_common(1)]
	return ecommon[0]
		
			
	
def getData(request):
	if 'c1' in request.POST:
		return 1
	elif 'c2' in request.POST:
		return 2
	elif 'c3' in request.POST:
		return 3
	elif 'c4' in request.POST:
		return 4
	elif 'c5' in request.POST:
		return 5
	elif 'c6' in request.POST:
		return 6
	elif 'c7' in request.POST:
		return 7
	elif 'c8' in request.POST:
		return 8
	elif 'c9' in request.POST:
		return 9

	