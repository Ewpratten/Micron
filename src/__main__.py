import sys

if len(sys.argv) < 3:
	print("Incorrect usage of command: diras")
	print("	Please use: diras /path/to/file /output/file")
	exit(1)

with open(sys.argv[1]) as File:
	asm_file = [line.split() for line in File]

class LineBuffer(object):
	def __init__(self):
		self.content = ""
	
	def append(self, text):
		self.content += text
	
	def clear(self):
		self.content = ""

def comment(text):
	if len(sys.argv) >= 4:
		if sys.argv[3] == "--with-comments":
			return text
	else:
		return ""

strdelim = '"'

# Macro Functions:
def macro_print(line):
	text = ""
	
	for word in line[1:]:
		text += word
		text += "_"
	
	text = text[1:len(text) - 2]
	
	output = "movs ["
	output += str(len(text))
	output += ","
	output += str(text.lower())
	output += "] e3"
	output += "\ncall 1"
	
	return output

def macro_display(line):
	command = line[1]
	output = ""
	
	if command == "init":
		output += comment("# Display INIT")
		output += "mov 1 e2"
	elif command == "clear":
		output += comment("# Display CLEAR")
		output += "mov 0 e2"
	elif command == "write":
		output += comment("# Display WRITE")
		output += "mov 2 e2"
	elif command == "cursor":
		if len(line) < 4:
			print("FATAL ERROR: :display cursor called without arguments")
			exit(1)
		output += comment("# Display CURSOR")
		output += "mov "+ line[2] +" e5"
		output += "\nmov "+ line[3] +" e4"
	
	output += "\ncall 1"
	return output

# Macro vars:
macro_identifier = ":"

macros = {
	"print":macro_print,
	"display":macro_display
}

line_buffer = LineBuffer()
output = ""

ismacro = False

for line in asm_file:
	line_buffer.clear()
	for mnemonic in line:
		if mnemonic[1:] in macros and mnemonic[0] == macro_identifier:
			ismacro = True
			line_buffer.clear()
			line_buffer.append(macros[mnemonic[1:]](line))
		else:
			if not ismacro:
				line_buffer.append(mnemonic + " ")
	ismacro = False
	output += line_buffer.content
	output += "\n"

f = open(sys.argv[2], "w")
f.write(output)