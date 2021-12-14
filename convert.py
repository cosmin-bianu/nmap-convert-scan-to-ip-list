from sys import argv
import xml.etree.ElementTree as ET

if len(argv) != 3:
    print('Usage: ./convert.py <nmap-output-xml> <output-file>')

tree = ET.parse(argv[1])

out = open(argv[2], 'w')

root = tree.getroot()

service_filter = ['http', 'https']

for host in root.findall('host'):
    for port in host.find('ports').findall('port'):
        service_name = port.find('service').attrib['name']
        if service_name in service_filter:
            host_addr = host.find('address').attrib['addr']
            port_number = port.attrib['portid']
            out.write(f'{service_name}://{host_addr}:{port_number}\n')

out.close()