import os
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def menuMon():  ## menuManagger
	os.system("clear")
	currentMenu='menuMake'
	print (	bcolors.HEADER+'''
	PAREDICMON - REDIS CLUSTER MONITOR
	------------------------------------------------'''+bcolors.ENDC)
	print (bcolors.BOLD+'	  1 - Ping  Node(s)    	        '+bcolors.ENDC)
	print (bcolors.BOLD+'	  2 - List Nodes        		'+bcolors.ENDC)
	print (bcolors.BOLD+'	  3 - node(s) Info     			'+bcolors.ENDC)
	print (bcolors.BOLD+'	  4 - Server Info            	'+bcolors.ENDC)
	print (bcolors.BOLD+'	  5 - Slots Info                '+bcolors.ENDC)
	print (bcolors.BOLD+'	  6 - Cluster State             '+bcolors.ENDC)
	print (bcolors.BOLD+'	  7 - Show Memory Usage         '+bcolors.ENDC)
	print (bcolors.BOLD+'	  8 - Not Designated            '+bcolors.ENDC)
	print (bcolors.BOLD+'	  9 - Main Menu                 '+bcolors.ENDC)	
	print (bcolors.BOLD+'	 10 - Exit                      '+bcolors.ENDC)
	print (bcolors.HEADER+'''
	------------------------------------------------'''+ bcolors.ENDC)
def menuMan():  ## menuMonitor
	os.system("clear")
	currentMenu='menuMake'
	print (	bcolors.HEADER+'''
	PAREDICMAN - REDIS CLUSTER MANAGER
	------------------------------------------------'''+bcolors.ENDC)
	print (bcolors.BOLD+'	  1 - Start/Stop/Restart Redis Node     		'+ bcolors.ENDC)
	print (bcolors.BOLD+'	  2 - Switch Master/Slave Nodes					'+ bcolors.ENDC)
	print (bcolors.BOLD+'	  3 - Change Redis Configuration Parameter		'+ bcolors.ENDC)
	print (bcolors.BOLD+'	  4 - Save Redis Configuration to redis.conf  	'+ bcolors.ENDC)
	print (bcolors.BOLD+'	  5 - Rolling Restart   	            		'+ bcolors.ENDC)
	print (bcolors.BOLD+'	  6 - Command for all nodes			    		'+ bcolors.ENDC)	
	print (bcolors.BOLD+'	  7 - Not Designated            '+ bcolors.ENDC)
	print (bcolors.BOLD+'	  8 - Not Designated            '+ bcolors.ENDC)
	print (bcolors.BOLD+'	  9 - Main Menu                 '+ bcolors.ENDC)	
	print (bcolors.BOLD+'	 10 - Exit                      '+ bcolors.ENDC)
	print (bcolors.HEADER+'''
	------------------------------------------------'''+ bcolors.ENDC)
def menuMum():  ## menuMonitor
	os.system("clear")
	currentMenu='menuMake'
	print (	bcolors.HEADER+'''
	PAREDICMUM - REDIS CLUSTER MIGRATION&UPGRADE&MAINTENANCE
	------------------------------------------------'''+bcolors.ENDC)
	print (bcolors.BOLD+'	  1 - Add/Delete Redis Node        				'+ bcolors.ENDC)
	print (bcolors.BOLD+'	  2 - Move Slot(s)       						'+ bcolors.ENDC)
	print (bcolors.BOLD+'	  3 - Redis Cluster Nodes Version Upgrade 		'+ bcolors.ENDC)
	print (bcolors.BOLD+'	  4 - Redis Cluster Nodes Version Control		'+ bcolors.ENDC)
	print (bcolors.BOLD+'	  5 - Maintain Server				    		'+ bcolors.ENDC)	
	print (bcolors.BOLD+'	  6 - Migrate Data From Remote Redis			'+ bcolors.ENDC)	
	print (bcolors.BOLD+'	  7 - Cluster Slot(load) Balancer			    '+ bcolors.ENDC)
	print (bcolors.BOLD+'	  8 - Not Designated    					    '+ bcolors.ENDC)
	print (bcolors.BOLD+'	  9 - Main Menu                 '+ bcolors.ENDC)	
	print (bcolors.BOLD+'	 10 - Exit                      '+ bcolors.ENDC)
	print (bcolors.HEADER+'''
	------------------------------------------------'''+ bcolors.ENDC)
def menuMain():
	os.system("clear")
	currentMenu='menuMain'
	if(os.path.isfile('paredicma.done')):
		print (bcolors.HEADER+'''
	PAREDICMA CLI (Python Automatic REDIs Cluster MAker)                
	------------------------------------------------'''+ bcolors.ENDC)
		print (bcolors.BOLD+'	1 - Redis Cluster Monitor - ( paredicmon ) '+ bcolors.ENDC)
		print (bcolors.BOLD+'	2 - Redis Cluster Manager - ( paredicman ) '+ bcolors.ENDC)
		print (bcolors.BOLD+'	3 - Redis Cluster Upgrade & Migration & Maintenance - ( paredicmum ) '+ bcolors.ENDC)
		print (bcolors.WARNING+'	NAP - Redis Cluster Maker - Already Done - ( paredicma  ) '+ bcolors.ENDC)
		print (bcolors.BOLD+'	5 - Exit                  								   '+ bcolors.ENDC)
		print (bcolors.HEADER+'''
	------------------------------------------------'''+ bcolors.ENDC)
	else :
		print (bcolors.HEADER+'''
	PAREDICMA CLI (Python Automatic REDIs Cluster MAker)
	------------------------------------------------'''+ bcolors.ENDC)
		print (bcolors.WARNING+'	NAP - Redis Cluster Monitor - ( paredicmon ) '+ bcolors.ENDC)
		print (bcolors.WARNING+'	NAP - Redis Cluster Manager - ( paredicman ) '+ bcolors.ENDC)
		print (bcolors.WARNING+'	NAP - Redis Cluster Upgrade&Migration&Maintenance - ( paredicmum ) '+ bcolors.ENDC)
		print (bcolors.BOLD+'	4 - Redis Cluster Maker - ( paredicma  ) '+ bcolors.ENDC)
		print (bcolors.BOLD+'	5 - Exit											                '+ bcolors.ENDC)
		print (bcolors.HEADER+'''
	------------------------------------------------'''+ bcolors.ENDC)

		