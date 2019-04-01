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
		memFrag=0.0
		printTextMaster=''
		printTextSlave=''
		isMaster=False
		for pareNode in pareNodes:
			nodeIP=pareNode[0][0]
			portNumber=pareNode[1][0]
			nodeNumber=nodeNumber+1
			if (pareNode[4]):
				memStatus,memResponse = commands.getstatusoutput(redisConnectCmd(nodeIP,portNumber,' info memory | grep  -e "mem_fragmentation_ratio:" '))
				if ( memStatus == 0 ):
					memFrag=float(memResponse[24:memResponse.find('mem_fragmentation_ratio:')-1])
					if (isNodeMaster(nodeIP,nodeNumber,portNumber)):
						isMaster=True
						str(nodeNumber)+'	'+nodeIP+'-( M )			'+portNumber+'		'+str(memFrag)+bcolors.ENDC+'\n'
					else:
						isMaster=False
						str(nodeNumber)+'	'+nodeIP+'-( S )			'+portNumber+'		'+str(memFrag)+bcolors.ENDC+'\n'
					if (memFrag>=1.50):
						if(isMaster):
							printTextMaster+=bcolors.FAIL+str(nodeNumber)+'	'+nodeIP+'-( M )			'+portNumber+'		'+str(memFrag)+bcolors.ENDC+'\n'
						else:
							printTextSlave+=bcolors.FAIL+str(nodeNumber)+'	'+nodeIP+'-( S )			'+portNumber+'		'+str(memFrag)+bcolors.ENDC+'\n'
					elif (memFrag>=1.20 and memFrag<1.50):
						if(isMaster):
							printTextMaster+=bcolors.WARNING+str(nodeNumber)+'	'+nodeIP+'-( M )			'+portNumber+'		'+str(memFrag)+bcolors.ENDC+'\n'
						else:
							printTextSlave+=bcolors.WARNING+str(nodeNumber)+'	'+nodeIP+'-( S )			'+portNumber+'		'+str(memFrag)+bcolors.ENDC+'\n'
					else:
						if(isMaster):
							printTextMaster+=bcolors.OKGREEN+str(nodeNumber)+'	'+nodeIP+'-( M )			'+portNumber+'		'+str(memFrag)+bcolors.ENDC+'\n'
						else:
							printTextSlave+=bcolors.OKGREEN+str(nodeNumber)+'	'+nodeIP+'-( S )			'+portNumber+'		'+str(memFrag)+bcolors.ENDC+'\n'
				else :
					print (bcolors.FAIL+'!!! Warning !!!! A problem occurred, while memory usage checking !!! nodeID :'+str(nodeNumber)+' NodeIP:'+nodeIP+' NodePort:'+portNumber+''+bcolors.ENDC)
		os.system("clear")
                print ( bcolors.HEADER+projectName+' Redis Cluster  Memory Usage'+bcolors.ENDC+' ( '+get_datetime()+' )\n---------------------------------------------')
                print (bcolors.HEADER+'nodeID           NodeIP                           NodePort       mem_fragmentation_ratio'+bcolors.ENDC)
		print printTextMaster+bcolors.BOLD+'-------------------------------------------------------------------------------------------------------'+bcolors.ENDC
		print printTextSlave
		sleep(10)
main()
