import re
from mistletoe import HTMLRenderer, Document
from mistletoe.span_token import SpanToken, RawText, Strikethrough
from mistletoe.block_token import BlockToken, Paragraph
#from mistletoe.parse_context import get_parse_context

# Custom tags for mistletoe
# Ogni volta che find() trova una corrispondenza, il parser crea un'oggetto di questo tipo
# chiamando nel construttore il match_obj generato dal regex in pattern. Cosa faccia quando
# uso un find() personalizzato non so!

class DramaUserTag(SpanToken):
	pattern = re.compile(r"(^|\s|<p>)@(([a-zA-Z0-9_\-]){1,25})")
	def __init__(self, match_obj):
		self.target = match_obj.group(2)


class RedditInternalLink(SpanToken):
	# TODO the original contained backtracing stuff to inhibit the regex if inside <code> et similia tags
	# idk if this will be necessary as in those Elements there's no inner parsing thus this pattern should
	# be evaluated. On the other hand rDrama allows user HTML so idk
	pattern = re.compile(r"(^|\s|<p>)\/?((r|u)\/(\w|-){3,25})")
	def __init__(self, match):
		self.type = match.group(3)
		self.target = match.group(2)


class HoleLink(SpanToken):
	pattern = re.compile(r"(^|\s|<p>)\/?(h\/(\w|-){3,25})")
	def __init__(self, match):
		self.target = match.group(2)


class ImageUrl(SpanToken):
	pattern = re.compile(r"(https:\/\/[\w\-.#&/=\?@%;+,:]{5,250}(\.png|\.jpg|\.jpeg|\.gif|\.webp)(\?[\w\-.#&/=\?@%;+,:]*)?)", flags=re.I)
	def __init__(self, match):
		self.src = match.group(1)
		self.title = ""


class Spoiler(SpanToken):
	'''
	Spoiler tag. I copied it from Strikethrough from mistletoe.span_tokens lmao
	I removed the custom find() method that made some magic for nested exps or some shit
	bc I could't get it to work. FIXME Make it to work.
	'''
	pattern = re.compile(r"(?<!\\)(?:\\\\)*\|\|(.+?)\|\|", re.DOTALL)


class SingleTildeStrikethrough(Strikethrough):
	pattern = re.compile(r"(?<!\\)(?:\\\\)*~(.+?)~", re.DOTALL)
	precedence = 4 # lower priorirty that normal Strike obv


class Emoji(SpanToken):
	pattern = re.compile(r":([!#@]{0,3})([a-zA-Z0-9_\-]+):")
	precedence = 6
	def __init__(self, match):
		self.isBig = match.group(1).find('#') != -1
		self.isMirror = match.group(1).find('!') != -1
		self.isUser = match.group(1).find('@') != -1
		self.isPat = match.group(2).endswith('pat')
		self.name = match.group(2).replace('pat','')
		self.altname = ':' + match.group(1) + match.group(2) + ':'


######################## BLOCK TOKENS #####################################

class GreenText(Paragraph):
	startPattern = re.compile(r"^>([^ ][^\n]*)")

	#def __init__(self, lines):
	#	self.children = (RawText(''.join(lines)),)

	#@classmethod
	#def read(cls, lines):
	#	line_buffer = []
	#	for line in lines:
	#		line_buffer.append(line[1:])
	#	return line_buffer

	@classmethod
	def start(self, line: str):
		return self.startPattern.match(line) is not None


class CommentCommand(BlockToken):
	allowedCommands = ["#fortune", "#8ball", "#factcheck"]

	def __init__(self, lines):
		self.command = CommentCommand._normalize(lines[0])

	@staticmethod
	def _normalize(line: str):
		line = line.replace('\n', '')
		for command in CommentCommand.allowedCommands:
			if line.startswith(command):
				return command
		return None

	@staticmethod
	def start(line: str):
		return CommentCommand._normalize(line) is not None
