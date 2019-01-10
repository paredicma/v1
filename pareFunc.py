##################### PAREDICMA ( PYTHON AUTOMATIC REDIS CLUSTER MAKER) ############
#!/usr/bin/python
#-*- coding: utf-8 -*-
## Author			: Mustafa YAVUZ 
## E-mail			: msyavuz@gmail.com,paredicma@gmail.com
## Version			: 0.4
## Date				: 26.12.2018
## OS System 		: Redhat/Centos 6-7, debian/Ubuntu
## Redis Version 	: 5.0.0 and above
##################PARAMETERS################################
import os
import commands
from time import *
from pareConfig import *
from pareNodeList import *
import socket
from string import *
from screenMenu import *
def clusterCheck(contactNode):
	myNodeIP=pareNodes[contactNode-1][0][0]
	myNodePORT=pareNodes[contactNode-1][1][0]
	clusterString=redisBinaryDir+'src/redis-cli --cluster check '+myNodeIP+':'+myNodePORT+''	
	if(redisPwdAuthentication == 'on'):
		clusterString+=' -a '+redisPwd+' '	
	retVal='Unkown'
	checkStatus,checkResponse = commands.getstatusoutput(clusterString)		
	if ( checkResponse.find('[ERR]') != -1 ):
		return False
	else:
		return True
def clusterFix(contactNode):
	myNodeIP=pareNodes[contactNode-1][0][0]
	myNodePORT=pareNodes[contactNode-1][1][0]
	clusterString=redisBinaryDir+'src/redis-cli --cluster fix '+myNodeIP+':'+myNodePORT
	if(redisPwdAuthentication == 'on'):
		clusterString+=' -a '+redisPwd+' '
	retVal='Unkown'
	fixStatus,fixResponse = commands.getstatusoutput(clusterString)		
	if ( fixResponse.find('[OK]') != -1 ):
		return True
	else:
		return False
def showRedisLogFile(nodeIP,nodeNum,portNumber,myLineNum):
	if(nodeIP==pareServerIp):
		returnCmd,cmdResponse = commands.getstatusoutput('tail -'+myLineNum+' '+redisLogDir+'redisN'+nodeNum+'_P'+portNumber+'.log')
		print (bcolors.OKGREEN+cmdResponse+bcolors.ENDC)
		raw_input(bcolors.BOLD+'\n----------------------\nPress Enter to Return Paredicman Menu'+bcolors.ENDC )
	else:
		returnCmd,cmdResponse = commands.getstatusoutput('ssh -q -o "StrictHostKeyChecking no"  '+pareOSUser+'@'+nodeIP+' -C  "tail -'+myLineNum+' '+redisLogDir+'redisN'+nodeNum+'_P'+portNumber+'.log"')
		print (bcolors.OKGREEN+cmdResponse+bcolors.ENDC)
		raw_input(bcolors.BOLD+'\n----------------------\nPress Enter to Return Paredicman Menu'+bcolors.ENDC )
def clusterSlotBalanceMapper(balanceStrategy,maxSlotBarier):
	nodeNumber=0
	contactNode=-1
	spResponse=''
	myNodeInfoList=[]
	allSlotNumber=16386
	if(maxSlotBarier==0):
		maxSlotBarier=4000	
	maxSlotBarier+=1
	for pareNode in pareNodes:
		nodeIP=pareNode[0][0]
		portNumber=pareNode[1][0]
		nodeNumber=nodeNumber+1
		if ( pareNode[4] ):
			isPing=pingNode(nodeIP,portNumber)
			if (isPing):
				if(contactNode==-1):
					contactNode=nodeNumber
#				spStatus,spResponse = commands.getstatusoutput(redisConnectCmd(nodeIP,portNumber,' CLUSTER NODES |  grep master |  grep myself | grep -v fail'))
				spStatus,spRes = commands.getstatusoutput(redisConnectCmd(nodeIP,portNumber,' CLUSTER NODES |  grep master |  grep myself | grep -v fail'))
				if (len(spRes)>20 ):
					spResponse+=spRes+'\n'
#				break
	spResponseRaw=spResponse.split('\n')	
#	print spResponseRaw
	for spResponseLine in spResponseRaw:
		spResponseArray=spResponseLine.split(' ')
		nodeSlotNumber=0
		if(len(spResponseArray)>=8 and spResponseArray[7]=='connected'):
			
			if(len(spResponseArray)==8):
				myNodeInfoList.append([spResponseArray[0],0])
				#print 'step 1')
			else:
				myIndex=8
				maxIndexNumber=len(spResponseArray)
				while (myIndex<=maxIndexNumber):
					slotNumber=spResponseArray[myIndex-1]
					if(slotNumber.find('-')==-1):
						nodeSlotNumber+=1
					else:
						slotRange=slotNumber.split('-')
						#print ('step 4')
						nodeSlotNumber=nodeSlotNumber+(int(slotRange[1])-int(slotRange[0]))+1					
					myIndex+=1
				myNodeInfoList.append([spResponseArray[0],nodeSlotNumber-1])	
	
	if(balanceStrategy=='nodeBase'):
		movedSlotsNumber=0
		balanceSlotNumber=0
		totalNodes=len(myNodeInfoList)
		FloatBalanceSlotNumber=float(allSlotNumber/totalNodes)
		FloatBalanceSlotNumberInt=int(allSlotNumber/totalNodes)
#		print (str(FloatBalanceSlotNumber))
#		print (str(float(FloatBalanceSlotNumberInt)))
#		sleep(3)
		if (maxSlotBarier==4001):
			clusterString=redisBinaryDir+'src/redis-cli --cluster rebalance '+pareNodes[contactNode-1][0][0]+':'+pareNodes[contactNode-1][1][0]
			if(redisPwdAuthentication == 'on'):
				clusterString+=' -a '+redisPwd+' '
			os.system(clusterString)
		else:
		
			if (FloatBalanceSlotNumber==float(FloatBalanceSlotNumberInt)):
				balanceSlotNumber=int(FloatBalanceSlotNumber)
			else:
				balanceSlotNumber=int(FloatBalanceSlotNumber)-1
			myNodeInfoListIndexer=0
			proccessHealth=True
			for myNodeInfo in myNodeInfoList:
				if(proccessHealth):
					if(movedSlotsNumber<=maxSlotBarier ):
	#					print ('Step 1:Slot Barier :'+str(maxSlotBarier))
	#					print ('Step 1:balanceSlotNumber :'+str(balanceSlotNumber))
						if(myNodeInfo[1] < balanceSlotNumber):
							slotDiff=balanceSlotNumber-myNodeInfo[1]
							stepSize=1
							while ( slotDiff > 0  and movedSlotsNumber<=maxSlotBarier ):
	#							print ('Step 3:balanceSlotNumber :'+str(balanceSlotNumber))
								# if(slotDiff>10 and slotDiff<=100):
									# stepSize=10							
								if(myNodeInfoList[myNodeInfoListIndexer][1]>balanceSlotNumber and myNodeInfoList[myNodeInfoListIndexer][0]!=myNodeInfo[0]):
									if ( myNodeInfoList[myNodeInfoListIndexer][1]>balanceSlotNumber+30 and slotDiff>30):
										stepSize=30
									elif ( myNodeInfoList[myNodeInfoListIndexer][1]>balanceSlotNumber+10 and slotDiff>10):
										stepSize=10
									elif ( myNodeInfoList[myNodeInfoListIndexer][1]>balanceSlotNumber+5 and slotDiff>5):
										stepSize=5									
									else:
										stepSize=1
									reshardClusterSlient(contactNode,myNodeInfoList[myNodeInfoListIndexer][0],myNodeInfo[0],str(stepSize))
									print ('FROM Node ID'+myNodeInfoList[myNodeInfoListIndexer][0]+'\n-> TO Node ID :'+myNodeInfo[0]+'\nMoved Slots :'+str(stepSize)+ bcolors.OKGREEN+' OK :)'+bcolors.ENDC)
									print ('TO Node ID :'+str(myNodeInfo[0])+'		Slot Diff :'+bcolors.OKBLUE+str(slotDiff)+bcolors.ENDC)														
									sleep(3)
									if(clusterCheck(contactNode)==False):
										print (bcolors.FAIL+'!!! Warning !!! Cluster Check Fail. I will try to fix It'+bcolors.ENDC)
										sleep(10)
										if(clusterFix(contactNode)):
											print (bcolors.OKGREEN+' OK :) I fixed it ;)'+bcolors.ENDC)
											sleep(5)
										else:
											proccessHealth=False							
									myNodeInfoList[myNodeInfoListIndexer][1]-=stepSize
									myNodeInfo[1]+=stepSize
									slotDiff-=stepSize
									movedSlotsNumber+=stepSize
								if ( slotDiff <= 10):
									stepSize=1
								if(myNodeInfoListIndexer<len(myNodeInfoList)-1):
									myNodeInfoListIndexer+=1
								else:
									myNodeInfoListIndexer=0
						else:
							print (bcolors.WARNING+'This node has more (or equal ) slots than  balance slot level :) '+myNodeInfo[0]+bcolors.ENDC)
					else:
						print (bcolors.WARNING+'You reached "max  move slots" per node barier. If you want to move further, run balancer again. Total Moved Slot Number:  '+str(movedSlotsNumber)+bcolors.ENDC)
				else:
					print (bcolors.FAIL+' !!! ERROR !!! I tried to fix Slots, however it does NOT work. The proccess was terminated !!! '+bcolors.ENDC)
		
		clusterInfo(pareNodes[contactNode-1][0][0],pareNodes[contactNode-1][1][0])
		showMemoryUsage()
	elif(balanceStrategy=='memBase'):	
		movedSlotsNumber=0
		stepSize=1	
		loopControl=0
		myIndexArray1=0
		myIndexArray2=0
		myNodeSlotList=getMemoryBaseBalanceSlotNumbers()
		myIndexMax=len(myNodeSlotList)
		# print myNodeSlotList
		# print '----------***************************------------'
		# print myNodeInfoList
		sleep(1)
#		myNodeInfoList[nodeId][SlotNumber]
#		myNodeSlotList [nodeNumber][balancedSlotsNumber]
		proccessHealth=True
		stepSize=1
		if(myIndexMax==len(myNodeInfoList)):
			if(movedSlotsNumber<maxSlotBarier ):
				while (myIndexArray1 < myIndexMax and movedSlotsNumber<maxSlotBarier ):
#					print 'step 1 myIndexArray1 :'+str(myIndexArray1 )+' <  myIndexMax:'+str(myIndexMax)
#					print 'step 1 movedSlotsNumber :'+str(movedSlotsNumber )+' <  maxSlotBarier:'+str(maxSlotBarier)
					stepSize=1
#					sleep(1)
					while(myNodeInfoList[myIndexArray1][1]<myNodeSlotList[myIndexArray1][1]):
						print ('Node Slot Number :'+str(myNodeInfoList[myIndexArray1][1])+'		Slot Diff :'+bcolors.OKBLUE+str( myNodeSlotList[myIndexArray1][1] - myNodeInfoList[myIndexArray1][1] )+bcolors.ENDC)	
#						print 'step 2 myNodeInfoList[myIndexArray1][1]:'+str(myNodeInfoList[myIndexArray1][1])+' <  yNodeSlotList[myIndexArray1][1]-1:'+str(myNodeSlotList[myIndexArray1][1]-1)
						myIndexArray2=0
						loopControl+=1
						while ( myIndexArray2 < myIndexMax and movedSlotsNumber<maxSlotBarier ):
#							print 'step 3 myIndexArray2:'+str(myIndexArray2)+'  myIndexMax'+str(myIndexMax)
#							print 'step 3 movedSlotsNumber:'+str(movedSlotsNumber)+'  maxSlotBarier'+str(maxSlotBarier)
							loopControl+=1
							if(myIndexArray1==myIndexArray2 and myIndexArray2 < myIndexMax-1):
								myIndexArray2+=1
							elif(myIndexArray1==myIndexArray2 and myIndexArray2 >= myIndexMax-1):
								myIndexArray2=0
							else:
								if(myNodeInfoList[myIndexArray2][1]>myNodeSlotList[myIndexArray2][1] and myNodeInfoList[myIndexArray1][1]<myNodeSlotList[myIndexArray1][1]):
#									print 'step 4 myNodeInfoList[myIndexArray2][1]:'+str(myNodeInfoList[myIndexArray2][1])+'  myNodeSlotList[myIndexArray2][1]+1:'+str(myNodeSlotList[myIndexArray2][1]+1)
#									print 'step 4 myNodeInfoList[myIndexArray1][1]:'+str(myNodeInfoList[myIndexArray1][1])+'  myNodeSlotList[myIndexArray1][1]-1'+str(myNodeSlotList[myIndexArray1][1]-1)
									if ( myNodeInfoList[myIndexArray2][1]>myNodeSlotList[myIndexArray2][1]+30 and myNodeInfoList[myIndexArray1][1]<myNodeSlotList[myIndexArray1][1]-30):
										stepSize=30
									elif ( myNodeInfoList[myIndexArray2][1]>myNodeSlotList[myIndexArray2][1]+10 and myNodeInfoList[myIndexArray1][1]<myNodeSlotList[myIndexArray1][1]-10):
										stepSize=10
									elif ( myNodeInfoList[myIndexArray2][1]>myNodeSlotList[myIndexArray2][1]+5 and myNodeInfoList[myIndexArray1][1]<myNodeSlotList[myIndexArray1][1]-5):
										stepSize=5
									else:
										stepSize=1
									if(reshardClusterSlient(contactNode,myNodeInfoList[myIndexArray2][0],myNodeInfoList[myIndexArray1][0],str(stepSize))):
										print ('FROM Node ID'+myNodeInfoList[myIndexArray2][0]+'\n-> TO Node ID :'+myNodeInfoList[myIndexArray1][0]+'\nMoved Slots :'+str(stepSize)+ bcolors.OKGREEN+' OK :)'+bcolors.ENDC)
										myNodeInfoList[myIndexArray1][1]+=stepSize
										myNodeInfoList[myIndexArray2][1]-=stepSize
										movedSlotsNumber+=stepSize
										myIndexArray2+=1
									stepSize=1	
								else:
									myIndexArray2+=1
							stepSize=1
							if(movedSlotsNumber>=maxSlotBarier or loopControl==100000):
								break
						if(movedSlotsNumber>=maxSlotBarier or loopControl==100000):
							break
							
					sleep(2)
					if(clusterCheck(contactNode)==False):
						print (bcolors.FAIL+'!!! Warning !!! Cluster Check Fail. I will try to fix It'+bcolors.ENDC)
						sleep(2)
						if(clusterFix(contactNode)):
							print (bcolors.OKGREEN+' OK :) I fixed it ;)'+bcolors.ENDC)
							sleep(2)							
					myIndexArray1+=1
					if(movedSlotsNumber>=maxSlotBarier or loopControl==100000):
						break
			clusterInfo(pareNodes[contactNode-1][0][0],pareNodes[contactNode-1][1][0])
			showMemoryUsage()
			
		else:
			(bcolors.WARNING+'!!! ERROR Different Array Size !!!'+bcolors.ENDC)
	else:
		return False
# def reshardClusterSlientUbuntu(contactNode,fromNodeID,toNodeID,slotNumber):
	# myNodeIP=pareNodes[contactNode-1][0][0]
	# myNodePORT=pareNodes[contactNode-1][1][0]
	# clusterString=redisBinaryDir+'src/redis-cli --cluster reshard '+myNodeIP+':'+myNodePORT+' --cluster-from '+fromNodeID+' --cluster-to '+toNodeID+' --cluster-slots '+slotNumber+' --cluster-yes'
	# returnCmd=os.system(clusterString)	
	# if(returnCmd==0):
		# return True
	# else:
		# return False		
def reshardClusterSlient(contactNode,fromNodeID,toNodeID,slotNumber):
	myNodeIP=pareNodes[contactNode-1][0][0]
	myNodePORT=pareNodes[contactNode-1][1][0]
	clusterString=redisBinaryDir+'src/redis-cli --cluster reshard '+myNodeIP+':'+myNodePORT+' --cluster-from '+fromNodeID+' --cluster-to '+toNodeID+' --cluster-slots '+slotNumber+' --cluster-yes'
#	returnCmd=os.system(clusterString)	
	if(redisPwdAuthentication == 'on'):
		clusterString+=' -a '+redisPwd+' '
	returnCmd,cmdResponse = commands.getstatusoutput(clusterString)	
	if(returnCmd==0):
		return True
	else:
		return False
def reshardCluster(contactNode,fromNodeID,toNodeID,slotNumber):
	myNodeIP=pareNodes[contactNode-1][0][0]
	myNodePORT=pareNodes[contactNode-1][1][0]
	clusterString=redisBinaryDir+'src/redis-cli --cluster reshard '+myNodeIP+':'+myNodePORT+' --cluster-from '+fromNodeID+' --cluster-to '+toNodeID+' --cluster-slots '+slotNumber+' --cluster-yes'
	if(redisPwdAuthentication == 'on'):
		clusterString+=' -a '+redisPwd+' '
	returnCmd=os.system(clusterString)
	if(returnCmd==0):
		return True
	else:
		return False
	slotInfo(myNodeIP,myNodePORT)		
def changePareNodeListFile(oldValue,newValue):
	fileContent=fileReadFull("pareNodeList.py")
	newFileContent=fileContent.replace(oldValue,newValue)
	fileClearWrite("pareNodeList.py", newFileContent+'\n#### Node list File was Changed by paredicma at '+get_datetime()+'\n#### old value:'+oldValue+'\n#### new value:'+newValue)
def changePareConfigFile(oldValue,newValue):
	retVal=False
	fileContent=fileReadFull("pareConfig.py")
	newFileContent=fileContent.replace(oldValue,newValue)
	fileClearWrite("pareConfig.py", newFileContent+'\n#### Config File was Changed by paredicma at '+get_datetime()+'\n#### old value:'+oldValue+'\n#### new value:'+newValue)
	retVal=True
	return retVal
def redisNodesVersionControl():
	nodeNumber=0
	for pareNode in pareNodes:	
		nodeIP=pareNode[0][0]
		portNumber=pareNode[1][0]
		nodeNumber=nodeNumber+1
		if (pareNode[4]):
			print (bcolors.BOLD+'Node Number :'+str(nodeNumber)+'  Node IP :'+nodeIP+'  Node Port :'+portNumber+bcolors.ENDC)
			os.system(redisConnectCmd(nodeIP,portNumber,' info server | grep  redis_version'))
def checkReplicationStatus():
	retCRS=True
	for pareNode in pareNodes:	
		redisBinaryDir=redisBinaryDir.replace('redis-'+redisVersion,'redis-'+newRedisVersion)
		nodeIP=pareNode[0][0]
		portNumber=pareNode[1][0]
		nodeNumber=nodeNumber+1
		if (pareNode[4]):
			print (bcolors.BOLD+'Node Number :'+str(nodeNumber)+'  Node IP :'+nodeIP+'  Node Port :'+portNumber+bcolors.ENDC)
			if ( isNodeMaster(nodeIP,nodeNumber,portNumber)) :
				pmdStatus,cmdResponse = commands.getstatusoutput(redisConnectCmd(nodeIP,portNumber,' info replication'))
				if(cmdResponse.find('state=online')==-1):
					retCRS=False
					print (bcolors.WARNING+'!!! Master Node :'+str(nodeNumber)+' IP: '+nodeIP+' PORT:' +portNumber+' has no ONLINE REPLICA SLAVE !!!\n Operation canceled.  '+bcolors.ENDC)
				searchKeyOffset='offset='
				searchMasterKeyOffset='master_repl_offset:'
				colNumOffset=cmdResponse.find('offset=')
				cmdResponse=cmdResponse[colNumOffset+len(searchKeyOffset):]
				colNumOffset=cmdResponse.find(',')
				slaveOffset=int(cmdResponse[:colNumOffset])
				colNumOffset=cmdResponse.find(searchMasterKeyOffset)
				cmdResponse=cmdResponse[colNumOffset+len(searchMasterKeyOffset):]
				colNumOffset=cmdResponse.find('\n')
				masterOffset=int(cmdResponse[:colNumOffset])
				print ('Master offset:'+str(masterOffset)+' : slave offset:'+str(slaveOffset))
				if(masterOffset-slaveOffset>3):
					retCRS=False
					print (bcolors.WARNING+'!!! Master Node :'+str(nodeNumber)+' IP: '+nodeIP+' PORT:' +portNumber+' has no SYNC REPLICA SLAVE !!!\n Operation canceled. '+bcolors.ENDC)
	return retCRS
def restartAllMasters(newRedisVersion):
	global redisBinaryDir
	global redisVersion
	stateResult=True
	nodeNumber=0
	if(checkReplicationStatus):				
		for pareNode in pareNodes:	
			redisBinaryDir=redisBinaryDir.replace('redis-'+redisVersion,'redis-'+newRedisVersion)
			nodeIP=pareNode[0][0]
			portNumber=pareNode[1][0]
			dedicateCpuCores=pareNode[2][0]					
			nodeNumber=nodeNumber+1
			if (pareNode[4]):
				print (bcolors.BOLD+'Node Number :'+str(nodeNumber)+'  Node IP :'+nodeIP+'  Node Port :'+portNumber+bcolors.ENDC)
				if ( isNodeMaster(nodeIP,nodeNumber,portNumber)) :
					pmdStatus,cmdResponse = commands.getstatusoutput(redisConnectCmd(nodeIP,portNumber,' info server | grep  redis_version'))
					if(cmdResponse.find(newRedisVersion)==-1):
						stopNode(nodeIP,str(nodeNumber),portNumber)
						startNode(nodeIP,str(nodeNumber),portNumber,dedicateCpuCores)
	#				sleep(2)
						pmdStatus,cmdResponse = commands.getstatusoutput(redisConnectCmd(nodeIP,portNumber,' info server | grep  redis_version'))
						if(cmdResponse.find(newRedisVersion)>=0):
							print (bcolors.OKGREEN+'Master redis node started  with new version :'+newRedisVersion+bcolors.ENDC)
							print (cmdResponse)
							print (bcolors.BOLD+'node Id :'+str(nodeNumber)+' nodeIP: '+nodeIP+' nodePort:'+portNumber+bcolors.ENDC)
						else:
							stateResult=False
							print (bcolors.FAIL+'!!! There might be a problem with master restart !!! Manuel check is recommended !!!'+bcolors.ENDC)
					else:
						print (bcolors.WARNING+'This node has already upgrated..'+bcolors.ENDC)
#			restartNode(nodeIP,str(nodeNumber),portNumber,dedicateCpuCores)
	else:
		print ('!!! Master nodes upgrade was canceled !!! Not Sync !!!')
		stateResult=False
	return stateResult
def restartAllSlaves(newRedisVersion):
	global redisBinaryDir
	global redisVersion
	stateResult=True
	nodeNumber=0
	for pareNode in pareNodes:	
		redisBinaryDir=redisBinaryDir.replace('redis-'+redisVersion,'redis-'+newRedisVersion)
		nodeIP=pareNode[0][0]
		portNumber=pareNode[1][0]
		dedicateCpuCores=pareNode[2][0]					
		nodeNumber=nodeNumber+1
		if (pareNode[4]):
			print (bcolors.BOLD+'Node Number :'+str(nodeNumber)+'  Node IP :'+nodeIP+'  Node Port :'+portNumber+bcolors.ENDC)
			if ( isNodeMaster(nodeIP,nodeNumber,portNumber)==False ) :
				pmdStatus,cmdResponse = commands.getstatusoutput(redisConnectCmd(nodeIP,portNumber,' info server | grep  redis_version'))
				if(cmdResponse.find(newRedisVersion)==-1):
					stopNode(nodeIP,str(nodeNumber),portNumber)
					startNode(nodeIP,str(nodeNumber),portNumber,dedicateCpuCores)
					pmdStatus,cmdResponse = commands.getstatusoutput(redisConnectCmd(nodeIP,portNumber,' info server | grep  redis_version'))
					if(cmdResponse.find(newRedisVersion)>=0):
						print (bcolors.BOLD+'Slave redis node started  with new version :'+newRedisVersion)
						print (cmdResponse)
						print (bcolors.BOLD+'node Id :'+str(nodeNumber)+' nodeIP: '+nodeIP+' nodePort:'+portNumber+bcolors.ENDC)
					else:
						stateResult=False
						print (bcolors.FAIL+'!!! There might be a problem with slave restart !!! Manuel check is recommended !!!'+bcolors.ENDC)
				else:
					print (bcolors.WARNING+'This node has already upgrated..'+bcolors.ENDC)
#			restartNode(nodeIP,str(nodeNumber),portNumber,dedicateCpuCores)
	return stateResult
def clusterStateInfo(nodeIP,nodeNumber,portNumber):
	print (bcolors.BOLD+'\nCluster State node ->'+str(nodeNumber)+' node IP :'+nodeIP+' node Port : '+portNumber+'\n'+bcolors.ENDC)
	pmdStatus,cmdResponse = commands.getstatusoutput(redisConnectCmd(nodeIP,portNumber,' cluster info | grep  cluster_state'))
	if(cmdResponse.find('ok')>=0):
		print (bcolors.OKGREEN+cmdResponse+bcolors.ENDC)
	else:
		print (bcolors.FAIL+cmdResponse+bcolors.ENDC)
def clusterInfo(nodeIP,portNumber):
	print ('\n------- Cluster Nodes -------\n')
	os.system(redisConnectCmd(nodeIP,portNumber,' CLUSTER NODES |  grep master'))
	print ('\nCluster Slots Check\n------------------------------------------ ')
	clusterString=redisBinaryDir+'src/redis-cli --cluster check '+nodeIP+':'+portNumber
	if(redisPwdAuthentication == 'on'):
		clusterString+=' -a '+redisPwd+' '
	clStatus,clResponse = commands.getstatusoutput(clusterString)	
	print (bcolors.BOLD+clResponse[:clResponse.find('>>>')]+bcolors.ENDC)
	raw_input(bcolors.BOLD+'\n----------------------\nPress Enter to Return Paredicmon Menu'+bcolors.ENDC)
def slotInfo(nodeIP,portNumber):
	print ('\n------- Cluster Slots -------\n')
	os.system(redisConnectCmd(nodeIP,portNumber,' CLUSTER SLOTS'))
	os.system(redisConnectCmd(nodeIP,portNumber,' CLUSTER NODES |  grep master'))
	print ('\nCluster Slots Check\n------------------------------------------ ')
	clusterString=redisBinaryDir+'src/redis-cli --cluster check '+nodeIP+':'+portNumber
	if(redisPwdAuthentication == 'on'):
		clusterString+=' -a '+redisPwd+' '
	clStatus,clResponse = commands.getstatusoutput(clusterString)	
	print (bcolors.BOLD+clResponse[:clResponse.find('>>>')]+bcolors.ENDC)
	raw_input(bcolors.BOLD+'\n----------------------\nPress Enter to Return Paredicmon Menu'+bcolors.ENDC )
def funcNodesList():
	print (bcolors.BOLD+'Listing Nodes'+bcolors.ENDC )
	masterNodeList=''
	slaveNodeList=''
	unknownNodeList=''
	nodeNumber=0
	for pareNode in pareNodes:
		nodeIP=pareNode[0][0]
		portNumber=pareNode[1][0]
		nodeNumber=nodeNumber+1
		if (pareNode[4]):
			returnVal=slaveORMasterNode(nodeIP,nodeNumber,portNumber)
			if (returnVal=='M'):
				masterNodeList+=bcolors.OKGREEN+'Node Number :'+str(nodeNumber)+' Server IP :'+nodeIP+' Port:'+portNumber+' UP\n'+bcolors.ENDC  
			elif (returnVal=='S'):
				slaveNodeList+= bcolors.OKBLUE+'Node Number :'+str(nodeNumber)+' Server IP :'+nodeIP+' Port:'+portNumber+' UP\n'+bcolors.ENDC  
			else:
				unknownNodeList+= bcolors.FAIL+'Node Number :'+str(nodeNumber)+' Server IP :'+nodeIP+' Port:'+portNumber+' DOWN\n'+bcolors.ENDC 
	returnVAl=raw_input(bcolors.BOLD+'\n------- Master Nodes -------\n'+bcolors.ENDC +masterNodeList+bcolors.BOLD+'\n------- Slave Nodes -------\n'+bcolors.ENDC+slaveNodeList+bcolors.BOLD+'\n------- Down Nodes -------\n'+bcolors.ENDC+unknownNodeList+bcolors.BOLD+'\n--------------\nPress enter to continue...'+bcolors.ENDC )
def serverInfo(serverIP):
	if(serverIP==pareServerIp):
		print ('\n------- Server Informations ('+serverIP+') ------\n')
		print ('\n------- CPU Cores -------------------------------\n')
		os.system("numactl --hardware")
		print ('\n------- Memory Usage-----------------------------\n')
		os.system("free -g")
		print ('\n------- Disk Usage-------------------------------\n')
		os.system("df -h")
		print ('\n------- Redis  Nodes ----------------------------\n')
	else :	
		print ('\n------- Server Informations ('+serverIP+') ------\n')
		print ('\n------- CPU Cores -------------------------------\n')
		os.system('ssh -q -o "StrictHostKeyChecking no"  '+pareOSUser+'@'+serverIP+' -C  "numactl --hardware"')
		print ('\n------- Memory Usage-----------------------------\n')
		os.system('ssh -q -o "StrictHostKeyChecking no"  '+pareOSUser+'@'+serverIP+' -C  "free -g"')
		print ('\n------- Disk Usage-------------------------------\n')
		os.system('ssh -q -o "StrictHostKeyChecking no"  '+pareOSUser+'@'+serverIP+' -C  "df -h"')
		print ('\n------- Redis  Nodes ----------------------------\n')
	masterNodeList=''
	slaveNodeList=''
	unknownNodeList=''
	nodeNumber=0
	for pareNode in pareNodes:
		if (pareNode[0][0]==serverIP):
			nodeNumber+=1
			portNumber=pareNode[1][0]
			nodeNumber=nodeNumber+1
			if (pareNode[4]):
				returnVal=slaveORMasterNode(serverIP,nodeNumber,portNumber)
				if (returnVal=='M'):
					masterNodeList+= bcolors.OKGREEN+'Node Number :'+str(nodeNumber)+' Server IP :'+serverIP+' Port:'+portNumber+' UP\n'+bcolors.ENDC 
				elif (returnVal=='S'):
					slaveNodeList+= bcolors.OKBLUE+'Node Number :'+str(nodeNumber)+' Server IP :'+serverIP+' Port:'+portNumber+' UP\n'+bcolors.ENDC 
				else:
					unknownNodeList+= bcolors.FAIL+'Node Number :'+str(nodeNumber)+' Server IP :'+serverIP+' Port:'+portNumber+'\n DOWN'+bcolors.ENDC
	raw_input(bcolors.BOLD+'\n------- Master Nodes -------\n'+bcolors.ENDC +masterNodeList+bcolors.BOLD+'\n------- Slave Nodes -------\n'+bcolors.ENDC +slaveNodeList+bcolors.BOLD+'\n------- Unknown Nodes -------\n'+bcolors.ENDC+unknownNodeList+bcolors.BOLD+'\n--------------\nPress Enter to Return Paredicmon Menu'+bcolors.ENDC)
def validIP(IPaddr):
	try:
		socket.inet_aton(IPaddr)
		return True
	except socket.error:
		return False
def redisConnectCmd(nodeIP,portNumber,redisCmd):
	redisCliCmd = ''
	if ( redisPwdAuthentication ):
		redisCliCmd='./redis-'+redisVersion+'/src/redis-cli -h '+nodeIP+' -p '+portNumber+' --no-auth-warning -a '+redisPwd+' '+redisCmd
	else:
		redisCliCmd='./redis-'+redisVersion+'/src/redis-cli -h '+nodeIP+' -p '+portNumber+' '+redisCmd
	return redisCliCmd
def nodeInfo(nodeIP,nodeNumber,portNumber,infoCmd):
	retVal='Unkown'
	listStatus,listResponse = commands.getstatusoutput(redisConnectCmd(nodeIP,portNumber,'info '+infoCmd))		
	if ( listStatus == 0 ):
		retVal=listResponse
	else:
		retVal=bcolors.FAIL+' !!! No Information or Connection Problem !!!'+bcolors.ENDC 
	return retVal
def slaveORMasterNode(nodeIP,nodeNumber,portNumber):
	retVal='U'
	listStatus,listResponse = commands.getstatusoutput(redisConnectCmd(nodeIP,portNumber,'cluster nodes | grep myself'))
	if ( listStatus == 0 ):
		if 'master' in listResponse:
			retVal='M'
		elif 'slave' in listResponse:
			retVal='S'
	else:
		retVal='U'
	return retVal
def getMemoryBaseBalanceSlotNumbers():
	nodeNumber=0
	totalMemPer=0.0
	totalMaxMemByte=0.0
	nodeListSlots=[]
	nodeListMem=[]
	for pareNode in pareNodes:
		nodeIP=pareNode[0][0]
		portNumber=pareNode[1][0]
		nodeNumber=nodeNumber+1
		if (pareNode[4]):
			memStatus,memResponse = commands.getstatusoutput(redisConnectCmd(nodeIP,portNumber,' info memory | grep  -e "maxmemory:" '))
			if ( memStatus == 0 and isNodeMaster(nodeIP,nodeNumber,portNumber) ):				
				maxMemByte=float(memResponse[memResponse.find('maxmemory:')+10:])
				nodeListMem.append([nodeNumber,maxMemByte])
				totalMaxMemByte+=maxMemByte
	if (totalMaxMemByte==0):
		print (bcolors.FAIL+ '!!!Division by Zero ERROR !!!'+bcolors.ENDC)
	else:		
		for nodeMem in nodeListMem:
			nodeListSlots.append([nodeMem[0],int((nodeMem[1]/totalMaxMemByte)*16384)])		
	return nodeListSlots
def showMemoryUsage():
	os.system("clear")
#	while(True):
#	sleep(1)
	print ('Memory Usage\n-------------------------------')
	print (bcolors.HEADER+'nodeID 		NodeIP				 NodePort	Used Mem(GB)	Max Mem(GB)	Usage (%)'+bcolors.ENDC)
	nodeNumber=0
	totalMemPer=0.0
	totalUsedMemByte=0
	totalMaxMemByte=0
	printTextMaster=''
	printTextSlave=''
	isMaster=False
	for pareNode in pareNodes:
		nodeIP=pareNode[0][0]
		portNumber=pareNode[1][0]
		nodeNumber=nodeNumber+1
		if (pareNode[4]):
			memStatus,memResponse = commands.getstatusoutput(redisConnectCmd(nodeIP,portNumber,' info memory | grep  -e "used_memory:" -e "maxmemory:" '))
			if ( memStatus == 0 ):
				usedMemByte=float(memResponse[12:memResponse.find('maxmemory:')-1])
				maxMemByte=float(memResponse[memResponse.find('maxmemory:')+10:])
				usedMem=round((usedMemByte)/(1024*1024*1024),3)
				maxMem=round((maxMemByte)/(1024*1024*1024),3)
				usagePerMem=round((usedMem/maxMem)*100,2)
				# totalUsedMemByte+=usedMemByte
				# totalMaxMemByte+=maxMemByte
				if (isNodeMaster(nodeIP,nodeNumber,portNumber)):
					isMaster=True
					totalUsedMemByte+=usedMemByte
					totalMaxMemByte+=maxMemByte
					str(nodeNumber)+'	'+nodeIP+'-( M )			'+portNumber+'		'+str(usedMem)+'		'+str(maxMem)+'		'+str(usagePerMem)+'%'+bcolors.ENDC+'\n'
				else:
					isMaster=False
					str(nodeNumber)+'	'+nodeIP+'-( S )			'+portNumber+'		'+str(usedMem)+'		'+str(maxMem)+'		'+str(usagePerMem)+'%'+bcolors.ENDC+'\n'
				if (usagePerMem>=90.0):
					if(isMaster):
						printTextMaster+=bcolors.FAIL+str(nodeNumber)+'	'+nodeIP+'-( M )			'+portNumber+'		'+str(usedMem)+'		'+str(maxMem)+'		'+str(usagePerMem)+'%'+bcolors.ENDC+'\n'
					else:
						printTextSlave+=bcolors.FAIL+str(nodeNumber)+'	'+nodeIP+'-( S )			'+portNumber+'		'+str(usedMem)+'		'+str(maxMem)+'		'+str(usagePerMem)+'%'+bcolors.ENDC+'\n'
				elif (usagePerMem>=80.00 and usagePerMem<90.00):
					if(isMaster):
						printTextMaster+=bcolors.WARNING+str(nodeNumber)+'	'+nodeIP+'-( M )			'+portNumber+'		'+str(usedMem)+'		'+str(maxMem)+'		'+str(usagePerMem)+'%'+bcolors.ENDC+'\n'
					else:
						printTextSlave+=bcolors.WARNING+str(nodeNumber)+'	'+nodeIP+'-( S )			'+portNumber+'		'+str(usedMem)+'		'+str(maxMem)+'		'+str(usagePerMem)+'%'+bcolors.ENDC+'\n'
				else:
					if(isMaster):
						printTextMaster+=bcolors.OKGREEN+str(nodeNumber)+'	'+nodeIP+'-( M )			'+portNumber+'		'+str(usedMem)+'		'+str(maxMem)+'		'+str(usagePerMem)+'%'+bcolors.ENDC+'\n'
					else:
						printTextSlave+=bcolors.OKGREEN+str(nodeNumber)+'	'+nodeIP+'-( S )			'+portNumber+'		'+str(usedMem)+'		'+str(maxMem)+'		'+str(usagePerMem)+'%'+bcolors.ENDC+'\n'
			else :
				print (bcolors.FAIL+'!!! Warning !!!! A problem occurred, while memory usage checking !!! nodeID :'+str(nodeNumber)+' NodeIP:'+nodeIP+' NodePort:'+portNumber+''+bcolors.ENDC)
	print printTextMaster+bcolors.BOLD+'-------------------------------------------------------------------------------------------------------'+bcolors.ENDC
	print printTextSlave
	totalUsedMem=round(((totalUsedMemByte)/(1024*1024*1024)),3)
	totalMaxMem=round(((totalMaxMemByte)/(1024*1024*1024)),3)
	if (totalMaxMem==0):
		totalMemPer=0.0
	else:
		totalMemPer=round(((totalUsedMem/totalMaxMem)*100),2)
	print (bcolors.BOLD+'-------------------------------------------------------------------------------------------------------'+bcolors.ENDC)
	print (bcolors.BOLD+'TOTAL ( Only Master )						:'+str(totalUsedMem)+'GB	'+str(totalMaxMem)+'GB		'+str(totalMemPer)+'% '+bcolors.ENDC)
	raw_input('\n-----------------------------------------\nPress Enter to Return Paredicmon Menu')
def pingNode(nodeIP,portNumber):
	pingStatus,pingResponse = commands.getstatusoutput(redisConnectCmd(nodeIP,portNumber,' ping '))
	if ( pingStatus == 0 & pingResponse.find('PONG')>-1 ):
		return True
	else :
		return False
def isNodeMaster(nodeIP,nodeNumber,portNumber):
	queryRespond='  master'
	pingStatus,queryRespond = commands.getstatusoutput(redisConnectCmd(nodeIP,portNumber,'info replication | grep role '))
	if ( queryRespond.find('master')>0 ):
		return True
	else :
		return False
def migrateDataFrom(toIP,toPort,fromIP,fromPORT,fromPWD):
	if(redisPwdAuthentication == 'on'):
		nodeNumber=0
		for pareNode in pareNodes:
			nodeIP=pareNode[0][0]
			portNumber=pareNode[1][0]
			nodeNumber=nodeNumber+1
			if ( pareNode[4] ):
#				print ('Redis configuration will change  will rewrite on Node Number :'+str(nodeNumber)+'  Node IP :'+nodeIP+'  Node Port :'+portNumber )
				os.system(redisConnectCmd(nodeIP,portNumber,' CONFIG SET requirepass "" '))						
	if(fromPWD==''):		
		os.system('date')
		print (bcolors.BOLD +"\nData importing is starting... Please wait !!!"+bcolors.ENDC)
		os.system('./redis-'+redisVersion+'/src/redis-cli --cluster import '+toIP+':'+toPort+' --cluster-from '+fromIP+':'+fromPORT+' --cluster-copy > /dev/null')
		os.system('date')
		print (bcolors.BOLD +"\nData importing ended. "+bcolors.ENDC)
	else:
		os.system('./redis-'+redisVersion+'/src/redis-cli -h '+fromIP+' -p '+fromPORT+' --no-auth-warning -a '+fromPWD+' Config set requirepass ""')
		os.system('date')
		print (bcolors.BOLD +"\nData importing is starting... Please wait !!!"+bcolors.ENDC)
		os.system('./redis-'+redisVersion+'/src/redis-cli --cluster import '+toIP+':'+toPort+' --cluster-from '+fromIP+':'+fromPORT+' --cluster-copy > /dev/null')
		os.system('date')
		print (bcolors.BOLD +"\nData importing ended. "+bcolors.ENDC)
		os.system('./redis-'+redisVersion+'/src/redis-cli -h '+fromIP+' -p '+fromPORT+' Config set requirepass "'+fromPWD+'"')
	if(redisPwdAuthentication == 'on'):
		nodeNumber=0
		for pareNode in pareNodes:
			nodeIP=pareNode[0][0]
			portNumber=pareNode[1][0]
			nodeNumber=nodeNumber+1
			if ( pareNode[4] ):
#				print ('Redis configuration will change  will rewrite on Node Number :'+str(nodeNumber)+'  Node IP :'+nodeIP+'  Node Port :'+portNumber )
				os.system(redisConnectCmd(nodeIP,portNumber,' CONFIG SET requirepass '+redisPwd))						
def isNodeHasSlave(nodeIP,nodeNumber,portNumber):
	pingStatus,pingResponse = commands.getstatusoutput(redisConnectCmd(nodeIP,portNumber,' info replication | grep connected_slaves '))
	if ( pingStatus == 0 & pingResponse.find(':0')>0 ):
		return False
	else :
		return True
def makeRedisCluster( nodesString,redisReplicationNumber ):
	clusterString=''
	if(redisReplicationNumber=='0'):
		clusterString=redisBinaryDir+'src/redis-cli --cluster create '+nodesString
	else:
		clusterString=redisBinaryDir+'src/redis-cli --cluster create '+nodesString+' --cluster-replicas '+redisReplicationNumber
	if(redisPwdAuthentication == 'on'):
		clusterString+=' -a '+redisPwd+' '
	logWrite(pareLogFile,bcolors.BOLD+':: Cluster create string : '+clusterString+bcolors.ENDC)
	os.system(clusterString)
def delPareNode(delNodeID):
	serverIP=pareNodes[int(delNodeID)-1][0][0]
	serverPORT=pareNodes[int(delNodeID)-1][1][0]
	nodeNumber=0
	for pareNode in pareNodes:
		if ( pareNode[4] ):
			if(isNodeMaster(pareNode[0][0],str(nodeNumber+1),pareNode[1][0])):
				targetIP=pareNode[0][0]
				targetPORT=pareNode[1][0]
				break		
		nodeNumber+=1
	pingStatus,queryRespond = commands.getstatusoutput(redisConnectCmd(serverIP,serverPORT,' cluster nodes | grep myself'))
	if(pingStatus==0):
		queryRespondList=queryRespond.split(' ')
		clusterString=redisBinaryDir+'src/redis-cli --cluster del-node '+targetIP+':'+targetPORT+' '+queryRespondList[0]+' '
		if(redisPwdAuthentication == 'on'):
			clusterString+=' -a '+redisPwd+' '
		logWrite(pareLogFile,bcolors.BOLD+'deleting cluster node from redis cluster : '+clusterString+bcolors.ENDC)
		procStatus,procResult = commands.getstatusoutput(clusterString)
		if(procResult.find('[ERR]')==-1):
			print (queryRespond)
			return True
			print (bcolors.OKGREEN+'Node was deleted. OK :)!!!: '+clusterString+bcolors.ENDC)
		else:
			print (queryRespond)
			print (bcolors.FAIL+'!!! deleting cluster node was canceled !!!: '+clusterString+bcolors.ENDC)
			print (bcolors.FAIL+'!!! This node might be NON-empty master node !!!'+bcolors.ENDC)
			return False
	else:
		return False
def addMasterNode(serverIP,serverPORT):
	targetIP=''
	targetPORT=''
	nodeNumber=0
	for pareNode in pareNodes:
		if ( pareNode[4] ):
			if(isNodeMaster(pareNode[0][0],str(nodeNumber+1),pareNode[1][0])):
				targetIP=pareNode[0][0]
				targetPORT=pareNode[1][0]
				break		
		nodeNumber+=1
	clusterString=redisBinaryDir+'src/redis-cli --cluster add-node '+serverIP+':'+serverPORT+' '+targetIP+':'+targetPORT
	if(redisPwdAuthentication == 'on'):
		clusterString+=' -a '+redisPwd+' '	
	if(pingNode(serverIP,serverPORT)):
		logWrite(pareLogFile,bcolors.BOLD+'Adding new master node to redis cluster : '+clusterString+bcolors.ENDC)
		if(os.system(clusterString)==0):
			return True
			print (bcolors.OKGREEN+'New Node was added. OK :)!!!: Node IP:'+serverIP+' PORT:'+serverPORT+bcolors.ENDC)
		else:
			return False
	else:
		return False
def addSlaveNode(serverIP,serverPORT):
	targetIP=''
	targetPORT=''
	nodeNumber=0
	for pareNode in pareNodes:
		if ( pareNode[4] ):
			if(isNodeMaster(pareNode[0][0],str(nodeNumber+1),pareNode[1][0])):
				targetIP=pareNode[0][0]
				targetPORT=pareNode[1][0]
				break		
		nodeNumber+=1
	clusterString=redisBinaryDir+'src/redis-cli --cluster add-node '+serverIP+':'+serverPORT+' '+targetIP+':'+targetPORT+' --cluster-slave'
	if(redisPwdAuthentication == 'on'):
		clusterString+=' -a '+redisPwd+' '	
	if(pingNode(serverIP,serverPORT)):
		logWrite(pareLogFile,bcolors.BOLD+'Adding new slave node to redis cluster : '+clusterString+bcolors.ENDC)
		if(os.system(clusterString)==0):
			return True
		else:
			return False
	else:
		return False
def addSpecificSlaveNode(serverIP,serverPORT,cMasterID):
	targetIP=''
	targetPORT=''
	nodeNumber=0
	for pareNode in pareNodes:
		if ( pareNode[4] ):
			if(isNodeMaster(pareNode[0][0],str(nodeNumber+1),pareNode[1][0])):
				targetIP=pareNode[0][0]
				targetPORT=pareNode[1][0]
				break		
		nodeNumber+=1
	clusterString=redisBinaryDir+'src/redis-cli --cluster add-node '+serverIP+':'+serverPORT+' '+targetIP+':'+targetPORT+' --cluster-slave --cluster-master-id '+cMasterID
	if(redisPwdAuthentication == 'on'):
		clusterString+=' -a '+redisPwd+' '
	if(pingNode(serverIP,serverPORT)):
		logWrite(pareLogFile,bcolors.BOLD+'Adding new slave node to redis cluster : '+clusterString+bcolors.ENDC)
		if(os.system(clusterString)==0):
			return True
		else:
			return False
	else:
		return False	
def getMasterNodesID():
	print ('Master Node IDs :')
	pongNumber=0
	nonPongNumber=0
	for pareNode in pareNodes:
		nodeIP=pareNode[0][0]
		portNumber=pareNode[1][0]
		if ( pareNode[4] ):
			isPing=pingNode(nodeIP,portNumber)
			if (isPing):
				os.system(redisConnectCmd(nodeIP,portNumber,' cluster nodes | grep master'))
				break
def startNode(nodeIP,nodeNumber,portNumber,dedicateCpuCores):
	startResult=1
	if(pingNode(nodeIP,portNumber)):
		logWrite(pareLogFile,bcolors.WARNING+':: '+nodeIP+' :: WARNING !!! redis node  '+nodeNumber+' has been  already started. The proccess was canceled.'+bcolors.ENDC )
	else :
		if(nodeIP==pareServerIp):
			if ( dedicateCore ) :
				startResult,startOutput =commands.getstatusoutput('cd '+redisDataDir+';numactl --physcpubind='+dedicateCpuCores+' '+redisBinaryDir+'src/redis-server '+redisConfigDir+'node'+nodeNumber+'/redisN'+nodeNumber+'_P'+portNumber+'.conf')
				print ('numactl --physcpubind='+dedicateCpuCores+' '+redisBinaryDir+'src/redis-server '+redisConfigDir+'node'+nodeNumber+'/redisN'+nodeNumber+'_P'+portNumber+'.conf')
			else:
				startResult,startOutput =commands.getstatusoutput('cd '+redisDataDir+';'+redisBinaryDir+'src/redis-server '+redisConfigDir+'node'+nodeNumber+'/redisN'+nodeNumber+'_P'+portNumber+'.conf')		
		else:
			if ( dedicateCore ) :
				startResult,startOutput =commands.getstatusoutput('ssh -q -o "StrictHostKeyChecking no"  '+pareOSUser+'@'+nodeIP+' -C  "cd '+redisDataDir+';numactl --physcpubind='+dedicateCpuCores+' '+redisBinaryDir+'src/redis-server '+redisConfigDir+'node'+nodeNumber+'/redisN'+nodeNumber+'_P'+portNumber+'.conf"')
			else:
				startResult,startOutput =commands.getstatusoutput('ssh -q -o "StrictHostKeyChecking no"  '+pareOSUser+'@'+nodeIP+' -C  "cd '+redisDataDir+';'+redisBinaryDir+'src/redis-server '+redisConfigDir+'node'+nodeNumber+'/redisN'+nodeNumber+'_P'+portNumber+'.conf"')
		if ( startResult == 0 ):
			logWrite(pareLogFile,bcolors.OKGREEN+':: '+nodeIP+' :: OK -> redis node  '+nodeNumber+' started.'+bcolors.ENDC )
			logWrite(pareLogFile,bcolors.BOLD+':: '+nodeIP+' :: checking... -> redis node : '+nodeNumber+bcolors.ENDC )
			sleep(5)
			pingStatus,pingResponse = commands.getstatusoutput(redisConnectCmd(nodeIP,portNumber,' ping '))
			if ( pingStatus == 0 & pingResponse.find('PONG')>-1 ):
				logWrite(pareLogFile,bcolors.OKGREEN+':: '+nodeIP+' :: OK  -> redis node : '+nodeNumber+bcolors.ENDC )
			else :
				logWrite(pareLogFile,bcolors.FAIL+':: '+nodeIP+' :: WARNING !!! redis node  '+nodeNumber+' WAS NOT PING. CHECK IT.'+bcolors.ENDC)
		else:
			logWrite(pareLogFile,bcolors.FAIL+':: '+nodeIP+' :: WARNING !!! redis node  '+nodeNumber+' DID NOT started. CHECK IT.'+bcolors.ENDC)
def switchMasterSlave(nodeIP,nodeNumber,portNumber):
	if ( isNodeMaster(nodeIP,nodeNumber,portNumber) ) :
		proccessStatus,proccessResponse = commands.getstatusoutput(redisConnectCmd(nodeIP,portNumber,' info replication | grep slave0'))
		spStatus=1
		if(proccessResponse.find('online')>0):
			cutCursor1=proccessResponse.find('ip=')
			proccessResponse=proccessResponse[cutCursor1+3:]
			cutCursor2=proccessResponse.find(',')
			slaveIP=proccessResponse[:cutCursor2]
			proccessResponse=proccessResponse[cutCursor2:]
			cutCursor3=proccessResponse.find('port=')
			proccessResponse=proccessResponse[cutCursor3+5:]
			cutCursor4=proccessResponse.find(',')
			slavePort=proccessResponse[:cutCursor4]
			print (bcolors.WARNING+'Master/slave switch proccess is starting... This might take some times'+bcolors.ENDC)
			spStatus,spResponse = commands.getstatusoutput(redisConnectCmd(slaveIP,slavePort,' CLUSTER FAILOVER '))
			sleep(20)
			if (spStatus==0):
#				print (redisConnectCmd(nodeIP,portNumber,' CLUSTER FAILOVER ')
				print (bcolors.OKGREEN+'Switch master/slave command successed.'+bcolors.ENDC)
				print (bcolors.OKBLUE+'New Slave  IP:PORT '+nodeIP+':'+portNumber+bcolors.ENDC)
				print (bcolors.OKBLUE+'New Master IP:PORT '+slaveIP+':'+slavePort+bcolors.ENDC)
				return True
			else:
				print (bcolors.FAIL+'!!! Switch master/slave command failed. !!!'+bcolors.ENDC)
				return False

		else:
			print (bcolors.FAIL+'!!! There is no designated slave for node :' + str(nodeNumber) +' . Operation was canceled !!!'+bcolors.ENDC)
			return False
	else:
		print (bcolors.FAIL+'!!!This node is not Master. The proccess canceled!!!'+bcolors.ENDC)
		return False
def killNode(nodeIP,nodeNumber,portNumber):
	proccessResponse = ''
	proccessID = 'NULL'
	killNode='NO'
	hasSlave=False
	if ( isNodeMaster(nodeIP,nodeNumber,portNumber) ) :
		myResponse=raw_input(bcolors.FAIL+"\nThis node is Master node( nodeIP:"+nodeIP+" nodePort:"+portNumber+"), Do you want to stop this node (yes/no): "+bcolors.ENDC ) 
		if (lower(myResponse)=='yes'):
			if(isNodeHasSlave(nodeIP,nodeNumber,portNumber)):
				isSwitch=switchMasterSlave(nodeIP,nodeNumber,portNumber)
				if (isSwitch):
					killNode='YES'
				else:
					myResponse=raw_input(bcolors.FAIL+"\n Switching Master to slave failed \n Do you want to continue (force kill) ? (yes/no): "+bcolors.ENDC ) 
					if (lower(myResponse)=='yes'):				
						killNode='YES'
					elif(lower(myResponse)=='no'):
						print (bcolors.WARNING+' You canceled stoping proccess.'+bcolors.ENDC )
						sleep(2)
					else:
						print (bcolors.FAIL+'You entered wrong value :' + myResponse+bcolors.ENDC )
			else:
				myResponse=raw_input("\n!!!! This node is Master node, and has no slave !!!!!\n !!!! which means that redis cluster will be DOWN(FAIL) !!!!!\n Do you want to continue ? (yes/no): "+bcolors.ENDC ) 
				if (lower(myResponse)=='yes'):				
					killNode='YES'
				elif(lower(myResponse)=='no'):
					print (bcolors.WARNING+' You canceled stoping proccess.'+bcolors.ENDC )
					sleep(2)
				else:
					print (bcolors.FAIL+'You entered wrong value :' + myResponse+bcolors.ENDC )
					sleep(2)
		elif(lower(myResponse)=='no'):
			killNode='NO'
			print (bcolors.WARNING+' You canceled stoping proccess.'+bcolors.ENDC )
			sleep(3)
		else:
			print (bcolors.FAIL+'You entered wrong value :' + myResponse+bcolors.ENDC )
	else:
		killNode='YES'
	proccessStatus,proccessResponse = commands.getstatusoutput(	redisConnectCmd(nodeIP,portNumber,' info server | grep process_id:'))
	prCursor=proccessResponse.find('process_id:')
	proccessID=proccessResponse[prCursor+11:len(proccessResponse)-1] ##.replace('process_id:',' ')
	if(nodeIP==pareServerIp and proccessID<>'NULL' and  killNode=='YES'):	
		killResult=os.system('kill '+proccessID+' ')
		sleep(7)
	elif(nodeIP<>pareServerIp and proccessID<>'NULL' and  killNode=='YES'):
		killResult=os.system('ssh -q -o "StrictHostKeyChecking no"  '+pareOSUser+'@'+nodeIP+' -C  "kill  '+proccessID+'"')
		sleep(7)
	else :
		print ('!!!The proccess canceled!!!')
def stopNode(nodeIP,nodeNumber,portNumber):
	stopResult=1
	if(pingNode(nodeIP,portNumber)):
		killNode(nodeIP,nodeNumber,portNumber)
	else :
		logWrite(pareLogFile,bcolors.FAIL+':: '+nodeIP+' :: WARNING !!! redis node  '+nodeNumber+' has been already stoped. The proccess was canceled.'+bcolors.ENDC )
def restartNode(nodeIP,nodeNumber,portNumber,dedicateCpuCores):
	stopNode(nodeIP,nodeNumber,portNumber)
	startNode(nodeIP,nodeNumber,portNumber,dedicateCpuCores)
def redisBinaryCopier(myServerIP,myRedisVersion):
	if(myServerIP==pareServerIp):
		#cmdStatus=os.system('cp -pr redis-'+myRedisVersion+'/* '+redisBinaryDir)
		cmdStatus,cmdResponse = commands.getstatusoutput('cp -pr redis-'+myRedisVersion+'/* '+redisBinaryDir)
		if(cmdStatus==0):
			logWrite(pareLogFile,bcolors.OKGREEN+':: '+myServerIP+' :: OK -> redis binary was  copied.'+bcolors.ENDC)
			return True
		else:
			print (bcolors.FAIL+' !!! A problem occurred while binary copy proccess !!!'+bcolors.ENDC)
			return False
	else:
#		cmdStatus=os.system('scp -r redis-'+myRedisVersion+'/* '+pareOSUser+'@'+myServerIP+':'+redisBinaryDir)
		cmdStatus,cmdResponse = commands.getstatusoutput('scp -r redis-'+myRedisVersion+'/* '+pareOSUser+'@'+myServerIP+':'+redisBinaryDir)
		if(cmdStatus==0):
			logWrite(pareLogFile,bcolors.OKGREEN+':: '+myServerIP+' :: OK -> redis binary was copied.'+bcolors.ENDC)
			return True
		else:
			print (bcolors.FAIL+' !!! A problem occurred while binary copy proccess !!!'+bcolors.ENDC)
			return False			
def redisNewBinaryCopier(myServerIP,myRedisVersion):
	global redisBinaryDir
	global redisVersion
#	redisBinaryDir=redisBinaryDir.replace(redisVersion,myRedisVersion)
	redisBinaryDir=redisBinaryDir.replace('redis-'+redisVersion,'redis-'+myRedisVersion)
	if(myServerIP==pareServerIp):
		if ( makeDir(redisBinaryDir) ):
			print ('cp -pr redis-'+myRedisVersion+'/* '+redisBinaryDir)
			cmdStatus=os.system('cp -pr redis-'+myRedisVersion+'/* '+redisBinaryDir+' > /dev/null ')
			#cmdStatus,cmdResponse = commands.getstatusoutput('cp -pr redis-'+myRedisVersion+'/* '+redisBinaryDir)
			if(cmdStatus==0):
				logWrite(pareLogFile,bcolors.OKGREEN+':: '+myServerIP+' :: OK -> redis binary was  copied.'+bcolors.ENDC)
				return True
			else:
				print (bcolors.FAIL+' !!! A problem occurred while binary copy proccess !!!'+bcolors.ENDC)
				return False
		else:
			print (bcolors.FAIL+' !!! A problem occurred while binary directory making !!!'+bcolors.ENDC)
			return False							
	else:
		if(makeRemoteDir(redisBinaryDir,myServerIP)):
			print ('scp -r redis-'+myRedisVersion+'/* '+pareOSUser+'@'+myServerIP+':'+redisBinaryDir)
			cmdStatus=os.system('scp -r redis-'+myRedisVersion+'/* '+pareOSUser+'@'+myServerIP+':'+redisBinaryDir)
			if(cmdStatus==0):
				logWrite(pareLogFile,bcolors.OKGREEN+':: '+myServerIP+' :: OK -> redis binary was copied.'+bcolors.ENDC)
				return True
			else:
				print (bcolors.FAIL+' !!! A problem occurred while binary copy proccess !!!'+bcolors.ENDC)
				return False			
		else:
			print (bcolors.FAIL+' !!! A problem occurred while binary directory making !!!'+bcolors.ENDC)		
			return False			
def compileRedis(redisTarFileName,redisCurrentVersion):
	compileStatus=False
	isExtract,comResponse = commands.getstatusoutput('tar -xvf '+redisTarFileName)
	if(isExtract==0):
		logWrite(pareLogFile,bcolors.OKGREEN+' ::'+redisTarFileName+' was extracted.\nplease wait, the proccess (compile Redis - make) continue...'+bcolors.ENDC)
		os.system('cd redis-'+redisCurrentVersion)
		compileResponse = commands.getoutput('cd redis-'+redisCurrentVersion+';make')
#		os.system('pwd')
		if( compileResponse.find('make test')!=-1):
			logWrite(pareLogFile,bcolors.OKGREEN+' :: OK ->  redis was compiled.'+bcolors.ENDC)
			doMakeTest=raw_input(bcolors.BOLD+'\n Do you want to "make test" Press (yes/no): '+bcolors.ENDC )
			if(lower(doMakeTest)=='yes'):
				logWrite(pareLogFile,bcolors.WARNING+'please wait, the proccess (compile test - make test ) continue...'+bcolors.ENDC)
				compileResponseTest = commands.getoutput('cd redis-'+redisCurrentVersion+';make test')
				if( compileResponseTest.find('\o/ All tests passed')!=-1):
#				print ("step 3")
					logWrite(pareLogFile,bcolors.OKGREEN+' :: OK -> redis make test is successfull.'+bcolors.ENDC)
					compileStatus=True
				else:
					doContinue=raw_input(bcolors.FAIL+'!!! A problem was occured, during "make test". \n You should run command  "make test" manuelly on another screen then you should continue from here.  \n Do you want to continue? Press (yes/no): '+bcolors.ENDC )
					if(lower(doContinue)=='yes'):
						compileStatus=True
					else:
						compileStatus=False
			elif(lower(doMakeTest)=='no'):
				compileStatus=True
				logWrite(pareLogFile,bcolors.WARNING+'You entered "no" . "make test" canceled.'+bcolors.ENDC)
			else:
				compileStatus=True
				logWrite(pareLogFile,bcolors.WARNING+' !!! You entered wrong value. "make test" canceled !!!'+bcolors.ENDC)
	return compileStatus
def redisConfMaker(nodeIP,nodeNumber,portNumber,maxMemorySize):
	redisConfigText='#######This config file was generated by paredicma#######\n'
	redisConfigText+='bind '+nodeIP+'\n'
	redisConfigText+='port '+portNumber+'\n'
	redisConfigText+='unixsocket "'+unixSocketDir+'redisN'+nodeNumber+'_P'+portNumber+'.sock"\n'
	redisConfigText+='pidfile "'+pidFileDir+'redisN'+nodeNumber+'_P'+portNumber+'.pid"\n'
	redisConfigText+='logfile "'+redisLogDir+'redisN'+nodeNumber+'_P'+portNumber+'.log"\n'
	if( rdb == 'on'):
		redisConfigText+='dbfilename  "dumpN'+nodeNumber+'_P'+portNumber+'.rdb"\n'
		redisConfigText+=rdbValue+'\n'
	if( aof == 'on'):
		redisConfigText+='appendonly yes\n'	
		redisConfigText+='appendfilename  "appendonlyN'+nodeNumber+'_P'+portNumber+'.aof"\n'
		redisConfigText+=aofValue+'\n'
	if( redisCluster == 'on'):
		redisConfigText+='cluster-enabled yes\n'
		redisConfigText+='cluster-config-file "'+redisConfigDir+'node'+nodeNumber+'/'+'node'+nodeNumber+'_P'+portNumber+'.conf"\n'
		redisConfigText+=clusterNodeTimeout+'\n'
		redisConfigText+=clusterParameters+'\n'
	if (maxMemory == 'on' ):
		redisConfigText+='maxmemory '+maxMemorySize+'\n'
	if ( redisPwdAuthentication == 'on'):
		redisConfigText+='requirepass "'+redisPwd+'"\n'
		redisConfigText+='masterauth "'+redisPwd+'"'
	redisConfigText+=redisParameters
	fileClearWrite(pareTmpDir+'redisN'+nodeNumber+'_P'+portNumber+'.conf', redisConfigText)
	logWrite(pareLogFile,bcolors.OKGREEN+' ::'+nodeIP+'::'+ pareTmpDir+'redisN'+nodeNumber+'_P'+portNumber+'.conf file was created.'+bcolors.ENDC)
	if(nodeIP==pareServerIp):
		comResponse = commands.getoutput('cp -f '+pareTmpDir+'redisN'+nodeNumber+'_P'+portNumber+'.conf '+redisConfigDir+'node'+nodeNumber+'/')
		logWrite(pareLogFile,bcolors.OKGREEN+' ::'+nodeIP+':: redisN'+nodeNumber+'_P'+portNumber+'.conf file was copied.'+bcolors.ENDC)

	else:
		isOK,comResponse = commands.getstatusoutput('scp '+pareTmpDir+'redisN'+nodeNumber+'_P'+portNumber+'.conf '+pareOSUser+'@'+nodeIP+':'+redisConfigDir+'node'+nodeNumber+'/')
		if (isOK==0):
			logWrite(pareLogFile,bcolors.OKGREEN+' ::'+nodeIP+':: redisN'+nodeNumber+'_P'+portNumber+'.conf file was copied.'+bcolors.ENDC)
		else:
			logWrite(pareLogFile,bcolors.FAIL+' ::'+nodeIP+':: redisN'+nodeNumber+'_P'+portNumber+'.conf !!!ERROR when file copy.'+bcolors.ENDC)
def redisDirMaker(nodeIP,nodeNumber):
	directoryDone = False
	if(nodeIP==pareServerIp):
		if ( makeDir(redisDataDir) &  makeDir(redisConfigDir) & makeDir(redisLogDir) & makeDir(redisBinaryDir) & makeDir(unixSocketDir)  & makeDir(pidFileDir) & makeDir(redisConfigDir+'node'+nodeNumber)):
			directoryDone = True
	else:
		print (bcolors.WARNING+'Working on remote server...'+bcolors.ENDC)
		if ( makeRemoteDir(redisDataDir,nodeIP) &  makeRemoteDir(redisConfigDir,nodeIP) & makeRemoteDir(redisLogDir,nodeIP) & makeRemoteDir(redisBinaryDir,nodeIP) & makeRemoteDir(unixSocketDir,nodeIP)  & makeRemoteDir(pidFileDir,nodeIP) & makeRemoteDir(redisConfigDir+'node'+nodeNumber,nodeIP)):
			directoryDone = True
def makeRemoteDir(dir_name,nodeIP):
	try:
		isOK = commands.getoutput('ssh -q -o "StrictHostKeyChecking no"  '+pareOSUser+'@'+nodeIP+' -C  "if [ -d '+dir_name+' ]; then echo yesThereIs; else echo noThereIsNot; fi"')
		if (isOK.find('yesThereIs')==-1):
			comResponse = commands.getoutput('ssh -q -o "StrictHostKeyChecking no"  '+pareOSUser+'@'+nodeIP+' -C  "mkdir -p '+dir_name+'"')
			logWrite(pareLogFile,bcolors.OKGREEN+' ::'+nodeIP+':: Directory was created = ' + dir_name+bcolors.ENDC)
			return True
		else:
			logWrite(pareLogFile,bcolors.WARNING+' ::'+nodeIP+':: Directory has been already existed  = ' + dir_name+bcolors.ENDC)
			return True
			
	except :
		logWrite(pareLogFile,bcolors.FAIL+'!!! An error is occurred while writing directory  !!! = ' + dir_name+bcolors.ENDC)
		return False		
def makeDir(dir_name):
	try:
		if(os.path.isdir(dir_name)):
			logWrite(pareLogFile,bcolors.WARNING+'Directory has been already existed = ' + dir_name+bcolors.ENDC)
			return True
		else:
			os.makedirs(dir_name)
			logWrite(pareLogFile,bcolors.OKGREEN+'Directory was created = ' + dir_name+bcolors.ENDC)
			return True
	except :
		logWrite(pareLogFile,bcolors.FAIL+'!!! An error is occurred while writing directory  !!! = ' + dir_name+bcolors.ENDC)
		return False
def get_datetime():
	mounth=str(localtime()[1])
	my_hour=str(localtime()[3])
	my_min=str(localtime()[4])
	if(len(str(localtime()[1]))==1):
		mounth="0"+str(localtime()[1])
	day=str(localtime()[2])
	if(len(str(localtime()[2]))==1):
		day="0"+str(localtime()[2])
	return str(localtime()[0])+"."+mounth+"."+day+" "+my_hour+":"+my_min
def fileAppendWrite(file, writeText):
	try :
		fp=open(file,'ab')
		fp.write(writeText+'\n')
		fp.close()
	except :
		print (bcolors.FAIL+'!!! An error is occurred while writing file !!!'+bcolors.ENDC)
def fileRead(file):
	returnTEXT=""
	try :
		fp=open(file,'r')
		returnTEXT=fp.readlines()
		fp.close()
		return returnTEXT
	except :
		print (bcolors.FAIL+'!!! An error is occurred while reading file !!!'+bcolors.ENDC)
		return ""
def fileReadFull(file):
	returnTEXT=""
	try :
		fp=open(file,'r')
		returnTEXT=fp.read()
		fp.close()
		return returnTEXT
	except :
		print (bcolors.FAIL+'!!! An error is occurred while reading file !!!'+bcolors.ENDC)
		return ""
def fileClearWrite(file, writeText):
	try :
		fp=open(file,'w')
		fp.write(writeText+'\n')
		fp.close()
	except :
		print (bcolors.FAIL+'!!! An error is occurred while writing file !!!'+bcolors.ENDC)
def logWrite(logFile,logText):
	if(writePareLogFile):
		print (logText)
		logText='* ('+get_datetime()+') '+logText
		fileAppendWrite(logFile,logText)		
	else:
		print (logText)
