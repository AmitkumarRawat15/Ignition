def getServerDetails():
	SystemName = system.tag.readBlocking("[System]Gateway/SystemName")

def getSystemDetails():
	import system.util
	systemList=[]
	tag_paths = [
	    "[System]Gateway/SystemName",
	    "[System]Gateway/UptimeSeconds",
	    "[System]Gateway/Timezone",
	    "[System]Gateway/CurrentDateTime",
	    "[default]Server_Maintenance/Servers/Development" 
	]
	tag_values = system.tag.readBlocking(tag_paths)
	SystemName = tag_values[0].value
	UpTime = tag_values[1].value
	TimeZone = tag_values[2].value
	Current_Date_Time = tag_values[3].value
	Gateway_Address =  tag_values[4].value
	Gateway_Connected =  system.util.getGatewayStatus(str(Gateway_Address))
	systemList = [SystemName, UpTime, TimeZone, Current_Date_Time,Gateway_Address,Gateway_Connected]
	return systemList
	

def getSystemPerformance():
	systemPerformanceList=[]
	tag_paths = [
		    "[System]Gateway/Performance/CPU Usage",
		    "[System]Gateway/Performance/Available Disk Space (MB)",
		    "[System]Gateway/Performance/Disk Utilization",
		    "[System]Gateway/Performance/Max Memory",
		    "[System]Gateway/Performance/Memory Usage",
		    "[System]Gateway/Performance/Memory Utilization"
		]
	tag_values = system.tag.readBlocking(tag_paths)
	CPU_Usage= tag_values[0].value
	Available_Disk_Space = tag_values[1].value
	Disk_Utilisation = tag_values[2].value
	Max_Memory = tag_values[3].value
	Memory_Usage = tag_values[4].value
	Memory_Utilisation = tag_values[5].value
	systemPerformanceList = [CPU_Usage,Available_Disk_Space,Disk_Utilisation,Max_Memory,Memory_Usage,Memory_Utilisation]
	return systemPerformanceList

def Redundancy():
	redundancyList=[]
	tag_paths = [
			    "[System]Gateway/Redundancy/ActivityLevel",
			    "[System]Gateway/Redundancy/Role",
			    "[System]Gateway/Redundancy/IsActive",
			    "[System]Gateway/Redundancy/IsMaster",
			    "[System]Gateway/Redundancy/Connection/PeerId",
			    "[System]Gateway/Redundancy/Connection/IsConnected"
			]
	tag_values = system.tag.readBlocking(tag_paths)
	Activity_Level = tag_values[0].value
	Role = tag_values[1].value
	IsActive = tag_values[2].value 
	IsMaster = tag_values[3].value
	PeerId = tag_values[4].value
	PeerConnected = tag_values[5].value
	redundancyList=[Activity_Level,Role,IsActive,IsMaster,PeerId,PeerConnected]
	return redundancyList
	
def getGatewayVersion():
	import platform	
	gatewayVersionList=[]
	version = system.util.getVersion()
	tag_paths = [
				    "[System]Client/System/FPMIVersion",
				    "[System]Gateway/LicenseState",
				    "[System]Client/System/JavaVersion"
	]
	tag_values = system.tag.readBlocking(tag_paths)
	Version = tag_values[0].value 
	License = tag_values[1].value 
	JavaVersion = platform.java_ver()
	JavaVersion = JavaVersion[0]
	gatewayVersionList=[version,License,JavaVersion]
	return gatewayVersionList

def getGatewayNetworkConnections():
	allServers = system.net.getRemoteServers()
	Headers = ["GatewayNetwork","IsAvailable","LastCommunication"]
	Data = []
	for row in range(len(allServers)):
		server = allServers[row]
		IsAvailable = system.tag.readBlocking("[System]Gateway/Gateway Network/"+str(server)+"/IsAvailable")
		if IsAvailable is not None and len(IsAvailable) > 0:
			if IsAvailable == "true":
				IsAvailable = "Yes"
			elif IsAvailable == "false":
				IsAvailable = "No"
		LastComm = system.tag.readBlocking("[System]Gateway/Gateway Network/"+str(server)+"/LastComm")
		Data.append([server,IsAvailable,LastComm])
	gatewayNetworkConnections = system.dataset.toDataSet(Headers, Data)
	return gatewayNetworkConnections
	
def getOPCServers():
	allOPCServers = system.opc.getServers()
	Headers = ["OPCServer","IsEnabled","IsConnected","State"]
	Data = []
	for row  in range(len(allOPCServers)):
		server = allOPCServers[row]
		IsEnabled =  system.tag.readBlocking("[System]Gateway/OPC/Connections/"+str(server)+"/Enabled")
		IsConnected =  system.tag.readBlocking("[System]Gateway/OPC/Connections/"+str(server)+"/Connected")
		State =  system.tag.readBlocking("[System]Gateway/OPC/Connections/"+str(server)+"/State")
		Data.append([server,IsEnabled,IsConnected,State])
	OPCServers = system.dataset.toDataSet(Headers, Data)
	return OPCServers
			    
def getDesignersinfo():
	session_filter = {"clientType": "designer"}	
	session_info = system.util.getSessionInfo(sessionFilter=session_filter)	
	if session_info is not None:		        
		active_session_count = len(session_info)	
		designers = str(active_session_count)+" "+str("Open")       
	else:	        
		designers = "0"+" "+str("Open")  
	return 	 designers  	  
   
def getPerspectiveinfo():
	sessions = system.perspective.getSessionInfo()
	clientcount=0  
	for session in sessions:
	    	client= session.get("sessionScope")
	    	if client != 'designer':
	    		clientcount=clientcount+1
	Perspectives = str(clientcount)+" "+str("Open") 
	return sessions
	
	

def getDatabaseDetails():
	connections = system.db.getConnections()
	connections=system.dataset.toPyDataSet(connections)
	totalconnected = len(connections)
	active=0
	for row in range(len(connections)):
		connection_status = connections[row]['Status']
		if connection_status:
			  active=active+1
	Database = str(active)+ "/"+ str(totalconnected)+" "+"connected"	
	return connections
									       						 			 			             		 		 			             			  	
def getDevicesinfo():
 	DeviceDataset = system.dataset.toPyDataSet(system.device.listDevices())
 	
 	device = system.device.listDevices()
 	device=system.dataset.toPyDataSet(device)	
 	devicecount=len(device)
 	Devices = str(devicecount)+" "+"enabled"	
 	return DeviceDataset		

def getRemoteServers():
	import system
	from java.net import InetAddress
	from java.util import Date
	
	remote_servers = ["10.198.145.6","10.198.132.23"]
	latency = 0
	def ping_server(server):
	    try:
	        start_time = Date().getTime()
	        inet_address = InetAddress.getByName(server)
	        reachable = inet_address.isReachable(5000)  # Timeout in milliseconds
	        end_time = Date().getTime()
	        latency = int(end_time - start_time) if reachable else None
	        return latency, reachable
	    except Exception as e:
	        return None, False
	
	Address = ["10.198.145.6:8088","10.198.132.23:8088"]
	Server = ["Development","Quality"]
	length_Address = len(Address)
	Headers = ["Server","IsRunning","Latency(ms)"]
	Data = []
	for row in range(length_Address):
		IsRunning =  system.util.getGatewayStatus(str(Address[row]))
		if IsRunning == "RUNNING":
			latency, reachable = ping_server(remote_servers[row])
		Servers = Server[row]
		Data.append([Servers,IsRunning,latency])
	RemoteServers = system.dataset.toDataSet(Headers, Data)
	return RemoteServers

def getModulesStatus():
	Modules = system.util.getModules()
	return Modules
	 	 	 	 		 
def getThreadDump():
	ThreadDump = system.util.threadDump()
	return ThreadDump	 		 
 	 	 		 
 		 
 	
	 
	 
	 		       						 			 			             		 			 			                        
	 	 	 								       						 			 			             		 			 			             
	 	 	 						 			 			             				 			              	 
	 	 						       						 			 			             		 			 			                           
	 	 						       						 			 			             		 			 			                           
						       						 			 			             		 			 			                          
				 			 			             		 			 			                 	
		 			 			             		 			 			                 		 			             
	 			 			             
	 			          			         
	 			          			          			         
	 			          			          			          			          			         
		  		        
       	    	


    

	
	
	
	
	
	