import os
import sys
from time import *
#from  pareConfig import *
from pareFunc import *
from screenMenu import *
from paredicma import *
def main():
	os.system("clear")
	while(True):
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
					usedMem=round((usedMemByte)/(1024*1024*1024),2)
					maxMem=round((maxMemByte)/(1024*1024*1024),2)
					usagePerMem=round((usedMem/maxMem)*100,2)
					if (isNodeMaster(nodeIP,nodeNumber,portNumber)):
						totalUsedMemByte+=usedMemByte
						totalMaxMemByte+=maxMemByte						
						isMaster=True
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
		sleep(2)					
		os.system("clear")					
		print ( bcolors.HEADER+projectName+' Redis Cluster  Memory Usage'+bcolors.ENDC+'\n---------------------------------------------')
		print (bcolors.HEADER+'nodeID 		NodeIP				 NodePort	Used Mem(GB)	Max Mem(GB)	Usage Percentage(%)'+bcolors.ENDC)
		print printTextMaster+bcolors.BOLD+'-------------------------------------------------------------------------------------------------------'+bcolors.ENDC
		print printTextSlave
		totalUsedMem=round(((totalUsedMemByte)/(1024*1024*1024)),2)
		totalMaxMem=round(((totalMaxMemByte)/(1024*1024*1024)),2)
		if (totalMaxMem==0):
			totalMemPer=0.0
		else:
			totalMemPer=round(((totalUsedMem/totalMaxMem)*100),2)
		print (bcolors.BOLD+'-------------------------------------------------------------------------------------------------------'+bcolors.ENDC)
		print (bcolors.BOLD+'TOTAL ( Only Master)						:'+str(totalUsedMem)+'GB	'+str(totalMaxMem)+'GB		'+str(totalMemPer)+'% '+bcolors.ENDC)
main()
