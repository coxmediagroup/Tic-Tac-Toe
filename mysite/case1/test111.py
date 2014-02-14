from collections import Counter
WinList=[[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[4,5,7]]
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
pc=[1,4,7]
hm=[5,4,8]
print computerturn(hm,pc)
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
print whowin(hm,pc)