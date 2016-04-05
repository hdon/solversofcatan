from catan import Catan
from bot import Bot
from time import sleep

catan = Catan()
#print '-- random init'
catan.randomInit(4)
bots = map(lambda n: Bot(catan, n+1), xrange(4))
while 1:
  catan.roll()
  catan.activePlayer = catan.activePlayer % 4 + 1
  bots[catan.activePlayer-1].move()
  catan.printBoard()
  #print catan.playerResources
  #c = raw_input('enter to continue')
  #if c.startswith('q'):
    #raise SystemExit
  sleep(1)
  
#catan.dumpCampSites()
#catan.dumpLand()
#numbers = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
#random.shuffle(numbers)
#for i in xrange(1, 5):
  #tn = numbers.pop()
  #for tx, ty in catan.tilesByTargetNumber[tn]:
    #for x, y in catan.campsitesAtLand(tx, ty):
      #catan.setCampsite(x, y, i, ~CAMP_WHO_MASK)
#print catan.thief
