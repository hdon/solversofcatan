import random, sys, colorama, itertools
from math import ceil

# Term codes
B_BLACK = colorama.Back.BLACK
B_BLUE = colorama.Back.BLUE
B_CYAN = colorama.Back.CYAN
B_GREEN = colorama.Back.GREEN
B_MAGENTA = colorama.Back.MAGENTA
B_RED = colorama.Back.RED
B_RESET = colorama.Back.RESET
B_WHITE = colorama.Back.WHITE
B_YELLOW = colorama.Back.YELLOW

F_BLACK = colorama.Fore.BLACK
F_BLUE = colorama.Fore.BLUE
F_CYAN = colorama.Fore.CYAN
F_GREEN = colorama.Fore.GREEN
F_MAGENTA = colorama.Fore.MAGENTA
F_RED = colorama.Fore.RED
F_RESET = colorama.Fore.RESET
F_WHITE = colorama.Fore.WHITE
F_YELLOW = colorama.Fore.YELLOW

BRIGHT = colorama.Style.BRIGHT

FB_RESET = F_RESET + B_RESET
#FB_RESET = ''

FB_RESET_PERMA = F_RESET + B_RESET

LAND_COLORS = [
  colorama.Back.BLACK  + colorama.Fore.WHITE # SAND
, colorama.Back.GREEN  + colorama.Fore.WHITE # WOOD
, colorama.Back.RED    + colorama.Fore.WHITE # CLAY
, colorama.Back.WHITE  + colorama.Fore.BLACK # WOOL
, colorama.Back.YELLOW + colorama.Fore.BLACK # WHEAT
, colorama.Back.CYAN   + colorama.Fore.BLACK # STONE
]

#'ocean:'

BRIGHT_YELLOW_YELLOW = colorama.Fore.BLACK + colorama.Back.YELLOW + colorama.Style.BRIGHT
THIEF_SPACES = [' ', '8', '_', ' ', '/', '/']
LAND_ART = [
  [ # SAND
    r'%s   %s'   % (BRIGHT_YELLOW_YELLOW, FB_RESET)
, r'%s       %s' % (BRIGHT_YELLOW_YELLOW, FB_RESET)
, r'%s  %%s    %s' % (BRIGHT_YELLOW_YELLOW, FB_RESET)
, r'%s       %s' % (BRIGHT_YELLOW_YELLOW, FB_RESET)
,   r'%s   %s'   % (BRIGHT_YELLOW_YELLOW, FB_RESET)
],[ # WOOD
    r'%s   %s'   % (BRIGHT + colorama.Fore.BLACK + colorama.Back.GREEN, FB_RESET)
, r'%s  88888%s' % (BRIGHT + colorama.Fore.BLACK + colorama.Back.GREEN, FB_RESET)
, r'%s8%%%%s%s%%02d%s888%s' % (BRIGHT + F_BLACK + B_GREEN, F_WHITE, F_BLACK, FB_RESET)
, r'%s8888|||%s' % (BRIGHT + colorama.Fore.BLACK + colorama.Back.GREEN, FB_RESET)
,   r'%s|||%s'   % (BRIGHT + colorama.Fore.BLACK + colorama.Back.GREEN, FB_RESET)
],[ # CLAY
    r'%s/_/%s'   % (colorama.Fore.RED + colorama.Back.RED + colorama.Style.BRIGHT, FB_RESET)
, r'%s \/ \/ %s' % (colorama.Fore.RED + colorama.Back.RED + colorama.Style.BRIGHT, FB_RESET)
, r'%s/%%%%s%%02d_//%s' % (colorama.Fore.RED + colorama.Back.RED + colorama.Style.BRIGHT, FB_RESET)
, r'%s/ \/ \/%s' % (colorama.Fore.RED + colorama.Back.RED + colorama.Style.BRIGHT, FB_RESET)
,   r'%s///%s'   % (colorama.Fore.RED + colorama.Back.RED + colorama.Style.BRIGHT, FB_RESET)
],[ # WOOL
    r'%s   %s'   % (colorama.Fore.WHITE + colorama.Back.GREEN + colorama.Style.BRIGHT, FB_RESET)
, r'%s       %s' % (colorama.Fore.WHITE + colorama.Back.GREEN + colorama.Style.BRIGHT, FB_RESET)
, r'%s %%%%s%%02d;  %s' % (colorama.Fore.WHITE + colorama.Back.GREEN + colorama.Style.BRIGHT, FB_RESET)
, r'%s.,;:   %s' % (colorama.Fore.WHITE + colorama.Back.GREEN + colorama.Style.BRIGHT, FB_RESET)
,   r'%s:" %s'   % (colorama.Fore.WHITE + colorama.Back.GREEN + colorama.Style.BRIGHT, FB_RESET)
],[ # WHEAT
    r'%s///%s'   % (colorama.Fore.YELLOW + colorama.Back.GREEN + colorama.Style.BRIGHT, FB_RESET)
, r'%s///////%s' % (colorama.Fore.YELLOW + colorama.Back.GREEN + colorama.Style.BRIGHT, FB_RESET)
, r'%s/%%%%s%%02d///%s' % (colorama.Fore.YELLOW + colorama.Back.GREEN + colorama.Style.BRIGHT, FB_RESET)
, r'%s///////%s' % (colorama.Fore.YELLOW + colorama.Back.GREEN + colorama.Style.BRIGHT, FB_RESET)
,   r'%s///%s'   % (colorama.Fore.YELLOW + colorama.Back.GREEN + colorama.Style.BRIGHT, FB_RESET)
],[ # STONE
    r'%s /\%s'   % (colorama.Fore.BLACK + colorama.Back.WHITE + colorama.Style.BRIGHT, FB_RESET)
, r'%s  //\\ %s' % (colorama.Fore.BLACK + colorama.Back.WHITE + colorama.Style.BRIGHT, FB_RESET)
, r'%s\%%%%s%%02d\\/%s' % (colorama.Fore.BLACK + colorama.Back.WHITE + colorama.Style.BRIGHT, FB_RESET)
, r'%s\\//\//%s' % (colorama.Fore.BLACK + colorama.Back.WHITE + colorama.Style.BRIGHT, FB_RESET)
,   r'%s\//%s'   % (colorama.Fore.BLACK + colorama.Back.WHITE + colorama.Style.BRIGHT, FB_RESET)
],[ # OCEAN
    r'%s%s%svvv%s'   % (colorama.Fore.WHITE, colorama.Back.BLUE, colorama.Style.BRIGHT, FB_RESET)
, r'%s%s%svvvvvvv%s' % (colorama.Fore.WHITE, colorama.Back.BLUE, colorama.Style.BRIGHT, FB_RESET)
, r'%s%s%svvvvvvv%s' % (colorama.Fore.WHITE, colorama.Back.BLUE, colorama.Style.BRIGHT, FB_RESET)
, r'%s%s%svvvvvvv%s' % (colorama.Fore.WHITE, colorama.Back.BLUE, colorama.Style.BRIGHT, FB_RESET)
,   r'%s%s%svvv%s'   % (colorama.Fore.WHITE, colorama.Back.BLUE, colorama.Style.BRIGHT, FB_RESET)
]]

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
RESOURCE_STR = [ 'sand', 'wood', 'clay', 'wool', 'wheat', 'stone', 'water' ]

# TODO maybe this aren't useful
BUY_SETTLEMENT  = 'BUY_SETTLEMENT'
BUY_ROAD        = 'BUY_ROAD'
BUY_CITY        = 'BUY_CITY'
BUY_DEVELOPMENT = 'BUY_DEVELOPMENT'
END_TURN        = 'END_TURN'

# Vertices -- some of these also apply to roads
CAMP_WHO_MASK   = 0x0007
PLAYER1         = 0x0001
PLAYER2         = 0x0002
PLAYER3         = 0x0003
PLAYER4         = 0x0004
PLAYER5         = 0x0005
PLAYER6         = 0x0006
CAMP_BLOCKED    = 0x0007

CAMP_SIZE_MASK  = 0x0008
CAMP_SETTLEMENT = 0x0000
CAMP_CITY       = 0x0008

CAMP_PORT_MASK  = 0x00f0
CAMP_PORT_NONE  = 0x0000
CAMP_PORT_1     = 0x0010
CAMP_PORT_2     = 0x0020
CAMP_PORT_3     = 0x0030
CAMP_PORT_4     = 0x0040
CAMP_PORT_5     = 0x0050
CAMP_PORT_6     = 0x0060
CAMP_PORT_7     = 0x0070
CAMP_PORT_8     = 0x0080
CAMP_PORT_9     = 0x0090

CAMP_VOID       = 0x8000 # no player can settle here

CAMP_FREE_MASK  = CAMP_VOID | CAMP_WHO_MASK
CAMP_FREE       = 0x0000

def intersectRect(x0, y0, x1, y1):
  def intersectRect(f):
    def intersectRect(*args):
      for x, y in f(*args):
        if x0 <= x < x1 and y0 <= y < y1:
          yield x, y
    return intersectRect
  return intersectRect

class IllegalMoveError(Exception):
  def __init__(self, msg):
    Exception.__init__(self, msg)

class CampUnavailableForSettlementError(IllegalMoveError):
  def __init__(self, x, y, cs):
    self.params = x, y, cs
  def __str__(self):
    return 'Illegal Move: Camp at (%d, %d) With Value %04x Unavailable for Settlement' % self.params

class NotActivePlayerError(Exception):
  def __init__(self, requestedPlayer, actualPlayer):
    Exception.__init__(self)

class Catan:
  def __init__(self):
    self.w = 6
    self.h = 5
    self.vh = (self.h + 1) * 2 # :(

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

    desert = random.randint(0, 18) # inclusive range
    landTypes.insert(desert, SAND)
    landWealth.insert(desert, 0)

    thief_index = \
      desert + 1 if desert < 3  else \
      desert + 3 if desert < 7  else \
      desert + 5 if desert < 12 else \
      desert + 6 if desert < 16 else \
      desert + 9

    self.thief = (thief_index % self.w, thief_index // self.w)

    i = iter(zip(landTypes, landWealth))
    def ocean():
      return (OCEAN, 0)

    self.land = [
      ocean(), i.next(),i.next(),i.next(), ocean(), ocean()
    , i.next(),i.next(),i.next(),i.next(), ocean(), ocean()
    , i.next(),i.next(),i.next(),i.next(),i.next(), ocean()
    , i.next(),i.next(),i.next(),i.next(), ocean(), ocean()
    , ocean(), i.next(),i.next(),i.next(), ocean(), ocean()
    ]

    self.tilesByTargetNumber = {}
    for y in xrange(self.h):
      for x in xrange(self.w):
        number = self.land[ y * self.w + x ][1]
        if number:
          if number not in self.tilesByTargetNumber:
            self.tilesByTargetNumber[ number ] = []
          self.tilesByTargetNumber[ number ].append((x, y))

    self.initCampSites()
    self.initRoutes()

    # no need to complicate routes with many different flags and values
    # the campsites tell us all we need to know about where roads can be
    # built.

    # Player initialization
    numPlayers = 4
    self.playerResources = [[0 for res in xrange(OCEAN)] for player in xrange(4)]
    self.playerSettlements = [[] for player in xrange(4)]
    self.activePlayer = PLAYER1

  def initRoutes(self):
    b = CAMP_VOID
    g = CAMP_FREE
    self.routes = [
        b,  b,  g,  g,  g,  g,  g,  g,  b,  b,  b,  b # 12
    , b,      g,      g,      g,      g,      b
    ,   b,  g,  g,  g,  g,  g,  g,  g,  g,  b,  b,  b
    ,     g,      g,      g,      g,      g,      b
    ,   g,  g,  g,  g,  g,  g,  g,  g,  g,  g,  b,  b
    , g,      g,      g,      g,      g,      g
    ,   g,  g,  g,  g,  g,  g,  g,  g,  g,  g,  b,  b
    ,     g,      g,      g,      g,      g,      b
    ,   b,  g,  g,  g,  g,  g,  g,  g,  g,  b,  b,  b
    , b,      g,      g,      g,      g,      b
    ,   b,  b,  g,  g,  g,  g,  g,  g,  b,  b,  b,  b
    ]

  def initCampSites(self):
    o = CAMP_VOID
    z = CAMP_FREE
    a = z | CAMP_PORT_1
    b = z | CAMP_PORT_2
    c = z | CAMP_PORT_3
    d = z | CAMP_PORT_4
    e = z | CAMP_PORT_5
    f = z | CAMP_PORT_6
    g = z | CAMP_PORT_7
    h = z | CAMP_PORT_8
    i = z | CAMP_PORT_9
    self.campSites = [
         o,    a,    b,    z,    o,    o,    o
    , o,    a,    z,    b,    z,    o,    o
    , o,    z,    z,    z,    c,    o,    o
    ,    i,    z,    z,    z,    c,    o,    o
    ,    i,    z,    z,    z,    z,    o,    o
    , z,    z,    z,    z,    z,    d,    o
    , z,    z,    z,    z,    z,    d,    o
    ,    h,    z,    z,    z,    z,    o,    o
    ,    h,    z,    z,    z,    e,    o,    o
    , o,    z,    z,    z,    e,    o,    o
    , o,    g,    z,    f,    z,    o,    o
    ,    o,    g,    f,    z,    o,    o,    o
    ]

  def playerBuildSettlement(self, pos, player):
    # validate active player
    if player != self.activePlayer:
      raise NotActivePlayerError(player, self.activePlayer)

    # check campsite bounds before doing road calculations
    if pos[0] < 0 or self.w <= pos[0] \
    or pos[1] < 0 or self.h <= pos[1]:
      raise IndexError('No such campsite')
    
    # reserve cost of settlement
    rez = self.playerResources[player]
    if rez[CLAY] == 0 and rez[WOOD] == 0 and rez[WOOL] == 0 and rez[WHEAT] == 0:
      raise IllegalMoveError()

    # Does the player have a road leading to this campsite?
    hasRoad = False
    for rx, ry in self.roadsTo(*pos):
      if self.getRoad(rx, ry) & CAMP_WHO_MASK == player:
        hasRoad = True
        break
    if not hasRoad:
      raise IllegalMoveError()

    # placeSettlement will ensure no campsite collisions
    self.placeSettlement(x, y, player)

    # finally, deduct cost of settlement
    rez[CLAY]  -= 1
    rez[WOOD]  -= 1
    rez[WOOL]  -= 1
    rez[WHEAT] -= 1

  def playerUpgradeSettlement(self, pos, player):
    if player != self.activePlayer:
      raise NotActivePlayerError(player, self.activePlayer)

  def roll(self):
    number = random.randint(1,6) + random.randint(1,6)
    #print 'rolled', number
    if number == 7:
      # TODO thief
      # Halve any player's resources over 8
      # TODO allow the player to choose
      for rez in self.playerResources:
        if sum(rez) < 8:
          continue
        for iRez in xrange(len(rez)):
          # This will actually discard more resources than are
          # necessary, but this code is only a stand-in for
          # allowing the player to choose which resource cards
          # to discard.
          rez[iRez] /= 2
    else:
      for tx, ty in self.tilesByTargetNumber[ number ]:
        land = self.getLand(tx, ty)
        res = land[0]
        for vx, vy in self.campsitesAtLand(tx, ty):
          cs = self.getCampsite(vx, vy)
          player = cs & CAMP_WHO_MASK
          if PLAYER1 <= player and player <= PLAYER4:
            self.givePlayerResource(player, res)

  def whatCanIBuy(self, player):
    rez = self.playerResources[player-1]
    if rez[CLAY] and rez[WOOD]:
      yield BUY_ROAD
      if rez[WOOL] and rez[WHEAT]:
        yield BUY_SETTLEMENT
    if rez[STONE] >= 3 and rez[WHEAT] >= 2:
      yield BUY_CITY
    if rez[STONE] and rez[WOOL] and rez[WHEAT]:
      yield BUY_DEVELOPMENT

  def canIBuy(self, player, buy):
    rez = self.playerResources[player-1]
    if buy == BUY_ROAD:
      return rez[WOOD] and rez[CLAY]
    if buy == BUY_SETTLEMENT:
      return rez[WOOD] and rez[CLAY] and rez[WOOL] and rez[WHEAT]
    if buy == BUY_CITY:
      return rez[STONE] >= 3 and rez[WHEAT] >= 2
    if buy == BUY_DEVELOPMENT:
      return rez[WOOL] and rez[WHEAT] and rez[STONE]

  def buy(self, player, buy):
    if not self.canIBuy(player, buy):
      raise IllegalMoveError('player %s cannot afford to buy %s' % (player, buy))
    rez = self.playerResources[player-1]
    if buy == BUY_ROAD:
      rez[WOOD] -= 1
      rez[CLAY] -= 1
    elif buy == BUY_SETTLEMENT:
      rez[WOOD] -= 1
      rez[CLAY] -= 1
      rez[WOOL] -= 1
      rez[WHEAT] -= 1
    elif buy == BUY_CITY:
      rez[STONE] -= 3
      rez[WHEAT] -= 2
    elif buy == BUY_DEVELOPMENT:
      rez[WOOL] -= 1
      rez[WHEAT] -= 1
      rez[STONE] -= 1

  def whereCanISettle(self, player):
    pass

  def whereCanIUpgrade(self, player):
    pass

  def whereDoMyRoadsGo(self, player):
    for y in xrange(self.h*2+1):
      self.placeRoad(0, y, PLAYER1)

  def whereCanIDrive(self, player):
    pass

  def givePlayerResource(self, player, res, n=1):
    #print 'giving player', player, n, 'of', RESOURCE_STR[ res ]
    reses = self.playerResources[player-1]
    reses[res] += n

  def printBoard(self):
    import fb
    tb = fb.TermBuffer(80-19, 25)
    out = tb.cursor()
    w = self.w
    h = self.h
    CS = self.campSites
    LAND = self.land
    #out.writec(F_RESET + B_RESET + '\n')
    #print self.campSites
    for y in xrange(0, (h+1)*2):
      for isRoadLine in xrange(2):
        #out.writec("%sy=%02d r=%01d " % (FB_RESET_PERMA, y, isRoadLine))
        if isRoadLine:
          if y == (h+1)*2-1:
            continue

          stagger = (y+1) & 2 == 0

          if y % 2:
            if stagger:
              out.writec('%s%s%svvVv%s' % (
                colorama.Fore.WHITE, colorama.Back.BLUE, colorama.Style.BRIGHT, FB_RESET))

            for x in xrange(w):
              land_x = x
              land_y = (y - 1) // 2
              land_index = land_y * w + x
              if y == 0 or y == h*2 + 1 or x == w:
                land, landNumber = OCEAN, 0
              else:
                land = (y - 1) // 2 * w + x
                land, landNumber = LAND[land_index]
              road = self.getRoad(x, y)
              if road & CAMP_VOID:
                out.writec(B_BLUE + F_WHITE + BRIGHT + 'W' + FB_RESET)
              else:
                if road & CAMP_WHO_MASK:
                  road_a = '%01d' % (road & CAMP_WHO_MASK)
                else:
                  road_a = ' '
                out.writec(FB_RESET + F_MAGENTA + road_a)
              landSegment = LAND_ART[land][2]
              if land >= WOOD and land <= STONE:
                landSegment = landSegment % landNumber
              if land >= SAND and land <= STONE:
                if self.thief[0] == land_x and self.thief[1] == land_y:
                  landSegment = landSegment % 'X'
                else:
                  landSegment = landSegment % THIEF_SPACES[land]
              else:
                pass
              out.writec(landSegment)
              #out.writec('%s%s%02d..' % (road_a, land))
          else:
            out.writec(
              colorama.Back.BLUE
            + colorama.Style.BRIGHT
            + 'ww'
            + FB_RESET
            )
            #print 'y=',y
            for x in xrange(w*2):
              # top or bottom of hex?
              tobo = (y // 2 + x) & 1
              road = self.getRoad(x, y)
              if road & CAMP_VOID:
                road_a = colorama.Back.BLUE + colorama.Style.BRIGHT + 'W' + FB_RESET
              else:
                routePlayer = road & CAMP_WHO_MASK
                if routePlayer:
                  road_a = '%01d' % routePlayer
                else:
                  road_a = ' ' if (y // 2 + x) & 1 else ' '
                road_a = FB_RESET + F_MAGENTA + road_a

              land = self.getLandTypeOrOcean(
                x // 2,
                y // 2 - (1 if tobo else 0)
              )

              out.writec(road_a)
              out.writec(LAND_ART[land][4 if tobo else 0])
        else:
          #out.writec('>' if y % 2 == 1 and y // 2 < h else ' ')
          stagger = (y+1) & 2 == 0
          if stagger:
            out.writec('%s%s%svvvv%s' % (
              colorama.Fore.WHITE, colorama.Back.BLUE, colorama.Style.BRIGHT, FB_RESET))
            
          for x in xrange(0, w+1):
            cs = y*(w+1)+x
            cs = CS[cs]

            if y == 0 or y == h*2 + 1 or x == w:
              land = OCEAN
            else:
              land = (y - 1) // 2 * w + x
              land = LAND[land][0]

            if cs == CAMP_VOID:
              cs = colorama.Back.BLUE+colorama.Fore.WHITE+colorama.Style.BRIGHT+'V'
            else:
              if cs & CAMP_WHO_MASK == CAMP_BLOCKED:
                cs = FB_RESET + '-'
              elif cs & CAMP_WHO_MASK == CAMP_FREE:
                cs = FB_RESET + ' '
              else:
                cs = FB_RESET + '%d' % (cs & CAMP_WHO_MASK)
              
            #land = '..%02d.' % land
            if 1 or land >= 0:
              land = LAND_ART[land][3 if (y + 1) & 1 else 1]
              #iLand = land
              #land = LAND_COLORS[land]
              #land = ''
              #land = '%s %02d  %s' % (land, iLand, B_RESET + F_RESET)
            else:
              land = '     '

            #land = '.....'
            #land = ' ' if land == OCEAN else 'x'
            segment = '%s%s' % (cs, land)

            out.writec(segment)
        out.writec('\n')
    tb.printout()
    print F_RESET + B_RESET

  def randomInit(self, numPlayers):
    self.numPlayers = numPlayers
    remainingSites = list(itertools.product(xrange(self.w + 1), xrange((self.h + 1) * 2)))
    random.shuffle(remainingSites)
    for player in xrange(1, numPlayers+1):
      numSettlements = 2
      while numSettlements:
        cx, cy = remainingSites.pop()
        cs = self.getCampsite(cx, cy)
        #print 'valuating campsite (%d,%d) for random placement. value = 0x%04x' % (cx, cy, cs)
        if cs & CAMP_FREE_MASK != CAMP_FREE:
          #print "  can't use"
          continue
        #print 'placing', cx, cy, player
        self.placeSettlement(cx, cy, player)
        numSettlements -= 1
        # place adjoining road
        for rx, ry in self.roadsTo(cx, cy):
          if self.getRoad(rx, ry) & CAMP_WHO_MASK == CAMP_FREE:
            self.placeRoad(rx, ry, player)
            break
  
  def getLandTypeOrOcean(self, x, y):
    if x < 0 or x >= self.w or y < 0 or y >= self.h:
      return OCEAN
    return self.land[y * self.w + x][0]

  def getLand(self, x, y):
    if x < 0 or x >= self.w or y < 0 or y >= self.h:
      raise IndexError('Land index out of bounds')
    return self.land[y * self.w + x]

  def getCampsite(self, x, y):
    return self.campSites[self.indexCampsite(x, y)]

  def setCampsite(self, x, y, value, mask=0):
    index = self.indexCampsite(x, y)
    self.campSites[index] = (self.campSites[index] & mask) | value

  def blockNearbyCampsite(self, x, y):
    try:
      if self.getCampsite(x, y) & CAMP_VOID == 0:
        self.setCampsite(x, y, CAMP_BLOCKED, ~CAMP_WHO_MASK)
    except IndexError:
      pass

  def indexCampsite(self, x, y):
    if x < 0 or self.w*2 <= x or y < 0 or (self.h+1)*2 <= y:
      raise IndexError('Campsite (%s,%s) out of bounds' % (x, y))
    return y * (self.w + 1) + x

  def campsitesAtLand(self, x, y):
    '''A generator for campsite coords adjacent to given hex tile coords'''
    sx = x + (y & 1)
    yield sx + 0, y * 2
    yield  x + 0, y * 2 + 1
    yield  x + 1, y * 2 + 1
    yield  x + 0, y * 2 + 2
    yield  x + 1, y * 2 + 2
    yield sx + 0, y * 2 + 3

  def neighborsOf(self, x, y):
    '''A generator for campsite coords adjacent to given campsite coords'''
    x2 = x + ( -1 if (y+1) & 2 else 1 )
    y2 = y + ( -1 if  y    & 1 else 1 )
    yield x, y-1
    yield x, y+1
    yield x2, y2

  def roadsTo(self, x, y):
    stagger = (y+1) & 2 == 0
    legs_y = y - (y & 1)
    leg_dx = 1 if stagger else -1

    for rx, ry in [
      (x, y - (y & 1 ^ 1))
    , (x * 2,          legs_y)
    , (x * 2 + leg_dx, legs_y)
    ]:
      if self.roadInBounds(rx, ry):
        #print 'road to %d,%d: %d,%d' % (x, y, rx, ry)
        yield rx, ry
      else:
        #print 'daor to %d,%d: %d,%d' % (x, y, rx, ry)
        pass

  def campsitesFromRoad(self, x, y):
    '''A generator enumerating campsites by a given road'''
    doubleRoads = y & 1 == 0
    if doubleRoads:
      roadDir = bool(y&2) ^ bool(x&1)
      if roadDir:
        yield x//2 + x%2, y+1
        yield x//2      , y
      else:
        yield x//2 + x%2, y
        yield x//2      , y+1
    else:
      yield x, y
      yield x, y+1

  def placeRoad(self, x, y, player):
    '''Place a road if it is allowed; implement side-effects'''
    # TODO longest roaD
    if player < PLAYER1 or player > PLAYER6:
      raise ValueError('NO SUCH PLAYER')
    if self.getRoad(x, y) & CAMP_FREE_MASK != CAMP_FREE:
      raise IllegalMoveError('ROAD UNAVAILABLE')

    self.setRoad(x, y, player, ~CAMP_WHO_MASK)

  def placeSettlement(self, x, y, player):
    '''Place a settlement if it is allowed; implement side-effects'''
    # TODO bump score
    if self.getCampsite(x, y) & CAMP_FREE_MASK != CAMP_FREE:
      raise CampUnavailableForSettlementError(x, y, self.getCampsite(x, y))
    if player < PLAYER1 or player > PLAYER6:
      raise ValueError('NO SUCH PLAYER')

    self.setCampsite(x, y, player, ~CAMP_WHO_MASK)
    self.playerSettlements[ player-1 ].append((x, y))

    for nx, ny in self.neighborsOf(x, y):
      self.blockNearbyCampsite(nx, ny)

    # just a test
    #for rx, ry in self.roadsTo(x, y):
      #if self.getRoad(rx, ry) & CAMP_FREE_MASK == CAMP_FREE:
        #self.placeRoad(rx, ry, player)

  def roadInBounds(self, x, y):
    return \
      y >= 0 and \
      y < (self.h + 1) * 2 - 1 and \
      x >= 0 and \
      x < (self.w if y & 1 else self.w * 2)
    
  # Maybe this could be useful somewhere...?
  def filterCampSiteBounds(self):
    '''Decorate a member function with this I guess'''
    def filterCampSiteBounds(f):
      def filterCampSiteBounds(*args):
        for x, y in f(*args):
          if x >= 0 and x < self.w+1 and y >= 0 and y < (self.h+1)*2:
            yield x, y
      return filterCampSiteBounds
    return filterCampSiteBounds

  def getRoadIndex(self,x , y):
    if y < 0 or y >= (self.h + 1) * 2 - 1 \
    or x < 0 or x >= (self.w if y & 1 else self.w * 2):
      raise IndexError('road index (%d,%d) out of bounds' % (x, y))
    return y // 2 * self.w * 3 + (self.w * 2 if y & 1 else 0) + x

  def getRoad(self, x, y):
    index = self.getRoadIndex(x, y)
    return self.routes[ index ]

  def setRoad(self, x, y, value, mask=0):
    index = self.getRoadIndex(x, y)
    self.routes[index] = (self.routes[index] & mask) | value

  def dumpCampSites(self):
    print 'dumpCampSites():'
    for y in xrange(self.h *2 + 1):
      for x in xrange(self.w +1 ):
        sys.stdout.write('%04x ' % self.getCampsite(x, y))
      sys.stdout.write('\n')
  def dumpLand(self):
    print 'dumpLand():'
    for y in xrange(self.h):
      for x in xrange(self.w):
        sys.stdout.write('%d ' % self.getLand(x, y)[0])
      print
