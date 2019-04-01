import os
import sys
from time import *
#from  pareConfig import *
from pareFunc import *
from screenMenu import *
from paredicma import *
def main():
	infoParam=str(sys.argv[1])
	reqValues=set(['used_memory','used_memory_human','used_memory_rss','used_memory_rss_human','used_memory_peak','used_memory_peak_human','used_memory_peak_perc','used_memory_overhead','used_memory_startup','used_memory_dataset','used_memory_dataset_perc','allocator_allocated','allocator_active','allocator_resident','total_system_memory','total_system_memory_human','used_memory_lua','used_memory_lua_human','used_memory_scripts','used_memory_scripts_human','number_of_cached_scripts','maxmemory','maxmemory_human','maxmemory_policy','allocator_frag_ratio','allocator_frag_bytes','allocator_rss_ratio','allocator_rss_bytes','rss_overhead_ratio','rss_overhead_bytes','mem_fragmentation_ratio','mem_fragmentation_bytes','mem_not_counted_for_evict','mem_replication_backlog','mem_clients_slaves','mem_clients_normal','mem_aof_buffer','mem_allocator','active_defrag_running','lazyfree_pending_objects','redis_version','redis_git_sha1','redis_git_dirty','redis_build_id','redis_mode','os','arch_bits','multiplexing_api','atomicvar_api','gcc_version','process_id','run_id','tcp_port','uptime_in_seconds','uptime_in_days','hz','configured_hz','lru_clock','executable','config_file','connected_clients','client_recent_max_input_buffer','client_recent_max_output_buffer','blocked_clients','loading','rdb_changes_since_last_save','rdb_bgsave_in_progress','rdb_last_save_time','rdb_last_bgsave_status','rdb_last_bgsave_time_sec','rdb_current_bgsave_time_sec','rdb_last_cow_size','aof_enabled','aof_rewrite_in_progress','aof_rewrite_scheduled','aof_last_rewrite_time_sec','aof_current_rewrite_time_sec','aof_last_bgrewrite_status','aof_last_write_status','aof_last_cow_size','total_connections_received','total_commands_processed','instantaneous_ops_per_sec','total_net_input_bytes','total_net_output_bytes','instantaneous_input_kbps','instantaneous_output_kbps','rejected_connections','sync_full','sync_partial_ok','sync_partial_err','expired_keys','expired_stale_perc','expired_time_cap_reached_count','evicted_keys','keyspace_hits','keyspace_misses','pubsub_channels','pubsub_patterns','latest_fork_usec','migrate_cached_sockets','slave_expires_tracked_keys','active_defrag_hits','active_defrag_misses','active_defrag_key_hits','active_defrag_key_misses','role','connected_slaves','slave0','master_replid','master_replid2','master_repl_offset','second_repl_offset','repl_backlog_active','repl_backlog_size','repl_backlog_first_byte_offset','repl_backlog_histlen','used_cpu_sys','used_cpu_user','used_cpu_sys_children','used_cpu_user_children','cluster_enabled','db0']) 
	if (infoParam!='' ) and (infoParam in reqValues):
		while(True):
			nodeNumber=0
			infoPar=''
			printTextMaster=''
			printTextSlave=''
			isMaster=False
			for pareNode in pareNodes:
				nodeIP=pareNode[0][0]
				portNumber=pareNode[1][0]
				nodeNumber=nodeNumber+1
				if (pareNode[4]):
					memStatus,memResponse = commands.getstatusoutput(redisConnectCmd(nodeIP,portNumber,' info | grep  -e "'+infoParam+':" '))
					if ( memStatus == 0 ):
						infoPar=(memResponse[len(infoParam)+1:memResponse.find(infoParam+':')-1])
						if (isNodeMaster(nodeIP,nodeNumber,portNumber)):
							isMaster=True
							str(nodeNumber)+'	'+nodeIP+'-( M )			'+portNumber+'		'+str(infoPar)+bcolors.ENDC+'\n'
						else:
							isMaster=False
							str(nodeNumber)+'	'+nodeIP+'-( S )			'+portNumber+'		'+str(infoPar)+bcolors.ENDC+'\n'
						if(isMaster):
							printTextMaster+=bcolors.OKGREEN+str(nodeNumber)+'	'+nodeIP+'-( M )			'+portNumber+'		'+str(infoPar)+bcolors.ENDC+'\n'
						else:
							printTextSlave+=bcolors.OKGREEN+str(nodeNumber)+'	'+nodeIP+'-( S )			'+portNumber+'		'+str(infoPar)+bcolors.ENDC+'\n'
					else :
						print (bcolors.FAIL+'!!! Warning !!!! A problem occurred, while memory usage checking !!! nodeID :'+str(nodeNumber)+' NodeIP:'+nodeIP+' NodePort:'+portNumber+''+bcolors.ENDC)
			os.system("clear")
       	        	print ( bcolors.HEADER+projectName+' Redis Cluster  Memory Usage'+bcolors.ENDC+' ( '+get_datetime()+' )\n-------------------------------------------------------------------------')
        	        print (bcolors.HEADER+'nodeID           NodeIP                           NodePort       '+infoParam+bcolors.ENDC)
			print printTextMaster+bcolors.BOLD+'-------------------------------------------------------------------------------------------------------'+bcolors.ENDC
			print printTextSlave
			print bcolors.BOLD+'-------------------------------------------------------------------------------------------------------'+bcolors.ENDC
			sleep(10)
	else:
		print ('The parameter must be like below')
		print ('------------------------------------------------------------------------------')
		print (reqValues)
main()
