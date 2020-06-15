

mwHome='/bcaproxy/bin/owt/12.2.1.4'
domainHome='/bcaproxy/owt/proxy/12.2.1.4/lab_script'
domainName='lab_script'
nodeManagerUsername='nodemanager'
nodeManagerPassword='node123#'
nodemanagerHome='/bcaproxy/owt/proxy/12.2.1.4/lab_script/nodemanager'
nodeManagerHost='192.168.43.21'
nodeManagerPort='21200'
nodeManagerMode='Plain'
jdkHome='/bcaproxy/bin/jvm/jdk1.8.0_241'

readTemplate(mwHome +'/wlserver/common/templates/wls/base_standalone.jar')
addTemplate(mwHome +'/ohs/common/templates/wls/ohs_standalone_template.jar')
#addTemplate(mwHome + '/bcaproxy/owt/proxy/12.2.1.4/lab_script/lab_script_template.jar')

cd('/')

create(domainName, 'SecurityConfiguration')
print('== Creating domain : ' + domainName)

cd('SecurityConfiguration/' + domainName)

set('NodeManagerUsername', nodeManagerUsername)
print('== Creating NodeManager User : ' + nodeManagerUsername)

set('NodeManagerPasswordEncrypted',nodeManagerPassword)
print('== Inserting Nodemanager Pass')

setOption('NodeManagerType', 'CustomLocationNodeManager');
print('== Set NM Type ')

setOption('NodeManagerHome', nodemanagerHome);
print('== Set NM Location : ' + nodemanagerHome)

setOption('JavaHome', jdkHome )
print('== jdk Home')

cd('/Machines/localmachine/NodeManager/localmachine')
cmo.setListenAddress(nodeManagerHost);
cmo.setListenPort(int(nodeManagerPort));
cmo.setNMType(nodeManagerMode);

cd('/')
create('ohs2', 'SystemComponent') #Proxy for ohs2: Name=ohs2, Type=SystemComponent
cd('/SystemComponent/ohs2')
cmo.setComponentType('OHS')
set('Machine', 'localmachine')
cd('/OHS/ohs2')
cmo.setAdminHost('192.168.43.21')
cmo.setAdminPort('5000')
cmo.setListenAddress('192.168.43.21')
cmo.setListenPort('7778')
cmo.setSSLListenPort('4444')
cmo.setServerName('http://192.168.43.21:7778')
delete('ohs1','SystemComponent') 
writeDomain(domainHome)
exit()

##> ohs_createInstance(instanceName='ohs1', machine='localmachine', '21200', [sslPort=XXXX], [adminPort=XXXX]) 
##readTemplate('/bcaproxy/bin/owt/12.2.1.4/wlserver/common/templates/wls/base_standalone.jar')
