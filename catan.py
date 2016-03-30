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
 ['%s%s%s       %s' % (colorama.Fore.BLACK, colorama.Back.YELLOW, '', FB_RESET)
, '%s%s%s       %s' % (colorama.Fore.BLACK, colorama.Back.YELLOW, '', FB_RESET)
, '%s%s%s   %s' % (colorama.Fore.BLACK, colorama.Back.YELLOW, '', FB_RESET)
, '%s%s%s   %s' % (colorama.Fore.BLACK, colorama.Back.YELLOW, '', FB_RESET)]
 # WOOD
,['%s%s%s8888888%s' % (colorama.Fore.YELLOW, colorama.Back.GREEN, '', FB_RESET)
, '%s%s%s|||||||%s' % (colorama.Fore.YELLOW, colorama.Back.GREEN, '', FB_RESET)
, '%s%s%s|||%s' % (colorama.Fore.YELLOW, colorama.Back.GREEN, '', FB_RESET)
, '%s%s%s|||%s' % (colorama.Fore.YELLOW, colorama.Back.GREEN, '', FB_RESET)]
 # CLAY
,['%s%s%s/\\///\\\\%s' % (colorama.Fore.RED, colorama.Back.RED, colorama.Style.BRIGHT, FB_RESET)
, '%s%s%s//////\\%s' % (colorama.Fore.RED, colorama.Back.RED, colorama.Style.BRIGHT, FB_RESET)
, '%s%s%s//\\%s' % (colorama.Fore.RED, colorama.Back.RED, colorama.Style.BRIGHT, FB_RESET)
, '%s%s%s//\\%s' % (colorama.Fore.RED, colorama.Back.RED, colorama.Style.BRIGHT, FB_RESET)]
 # WOOL
,['%s%s%s ....\' %s' % (colorama.Fore.WHITE, colorama.Back.GREEN, colorama.Style.BRIGHT, FB_RESET)
, '%s%s%s.::::  %s' % (colorama.Fore.WHITE, colorama.Back.GREEN, colorama.Style.BRIGHT, FB_RESET)
, '%s%s%s.: %s' % (colorama.Fore.WHITE, colorama.Back.GREEN, colorama.Style.BRIGHT, FB_RESET)
, '%s%s%s.: %s' % (colorama.Fore.WHITE, colorama.Back.GREEN, colorama.Style.BRIGHT, FB_RESET)]
 # WHEAT
,['%s%s%s//|////%s' % (colorama.Fore.YELLOW, colorama.Back.GREEN, colorama.Style.BRIGHT, FB_RESET)
, '%s%s%s/|/////%s' % (colorama.Fore.YELLOW, colorama.Back.GREEN, colorama.Style.BRIGHT, FB_RESET)
, '%s%s%s///%s' % (colorama.Fore.YELLOW, colorama.Back.GREEN, colorama.Style.BRIGHT, FB_RESET)
, '%s%s%s///%s' % (colorama.Fore.YELLOW, colorama.Back.GREEN, colorama.Style.BRIGHT, FB_RESET)]
 # STONE
,['%s%s%s/\\///\\\\%s' % (colorama.Fore.BLACK, colorama.Back.WHITE, colorama.Style.BRIGHT, FB_RESET)
, '%s%s%s//////\\%s' % (colorama.Fore.BLACK, colorama.Back.WHITE, colorama.Style.BRIGHT, FB_RESET)
, '%s%s%s//\\%s' % (colorama.Fore.BLACK, colorama.Back.WHITE, colorama.Style.BRIGHT, FB_RESET)
, '%s%s%s//\\%s' % (colorama.Fore.BLACK, colorama.Back.WHITE, colorama.Style.BRIGHT, FB_RESET)]
 # OCEAN
,['%s%s%svvvvvvv%s' % (colorama.Fore.WHITE, colorama.Back.BLUE, colorama.Style.BRIGHT, FB_RESET)
, '%s%s%svvvvvvv%s' % (colorama.Fore.WHITE, colorama.Back.BLUE, colorama.Style.BRIGHT, FB_RESET)
, '%s%s%svvv%s' % (colorama.Fore.WHITE, colorama.Back.BLUE, colorama.Style.BRIGHT, FB_RESET)
, '%s%s%svvv%s' % (colorama.Fore.WHITE, colorama.Back.BLUE, colorama.Style.BRIGHT, FB_RESET)]
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
      ocean(), i.next(),i.next(),i.next(), ocean(), ocean()
    , i.next(),i.next(),i.next(),i.next(), ocean(), ocean()
    , i.next(),i.next(),i.next(),i.next(),i.next(), ocean()
    , i.next(),i.next(),i.next(),i.next(), ocean(), ocean()
    , ocean(), i.next(),i.next(),i.next(), ocean(), ocean()
    ]

    b = CAMP_VOID
    g = CAMP_FREE
    self.campSites = [
         b,    g,    g,    g,    b,    b,    b
    , b,    g,    g,    g,    g,    b,    b
    , b,    g,    g,    g,    g,    b,    b
    ,    g,    g,    g,    g,    g,    b,    b
    ,    g,    g,    g,    g,    g,    b,    b
    , g,    g,    g,    g,    g,    g,    b
    , g,    g,    g,    g,    g,    g,    b
    ,    g,    g,    g,    g,    g,    b,    b
    ,    g,    g,    g,    g,    g,    b,    b
    , b,    g,    g,    g,    g,    b,    b
    , b,    g,    g,    g,    g,    b,    b
    ,    b,    g,    g,    g,    b,    b,    b
    ]

    self.routes = [
        b,  b,  g,  g,  g,  g,  g,  g,  b,  b,  b,  b # 12
    , b,      g,      g,      g,      g,      b,      b # 7
    ,   b,  g,  g,  g,  g,  g,  g,  g,  g,  b,  b,  b
    ,     g,      g,      g,      g,      g,      b,      b
    ,   g,  g,  g,  g,  g,  g,  g,  g,  g,  g,  b,  b
    , g,      g,      g,      g,      g,      g,      g
    ,   g,  g,  g,  g,  g,  g,  g,  g,  g,  g,  b,  b
    ,     g,      g,      g,      g,      g,      b,      g
    ,   b,  g,  g,  g,  g,  g,  g,  g,  g,  b,  b,  b
    , b,      g,      g,      g,      g,      b,      g
    ,   b,  b,  g,  g,  g,  g,  g,  g,  b,  b,  b,  b
    ]

    self.w = 6
    self.h = 5

    # no need to complicate routes with many different flags and values
    # the campsites tell us all we need to know about where roads can be
    # built.

  def printBoard(self):
    w = self.w
    h = self.h
    CS = self.campSites
    LAND = self.land
    #sys.stdout.write(F_RESET + B_RESET + '\n')
    #print self.campSites
    for y in xrange(0, (h+1)*2):
      for isRoadLine in xrange(2):
        if isRoadLine:
          if y == (h+1)*2-1:
            continue

          stagger = (y+1) & 2 == 0


          if y % 2:
            if stagger:
              sys.stdout.write('%s%s%svvVv%s' % (
                colorama.Fore.WHITE, colorama.Back.BLUE, colorama.Style.BRIGHT, FB_RESET))

            for x in xrange(w):
              if y == 0 or y == h*2 + 1 or x == w:
                land = OCEAN
              else:
                land = (y - 1) // 2 * w + x
                land = LAND[land][0]
              if self.getRoad(x, y) & CAMP_VOID:
                road_a = colorama.Back.BLUE + colorama.Style.BRIGHT + 'W' + FB_RESET
              else:
                road_a = '|'
              sys.stdout.write(road_a)
              sys.stdout.write(LAND_ART[land][1])
              #sys.stdout.write('%s%s%02d..' % (road_a, land))
          else:
            sys.stdout.write(
              colorama.Back.BLUE
            + colorama.Style.BRIGHT
            + 'ww'
            + FB_RESET
            )
            #print 'y=',y
            for x in xrange(w*2):
              if self.getRoad(x, y) & CAMP_VOID:
                road_a = colorama.Back.BLUE + colorama.Style.BRIGHT + 'W' + FB_RESET
              else:
                road_a = '\\' if (y // 2 + x) & 1 else '/'
              land = self.getLandTypeOrOcean(
                x // 2,
                y // 2 - (1 if (y // 2 + x) & 1 else 0)
              )
              #sys.stdout.write(road_a)
              sys.stdout.write(road_a)

              #sys.stdout.write('%02d ' % x)
              #sys.stdout.write('%01dx%01d' % (x, y))
              if 0:
                sys.stdout.write('%01dx%01d' % (
                  x // 2,
                  y // 2 - ((y // 2 + x) & 1)
                ))
              elif 0:
                sys.stdout.write('%02d ' % land)
              elif 1:
                sys.stdout.write(LAND_ART[land][3])
              #sys.stdout.write('   ')
        else:
          #sys.stdout.write('>' if y % 2 == 1 and y // 2 < h else ' ')
          stagger = (y+1) & 2 == 0
          if stagger:
            sys.stdout.write('%s%s%svvvv%s' % (
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
            elif cs & CAMP_WHO_MASK == CAMP_BLOCKED:
              cs = FB_RESET+'+'
            elif cs & CAMP_WHO_MASK == CAMP_FREE:
              cs = FB_RESET+'*'
            else:
              cs = '%s%d' % (FB_RESET, cs & CAMP_WHO_MASK)
              
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
    random.shuffle(remainingSites)
    for player in xrange(1, numPlayers+1):
      numSettlements = 2
      while numSettlements:
        x, y = remainingSites.pop()
        cs = self.getCampsite(x, y)
        print 'valuating campsite (%d,%d) for random placement. value = 0x%04x' % (x, y, cs)
        if cs & CAMP_FREE_MASK != CAMP_FREE:
          print "  can't use"
          continue
        #print 'placing', x, y, player
        self.placeSettlement(x, y, player)
        numSettlements -= 1
  
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

  def neighborsOf(self, x, y):
    '''A generator for campsite coords adjacent to given campsite coords'''
    x2 = x + ( -1 if (y+1) & 2 else 1 )
    y2 = y + ( -1 if  y    & 1 else 1 )
    yield x, y-1
    yield x, y+1
    yield x2, y2
    
  def placeSettlement(self, x, y, player):
    '''Place a settlement if it is allowed; implement side-effects'''
    if self.getCampsite(x, y) & CAMP_FREE_MASK != CAMP_FREE:
      raise IndexError('CAMP UNAVAILABLE')
    if player < PLAYER1 or player > PLAYER6:
      raise ValueError('NO SUCH PLAYER')

    self.setCampsite(x, y, player, ~CAMP_WHO_MASK)

    for x, y in self.neighborsOf(x, y):
      self.blockNearbyCampsite(x, y)

  def campsitesOfTile(self, x, y):
    '''Retrieve campsites lying on a given land hex'''
    w = self.w
    h = self.h
    for x in range(w+1):
      for y in range((h+1)*2):
        yield x, y

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

  def getRoad(self, x, y):
    return self.routes[ y // 2 * (self.w * 3 + 1) + (self.w * 2 if y & 1 else 0) + x ]

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

catan = Catan()
#for y in xrange(catan.h * 2 + 1):
#  for x in xrange(catan.w if y & 1 else catan.w * 2):
#    #sys.stdout.write('%dx%d ' % (x, y))
#    if catan.getRoad(x, y) & CAMP_VOID:
#      sys.stdout.write('.')
#    else:
#      sys.stdout.write('R')
#    #sys.stdout.write('%04x ' % catan.getRoad(x, y))
#  print
#raise SystemExit

print '-- blank init'
#catan.dumpCampSites()
catan.printBoard()

raise SystemExit

print '-- random init'
catan.randomInit(4)
catan.dumpCampSites()
catan.dumpLand()
catan.printBoard()

raise SystemExit
catan = Catan()
print '-- initial board'
catan.dumpCampSites()
catan.printBoard()
tx = int(sys.argv[1])
ty = int(sys.argv[2])

n = 0
for vx, vy in catan.campsitesOfTile(tx, ty):
  catan.setCampsite(vx, vy, n | CAMPOFFLIMITS)
  n = (n+1) % 4

print '-- rect board'
catan.dumpCampSites()
catan.printBoard()
print
