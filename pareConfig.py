from pareNodeList import *
##################PARAMETERS################################
projectName='testProject'
redisDataDir = '/home/hiccup/'+projectName+'/'
redisConfigDir = '/home/hiccup/'+projectName+'/'
redisLogDir = '/home/hiccup/'+projectName+'/'
redisVersion = '5.0.5'
redisTarFile = 'redis-5.0.5.tar.gz'
redisBinaryDir = '/home/hiccup/reBin/redis-'+redisVersion+'/'
dedicateCore = True   ## True/False
doCompile = True
doStartNodes = True
unixSocketDir = '/tmp/'
pidFileDir = '/var/run/'
writePareLogFile = True
pareLogFile = 'paredicma.log'
pareTmpDir = 'temparedicma/'
pareServerIp = '10.0.0.15' ## The server Which runs paredicma-cli.py 
pareOSUser = 'hiccup' ##'hiccup'
rdb = 'on'   ## on/off
rdbValue = 'save 3600 1000\nsave 1800 10000\nsave 600 100000'
aof = 'on'   ## on/off
aofValue = 'appendfsync everysec'
redisCluster = 'on'   ## on/off
#redisClusterRepNum = '1'  ## number of replica for each master
clusterNodeTimeout = 'cluster-node-timeout 5000'
clusterParameters = 'cluster-replica-validity-factor 0\ncluster-migration-barrier 1'
maxMemory = 'on'   ## on/off
redisPwdAuthentication = 'on'   ## on/off
redisPwd = 'my1Laydy7darbanville5*'
redisParameters = '''
daemonize yes
slowlog-log-slower-than 1000
latency-monitor-threshold 100
slowlog-max-len 10
rename-command FLUSHALL "Ahsa51111sMdbuva7_avsvs*1**"
rename-command FLUSHDB "Ahsa111115sMdbuva117_avsvs*1"
'''
