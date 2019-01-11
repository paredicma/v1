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
import sys
from time import *
from  pareConfig import *
from pareFunc import *
from screenMenu import *
from paredicma import *
def main():
	MenuState=0
	ans=True
	while ans:
		if(MenuState==0):
			menuMain()
			ans=raw_input("	What would you like to do? ") 
		if ans=="1" or  MenuState==1 : 
			if(os.path.isfile('paredicma.done')==False):
				resCluster=raw_input(bcolors.WARNING +"\nRedis cluster have NOT  been created yet. You DO NOT use this menu. (for force use 'touch paredicma.done' file)"+bcolors.ENDC) 
				MenuState=0
				menuMain() 
			else :
				MenuState=1		
				menuMon()
				nodeNumber=0
				returnVAl=raw_input("	What would you like to do? :") 
				if returnVAl=="1" :  ### ping Cluster nodes
					print ('Pinging Nodes...')
					pongNumber=0
					nonPongNumber=0
					for pareNode in pareNodes:
						nodeIP=pareNode[0][0]
						portNumber=pareNode[1][0]
						nodeNumber=nodeNumber+1
						if ( pareNode[4] ):
							isPing=pingNode(nodeIP,portNumber)
							if (isPing):
								print (bcolors.OKGREEN+'OK -> Node Number :'+str(nodeNumber)+' Server IP :'+nodeIP+' Port:'+portNumber+bcolors.ENDC )
								pongNumber+=1
							else:
								print (bcolors.FAIL+'!!!! NOT OK -> Node Number :'+str(nodeNumber)+' Server IP :'+nodeIP+' Port:'+portNumber+bcolors.ENDC )
								nonPongNumber+=1
					returnVAl=raw_input('\n--------------\n'+bcolors.OKGREEN+'OK Nodes = '+str(pongNumber)+bcolors.ENDC+bcolors.FAIL+'\nNot OK Nodes = '+str(nonPongNumber)+'\n--------------'+bcolors.ENDC+'\nPress Enter to Return Paredicmon Menu')
				elif returnVAl=="2" : 		### list redis Nodes
					funcNodesList()	
					print (bcolors.BOLD+'Press Enter to Return Paredicmon Menu'+bcolors.ENDC )
				elif returnVAl=="3" : 		### node Info
					infoCmd=''
					nodeCmd=raw_input(bcolors.BOLD+'\nPlease enter node nunmber and cmd ("4" or "2 memory" or "3 server" or "3 cpu" etc.) \n  nodeNumber ( and cmd ) : '+bcolors.ENDC )
					if (nodeCmd.isdigit()):
						if(int(nodeCmd)>len(pareNodes) or pareNodes[int(nodeCmd)-1][4] == False ):
							print (bcolors.WARNING+'\nYou entered wrong node nunmber\n'+bcolors.ENDC )
						else:
							nodeNumber=int(nodeCmd)
							nodeIP=pareNodes[nodeNumber-1][0][0]
							portNumber=pareNodes[nodeNumber-1][1][0]
							nodeInfoVal=nodeInfo(nodeIP,nodeNumber,portNumber,infoCmd)
							returnVAl=raw_input(bcolors.BOLD+'\n------- Node Info -------\nNode Number :'+str(nodeNumber)+' Server IP :'+nodeIP+' Port:'+portNumber+'\n'+nodeInfoVal+'\n------------------\nPress Enter to Return Paredicmon Menu'+bcolors.ENDC )
					else:
						cmdList=nodeCmd.split(' ')
						if (cmdList[0].isdigit() and ( lower(cmdList[1])=='server' or lower(cmdList[1])=='clients' or lower(cmdList[1])=='memory' or lower(cmdList[1])=='persistence' or lower(cmdList[1])=='stats' or lower(cmdList[1])=='replication' or lower(cmdList[1])=='cpu' or lower(cmdList[1])=='cluster' or lower(cmdList[1])=='keyspace')):
							if(int(cmdList[0])>len(pareNodes) or pareNodes[int(cmdList[0])-1][4] == False ):
								print (bcolors.WARNING+'\nYou entered wrong node nunmber \n------------------'+bcolors.ENDC )
							else:
								infoCmd=cmdList[1]
								nodeNumber=int(cmdList[0])
								nodeIP=pareNodes[nodeNumber-1][0][0]
								portNumber=pareNodes[nodeNumber-1][1][0]
								nodeInfoVal=nodeInfo(nodeIP,nodeNumber,portNumber,infoCmd)
								returnVAl=raw_input(bcolors.BOLD+'\n------- Node Info -------\nNode Number :'+str(nodeNumber)+' Server IP :'+nodeIP+' Port:'+portNumber+'\n------------------\n'+nodeInfoVal+'\n------------------\nPress Enter to Return Paredicmon Menu'+bcolors.ENDC )
						else:
							print (bcolors.WARNING+'\nYou entered wrong value \n------------------'+bcolors.ENDC )
				elif returnVAl=="4" : 		### Server Info
					serverIP=raw_input(bcolors.BOLD+'\n Enter server IP            :'+bcolors.ENDC )
					if (validIP(serverIP)):
						serverInfo(serverIP)
					else:
						print (bcolors.FAIL+'\nYou entered wrong IP nunmber\n'+bcolors.ENDC)
				elif returnVAl=="5" : 		### Slot Info
					nodeNumber=0
					for pareNode in pareNodes:
						nodeIP=pareNode[0][0]
						portNumber=pareNode[1][0]
						nodeNumber=nodeNumber+1
						if ( pareNode[4] ):
							isPing=pingNode(nodeIP,portNumber)
							if (isPing):
								slotInfo(nodeIP,portNumber)
								break					
				elif returnVAl=="6" : 		### Cluster Status
					nodeNumber=0
					for pareNode in pareNodes:
						nodeIP=pareNode[0][0]
						portNumber=pareNode[1][0]
						nodeNumber=nodeNumber+1
						if ( pareNode[4] ):
							isPing=pingNode(nodeIP,portNumber)
							if (isPing):
								clusterStateInfo(nodeIP,nodeNumber,portNumber)
					raw_input('\n----------------------\nPress Enter to Return Paredicmon Menu')						
				elif returnVAl=="7" : 		### Show Memory Usage
					showMemoryUsage()
#					raw_input('\n-----------------------------------------\nPress Enter to Return Paredicmon Menu')
				elif returnVAl=="8" : 		### Not Designated
					print ('hello man')
				elif returnVAl=="9" : 		### Main Menu
					print ("your Choise: "+returnVAl+" --- You are going to Main Menu ...")
					MenuState=0
				elif returnVAl=="10" : 		### Exit
					print ("your Choise : "+returnVAl)
					print("\n Goodbye") 
					exit()
				else :
					print(bcolors.WARNING +"\n !!! Not Valid Choice! Try again"+bcolors.ENDC)
					sleep(1)
		elif ans=="2"  or  MenuState==2:
			if(os.path.isfile('paredicma.done')==False):
				resCluster=raw_input(bcolors.WARNING +"\nRedis cluster have NOT  been created yet. You DO NOT use this menu. (for force use 'touch paredicma.done' file)"+bcolors.ENDC) 
				MenuState=0
				menuMain() 
			else :
				MenuState=2
				menuMan() 
				returnVAl=raw_input("	What would you like to do? :") 
				if returnVAl=="1" :     ### Start/Stop/Restart Redis Node 
					print (bcolors.BOLD+'Start/Stop/Restart Redis Node\n------------------\n'+bcolors.ENDC )
					funcNodesList()				
					myNodeNum=raw_input(bcolors.BOLD+"\nPlease Enter Node Number : "+bcolors.ENDC ) 
					print ('Your choise :'+bcolors.BOLD+myNodeNum+bcolors.ENDC)
					if (myNodeNum.isdigit()):
						nodeNumber=int(myNodeNum)
						if( nodeNumber<=len(pareNodes) and  pareNodes[nodeNumber-1][4] ):
							nodeIP = pareNodes[nodeNumber-1][0][0]				
							portNumber = pareNodes[nodeNumber-1][1][0]
							dedicateCpuCores = pareNodes[nodeNumber-1][2][0]
							myOps=raw_input(bcolors.BOLD+"\nPlease Choose Operation ( Start/Stop/Restart) : "+bcolors.ENDC)
							if (lower(myOps)=='start'):
								print (bcolors.BOLD+'Node :'+myNodeNum+' is starting...'+bcolors.ENDC)
								startNode(nodeIP,str(nodeNumber),portNumber,dedicateCpuCores)
							elif (lower(myOps)=='stop'):
								print (bcolors.BOLD+'Node :'+myNodeNum+' is stoping...'+bcolors.ENDC)
								stopNode(nodeIP,str(nodeNumber),portNumber)
							elif (lower(myOps)=='restart'):
								print (bcolors.BOLD+'Node :'+myNodeNum+' is restarting...'+bcolors.ENDC)
								restartNode(nodeIP,str(nodeNumber),portNumber,dedicateCpuCores)
							else:
								print (bcolors.FAIL+'!!!You entered wrong value!!! : ' + myOps+bcolors.ENDC)
						else:
							print (bcolors.FAIL+'!!!You entered wrong number!!! : ' + myNodeNum+bcolors.ENDC)
					else:
							print (bcolors.FAIL+'!!!You entered wrong value!!! : ' + myNodeNum+bcolors.ENDC)
					funcNodesList()	
				elif returnVAl=="2" : 		### Switch Master/Slave Nodes
					print (bcolors.BOLD+'Switch Master/Slave Redis Node\n------------------\n'+bcolors.ENDC)
					funcNodesList()				
					myNodeNum=raw_input(bcolors.BOLD+"\nPlease Enter Master Node Number : "+bcolors.ENDC) 
					print ('Your choise :'+myNodeNum)
					if (myNodeNum.isdigit()):
						nodeNumber=int(myNodeNum)
						if(nodeNumber<=len(pareNodes) and  pareNodes[nodeNumber-1][4]):
							nodeIP = pareNodes[nodeNumber-1][0][0]				
							portNumber = pareNodes[nodeNumber-1][1][0]
							dedicateCpuCores = pareNodes[nodeNumber-1][2][0]
							myOps=raw_input(bcolors.WARNING+"\nAre Youu Sure ( yes/no) : "+bcolors.ENDC)
							if (lower(myOps)=='yes'):
								print (bcolors.BOLD+'Node :'+myNodeNum+' is switching...'+bcolors.ENDC)
								swOK=switchMasterSlave(nodeIP,nodeNumber,portNumber)
	#							if(swOK)
							elif (lower(myOps)=='no'):
								print (colors.FAIL+'Operation canceled.'+bcolors.ENDC)
							else:
								print (colors.FAIL+'!!!You entered wrong value!!! : ' + myOps+bcolors.ENDC)
						else:
							print (colors.FAIL+'!!!You entered wrong number!!! : ' + myNodeNum+bcolors.ENDC)
					else:
							print (colors.FAIL+'!!!You entered wrong value!!! : ' + myNodeNum+bcolors.ENDC)
					funcNodesList()	
				elif returnVAl=="3" : 		### Change Redis Coonfiguration
					print (bcolors.BOLD+'Change Redis Configuration'+bcolors.ENDC)
					funcNodesList()				
					myNodeNum=raw_input(bcolors.BOLD+'\nPlease Enter Node Number or Enter "all": '+bcolors.ENDC)
					if (myLineNum.isdigit() or myLineNum==''):
						if ( myLineNum=='' ):
							myLineNum='40'
						if (int(myNodeNum)<=len(pareNodes) and  pareNodes[int(myNodeNum)-1][4]):
							myConfigParameter=raw_input(bcolors.BOLD+'\nPlease Enter Configuration  parameter (for example: "slowlog-max-len 10" ,"maxmemory 3gb" ext.) \n	: '+bcolors.ENDC)
							yesNo=raw_input(bcolors.WARNING+'\nAre you sure to set this parameter -> '+myConfigParameter+'  (yes/no):'+bcolors.ENDC)
							if (lower(yesNo)=='yes'):
								nodeIP=pareNodes[int(myNodeNum)-1][0][0]
								portNumber=pareNodes[int(myNodeNum)-1][1][0]
								print (bcolors.BOLD+'Redis configuration will change on Node Number :'+myNodeNum+'  Node IP :'+nodeIP+'  Node Port :'+portNumber +bcolors.ENDC)
								os.system(redisConnectCmd(nodeIP,portNumber,' CONFIG SET '+myConfigParameter))						
							else:
								print (colors.FAIL+'!!!Operation was canceled !!!'+bcolors.ENDC)
							
						else:
							print (colors.FAIL+'!!!You entered wrong value!!! : ' + myNodeNum+bcolors.ENDC)
					elif (lower(myNodeNum)=='all') :
						myConfigParameter=raw_input('\nPlease Enter Configuration  parameter (for example: "slowlog-max-len 10" ,"maxmemory 3gb" ext.) \n	: ')				
						yesNo=raw_input('\nAre you sure to set this parameter -> '+myConfigParameter+'  (yes/no):')
						if (lower(yesNo)=='yes'):
							nodeNumber=0
							for pareNode in pareNodes:
								nodeIP=pareNode[0][0]
								portNumber=pareNode[1][0]
								nodeNumber=nodeNumber+1
								if ( pareNode[4] ):
									print ('Redis configuration will change  will rewrite on Node Number :'+str(nodeNumber)+'  Node IP :'+nodeIP+'  Node Port :'+portNumber )
									os.system(redisConnectCmd(nodeIP,portNumber,' CONFIG SET '+myConfigParameter))						
						else:
							print ('!!!Operation was canceled !!!')
						
					else :
						print ('!!!You entered wrong value!!! : ' + myNodeNum)
					sleep(3)
					
					sleep(3)
				elif returnVAl=="4" : 		### Save Redis Config to redis.conf
					print (bcolors.BOLD+'Save Redis Configuration to redis.conf'+bcolors.ENDC)
					funcNodesList()				
					myNodeNum=raw_input(bcolors.BOLD+'\nPlease Enter Node Number or "all": '+bcolors.ENDC)
					if (myNodeNum.isdigit()):
						if (int(myNodeNum)<=len(pareNodes) and  pareNodes[int(myNodeNum)-1][4]):
							nodeIP=pareNodes[int(myNodeNum)-1][0][0]
							portNumber=pareNodes[int(myNodeNum)-1][1][0]
							print (bcolors.BOLD+'Redis config file  will rewrite on Node Number :'+myNodeNum+'  Node IP :'+nodeIP+'  Node Port :'+portNumber +bcolors.ENDC)
							os.system(redisConnectCmd(nodeIP,portNumber,' CONFIG REWRITE'))						
							
						else:
							print (colors.FAIL+'!!!You entered wrong value!!! : ' + myNodeNum+bcolors.ENDC)
					elif (lower(myNodeNum)=='all') :
						nodeNumber=0
						for pareNode in pareNodes:
							nodeIP=pareNode[0][0]
							portNumber=pareNode[1][0]
							nodeNumber=nodeNumber+1
							if ( pareNode[4] ):
								print (bcolors.BOLD+'Redis config file  will rewrite on Node Number :'+str(nodeNumber)+'  Node IP :'+nodeIP+'  Node Port :'+portNumber +bcolors.ENDC)
								os.system(redisConnectCmd(nodeIP,portNumber,' CONFIG REWRITE'))						
					else :
						print (colors.FAIL+'!!!You entered wrong value!!! : ' + myNodeNum+bcolors.ENDC)
					sleep(3)
				elif returnVAl=="5" : 		### Rolling Restart
					print ('Rolling Restart is launching.')
					nodeNumber=0
					waitSleep=raw_input(bcolors.BOLD+"\nsleep time between node restart (0 = no sleep time, minute(s) ) :"+bcolors.ENDC)
					rebootList=''
					if (waitSleep.isdigit()):
						for pareNode in pareNodes:
							nodeIP=pareNode[0][0]
							portNumber=pareNode[1][0]
							dedicateCpuCores=pareNode[2][0]					
							nodeNumber=nodeNumber+1
							if ( pareNode[4] and isNodeMaster(nodeIP,nodeNumber,portNumber)==False):
								print (bcolors.BOLD+'Node Number :'+str(nodeNumber)+'  Node IP :'+nodeIP+'  Node Port :'+portNumber+bcolors.ENDC)
								restartNode(nodeIP,str(nodeNumber),portNumber,dedicateCpuCores)
								rebootList+='N'+str(nodeNumber)+'N-'
								sleep(int(waitSleep)*60)
						nodeNumber=0
						for pareNode in pareNodes:
							nodeIP=pareNode[0][0]
							portNumber=pareNode[1][0]
							dedicateCpuCores=pareNode[2][0]					
							nodeNumber=nodeNumber+1
							if ( pareNode[4] and isNodeMaster(nodeIP,nodeNumber,portNumber) and rebootList.find('N'+str(nodeNumber)+'N-')==-1):
								print (bcolors.BOLD+'Node Number :'+str(nodeNumber)+'  Node IP :'+nodeIP+'  Node Port :'+portNumber+bcolors.ENDC)
								restartNode(nodeIP,str(nodeNumber),portNumber,dedicateCpuCores)
								sleep(int(waitSleep)*60)								
					else:
						print (colors.FAIL+'!!!You entered wrong value!!! : ' + waitSleep+bcolors.ENDC)
					sleep(3)
				elif returnVAl=="6" : 		### Command for all nodes
					RedisCmd=raw_input(bcolors.BOLD+"\nPlease Enter Redis Command :"+bcolors.ENDC)
					print ("your Command :"+bcolors.WARNING+RedisCmd+bcolors.ENDC)
					onlyMaster=raw_input(bcolors.BOLD+"\nDou you want to execute this command for !!! ONLY MASTER NODES !!! (yes/no) :"+bcolors.ENDC)
					if(lower(onlyMaster)=='yes' or lower(onlyMaster)=='no'):
						waitSleep=raw_input(bcolors.BOLD+"\nsleep time between command (0 = no sleep time, minute(s) ) :"+bcolors.ENDC)
						if (waitSleep.isdigit()):
							nodeNumber=0
							for pareNode in pareNodes:
								nodeIP=pareNode[0][0]
								portNumber=pareNode[1][0]
								nodeNumber=nodeNumber+1
								if ( pareNode[4] ):
									if(isNodeMaster(nodeIP,str(nodeNumber),portNumber)):
										print (bcolors.BOLD+'Command will execute on Node Number :'+str(nodeNumber)+'  Node IP :'+nodeIP+'  Node Port :'+portNumber +bcolors.ENDC)
										os.system(redisConnectCmd(nodeIP,portNumber,RedisCmd))
									else:
										if(lower(onlyMaster)=='no'):
											print (bcolors.BOLD+'Command will execute on Node Number :'+str(nodeNumber)+'  Node IP :'+nodeIP+'  Node Port :'+portNumber +bcolors.ENDC)
											os.system(redisConnectCmd(nodeIP,portNumber,RedisCmd))
									sleep(int(waitSleep)*60)
						else:
							print (bcolors.FAIL+'!!!You entered wrong value!!! : ' + waitSleep+bcolors.ENDC)
					else:
						print (bcolors.FAIL+'!!!You entered wrong value!!! : ' + onlyMaster+bcolors.ENDC)
					myR=raw_input(bcolors.BOLD+'\nPress Enter to continue...'+bcolors.ENDC)
				elif returnVAl=="7" : 		### Show Redis Log File
					funcNodesList()
					myNodeNum=raw_input(bcolors.BOLD+"\nPlease Enter Node Number : "+bcolors.ENDC ) 
					print ('Your choise :'+bcolors.BOLD+myNodeNum+bcolors.ENDC)
					if (myNodeNum.isdigit()):
						nodeNumber=int(myNodeNum)
						if( nodeNumber<=len(pareNodes) and  pareNodes[nodeNumber-1][4] ):
							myLineNum=raw_input(bcolors.BOLD+"\nHow many line do you want to see ( 1-1000 ) ? : "+bcolors.ENDC ) 
							if (myLineNum.isdigit()):
								if(int(myLineNum)<=1000 and int(myLineNum)>0):							
									nodeIP = pareNodes[nodeNumber-1][0][0]				
									portNumber = pareNodes[nodeNumber-1][1][0]									
									showRedisLogFile(nodeIP,str(nodeNumber),portNumber,myLineNum)									
								else:
									print (bcolors.FAIL+'!!!You entered wrong value. It must be between 1 - 1000 !!! : ' + myLineNum+bcolors.ENDC)									
							else:
								print (bcolors.FAIL+'!!!You entered wrong value!!! : ' + myLineNum+bcolors.ENDC)
						else:
							print (bcolors.FAIL+'!!!You entered wrong number!!! : ' + myNodeNum+bcolors.ENDC)
					else:
							print (bcolors.FAIL+'!!!You entered wrong value!!! : ' + myNodeNum+bcolors.ENDC)				
				elif returnVAl=="8" : 		### Not Designated
					print ('hello man'	)	
				elif returnVAl=="9" : 		### Main Menu
					print (bcolors.BOLD+"your Choise :"+returnVAl+" --- You are going to Main Menu ..."+bcolors.ENDC)
					MenuState=0
				elif returnVAl=="10" : 		### Exit
					print ("your Choise : "+bcolors.WARNING+returnVAl+bcolors.ENDC)
					print("\n Goodbye") 
					exit()
				else :
					print(bcolors.FAIL +"\n !!! Not Valid Choice! Try again"+bcolors.ENDC)
					sleep(1)
			sleep(1)
		elif ans=="3"  or  MenuState==3:
			if(os.path.isfile('paredicma.done')==False):
				resCluster=raw_input(bcolors.WARNING +"\nRedis cluster have NOT  been created yet. You DO NOT use this menu. (for force use 'touch paredicma.done' file)"+bcolors.ENDC) 
				MenuState=0
				menuMain() 
			else :
				MenuState=3
				menuMum() 
				returnVAl=raw_input(bcolors.BOLD +' What would you like to do? '+bcolors.ENDC) 
				if returnVAl=="1" : 		### Add/Delete Redis Node
					global redisVersion
					print (bcolors.BOLD+'Add/Delete Redis Node'+bcolors.ENDC)
					operationType=raw_input(bcolors.BOLD +'\nPlease enter operation type "1" ->add or "2" -> del:'+bcolors.ENDC)
					if(operationType=='1' or lower(operationType)=='add'):
						serverIP=raw_input(bcolors.BOLD +'\nPlease enter node IP :'+bcolors.ENDC)
						if (validIP(serverIP)):
							serverPORT=raw_input(bcolors.BOLD +'\nPlease enter node port :'+bcolors.ENDC)
							if(serverPORT.isdigit()):
								maxMemSize=raw_input(bcolors.BOLD +'\nPlease enter node memory size ("1gb","500mb","4gb" ext.) :'+bcolors.ENDC)
								cpuCoreOK=True
								cpuCoreIDs=raw_input(bcolors.BOLD +'\nPlease enter dedicate cpu core id(s)  ("1" or "3" or "4,5" or  "8,9,10,11" ext.) :'+bcolors.ENDC)
								coreList=cpuCoreIDs.split(',')
								for coreId in coreList:
									if(coreId.isdigit()==False):
										cpuCoreOK=False
								if(maxMemSize[:len(maxMemSize)-2].isdigit() and ( lower(maxMemSize[len(maxMemSize)-2:])=='gb' or lower(maxMemSize[len(maxMemSize)-2:])=='mb' ) ):
									if(pingNode(serverIP,serverPORT) and cpuCoreOK):
										print (bcolors.FAIL +'!!! This IP('+serverIP+'):Port('+serverPORT+') is already used by Redis Cluster !!!\n Operation canceled !!!'+bcolors.ENDC)
									else:
										isActive=False
										isNewServer=True
										nodeNumber=len(pareNodes)+1
										for pareNode in pareNodes:
											nodeIP=pareNode[0][0]
											portNumber=pareNode[1][0]
											if ( pareNode[4] ):
												if(nodeIP==serverIP):
													isNewServer=False
													if(portNumber==serverPORT ):
														isActive=True
										nodeStr=''
										if(isActive==False):
											if(isNewServer):
												redisDirMaker(serverIP,str(nodeNumber))										
												redisBinaryCopier(serverIP,redisVersion)
												redisConfMaker(serverIP,str(nodeNumber),serverPORT,maxMemSize)
											else:
												redisDirMaker(serverIP,str(nodeNumber))
												redisConfMaker(serverIP,str(nodeNumber),serverPORT,maxMemSize)
											startNode(serverIP,str(nodeNumber),serverPORT,cpuCoreIDs)
											willbeMasterNode=raw_input(bcolors.BOLD +'\nDo you want to set this node as MASTER (yes/no):'+bcolors.ENDC)
											if (lower(willbeMasterNode)=='yes'):
												if(addMasterNode(serverIP,serverPORT)):
													nodeStr="pareNodes.append([['"+serverIP+"'],['"+serverPORT+"'],['"+cpuCoreIDs+"'],['"+maxMemSize+"'],True])"
													fileAppendWrite("pareNodeList.py", '#### This node was added by paredicma at '+get_datetime()+'\n'+nodeStr)
													pareNodes.append([[serverIP],[serverPORT],[cpuCoreIDs],[maxMemSize],True])
													print (bcolors.OKGREEN +'Slave Node was added to Cluster\n'+nodeStr+bcolors.ENDC)
													funcNodesList()	
												else:
													print (bcolors.FAIL +'!!! Problem occured  while proccesing.. !!!\n'+nodeStr+bcolors.ENDC)
													raw_input(bcolors.BOLD +'\nPress enter to continue...'+bcolors.ENDC)
												
											elif (lower(willbeMasterNode)=='no'):
												willbeSSNode=raw_input(bcolors.BOLD +'\nDo you want to set this node SLAVE for Specific master node (yes/no):'+bcolors.ENDC)
												if (lower(willbeSSNode)=='yes'):
													getMasterNodesID()
													cMasterID=raw_input(bcolors.BOLD +'\nPlease enter master node id :'+bcolors.ENDC)
													if(addSpecificSlaveNode(serverIP,serverPORT,cMasterID)):
														nodeStr="pareNodes.append([['"+serverIP+"'],['"+serverPORT+"'],['"+cpuCoreIDs+"'],['"+maxMemSize+"'],True])"
														fileAppendWrite("pareNodeList.py", '#### This node was added by paredicma at '+get_datetime()+'\n'+nodeStr)
														pareNodes.append([[serverIP],[serverPORT],[cpuCoreIDs],[maxMemSize],True])
														print (bcolors.OKGREEN +'Slave Node was added to Cluster\n'+nodeStr+bcolors.ENDC)
														funcNodesList()	
													else:
														print (bcolors.FAIL +'!!! Problem occured  while proccesing.. !!!\n'+nodeStr+bcolors.ENDC)
														raw_input('\nPress enter to continue...'+bcolors.ENDC)
												elif(lower(willbeSSNode)=='no'):
													if(addSlaveNode(serverIP,serverPORT)):
														nodeStr="pareNodes.append([['"+serverIP+"'],['"+serverPORT+"'],['"+cpuCoreIDs+"'],['"+maxMemSize+"'],True])"
														fileAppendWrite("pareNodeList.py", '#### This node was added by paredicma at '+get_datetime()+'\n'+nodeStr)
														pareNodes.append([[serverIP],[serverPORT],[cpuCoreIDs],[maxMemSize],True])
														print (bcolors.OKGREEN +'Slave Node was added to Cluster\n'+nodeStr+bcolors.ENDC)
														funcNodesList()	
													else:
														print (bcolors.FAIL +'!!! Problem occured  while proccesing.. !!!\n'+nodeStr	+bcolors.ENDC	)
														raw_input(bcolors.BOLD +'\nPress enter to continue...'+bcolors.ENDC)
													
												else:
													print (bcolors.FAIL +'\nYou entered wrong value :'+willbeSSNode+bcolors.ENDC)
											else:
												print (bcolors.FAIL +'\nYou entered wrong value :'+willbeMasterNode+bcolors.ENDC)
												
											
										else:
											print (bcolors.FAIL +'!!! This IP('+serverIP+'):Port('+serverPORT+') is already used by pareNodes config !!!\n Operation canceled !!!'+bcolors.ENDC)
								else:
									print (bcolors.FAIL +'\nYou entered wrong memory size or cpu core id(s)  mem :'+maxMemSize+' cpu core id(s):'+bcolors.ENDC)
							else:
								print (bcolors.FAIL +'\nYou entered wrong Port nunmber:'+serverPORT+bcolors.ENDC)
						else:
							print (bcolors.FAIL +'\nYou entered wrong IP nunmber:'+serverIP+bcolors.ENDC)
					elif(operationType=='2' or lower(operationType)=='del'):
						funcNodesList()	
						delNodeID=raw_input('\nPlease enter node number which you want to delete :')
						if(delNodeID.isdigit()):
							 if( len(pareNodes)>=int(delNodeID)):
								if(delPareNode(delNodeID)):			
									serverIP=pareNodes[int(delNodeID)-1][0][0]
									serverPORT=pareNodes[int(delNodeID)-1][1][0]
									cpuCoreIDs=pareNodes[int(delNodeID)-1][2][0]
									maxMemSize=pareNodes[int(delNodeID)-1][3][0]
									oldVal="pareNodes.append([['"+serverIP+"'],['"+serverPORT+"'],['"+cpuCoreIDs+"'],['"+maxMemSize+"'],True])"
									newVal="pareNodes.append([['"+serverIP+"'],['"+serverPORT+"'],['"+cpuCoreIDs+"'],['"+maxMemSize+"'],False])"
									del pareNodes[int(delNodeID)-1]
									changePareNodeListFile(oldVal,newVal)
								else:
									print ('!!! Problem occured  while proccesing.. !!!\n')
							 else:
								print ('\nYou entered wrong Node nunmber:'+delNodeID)
						else:
							print ('\nYou entered wrong Node nunmber:'+delNodeID)
						raw_input('\nPress enter  to continue...')
					else:
						print (bcolors.FAIL +'!!!You entered wrong value!!! : ' + operationType+bcolors.ENDC)
				elif returnVAl=="2" : 		### Move Slot(s)
					print (bcolors.BOLD +'Move Slot(s)'+bcolors.ENDC)
					nodeNumber=0
					for pareNode in pareNodes:
						nodeIP=pareNode[0][0]
						portNumber=pareNode[1][0]
						nodeNumber=nodeNumber+1
						if ( pareNode[4] ):
							isPing=pingNode(nodeIP,portNumber)
							if (isPing):
								slotInfo(nodeIP,portNumber)
								break
					fromNodeID=raw_input(bcolors.BOLD +'\nPlease enter FROM node ID :'+bcolors.ENDC)
					toNodeID=raw_input(bcolors.BOLD +'\nPlease enter TO node ID :'+bcolors.ENDC)
					numberOfSlots=raw_input(bcolors.BOLD +'\nPlease enter NUMBER of SLOTs :'+bcolors.ENDC)
					if(numberOfSlots.isdigit()):
						if(int(numberOfSlots)<16386):
							reshardCluster(nodeNumber,fromNodeID,toNodeID,numberOfSlots)
							returnVAl=raw_input(bcolors.BOLD +"Operation completed. Press enter to continue..."+bcolors.ENDC)
						else:
							print (bcolors.FAIL +'!!! This is not valid number value (out of range) !!!'+bcolors.ENDC)
					else:
						print (bcolors.FAIL +'!!! This is not valid  value !!!'+bcolors.ENDC)
				elif returnVAl=="3" : 		### Redis Cluster Nodes Version Upgrade
					# pmdStatus,cmdResponse = commands.getstatusoutput(redisConnectCmd(nodeIP,portNumber,' info server | grep  redis_version'))
					# crsRes=cmdResponse.find('redis_version:')
					# redisVersion=cmdResponse[crsRes]
					global redisVersion
					global redisBinaryDir
	#				global redisTarFile
					print (bcolors.BOLD +'Redis Cluster Nodes Version Upgrade'+bcolors.ENDC)
					newTarFile=raw_input(bcolors.BOLD +"\nPlease Enter new Redis tar file name :"+bcolors.ENDC)
					serverList=[]
					noProblem=True
					for pareNode in pareNodes:
						nodeIP=pareNode[0][0]
						if ( pareNode[4] ):
							serverList.append(nodeIP)
					myServers=list(set(serverList))
					if (os.path.isfile(newTarFile) and newTarFile[len(newTarFile)-7:]=='.tar.gz' and lower(newTarFile[:6])=='redis-'):
						newRedisVersion=newTarFile[6:len(newTarFile)-7]
						if (newRedisVersion==redisVersion):
							print (bcolors.WARNING +'!!! New redis version equels to current version !!! Operation canceled. !!!'+bcolors.ENDC)
						else:
							if(compileRedis(newTarFile,newRedisVersion)):		
								for myServer in myServers:
									noProblem=redisNewBinaryCopier(myServer,newRedisVersion)
									if(noProblem==False):
										break
							else:
								print (bcolors.FAIL +' :: There is a problem. While compiling redis !!!'+bcolors.ENDC)
							if(noProblem==True):
								doRestart=raw_input(bcolors.OKGREEN +"\nRedis binary copy procces completed. Do you want to restart redis cluster nodes(yes/no)"+bcolors.ENDC)
								if (lower(doRestart)=='yes'):
									sRisOK=restartAllSlaves(newRedisVersion)
									if (sRisOK):
										mRisOK=restartAllMasters(newRedisVersion)
										if(mRisOK==False):
											myRes=raw_input(bcolors.BOLD +"\nDo you want to try again until all master nodes return OK (yes/no):"+bcolors.ENDC)
											if (lower(myRes)=='yes'):
												while (restartAllMasters(newRedisVersion)==False):
													print (bcolors.BOLD +'The Operation  will be tried again, 1 minute later. Please wait .. '+bcolors.ENDC)
													sleep(60)
												redisBinaryDir=redisBinaryDir.replace('redis-'+redisVersion,'redis-'+newRedisVersion)
												if(changePareConfigFile("redisVersion = '"+redisVersion+"'","redisVersion = '"+newRedisVersion+"'") and changePareConfigFile("redisTarFile = 'redis-"+redisVersion+".tar.gz'","redisTarFile = 'redis-"+newRedisVersion+".tar.gz'")):
													print (bcolors.OKGREEN +' :: Redis version was changed and pareConfig File was updated !!!'+bcolors.ENDC)
													nodeNumber=0
													redisVersion=newRedisVersion
													for pareNode in pareNodes:	
														nodeIP=pareNode[0][0]
														portNumber=pareNode[1][0]
														nodeNumber=nodeNumber+1
														if ( pareNode[4] ):
															print (bcolors.BOLD +'Node Number :'+str(nodeNumber)+'  Node IP :'+nodeIP+'  Node Port :'+portNumber+bcolors.ENDC)
															os.system(redisConnectCmd(nodeIP,portNumber,' info server | grep  redis_version'))											
												else:
													print (bcolors.FAIL +' :: There is a problem. While changing pareConfig File !!!'+bcolors.ENDC)
										else:
											redisBinaryDir=redisBinaryDir.replace('redis-'+redisVersion,'redis-'+newRedisVersion)
											if(changePareConfigFile("redisVersion = '"+redisVersion+"'","redisVersion = '"+newRedisVersion+"'") and changePareConfigFile("redisTarFile = 'redis-"+redisVersion+".tar.gz'","redisTarFile = 'redis-"+newRedisVersion+".tar.gz'")):
												print (bcolors.OKGREEN +' :: Redis version was changed and pareConfig File was updated !!!'+bcolors.ENDC)
												nodeNumber=0
												redisVersion=newRedisVersion
												for pareNode in pareNodes:	
													nodeIP=pareNode[0][0]
													portNumber=pareNode[1][0]
													nodeNumber=nodeNumber+1
													if ( pareNode[4] ):
														print (bcolors.BOLD +'Node Number :'+str(nodeNumber)+'  Node IP :'+nodeIP+'  Node Port :'+portNumber+bcolors.ENDC)
														os.system(redisConnectCmd(nodeIP,portNumber,' info server | grep  redis_version'))											
											else:
												print (bcolors.FAIL +' :: There is a problem. While changing pareConfig File !!!'+bcolors.ENDC)
									else:
										print (bcolors.FAIL +' :: There is a problem. While restarting slave nodes. !!!'+bcolors.ENDC)
								elif (lower(doRestart)=='no'):
									print (bcolors.FAIL +"The procces will end without Restart. You should do manuel restart."+bcolors.ENDC)
								else:
									print (bcolors.FAIL +'!!!You entered wrong value!!! : ' + doRestart	+bcolors.ENDC	)											
					else:
						print (bcolors.FAIL +'!!! You entered wrong file name!!!\n It must be like "redis-***.tar.gz"'+bcolors.ENDC)
					sleep(3)
				elif returnVAl=="4" : 		### Redis Cluster Nodes Version Control
					print (bcolors.BOLD +'Redis Cluster Nodes Version Control'+bcolors.ENDC)
					redisNodesVersionControl()
					returnVAl=raw_input(bcolors.BOLD +"Press enter to continue..."+bcolors.ENDC) 
					sleep(3)				
				elif returnVAl=="5" : 		### Maintain Server
					print (bcolors.BOLD +'Maintain Server\n------------------\n'+bcolors.ENDC)
					funcNodesList()	
					print (bcolors.WARNING +'!!! BE CAREFULL !!! Depend of your configuration, this procces might cause cluster status  FAIL !!!')
					myServerIP=raw_input(bcolors.BOLD +"\nPlease Enter Server IP : "+bcolors.ENDC) 
					print ('Your choise :'+myServerIP	)
					if (validIP(myServerIP)):
						nodeNumber=0
						for pareNode in pareNodes:
							nodeIP=pareNode[0][0]
							if ( nodeIP==myServerIP and  pareNode[4] ):
								portNumber=pareNode[1][0]
								nodeNumber=nodeNumber+1
								stopNode(nodeIP,str(myServerIP),portNumber)
					else:
							print (bcolors.FAIL +'!!!You entered wrong IP!!! : ' + myNodeNum+bcolors.ENDC)
				elif returnVAl=="6" : 		### Migrate data From 
					print (bcolors.WARNING +'!!! This procces will migrate whole data from target non-Clustered redis server !!!'+bcolors.ENDC)
					fromIP=raw_input(bcolors.BOLD +"\nPlease Enter target redis IP addres :"+bcolors.ENDC)
					if (validIP(fromIP)):
						fromPORT=raw_input(bcolors.BOLD +"\nPlease Enter target redis port number :"+bcolors.ENDC)
						fromPWD=raw_input(bcolors.BOLD +"\nPlease Enter target redis password ( If No password, press enter ) :"+bcolors.ENDC)
						if(fromPORT.isdigit()):
	#						targetPWD=raw_input("\nPlease Enter target redis password :")
							nodeNumber=0
							for pareNode in pareNodes:
								nodeIP=pareNode[0][0]
								portNumber=pareNode[1][0]
								nodeNumber=nodeNumber+1
								if ( pareNode[4] ):
									if(isNodeMaster(nodeIP,nodeNumber,portNumber)):
										break
							toIP=pareNodes[nodeNumber-1][0][0]
							toPort=pareNodes[nodeNumber-1][1][0]
							print (bcolors.BOLD +'Migrating procces is starting... ' +bcolors.ENDC)
#							os.system('date')						
							migrateDataFrom(toIP,toPort,fromIP,fromPORT,fromPWD)
#							os.system('date')						
							raw_input(bcolors.OKGREEN +"\n Migration completed. \n Press Enter to continue..."+bcolors.ENDC) 
						else:
							print (bcolors.FAIL +'!!! This is not valid port number !!!'+bcolors.ENDC)
					else:
						print (bcolors.FAIL +'!!! This is not valid IP address !!!'+bcolors.ENDC)
					sleep(3)
				elif returnVAl=="7" : 		### Cluster Load(Slots) Balancer
					print (bcolors.BOLD +'Cluster Slot(load) Balancer'+bcolors.ENDC)
					balanceSt=raw_input(bcolors.BOLD +"Please select balance Strategy\n1 - node base\n2 - memory size base \n :"+bcolors.ENDC)
					balanceStrategy=''
					if (balanceSt=='1'):
						balanceStrategy='nodeBase'									
						maxSlotBarier=raw_input(bcolors.BOLD +"\nPlease Enter max move slot Number per Node ( between 0 - 4000 )(0 means no limit):"+bcolors.ENDC)
						if(maxSlotBarier.isdigit() ):
							if(int(maxSlotBarier)<4001):
								clusterSlotBalanceMapper(balanceStrategy,int(maxSlotBarier))
							else:
								print (bcolors.FAIL +'\n!!! You  entered wrong value !!!'+bcolors.ENDC)
						else:
							print (bcolors.FAIL +'\n!!! You  entered wrong value !!!'+bcolors.ENDC)
					elif(balanceSt=='2'):
						balanceStrategy='memBase'
						maxSlotBarier=raw_input(bcolors.BOLD +"\nPlease Enter max move slot Number ( between 0 - 4000 )(0 means no limit):"+bcolors.ENDC)
						if(maxSlotBarier.isdigit() ):
							if(int(maxSlotBarier)<4001):
								clusterSlotBalanceMapper(balanceStrategy,int(maxSlotBarier))
							else:
								print (bcolors.FAIL +'\n!!! You  entered wrong value !!!'+bcolors.ENDC)
						else:
							print (bcolors.FAIL +'\n!!! You  entered wrong value !!!'+bcolors.ENDC)
						
					else:
						print (bcolors.FAIL +'\n!!! You  entered wrong choice !!!'+bcolors.ENDC	)			
				elif returnVAl=="8" : 		### Not Designated		
					print ("hello man")
				elif returnVAl=="9" : 		### Main Menu
					print (bcolors.BOLD +"your Choise :"+returnVAl+" --- You are going to Main Menu ..."+bcolors.ENDC)
					MenuState=0			
				elif returnVAl=="10" : 		### Exit
					print ("your Choise : "+bcolors.BOLD +returnVAl+bcolors.ENDC)
					print("\n Goodbye") 
					exit()
				else :
					print(bcolors.WARNING +"\n !!! Not Valid Choice! Try again"+bcolors.ENDC)
					sleep(1)
			sleep(1)
		elif ans=="4" :
			MenuState=0
			if(os.path.isfile('paredicma.done')):
				resCluster=raw_input(bcolors.WARNING +"\nRedis cluster is already done. You DO NOT remake cluster. (for force make remove 'paredicma.done' file)"+bcolors.ENDC) 
			else :
				resCluster=raw_input(bcolors.BOLD +" Are you sure to make Redis Cluster (yes/no) ? "+bcolors.ENDC) 
				if (lower(resCluster)=='yes'):
					redisReplicationNumber=raw_input(bcolors.BOLD +"How many replica( slave ) do you want for each master ('0','1','2' ext.) ? "+bcolors.ENDC) 
					if(redisReplicationNumber.isdigit()):
						if((int(redisReplicationNumber)*3)<=len(pareNodes)):
							pareClusterMaker(redisReplicationNumber)
							returnVAl=raw_input(bcolors.BOLD +"Press enter to continue..."+bcolors.ENDC) 
						else:
							print (bcolors.FAIL +"!!! You do NOT have enough nodes to setup this configuration !!!\n please check replication number and pareNodes.py file !!!!"+bcolors.ENDC)
					else:
						print (bcolors.FAIL +'!!! You entered wrong value !!!!'+bcolors.ENDC)
#					os.system('python paredicma.py')
					print (bcolors.OKGREEN +'WELL DONE ;)'+bcolors.ENDC)
			menuMain() 
		elif ans=="5":
			print("\n Goodbye") 
			exit()
		else:
			print(bcolors.WARNING +"\n !!! Not Valid Choice! Try again"+bcolors.ENDC) 		
main()

