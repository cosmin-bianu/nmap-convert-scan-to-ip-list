from sys import argv
import xml.etree.ElementTree as ET

if len(argv) != 3:
    print('Usage: ./convert.py <nmap-output-xml> <output-file>')

tree = ET.parse(argv[1])

out = open(argv[2], 'w')

root = tree.getroot()

service_filter = ['http', 'https', 'https-alt']

service_name_to_protocol_map = {
    'http':'http',
    'https':'https',
    'https-alt':'https',
    'domain':'dns',
    'ldap':'ldap',
    'ssh':'ssh',
}

for host in root.findall('host'):
    print(host.find('address').attrib['addr'])
    for port in host.find('ports').findall('port'):
        state = port.find('state').attrib['state']
        if state == 'open':
            service_name = port.find('service').attrib['name']
            if service_name in service_filter:
                host_addr = host.find('address').attrib['addr']
                protocol = service_name_to_protocol_map[service_name]
                port_number = port.attrib['portid']
                out.write(f'{protocol}://{host_addr}:{port_number}\n')

out.close()