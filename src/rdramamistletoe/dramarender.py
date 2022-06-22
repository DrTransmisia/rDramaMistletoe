from .customtags import *

class DramaHTMLRenderer(HTMLRenderer):
	"""
	Generates HTML stuff. Lambda memebers are supposed to be replaced with custom lambdas for the server side application
	The default lambdas should be alright for the client-side stuff.
	"""

	def __init__(self):
		super().__init__(DramaUserTag, RedditInternalLink, HoleLink, ImageUrl, Spoiler, SingleTildeStrikethrough, Emoji, GreenText,
			CommentCommand)

		self.getRandomMarsey = lambda: 'marseyquestionmark'
		self.getEmojiPath = lambda name: f"/e/{name}.webp"
		self.isEmojiValid = lambda name: True
		self.isEmojiRandomGold = lambda marseyCardinality: False

		self.getUserProfilePath = lambda username: f'/@{username}'
		self.getUserProfilePic = lambda username: f'/@{username}/pic'
		self.isUserValid = lambda username: True # TODO alter render accord.ly

		self.taggedUsers = []

		self.commands = []
		self.processCommands = lambda commands: "<span style=\"color: green\">Commands found: " + ' '.join(commands) + "</span>" if len(commands) > 0 else ""


	def render_drama_user_tag(self, token):
		template = ' <a href="{url}"><img class="profile-pic" loading="lazy" src="{pic}" alt="">@{username}</a> '
		target = self.escape_url(token.target)
		return template.format(username=target, pic=self.getUserProfilePic(target), url=self.getUserProfilePath(target))
	
	def render_reddit_internal_link(self, token):
		template = ' <a href="https://old.reddit.com/{inlk}" rel="nofollow noopener noreferrer">{inlk}</a> '
		return template.format(inlk=self.escape_url(token.target))
	
	def render_hole_link(self, token):
		template = ' <a href="/{hole}">/{hole}</a> '
		return template.format(hole=self.escape_url(token.target))
	
	# ACHTUNG! This could break if they change the guts of the library lol
	def render_image_url(self, token):
		return self.render_image(token)
	
	def render_spoiler(self, token: Spoiler):
		template = '<spoiler>{inner}</spoiler>'
		return template.format(inner=self.render_inner(token))
	
	def render_single_tilde_strikethrough(self, token: SingleTildeStrikethrough):
		return self.render_strikethrough(token)
	
	def render_emoji(self, token: Emoji):
		emoji_partial_pat = ' <img loading="lazy" alt="{0}" src="{1}"{2}> '
		emoji_partial = ' <img loading="lazy" data-bs-toggle="tooltip" alt="{0}" title="{0}" src="{1}"{2}> '
		emoji_html = None

		attrs = ''
		if token.isBig:
			attrs += ' b'
		if self.isEmojiRandomGold(0): #TODO COUNT EMOJIS DURING CONSTRUCTION OF PARSING TREE!
			attrs += ' g'

		alt = self.escape_html(token.altname)
		name = self.escape_html(token.name)

		if not self.isEmojiValid(name):
			return alt

		if token.isPat:
			if emoji.startswith('@'):
				#if u := get_user(emoji[1:-3], graceful=True):
				emoji_html = f'<span data-bs-toggle="tooltip" alt="{alt}" title="{alt}"><img src="/assets/images/hand.webp">{emoji_partial_pat.format(alt, self.getUserProfilePic(name), attrs)}</span>'
			else:
				emoji_html = f'<span data-bs-toggle="tooltip" alt="{alt}" title="{alt}"><img src="/assets/images/hand.webp">{emoji_partial_pat.format(alt, self.getEmojiPath(name), attrs)}</span>'
			return emoji_html
		
		emoji_html = emoji_partial.format(alt, self.getEmojiPath(name), attrs)
		return emoji_html
	
	def render_green_text(self, btoken):
		template = "<p class=\"greentext\">{inner}</p>"
		return template.format(inner=self.render_inner(btoken))
	
	def render_comment_command(self, btoken: CommentCommand):
		#if btoken.command is in self.commands:
		self.commands.append(btoken.command)
		return "\n"
	
	def render_document(self, token: Document):
		"""We override the document render fn to add to the bottom the shit"""
		doc = super().render_document(token)
		doc += self.processCommands(self.commands)

		return doc
