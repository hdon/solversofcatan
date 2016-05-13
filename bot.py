from catan import *
import random

class Bot:
  def __init__(self, game, player):
    self.game = game
    self.player = player
  def move(self):
    game = self.game
    for move in [ BUY_SETTLEMENT, BUY_ROAD, BUY_CITY, BUY_DEVELOPMENT, END_TURN ]:
      if not game.canIBuy(self.player, move):
        continue
      #print 'bot', self.player, 'evaluating move type', move
      if move == BUY_SETTLEMENT:
        # find a place to put a settlement
        for vy in xrange(game.vh):
          for vx in xrange(game.w):
            camp = game.getCampsite(vx, vy)
            # Is this camp free?
            #print 'evaluating campsite (%d,%d) = %04x' % (vx, vy, camp)
            if camp & CAMP_FREE_MASK == CAMP_FREE:
              # Do we have a road to this settlement?
              #print 'looking for roads to camp (%d,%d)' % (vx, vy)
              for rx, ry in game.roadsTo(vx, vy):
                #print 'road (%d,%d) = %04x' % (rx, ry, game.getRoad(rx, ry))
                if game.getRoad(rx, ry) & CAMP_WHO_MASK == self.player:
                  #print 'bot', self.player, 'placing settlement at', vx, vy
                  game.placeSettlement(vx, vy, self.player)
                  game.buy(self.player, BUY_SETTLEMENT)
                  return
            else:
              pass
              #print 'rejecting camp (%d,%d) because = %04x' % (vx, vy, game.getCampsite(vx, vy))

      elif move == BUY_ROAD:
        # look for roads
        for ry in xrange(game.h * 2 + 1):
          numRoadsInRow = game.w if ry & 1 else game.w * 2
          for rx in xrange(numRoadsInRow):
            # do we own the road?
            road = game.getRoad(rx, ry)
            if road & CAMP_WHO_MASK == self.player:
              print 'evaluating my road (%d,%d) for extension' % (rx, ry)
              # enumerate adjacent campsite
              for vx, vy in game.campsitesFromRoad(rx, ry):
                print '  adjacent campsite: (%d,%d)' % (vx, vy)
                # enumerate adjacent roads
                for rx2, ry2 in game.roadsTo(vx, vy):
                  print '    adjacent road: (%d,%d)' % (rx, ry)
                  road = game.getRoad(rx2, ry2)
                  if road & CAMP_FREE_MASK == CAMP_FREE:
                    game.placeRoad(rx2, ry2, self.player)
                    game.buy(self.player, BUY_ROAD)
                    return

        # find a settlement that belongs to us
        for vy in xrange(game.vh):
          for vx in xrange(game.w):
            if game.getCampsite(vx, vy) & CAMP_WHO_MASK == self.player:
              # is there an empty adjacent road?
              for rx, ry in game.roadsTo(vx, vy):
                if game.getRoad(rx, ry) & CAMP_FREE_MASK == CAMP_FREE:
                  print 'bot', self.player, 'placing road at', rx, ry
                  game.placeRoad(rx, ry, self.player)
                  game.buy(self.player, ROADBUY_ROAD)
                  return
