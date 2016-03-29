import random, sys, colorama, itertools
F_YELLOW = colorama.Fore.YELLOW
F_RED = colorama.Fore.RED
B_YELLOW = colorama.Back.YELLOW

F_RESET = colorama.Fore.RESET
B_RESET = colorama.Back.RESET
FB_RESET = F_RESET + B_RESET

LAND_COLORS = [
  colorama.Back.BLACK  + colorama.Fore.WHITE # SAND
, colorama.Back.GREEN  + colorama.Fore.WHITE # WOOD
, colorama.Back.RED    + colorama.Fore.WHITE # CLAY
, colorama.Back.WHITE  + colorama.Fore.BLACK # WOOL
, colorama.Back.YELLOW + colorama.Fore.BLACK # WHEAT
, colorama.Back.CYAN   + colorama.Fore.BLACK # STONE
]

#'ocean:'

LAND_ART = [
 # SAND
 ['%s%s%s     %s' % (colorama.Fore.BLACK, colorama.Back.YELLOW, '', FB_RESET)
, '%s%s%s     %s' % (colorama.Fore.BLACK, colorama.Back.YELLOW, '', FB_RESET)]
 # WOOD
,['%s%s%s88888%s' % (colorama.Fore.YELLOW, colorama.Back.GREEN, '', FB_RESET)
, '%s%s%s|||||%s' % (colorama.Fore.YELLOW, colorama.Back.GREEN, '', FB_RESET)]
 # CLAY
,['%s%s%s/\\/\\\\%s' % (colorama.Fore.RED, colorama.Back.RED, colorama.Style.BRIGHT, FB_RESET)
, '%s%s%s////\\%s' % (colorama.Fore.RED, colorama.Back.RED, colorama.Style.BRIGHT, FB_RESET)]
 # WOOL
,['%s%s%s ..\' %s' % (colorama.Fore.WHITE, colorama.Back.GREEN, colorama.Style.BRIGHT, FB_RESET)
, '%s%s%s.::  %s' % (colorama.Fore.WHITE, colorama.Back.GREEN, colorama.Style.BRIGHT, FB_RESET)]
 # WHEAT
,['%s%s%s//|//%s' % (colorama.Fore.YELLOW, colorama.Back.GREEN, colorama.Style.BRIGHT, FB_RESET)
, '%s%s%s/|///%s' % (colorama.Fore.YELLOW, colorama.Back.GREEN, colorama.Style.BRIGHT, FB_RESET)]
 # STONE
,['%s%s%s/\\/\\\\%s' % (colorama.Fore.BLACK, colorama.Back.WHITE, colorama.Style.BRIGHT, FB_RESET)
, '%s%s%s////\\%s' % (colorama.Fore.BLACK, colorama.Back.WHITE, colorama.Style.BRIGHT, FB_RESET)]
 # OCEAN
,['%s%s%svvvvv%s' % (colorama.Fore.WHITE, colorama.Back.BLUE, colorama.Style.BRIGHT, FB_RESET)
, '%s%s%svvvvv%s' % (colorama.Fore.WHITE, colorama.Back.BLUE, colorama.Style.BRIGHT, FB_RESET)]
]

class Settler:
  def __init__(self, index):
    self.resources = [0, 0, 0, 0, 0, 0]
    self.index = index

SAND = 0
WOOD = 1
CLAY = 2
WOOL = 3
WHEAT = 4
STONE = 5
OCEAN = 6

# Vertices
CAMPAVAILMASK = 0x3000
NOSUCHCAMP    = 0x1000
CAMPOFFLIMITS = 0x2000
CAMPAVAILABLE = 0x0000
SIZEMASK      = 0x0300
SETTLEMENT    = 0x0100
CITY          = 0x0200
PLAYERMASK    = 0x0003
PLAYER0       = 0x0000
PLAYER1       = 0x0001
PLAYER2       = 0x0002
PLAYER3       = 0x0003

class Catan:
  def __init__(self):
    self.players = map(Settler, xrange(4))

    # http://pop.h-cdn.co/assets/15/08/1424387153-catan.jpg

    landTypes = [
      WHEAT, WHEAT, WHEAT, WHEAT,
      WOOD,  WOOD,  WOOD,  WOOD,
      WOOL,  WOOL,  WOOL,  WOOL,
      CLAY,  CLAY,  CLAY,
      STONE, STONE, STONE,
    ]
    landWealth = [ 5, 2, 6, 8,10, 9, 3, 3,11, 4, 8, 4, 6, 5,10,11,12, 9]

    random.shuffle(landTypes)
    random.shuffle(landWealth)

    desert = random.randint(0, 19) # inclusive range
    landTypes.insert(desert, SAND)
    landWealth.insert(desert, 0)

    i = iter(zip(landTypes, landWealth))
    def ocean():
      return (OCEAN, 0)

    self.land = [
      ocean(), i.next(),i.next(),i.next(), ocean()
    , i.next(),i.next(),i.next(),i.next(), ocean()
    , i.next(),i.next(),i.next(),i.next(),i.next()
    , i.next(),i.next(),i.next(),i.next(), ocean()
    , ocean(), i.next(),i.next(),i.next(), ocean()
    ]

    b = NOSUCHCAMP
    g = CAMPAVAILABLE
    self.campSites = [
         b,    g,    g,    g,    b,    b
    , b,    g,    g,    g,    g,    b
    , b,    g,    g,    g,    g,    b
    ,    g,    g,    g,    g,    g,    b
    ,    g,    g,    g,    g,    g,    b
    , g,    g,    g,    g,    g,    g
    , g,    g,    g,    g,    g,    g
    ,    g,    g,    g,    g,    g,    b
    ,    g,    g,    g,    g,    g,    b
    , b,    g,    g,    g,    g,    b
    , b,    g,    g,    g,    g,    b
    ,    b,    g,    g,    g,    b,    b
    ]

    self.w = 5
    self.h = 5

  def printBoard(self):
    w = self.w
    h = self.h
    CS = self.campSites
    LAND = self.land
    #sys.stdout.write(F_RESET + B_RESET + '\n')
    #print self.campSites
    for y in xrange(0, (h+1)*2):
      #sys.stdout.write('>' if y % 2 == 1 and y // 2 < h else ' ')
      stagger = (y+1) & 2 == 0
      if stagger:
        sys.stdout.write('%s%s%svvv%s' % (
          colorama.Fore.WHITE, colorama.Back.BLUE, colorama.Style.BRIGHT, FB_RESET))
      else:
        sys.stdout.write('%s%s%s%s' % (
          colorama.Fore.WHITE, colorama.Back.BLUE, colorama.Style.BRIGHT, ''))
        
      for x in xrange(0, w+1):
        cs = y*(w+1)+x
        cs = CS[cs]

        if y == 0 or y == h*2 + 1 or x == w:
          land = OCEAN
        else:
          land = (y - 1) // 2 * w + x
          land = LAND[land][0]

        if cs == NOSUCHCAMP:
          cs = colorama.Back.BLUE+colorama.Fore.WHITE+colorama.Style.BRIGHT+'V'
        elif cs & CAMPAVAILMASK == CAMPAVAILABLE:
          cs = FB_RESET+'*'
        else:
          cs = '%s%d' % (FB_RESET, cs & PLAYERMASK)
          
        #land = '..%02d.' % land
        if 1 or land >= 0:
          land = LAND_ART[land][(y+1) % 2]
          #iLand = land
          #land = LAND_COLORS[land]
          #land = ''
          #land = '%s %02d  %s' % (land, iLand, B_RESET + F_RESET)
        else:
          land = '     '

        #land = '.....'
        #land = ' ' if land == OCEAN else 'x'
        segment = '%s%s' % (cs, land)

        sys.stdout.write(segment)
      sys.stdout.write('\n')

  def randomInit(self, numPlayers):
    self.numPlayers = numPlayers
    remainingSites = list(itertools.product(xrange(self.w + 1), xrange((self.h + 1) * 2)))
    print remainingSites
    random.shuffle(remainingSites)
    for player in xrange(numPlayers):
      player = 1
      numSettlements = 2
      while numSettlements:
        x, y = remainingSites.pop()
        if self.getCampsite(x, y) & CAMPAVAILMASK != CAMPAVAILABLE:
          continue
        #print 'placing', x, y, player
        self.placeSettlement(x, y, player)
        numSettlements -= 1
  
  def getCampsite(self, x, y):
    return self.campSites[self.indexCampsite(x, y)]

  def setCampsite(self, x, y, value, mask=0):
    index = self.indexCampsite(x, y)
    self.campSites[index] = (self.campSites[index] & mask) | value

  def blockNearbyCampsite(self,x , y):
    if x < 0 or self.w*2 <= x or y < 0 or (self.h+1)*2 <= y:
      print 'cant block nearby campsite', x, y
      return
    if self.getCampsite(x, y) & NOSUCHCAMP == 0:
      self.setCampsite(x, y, CAMPOFFLIMITS, ~CAMPAVAILMASK)

  def indexCampsite(self, x, y):
    return y * (self.w + 1) + x

  def neighborsOf(self, x, y):
    x2 = x + ( -1 if (y+1) & 2 else 1 )
    y2 = y + ( -1 if  y    & 1 else 1 )
    yield x, y-1
    yield x, y+1
    yield x2, y2
    
  def placeSettlement(self, x, y, player):
    if self.getCampsite(x, y) & CAMPAVAILMASK != CAMPAVAILABLE:
      raise IndexError('CAMP UNAVAILABLE')
    if player < PLAYER0 or player > PLAYER3:
      raise ValueError('NO SUCH PLAYER')

    self.setCampsite(x, y, CAMPOFFLIMITS | player, ~CAMPAVAILMASK)

    for x, y in self.neighborsOf(x, y):
      self.blockNearbyCampsite(x, y)

  def vertexIsAdjacentToTile(v, t):
    vr = v / (2 * self.w) 
    tr = t / self.w * 2
    if vr < tr or vr > tr + 2:
      return False

    vc = v % (2 % self.w)
    tc = t % self.w * 2
    if vc < tc or vc > tc * 2:
      return False

    return True

    # For now we just randomly place initial settlements and roads
    
catan = Catan()
catan.randomInit(4)
catan.printBoard()
print
