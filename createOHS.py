def createComp(csvLoc,domainHome):

    file = open(csvLoc)
    lines = filter(None, [line.rstrip() for line in file])
	
    for line in lines:
      	items = line.split(',')
      	items = [item.strip() for item in items]
      	(compName,admin,proxy,ssl,serverName) = items

      	adminHost = admin.split(':')[0]
      	adminPort = admin.split(':')[1]
      	proxyHost = proxy.split(':')[0]
      	proxyPort = proxy.split(':')[1]
      	sslHost = ssl.split(':')[0]
      	sslPort = ssl.split(':')[1]

    	cd('/')
    	create(compName, 'SystemComponent') #Proxy for ohs2: Name=ohs2, Type=SystemComponent
        print('-- Create component OHS : ' + compName)
    	cd('/SystemComponent/' + compName)
    	cmo.setComponentType('OHS')
    	set('Machine', 'localmachine')
    	cd('/OHS/' + compName)
    	cmo.setAdminHost(adminHost)
    	cmo.setAdminPort(adminPort)
    	cmo.setListenAddress(proxyHost)
    	cmo.setListenPort(proxyPort)
    	cmo.setSSLListenPort(sslPort)
    	cmo.setServerName(serverName)

    cd('/')
    delete('ohs1','SystemComponent') 
    writeDomain(domainHome)


def main():
    import sys, traceback, os, datetime
    from java.io import FileInputStream
    
    propInputStream = FileInputStream(sys.argv[1])
    configProps = Properties()
    configProps.load(propInputStream)

    mwHome = configProps.get("mwHome")
    domainHome = configProps.get("domainHome")
    domainName = configProps.get("domainName")
    nodeManagerUsername = configProps.get("nodeManagerUsername")
    nodeManagerPassword = configProps.get("nodeManagerPassword")
    nodemanagerHome = configProps.get("nodeManagerHome")
    nodeManagerHost = configProps.get("nodeManagerHost")
    nodeManagerPort = configProps.get("nodeManagerPort")
    nodeManagerMode = configProps.get("nodeManagerMode")
    jdkHome = configProps.get("jdkHome")
    csvLoc = configProps.get("csvLoc")


    readTemplate(mwHome +'/wlserver/common/templates/wls/base_standalone.jar')
    addTemplate(mwHome +'/ohs/common/templates/wls/ohs_standalone_template.jar')

    cd('/')

    create(domainName, 'SecurityConfiguration')
    print('== Creating domain : ' + domainName)

    cd('SecurityConfiguration/' + domainName)

    set('NodeManagerUsername', nodeManagerUsername)
    print('== Creating NodeManager User : ' + nodeManagerUsername)

    set('NodeManagerPasswordEncrypted', nodeManagerPassword)
    print('== Inserting Nodemanager Pass')
	
    setOption('NodeManagerType', 'CustomLocationNodeManager')
    print('== Set NM Type ')

    setOption('NodeManagerHome', str(nodemanagerHome))
    print('== Set NM Location : ' + str(nodemanagerHome))
	
    setOption('JavaHome', jdkHome )
    print('== jdk Home')

    cd('/Machines/localmachine/NodeManager/localmachine')
    cmo.setListenAddress(nodeManagerHost);
    cmo.setListenPort(int(nodeManagerPort));
    cmo.setNMType(nodeManagerMode);

    createComp(csvLoc,domainHome)


main()
