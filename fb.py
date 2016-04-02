import colorama, re
from sys import stdout

# This whole module is a dirty hack so that I don't have to
# Rewrite the output code in catan.py :P

# Special characters
ALPHA       = chr(0)

# TermBuffer color codes
F_FLAG      = 0x1000
F_MASK      = 0x000F
F_BLACK     = 0x1001
F_BLUE      = 0x1002
F_CYAN      = 0x1003
F_GREEN     = 0x1004
F_MAGENTA   = 0x1005
F_RED       = 0x1006
F_RESET     = 0x1007
F_WHITE     = 0x1008
F_YELLOW    = 0x1009

B_FLAG      = 0x2000
B_MASK      = 0x00F0
B_BLACK     = 0x2010
B_BLUE      = 0x2020
B_CYAN      = 0x2030
B_GREEN     = 0x2040
B_MAGENTA   = 0x2050
B_RED       = 0x2060
B_RESET     = 0x2070
B_WHITE     = 0x2080
B_YELLOW    = 0x2090

FB_RESET    = F_RESET | B_RESET

BRIGHT_ON   = 0x0100
BRIGHT_OFF  = 0x0200
BRIGHT_MASK = BRIGHT_ON | BRIGHT_OFF

# Mapping TermBuffer codes to terminal codes
TERM_CODES = {
  F_BLACK   & F_MASK: colorama.Fore.BLACK
, F_BLUE    & F_MASK: colorama.Fore.BLUE
, F_CYAN    & F_MASK: colorama.Fore.CYAN
, F_GREEN   & F_MASK: colorama.Fore.GREEN
, F_MAGENTA & F_MASK: colorama.Fore.MAGENTA
, F_RED     & F_MASK: colorama.Fore.RED
, F_RESET   & F_MASK: colorama.Fore.RESET
, F_WHITE   & F_MASK: colorama.Fore.WHITE
, F_YELLOW  & F_MASK: colorama.Fore.YELLOW

, B_BLACK   & B_MASK: colorama.Back.BLACK
, B_BLUE    & B_MASK: colorama.Back.BLUE
, B_CYAN    & B_MASK: colorama.Back.CYAN
, B_GREEN   & B_MASK: colorama.Back.GREEN
, B_MAGENTA & B_MASK: colorama.Back.MAGENTA
, B_RED     & B_MASK: colorama.Back.RED
, B_RESET   & B_MASK: colorama.Back.RESET
, B_WHITE   & B_MASK: colorama.Back.WHITE
, B_YELLOW  & B_MASK: colorama.Back.YELLOW

, BRIGHT_ON         : colorama.Style.BRIGHT
, BRIGHT_OFF        : colorama.Style.NORMAL
}

class TermBuffer:
  def __init__(self, w, h):
    self.w = w
    self.h = h
    self.char = [ ' ' ] * w * h # TODO change back to alpha
    self.mode = [ (F_RESET | B_RESET) & (F_MASK | B_MASK) ] * w * h
    self.cmode = 0

  def write(self, x, y, *args):
    w = self.w
    h = self.h
    char = self.char
    mode = self.mode
    cmode = mode[y * w + x]
    for arg in args:
      if type(arg) is str:
        for c in arg:
          i = y * w + x
          if c == '\n':
            x = w
          else:
            char[i] = c
            mode[i] = cmode
            x += 1
          if x >= w:
            x = 0
            y += 1
            if y >= h:
              y = 0
      elif type(arg) == int:
        if arg & F_FLAG:
          cmode = cmode & ~F_MASK | (arg & F_MASK)
        if arg & B_FLAG:
          cmode = cmode & ~B_MASK | (arg & B_MASK)
        if arg & BRIGHT_MASK:
          cmode = cmode & ~BRIGHT_MASK | (arg & BRIGHT_MASK)
    self.cmode = cmode
    return x, y

  def printout(self):
    char = self.char
    mode = self.mode
    cmode = -1 # no such mode
    dbg = ''
    #for y in xrange(7,8):
    for y in xrange(self.h):
      begin_row = y * self.w
      #for x in xrange(10, 30):
      for x in xrange(self.w):
        index = begin_row + x
        nmode = mode[index]
        if cmode != nmode:
          f = nmode & F_MASK
          if cmode & F_MASK != f:
            stdout.write(TERM_CODES[f])
            dbg += '%04x -> %s ' % (f, repr(TERM_CODES[f]))
          b = nmode & B_MASK
          if cmode & B_MASK != b:
            stdout.write(TERM_CODES[b])
            dbg += '%04x -> %s ' % (b, repr(TERM_CODES[b]))
          B = nmode & BRIGHT_MASK
          if cmode & BRIGHT_MASK != B:
            stdout.write(TERM_CODES[B if B == BRIGHT_ON else BRIGHT_OFF])
            dbg += '%04x -> %s ' % (B, repr( TERM_CODES[B if B == BRIGHT_ON else BRIGHT_OFF] ))
          cmode = nmode
        stdout.write(char[index])
        dbg += '%s ' % repr(char[index])
      stdout.write('\n')
    #for y in xrange(0, self.h):
    #print 'dbg', dbg
    #print 'memory', ' '.join(map(lambda x: '%04x %c' % (x[0],x[1]), zip(mode[y*self.w : (y+1)*self.w], char[y*self.w : (y+1)*self.w])))

  def cursor(self, pos=(0,0)):
    return TermCursor(self, pos)

colorama2termbufMap = {
  colorama.Fore.BLACK   : F_BLACK
, colorama.Fore.BLUE    : F_BLUE
, colorama.Fore.CYAN    : F_CYAN
, colorama.Fore.GREEN   : F_GREEN
, colorama.Fore.MAGENTA : F_MAGENTA
, colorama.Fore.RED     : F_RED
, colorama.Fore.RESET   : F_RESET
, colorama.Fore.WHITE   : F_WHITE
, colorama.Fore.YELLOW  : F_YELLOW

, colorama.Back.BLACK   : B_BLACK
, colorama.Back.BLUE    : B_BLUE
, colorama.Back.CYAN    : B_CYAN
, colorama.Back.GREEN   : B_GREEN
, colorama.Back.MAGENTA : B_MAGENTA
, colorama.Back.RED     : B_RED
, colorama.Back.RESET   : B_RESET
, colorama.Back.WHITE   : B_WHITE
, colorama.Back.YELLOW  : B_YELLOW

, colorama.Style.BRIGHT : BRIGHT_ON
, colorama.Style.NORMAL : BRIGHT_OFF
}

class TermCursor:
  def __init__(self, tb, pos=(0,0)):
    self.tb = tb
    self.pos = pos
    self.cmode = 0
  def write(self, *args):
    self.pos = self.tb.write(self.pos[0], self.pos[1], *args)
  def writec(self, s):
    args = map(lambda m: colorama2termbufMap[m[0]] if m[0] else m[1],
      re.findall('(\x1b\\[[^m]*m)|([^\x1b]+)', s))
    # XXX re-add args.insert(0, self.cmode)
    self.write(*args)
    #print 'writec:', map(lambda x:'%04x'%x if type(x) is int else '%s' % x, args)
    if type(args[-1]) is int:
      self.cmode = self.tb.cmode
