import xml_utils as u
import xml_fuzzer as xf
import  xml.etree.ElementTree as et
from pwn import * 

with open("./bin/xml1.txt", "r") as f:
    input = f.read().strip()

# print(input)

xml = et.fromstring(input)

for child in xml.iter():
    # print(child.tag)
    # print(child.text)
    # print(child.items())
    attributes = child.items()
    for a in attributes:
    if u.check_tag(child.tag) == True:
        child.text = u.bytes_replace()
        child.text = u.bits_flip(child.text)
        

# xmlstr = et.tostring(xml).decode()
# print(xmlstr)

# print(u.string_to_binary(""))
# print(u.bits_flip(""))

# p = process("./xml1")
# p.sendline(xmlstr.encode("UTF-8"))
# p.shutdown()
# code = p.poll(block=True)
# p.stdout.close()
# p.stderr.close()
# print(code)

# fuzzer = xf.XML_Fuzzer("./bin/xml1", xmlstr)
# print(fuzzer.check_type())
# print(fuzzer.run())