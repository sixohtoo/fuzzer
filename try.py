from plistlib import FMT_BINARY
import xml_utils as u
import xml_fuzzer as xf
import  xml.etree.ElementTree as et
from pwn import * 
import subprocess
import enum
import time

# with open("./bin/xml1.txt", "r") as f:
#     input = f.read().strip()
with open("./try3.txt", "r") as f:
    input = f.read().strip()

# print(input)
with open("trybad.txt", "w") as f:
    f.write(input)

xml = et.fromstring(input)

# dom_maniupulated = False
# rem = False
# attributes = []
# for child in xml.iter():
    # print(child.tag)
    # print(child.text)
    # print(child.items())
    # print(child.attrib)
    # element = random.choice(child[:])
    # #     # print(c)
    # if not rem:
    #     child.remove(element)
    #     rem = True
    #     break
    # attributes = child.items()
    # attributes.append(child.items())
# print(attributes)

    # for a in attributes:
    # print(attributes)
# a = random.choice(attributes)
# print(a)
# if len(a) > 0:
#     for child in xml.iter():
#         try:
#             child.attrib.pop(a[0][0])
#         except KeyError:
#             pass
    

        # if not u.check_tag(child.tag):
    #         # child.text = "%s"
    #         # for a in attributes:
    #         child.set(a[0], "%s")
            # child.text = u.bits_flip(child.text)
    # p = random.randint(0, 100)
    # i = 0
    # if p < 25:
    #     new_attrib = f"_new_attrib_{i}"
    #     new_text = f"#new_text_{i}"
    #     child.set(new_attrib, new_text)
    #     i += 1
    # dom_chance  = random.randint(0, 100)
    # dom_maniupulated = False
    # if not dom_maniupulated:
    # # # #     if dom_chance < 20:
    #     if(child.tag != 'root' and child.tag != 'html' and child.tag != 'head' and child.tag != 'tail' and child.tag != 'link' and child.tag != 'a' and child.tag != 'script' and child.tag != 'h1' and child.tag != 'h2' and child.tag != 'h3' and child.tag != 'h4' and child.tag != 'h5' and child.tag != 'h6' and child.tag != 'h7'):
    #         if(child.get('class') != 'no_add'):    
    #             #can manipulate dom
    #             elem_rule = DIV_NO_ADD
    # #             # element = ET.Element(elem_rule[0])
    # #             # element.set('class', elem_rule[1])
    # #             # element.text = elem_rule[2]
    #             element = et.fromstring(elem_rule)
    #             child.append(element)
    #             dom_maniupulated = True

xmlstr = et.tostring(xml).decode()
# print(xmlstr)
# print(len(xmlstr.encode("UTF-8")))

# # print(u.string_to_binary(""))
# # print(u.bits_flip("")

p = process("./bin/xml3", timeout=1.0)
p.sendline(xmlstr.encode("UTF-8"))
# pause()
p.shutdown()
code = p.poll(block=True)
p.stdout.close()
p.stderr.close()
print(code)

# fuzzer = xf.XML_Fuzzer("./bin/xml2", xmlstr)
# print(fuzzer.check_type())
# print(fuzzer.run())
# res = subprocess.run("./bin/xml1", 
#                       input=xmlstr, 
#                       stdout=subprocess.PIPE, 
#                       stderr=subprocess.PIPE,
#                       universal_newlines=True)
                      
# print(res,  res.returncode)