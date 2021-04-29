
import lz4.block
import hashlib
import struct
import sys


class Patch:
	def __init__(self, instrs, patch, offset=0):
		self.data = struct.pack(">%iI" %len(instrs), *instrs)
		self.patch = patch
		self.offset = offset


instrs1 = [
	0xF8031F2A, #MOV W24, WZR
	0x930200F9, #STR X19, [X20]
	0x9BFFFF17, #B ...
	0x480340F9, #LDR X8, [X26]
	0x080140F9, #LDR X8, [X8]
]

instrs2 = [
	0xE00317AA, #MOV X0, X23
	0x21008052, #MOV W1, #1
	0x5F010071, #CMP W10, #0
	0x2201889A  #CSEL X2, X9, X8, EQ
]

patches = [
	Patch(instrs1, 0x1F2003D5, -0x24), #NOP
	Patch(instrs2, 0x2A008052, -0x14)  #MOV W10, #1
]


def u32(data, offs):
	return struct.unpack_from("<I", data, offs)[0]

def get_segment(data, index):
	flags = u32(data, 0xC)
	comp = flags & (1 << index)
	
	offs = u32(data, 0x10 + index * 0x10)
	size = u32(data, 0x18 + index * 0x10)
	fsize = u32(data, 0x60 + 4 * index)
	
	buf = data[offs : offs + fsize]
	if comp:
		buf = lz4.block.decompress(buf, uncompressed_size=size)
	
	assert len(buf) == size
	
	h = hashlib.sha256(buf).digest()
	assert h == data[0xA0 + index * 0x20 : 0xC0 + index * 0x20]
	
	return buf

def generate_patch(data):
	assert data[:4] == b"NSO0"
	
	text = get_segment(data, 0)
	
	for patch in patches:
		if patch.data in text:
			addr = text.index(patch.data) + patch.offset + 0x100
			instruction = patch.patch
			break
	else:
		raise ValueError("Couldn't find place to patch")
	
	patch = struct.pack(">IHI", addr, 4, instruction)
	return b"IPS32" + patch + b"EEOF"

def main():
	if len(sys.argv) != 2:
		print("Usage: python3 generate_patch.py <filename>")
		return
	
	filename = sys.argv[1]
	with open(filename, "rb") as f:
		data = f.read()
	
	patch = generate_patch(data)
	
	module_id = data[0x40:0x60].hex().upper()
	with open("%s.ips" %module_id, "wb") as f:
		f.write(patch)

main()
