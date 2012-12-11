__author__ = 'ahawker'

#Term Format:
#|1  |1  |N   |
#|131|Tag|Data|

NEW_FLOAT       = 70        #|1 |8         |
                            #|70|IEEE float|
                            #IEEE float: uint64 (IEEE format)

BIT_BINARY      = 77        #|1 |4  |1   |Len |
                            #|77|Len|Bits|Data|
                            #Len: uint32
                            #Bits: uint8 (number of significant bits in last byte (MSB->LSB))
                            #Data: ??? #TODO

COMPRESSED      = 80        #|1 |4                |N                   |
                            #|80|Uncompressed Size|Zlib-Compressed Data|
                            #Uncompressed Size: uint32
                            #Zlib-Compressed Data: compressed data

SMALL_INTEGER   = 97        #|1 |1  |
                            #|97|Int|
                            #Int: uint8

INTEGER         = 98        #|1 |4  |
                            #|98|Int|
                            #Int: uint32

FLOAT           = 99        #|1 |4           |
                            #|99|Float String|
                            #Float String: "%.20e" format

ATOM            = 100       #|1  |2  |Len     |
                            #|100|Len|AtomName|
                            #Len: uint16
                            #AtomName: Max of 255

REFERENCE       = 101       #|1  |N   |4 |1       |
                            #|101|Node|ID|Creation|
                            #Node: Encoded atom
                            #ID: uint32 (first 18 bits significant)
                            #Creation: uint8 (first 2 bits significant)

PORT            = 102       #|1  |N   |4 |1       |
                            #|102|Node|ID|Creation|
                            #Node: Encoded atom
                            #ID: uint32 (first 18 bits significant)
                            #Creation: uint8 (first 2 bits significant)

PID             = 103       #|1  |N   |4 |4     |1       |
                            #|103|Node|ID|Serial|Creation|
                            #Node: Encoded atom
                            #ID: uint32 (first 15 bits significant)
                            #Serial: ??? #TODO
                            #Creation: uint 8 (first 2 bits significant)

SMALL_TUPLE     = 104       #|1  |1    |N       |
                            #|104|Arity|Elements|
                            #Arity: uint8
                            #Elements: ??? #TODO

LARGE_TUPLE     = 105       #|1  |4    |N       |
                            #|105|Arity|Elements|
                            #Arity: uint32
                            #Elements: ??? #TODO

NIL             = 106       #|1|
                            #|106|
                            #Represent as None or []?? #TODO

STRING          = 107       #|1 |2     |Len       |
                            #107|Length|Characters|
                            #Len: uint16
                            #Characters: ??? #TODO

LIST            = 108       #|1 |4     |        |    |
                            #108|Length|Elements|Tail|
                            #Length: uint32
                            #Elements: ??? #TODO
                            #Tail: ??? #TODO

BINARY          = 109       #|1  |4  |Len |
                            #|109|Len|Data|
                            #Len: uint32
                            #Data: ??? #TODO

SMALL_BIG       = 110       #|1  |1|1   |n            |
                            #|110|n|Sign|d(0)...d(n-1)|
                            #n: uint8
                            #Sign: uint8 (0:pos, 1:neg)
                            #d(0)...d(n-1): ??? #TODO

LARGE_BIG       = 111       #|1  |4|1   |n            |
                            #|111|n|Sign|d(0)...d(n-1)|
                            #n: uint32
                            #Sign: uint8 (0:pos, 1:neg)
                            #d(0)...d(n-1): ??? #TODO

NEW_FUN         = 112       #|1  |4   |1    |16  |4    |4      |N1    |N2      |N3     |N4 |N5       |
                            #|112|Size|Arity|Uniq|Index|NumFree|Module|OldIndex|OldUniq|Pid|Free vars|
                            #Size: uint32 (total bytes inc size field)
                            #Arity: uint8 (arity of function)
                            #Uniq: uint128 (MD5 of Beam file) #TODO
                            #Index: uint32 (func index within module)
                            #NumFree: uint32 (num free variables)
                            #Module: ATOM, SMALL_ATOM or ATOM_CACHE
                            #OldIndex: SMALL_INTEGER or INTEGER
                            #OldUniq: SMALL_INTEGER or INTEGER
                            #Pid: PID
                            #Free vars: NumFree encoded terms

EXPORT          = 113       #|1  |N1    |N2      |N3   |
                            #|113|Module|Function|Arity|
                            #Module: ATOM, SMALL_ATOM or ATOM_CACHE
                            #Function: ATOM, SMALL_ATOM or ATOM_CACHE
                            #Arity: SMALL_INTEGER

NEW_REFERENCE   = 114       #|1  |2  |N   |1       |N'|
                            #|114|Len|Node|Creation|ID|
                            #Len: uint16
                            #Node: Encoded atom
                            #Creation: uint8 (first 2 significant)
                            #ID: 4 * Len uint32 (first 18 significant)

SMALL_ATOM      = 115       #|1  |1  |Len     |
                            #|115|Len|AtomName|
                            #Len: uint8
                            #AtomName: 8 * Len characters

FUN             = 117       #|1  |4      |N1 |N2    |N3   |N4  |N5          |
                            #|117|NumFree|Pid|Module|Index|Uniq|Free vars|
                            #NumFree: uint32
                            #Pid: PID
                            #Module: ATOM, SMALL_ATOM or ATOM_CACHE
                            #Index: SMALL_INTEGER or INTEGER
                            #Uniq: SMALL_INTEGER or INTEGER
                            #Free vars: NumFree encoded terms