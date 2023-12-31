import io
file_path = "./Main.class"

#Числа для определения констант, содержащихся в файлe *.class
CONSTANT_Class = 7
CONSTANT_Fieldref = 9
CONSTANT_Methodref = 10
CONSTANT_InterfaceMethodref = 11
CONSTANT_String = 8
CONSTANT_Integer = 3
CONSTANT_Float = 4
CONSTANT_Long = 5
CONSTANT_Double = 6
CONSTANT_NameAndType = 12
CONSTANT_Utf8 = 1
CONSTANT_MethodHandle = 15
CONSTANT_MethodType = 16
CONSTANT_InvokeDynamic = 18

#Байты для флагов
class_access_flags = [
    ("ACC_PUBLIC", 0x0001), 	 
    ("ACC_FINAL", 0x0010), 	
    ("ACC_SUPER", 0x0020), 	 
    ("ACC_INTERFACE", 0x0200),
    ("ACC_ABSTRACT", 0x0400), 	
    ("ACC_SYNTHETIC", 0x1000), 	 
    ("ACC_ANNOTATION", 0x2000)
]   
methods_access_flags = [
    ("ACC_PUBLIC" , 0x0001),
    ("ACC_PRIVATE", 0x0002),
    ("ACC_PROTECTED", 0x0004),	
    ("ACC_STATIC", 0x0008), 	
    ("ACC_FINAL", 0x0010), 	
    ("ACC_SYNCHRONIZED", 0x0020), 	
    ("ACC_BRIDGE", 0x0040), 	
    ("ACC_VARARGS", 0x0080),	
    ("ACC_NATIVE", 0x0100), 	
    ("ACC_ABSTRACT", 0x0400), 	
    ("ACC_STRICT", 0x0800), 	
    ("ACC_SYNTHETIC", 0x1000) 	
]


def parse_flags(value: int, flags: [(str, int)]) -> [str]:
    return [name for (name, mask) in flags if (value & mask) != 0] 

def parse_attributes(f, count):
    attributes = []
    for i in range(count):
        attribute = {}
        attribute["attribute_name_index"] = parse_u2(f)
        attribute_lenght = parse_u4(f)
        attribute['info'] = f.read(attribute_lenght)
        attributes.append(attribute)   
    return attributes



def parse_u1(f): return int.from_bytes(f.read(1), "big")
def parse_u2(f): return int.from_bytes(f.read(2), "big")
def parse_u4(f): return int.from_bytes(f.read(4), "big")
def parse_uN(f, n): return int.from_bytes(f.read(n), "big")

#Байты в java коде хранятся в big endian

def parse_class_file(file_path):
    """Парсит файл java c расширением .class и складывает их в словарь"""
    with open(file_path, "rb") as f:
        clazz = {}
        clazz['magic'] = hex(parse_u4(f))
        clazz['minor'] = parse_u2(f)
        clazz['major'] = parse_u2(f)
        constant_pool_count = parse_u2(f)
        constant_pool = []
        for i in range(constant_pool_count-1):
            cp_info = {}
            tag = parse_u1(f)
            if tag == CONSTANT_Methodref:
                cp_info['tag'] = 'CONSTANT_Methodref'
                cp_info['class_index'] = parse_u2(f)
                cp_info['name_and_type_index'] = parse_u2(f)
            elif tag == CONSTANT_Class:
                cp_info['tag'] = 'CONSTANT_Class'
                cp_info['name_index'] = parse_u2(f)
            elif tag == CONSTANT_NameAndType:
                cp_info['tag'] = 'CONSTANT_NameAndType'
                cp_info['name_index'] = parse_u2(f)
                cp_info['descriptor_index'] = parse_u2(f)
            elif tag == CONSTANT_Utf8:
                cp_info['tag'] = 'CONSTANT_Utf8'
                length = parse_u2(f)
                cp_info['bytes'] = f.read(length)
            elif tag == CONSTANT_Fieldref:
                cp_info['tag'] = 'CONSTANT_Fieldref'
                cp_info['class_index'] = parse_u2(f)
                cp_info['name_and_type_index'] = parse_u2(f)
            elif tag == CONSTANT_String:
                cp_info['tag'] = 'CONSTANT_String'
                cp_info['string_index'] = parse_u2(f)
            else:
                raise NotImplementedError(f"Unexpected constant tag {tag} in class file {file_path}")
            constant_pool.append(cp_info)
        clazz['constant_pool'] = constant_pool
        clazz['access_flags'] = parse_flags(parse_u2(f), class_access_flags)
        clazz['this_class'] = parse_u2(f)
        clazz['super_class'] = parse_u2(f)
        interfaces_count = parse_u2(f)
        interfaces = []
        for i in range(interfaces_count):
            assert False, "Parsing interfaces is not implemented"
        clazz["interfaces"] = interfaces
        fields_count = parse_u2(f)
        fields = []
        for i in range(fields_count):
            assert False, "Parsing fields is not implemented"
        clazz["fields"] = fields

        methods_count = parse_u2(f)
        methods = []
        for i in range(methods_count):
            method = {}
            method['access_flags'] = parse_flags(parse_u2(f), methods_access_flags)
            method['name_index'] = parse_u2(f)
            method['descriptor_index'] = parse_u2(f)
            attribute_count = parse_u2(f)           
            method['attributes'] = parse_attributes(f, attribute_count)
            methods.append(method)
        clazz["methods"] = methods
        attributes_count = parse_u2(f)
        clazz['attributes'] = parse_attributes(f, attribute_count)
    return clazz

def find_methods_by_name(clazz, name: bytes):
    return [method for method in clazz['methods']
        if clazz['constant_pool'][method['name_index'] - 1]['bytes'] == name ]
def find_attributes_by_name(clazz, attributes, name: bytes):
    return [attrs for attrs in attributes 
        if clazz['constant_pool'][attrs['attribute_name_index'] - 1]['bytes'] == name]

def parse_code_info(info: bytes):
    with io.BytesIO(info) as f:
        code = {}
        code["max_stack"] = parse_u2(f)
        code["max_locals"] = parse_u2(f)
        code_lenght = parse_u4(f)
        code["code"] = f.read(code_lenght)
        exception_table_lenght = parse_u2(f)
        for i in range(exception_table_lenght):
            assert False, "Parsing exception table isn't implemented"
        attrubutes_count = parse_u2(f)
        code['attributes'] = parse_attributes(f, attrubutes_count)
        return code

getstatic_opcode = 0xB2
ldc_opcode = 0x12
invokevirtual_opcode = 0xb6
return_opcode = 0xB1
bipush_opcode = 0x10

def get_name_of_class(clazz, class_index) -> bytes:
    return clazz['constant_pool'][clazz['constant_pool'][class_index - 1]['name_index'] - 1]['bytes']

def get_name_of_member(clazz, name_and_type_index) -> bytes:
    return clazz['constant_pool'][clazz['constant_pool'][name_and_type_index - 1]["name_index"] - 1]['bytes']

def type_of(frame):
    if frame['type'] == 'FakePrintStream':
        return b'java/io/PrintStream'
    else:
        assert False, f"type_of isn't implemented for {frame}"

def execute_code(clazz, code: bytes):
    stack = []
    with io.BytesIO(code) as f:
        while f.tell() < len(code):
            opcode = parse_u1(f)
            # print(hex(opcode), opcode)
            if opcode == getstatic_opcode:
                index = parse_u2(f)
                fieldref = clazz['constant_pool'][index - 1]
                name_of_class = get_name_of_class(clazz, fieldref['class_index'])
                name_of_member = get_name_of_member(clazz, fieldref['name_and_type_index'])
                if name_of_class == b'java/lang/System' and name_of_member == b'out':
                    stack.append({
                    "type": "FakePrintStream"
                    })
                else:
                    assert False, f"Unexpected method {name_of_class}/{name_of_member} in getstatic construction"
            elif opcode == ldc_opcode:
                index = parse_u1(f)
                stack.append({"type": "Constant", "const": clazz['constant_pool'][index - 1]})
            elif opcode == invokevirtual_opcode:
                index = parse_u2(f)
                methodref = clazz['constant_pool'][index - 1]
                name_of_class = get_name_of_class(clazz, methodref['class_index'])
                name_of_member = get_name_of_member(clazz, methodref['name_and_type_index'])
                if name_of_class == b'java/io/PrintStream' and name_of_member == b'println': 
                    n = len(stack)
                    if n < 2:
                        assert False, f"{name_of_class}/{name_of_member} expected 2 arguments, but provided {n}"
                    obj = stack[-2]
                    typ = type_of(obj)
                    if typ != b'java/io/PrintStream':
                        assert False, f"Expected type java/io/PrintStream but got {typ}"
                    arg = stack[-1]
                    if arg['type'] == "Constant": 
                        if arg["const"]["tag"] == "CONSTANT_String":
                            print(clazz['constant_pool'][arg['const']['string_index'] - 1]['bytes'].decode('utf-8'))
                        else:
                            assert False, f"Support for {arg['const']['tag']} is not implemented"
                    elif arg['type'] == "Integer":
                        print(arg["value"])
                    else:
                        assert False, f"Support for {arg['value']} is not implemented"
                else:
                    assert False, f"Unknown method {name_of_class}/{name_of_member} in invokevirtual construction"
            elif opcode == bipush_opcode:
                byte = parse_u1(f)
                stack.append({"type": "Integer", "value": byte})
            elif opcode == return_opcode:
                return
            else:
                assert False, f"Unknown opcode {hex(opcode)}"




clazz = parse_class_file("./Main.class")
[main] = find_methods_by_name(clazz, b'main') #magic construction
[code] = find_attributes_by_name(clazz, main['attributes'], b'Code')
code_attrib = parse_code_info(code['info'])
print(code_attrib['code'])
execute_code(clazz, code_attrib['code'])


#class and superclass
# pp.pprint(clazz["constant_pool"][clazz['constant_pool'][clazz['this_class'] - 1]["name_index"] - 1]['bytes'])
# pp.pprint(clazz["constant_pool"][clazz['constant_pool'][clazz['super_class'] - 1]["name_index"] - 1]['bytes'])
# for method in clazz['methods']:
#     pp.pprint(clazz['constant_pool'][method["name_index"] - 1]) 

