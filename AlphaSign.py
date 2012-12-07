#!/usr/bin/env python
#
#       AlphaSign.py
#       Copyright 2009 anescient


import serial
import time

# formatting strings
FONT_5STD = '\x1a\x31'
FONT_5STROKE = '\x1a\x32'
FONT_7SLIM = '\x1a\x33'						# sign default
FONT_7STROKE = '\x1a\x34'
FONT_7SLIMFANCY = '\x1a\x35'
FONT_7STROKEFANCY = '\x1a\x36'
FONT_7SHADOW = '\x1a\x37'
FONT_7WIDESTROKEFANCY = '\x1a\x38'
FONT_7WIDESTROKE = '\x1a\x39'
FONT_7SHADOWFANCY = '\x1a\x3a'
FONT_5WIDE = '\x1a\x3b'
FONT_7WIDE = '\x1a\x3c'
FONT_7WIDEFANCY = '\x1a\x3d'
FONT_5WIDESTROKE = '\x1a\x3e'

COLOR_RED = '\x1c\x31'
COLOR_GREEN = '\x1c\x32'
COLOR_AMBER = '\x1c\x33'
COLOR_DIMRED = '\x1c\x34'
COLOR_DIMGREEN = '\x1c\x35'
COLOR_BROWN = '\x1c\x36'
COLOR_ORANGE = '\x1c\x37'
COLOR_YELLOW = '\x1c\x38'
COLOR_RAINBOW1 = '\x1c\x39'				# gradient
COLOR_RAINBOW2 = '\x1c\x41'				# mixed patches
COLOR_MIX = '\x1c\x42'						# mixed solid characters
COLOR_AUTO = '\x1c\x43'						# sign default

SPEED_1 = '\x15'
SPEED_2 = '\x16'
SPEED_3 = '\x17'
SPEED_4 = '\x18'									# sign default
SPEED_5 = '\x19'

TEXT_NOHOLD = '\x09'							# no delay before next message
TEXT_FIXLEFT = '\x1e\x31'
TEXT_CALLSTRING = '\x10'					# follow this code with a string file label
TEXT_CALLSMALLDOTS = '\x14'				# follow with a smalldots file label
TEXT_CLOCK = '\x13'								# show time
TEXT_NEWLINE = '\x0d'

TEXT_FLASHON = '\x071'
TEXT_FLASHOFF = '\x070'						# text between these two will flash

CHR_BLOCK = '\x7f' # not available in size 5 fonts


# transition effects, used at text loading time, not in-line formatting
# commented modes not available on betabrite 1036
MODE_ROTATE = 'a'
MODE_HOLD = 'b'
MODE_FLASH = 'c'
MODE_ROLLUP = 'e'
MODE_ROLLDOWN = 'f'
MODE_ROLLLEFT = 'g'
MODE_ROLLRIGHT = 'h'
MODE_WIPEUP = 'i'
MODE_WIPEDOWN = 'j'
MODE_WIPELEFT = 'k'
MODE_WIPERIGHT = 'l'
MODE_SCROLL = 'm'
MODE_AUTO = 'o'
#MODE_ROLLIN = 'p'
#MODE_ROLLOUT = 'q'
#MODE_WIPEIN = 'r'
#MODE_WIPEOUT = 's'
MODE_ROTATECOMPRESSED = 't'
#MODE_EXPLODE = 'u'
#MODE_CLOCK = 'v'
MODE_TWINKLE = 'n0'
MODE_SPARKLE = 'n1'
MODE_SNOW = 'n2'
MODE_INTERLOCK = 'n3'
#MODE_SWITCH = 'n4'
#MODE_SLIDE = 'n5'
MODE_SPRAY = 'n6'
MODE_STARBURST = 'n7'
MODE_WELCOME = 'n8'
MODE_SLOTMACHINE = 'n9'
MODE_NEWSFLASH = 'nA'
MODE_TRUMPET = 'nB'
#MODE_CYCLECOLORS = 'nC'
MODE_THANKYOU = 'nS'
MODE_NOSMOKING = 'nU'
MODE_DRINKDRIVE = 'nV'
MODE_FISH = 'nW'
MODE_FIREWORKS = 'nX'
MODE_BALLOONS = 'nY'
MODE_BOMB = 'nZ'

SND_LONGBEEP = '\x30'
SND_3BEEPS = '\x31'

ALPHA_PREAMBLE = '\x00' * 5				# may also be = '\x01' * 5
ALPHA_TYPEALL = 'Z00'							# all sign types, all addresses
ALPHA_SOH = '\x01'								# start of header
ALPHA_STX = '\x02'								# start of text (note: have >100ms delay after STX for nested packets)
ALPHA_ETX = '\x03'								# end of text
ALPHA_EOT = '\x04'								# end of transmission
ALPHA_ESC = '\x1b'								# escape
ALPHA_CR = '\x0d'
ALPHA_LF = '\x0a'

DOTS_MONO = '1000'
DOTS_3COLOR = '2000'
DOTS_8COLOR = '4000'

DOTC_BLACK = '0'
DOTC_RED = '1'
DOTC_GREEN = '2'
DOTC_AMBER = '3'
DOTC_DIMRED = '4'
DOTC_DIMGREEN = '5'
DOTC_BROWN = '6'
DOTC_ORANGE = '7'
DOTC_YELLOW = '8'

textcode = {}
#fonts
textcode[ '<5>' ] = FONT_5STD
textcode[ '<5b>' ] = FONT_5STROKE
textcode[ '<5w>' ] = FONT_5WIDE
textcode[ '<5h>' ] = FONT_5WIDESTROKE
textcode[ '<7>' ] = FONT_7SLIM
textcode[ '<7b>' ] = FONT_7STROKE
textcode[ '<7w>' ] = FONT_7WIDE
textcode[ '<7h>' ] = FONT_7WIDESTROKE
textcode[ '<7s>' ] = FONT_7SHADOW
textcode[ '<7f>' ] = FONT_7STROKEFANCY
textcode[ '<7hf>' ] = FONT_7WIDESTROKEFANCY
#colors
textcode[ '<auto>' ] = COLOR_AUTO
textcode[ '<r>' ] = COLOR_RED
textcode[ '<dr>' ] = COLOR_DIMRED
textcode[ '<g>' ] = COLOR_GREEN
textcode[ '<dg>' ] = COLOR_DIMGREEN
textcode[ '<y>' ] = COLOR_YELLOW
textcode[ '<a>' ] = COLOR_AMBER
textcode[ '<o>' ] = COLOR_ORANGE
textcode[ '<b>' ] = COLOR_BROWN
textcode[ '<mc>' ] = COLOR_MIX
textcode[ '<rb>' ] = COLOR_RAINBOW1
textcode[ '<pc>' ] = COLOR_RAINBOW2
#special characters
textcode[ '<block>' ] = CHR_BLOCK
#etc
textcode[ '<clock>' ] = TEXT_CLOCK
textcode[ '<slow>' ] = SPEED_1
textcode[ '<normal>' ] = SPEED_3
textcode[ '<fast>' ] = SPEED_3
textcode[ '<fastest>' ] = TEXT_NOHOLD
textcode[ '<string>' ] = TEXT_CALLSTRING
textcode[ '<smalldots>' ] = TEXT_CALLSMALLDOTS
textcode[ '<fixleft>' ] = TEXT_FIXLEFT
textcode[ '\n' ] = TEXT_NEWLINE

def encodeText ( s ):
	for code, decode in textcode.iteritems():
		s = s.replace( code, decode )
	return s


class Sign:
	"""interface to BetaBrite model 1036 on serial port"""

	# sign memory must be configured completely before data is loaded
	# MemConfig allows a memory setup to be built incrementally before sending to the sign
	class MemConfig:
		#files_avail set of unused labels
		#files_text { label: configstring including label }
		#files_string
		#files_dots

		def __init__ ( self ):
			self.clear()


		def clear ( self ):
			self.files_avail = set([ chr(c) for c in xrange( 0x20, 0x7f ) if chr(c) not in set('A012345?'+' \x7e') ])
			# exclude labels with any kind of special function
			# also exclude labels that act 'weird' in experimentation
			self.files_text = {}
			self.files_string = {}
			self.files_dots = {}


		def pushText ( self, size = 100 ):
			"""add a text file to the configuration and return the file label, or empty string on failure"""
			if size < 1 or not self.files_avail:
				return ''
			label = self.files_avail.pop()
			self.files_text[ label ] = '{0}AL{1:04X}FFFF'.format( label, size )
			return label


		def pushString ( self, size = 100 ):
			"""add a string file to the configuration and return the file label, or empty string on failure"""
			if size < 1 or not self.files_avail:
				return ''
			label = self.files_avail.pop()
			self.files_string[ label ] = '{0}BL{1:04X}0000'.format( label, size )
			return label


		def pushSmalldots ( self, width, height, format = DOTS_8COLOR ):
			"""add a SMALLDOTS image file to the configuration and return the file label, or empty string on failure"""
			if width < 0 or width > 255 or height < 0 or height > 31 or not self.files_avail:
				return ''
			label = self.files_avail.pop()
			self.files_dots[ label ] = '{0}DL{1:02X}{2:02X}{3}'.format( label, height, width, format )
			return label


		def getSetupString ( self ):
			"""return entire memory configuration string for current state"""
			# the order in which file configs are presented to the sign _is_ relevant
			# apparently they must be
			#   1st: all text files, then
			#   2nd: all dots files, then
			#   3rd: all strings files, then
			#   4th: all counter-text files (?)
			# file labels /should/ be 100% arbitrary
			config = ''
			config += ''.join( s for l, s in self.files_text.iteritems() )
			config += ''.join( s for l, s in self.files_dots.iteritems() )
			config += ''.join( s for l, s in self.files_string.iteritems() )
			return config

	######################################################

	def __init__ ( self, port = 0 ): # port may also be a dev file name
		self.comm = serial.Serial( port, 9600 )
		self.commwait = 0.1 # certain transmissions call for a short delay


	def clearMem ( self ):
		self.sendPacket( 'E$' ) # write special function, setup memory
		time.sleep( self.commwait )

	def setupMem ( self, config = MemConfig() ):
		self.sendPacket( 'E$' + config.getSetupString() )
		time.sleep( self.commwait )


	def sendText ( self, label, msg, mode = MODE_HOLD ):
		"""write a text file"""
		if not label:
			return
		dat = 'A' + label # write text
		if msg and mode:
			dat = dat + ALPHA_ESC + '0' # display position, ignored on 213C
			dat = dat + mode + msg
		self.sendPacket( dat )
	
	def sendTextPriority ( self, msg = '', mode = MODE_HOLD ):
		self.sendText( '0', msg[ : 125 ], mode )

	def getText ( self, label = '0', stripmode = True ):
		self.sendPacket( 'B' + label ) # read text
		txt = self.recvPacket()
		if not txt.startswith( 'A' + label ):
			return ''
		txt = txt[ 2: ] # strip type/label
		if stripmode and txt[ 0 ] == ALPHA_ESC:
			txt = txt[ 2: ] # strip ESC and disp. pos.
			if txt[ 0 ] == 'n': # special mode
				txt = txt[ 2: ] # strip special mode
			else:
				txt = txt[ 1: ] # strip normal mode
		return txt


	def sendString ( self, label, msg ):
		"""write a string file"""
		self.sendPacket( 'G' + label + msg )


	def sendSmalldots ( self, label, rows ):
		"""rows is a list of strings"""
		dat = 'I{0}{1:02X}{2:02X}'.format( label, len( rows ), len( rows[0] ) )
		for row in rows:
			dat = dat + row + ALPHA_CR
		self.sendPacket( dat )

	def getSmalldots ( self, label ):
		"""returns the format sendSmalldots accepts"""
		self.sendPacket( 'J' + label )
		dots = self.recvPacket()
		if not dots.startswith( 'I' + label ):
			return []
		dots = dots[ 2: ] # strip type/label
		if len( dots ) < 4:
			return []
		height = int( dots[ 0:2 ], 16 )
		width = int( dots[ 2:4 ], 16 )
		dots = dots[ 4: ] # strip dimensions
		dots = dots.rstrip( ALPHA_CR )
		rows = dots.split( ALPHA_CR )
		return rows


	def setSequence ( self, sequence = 'a' ):
		"""set message display sequence, sequence is a string of file labels"""
		self.sendPacket( 'E.SL' + sequence ) # write special function, run in order, locked


	def setClock ( self, settime = '' ):
		"""# time format is 'HHMM', 24 hour format, or omit to use current system time"""
		if len( settime ) != 4:
			settime = time.strftime( '%H%M', time.localtime() )
		self.sendPacket( 'E ' + settime )

	def getClock ( self ):
		"""# time format is 'HHMM', 24 hour format"""
		dat = self.getSpecialFunc( ' ' )
		if len( dat ) != 4:
			return ''
		return dat


	def getMeminfo ( self ):
		"""query sign, return tuple describing memory (bytestotal, bytesfree)"""
		meminfo = self.getSpecialFunc( '#' )
		if len( meminfo ) != 9:
			return ( 0, 0 )
		return ( int( meminfo[0:4], 16 ), int( meminfo[5:9], 16 ) )


	def enableSpeaker ( self ):
		self.sendPacket( 'E!00' )
		self.sendPacket( 'E(A' )

	def disableSpeaker ( self ):
		self.sendPacket( 'E!FF' )
		self.sendPacket( 'E(B' )

	def beep ( self, type = SND_LONGBEEP ):
		self.sendPacket( 'E(' + type )


	def sendPacket ( self, contents = '' ):
		if self.commwait > 0 and contents.startswith( 'I' ): # sending smalldots
			self.comm.write( ALPHA_PREAMBLE + ALPHA_SOH + ALPHA_TYPEALL + ALPHA_STX + contents[ : 5 ] )
			time.sleep( self.commwait )
			self.comm.write( contents[ 5 : ] + ALPHA_EOT )
		else:
			self.comm.write( ALPHA_PREAMBLE + ALPHA_SOH + ALPHA_TYPEALL + ALPHA_STX + contents + ALPHA_EOT )
		time.sleep( self.commwait )


	def recvPacket ( self ):
		self.comm.timeout = 1
		got = ''
		while True:
			c = self.comm.read()
			got += c
			if not c or c == ALPHA_EOT:
				break
		
		leadin = ALPHA_SOH + '000' + ALPHA_STX
		leadini = got.find( leadin )
		if leadini == -1:
			return ''
		endi = got.find( ALPHA_ETX, leadini + len( leadin ) )
		if endi == -1:
			return ''
		return got[ leadini + len( leadin ) : endi ]


	def getSpecialFunc ( self, specialfunc ):
		self.sendPacket( 'F' + specialfunc )
		dat = self.recvPacket()
		if not dat.startswith( 'E' + specialfunc ):
			return ''
		return dat[ 1 + len( specialfunc ) : ]
