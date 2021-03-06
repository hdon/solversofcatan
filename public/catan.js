var canvas, draw;
var tileHeight = 60, tileWidth = Math.sin(Math.PI / 3) * 60, tileFall = tileHeight * 0.75;
var game;
//var tileWidth = 60, tileHeight = 60;
var tileColors = '#fc5 green #c33 #7c3 #cc2 #8c8c8c blue'.split(' ');
var portColors = 'black green #c33 #7c3 #cc2 #8c8c8c magenta'.split(' ');
var playerColors = '#fff #f00 #0f0 #00f #c5c'.split(' ');

var SAND = 0
  , WOOD = 1
  , CLAY = 2
  , WOOL = 3
  , WHEAT = 4
  , STONE = 5
  , OCEAN = 6
  , RESOURCE_STR = [ 'sand', 'wood', 'clay', 'wool', 'wheat', 'stone', 'water' ]
  ;

var CAMP_WHO_MASK   = 0x0007
  , PLAYER1         = 0x0001
  , PLAYER2         = 0x0002
  , PLAYER3         = 0x0003
  , PLAYER4         = 0x0004
  , PLAYER5         = 0x0005
  , PLAYER6         = 0x0006
  , CAMP_BLOCKED    = 0x0007
  , CAMP_SIZE_MASK  = 0x0008
  , CAMP_SETTLEMENT = 0x0000
  , CAMP_CITY       = 0x0008
  , CAMP_VOID       = 0x8000
  , CAMP_FREE_MASK  = CAMP_VOID | CAMP_WHO_MASK
  , CAMP_FREE       = 0x0000
  ;

var CAMP_PORT_BIT_SHIFT = 4
  , CAMP_PORT_MASK  = 0x0070
  , CAMP_PORT_NONE  = 0x0000
  , CAMP_PORT_WOOD  = 0x0010
  , CAMP_PORT_CLAY  = 0x0020
  , CAMP_PORT_WOOL  = 0x0030
  , CAMP_PORT_WHEAT = 0x0040
  , CAMP_PORT_STONE = 0x0050
  , CAMP_PORT_341   = 0x0060
  ;

$(function() {
  canvas = document.querySelector('canvas');
  draw = canvas.getContext('2d');
  draw.imageSmoothingEnabled = false;
  draw.fillStyle = 'black';
  draw.fillRect(0, 0, 480, 480);

  lol();
});

function lol()
{
  $.get('/game.json', function(data) {
    game = data;
    drawBoard();
    lol();
  });
}

function drawBoard()
{
  var x, y, land;

  draw.fillStyle = '#000';
  draw.fillRect(0, 0, canvas.width, canvas.height);

  for (y=0; y<game.h; y++)
    drawLand(-1, y, OCEAN);
  for (x=-1; x<game.w; x++)
  {
    drawLand(x, -1, OCEAN);
    drawLand(x, game.h, OCEAN);
  }
  for (x=0; x<game.w; x++)
  {
    for (y=0; y<game.h; y++)
    {
      land = game.land[y * game.w + x];
      drawLand(x, y, land[0], land[1]);
    }
  }

  drawPorts();
  drawRoutes();
  drawCampsites();
  drawHands();
}

function drawPorts()
{
  var x, y, o;

  drawPort(0, -1, 3, game.campSites[1 + 0 * (game.w+1)]);

  drawPort(-1, 1, 2, game.campSites[0 + 3 * (game.w+1)]);
  drawPort(2, -1, 4, game.campSites[2 + 0 * (game.w+1)]);

  drawPort(-1, 3, 2, game.campSites[0 + 7 * (game.w+1)]);
  drawPort(4, 0, 4, game.campSites[4 + 2 * (game.w+1)]);

  drawPort(0, 5, 1, game.campSites[1 + 10 * (game.w+1)]);
  drawPort(5, 2, 5, game.campSites[5 + 5 * (game.w+1)]);

  drawPort(2, 5, 0, game.campSites[3 + 10 * (game.w+1)]);
  drawPort(4, 4, 0, game.campSites[4 + 9 * (game.w+1)]);
}

function drawPort(x, y, side, port)
{
  var n, stagger;

  stagger = y % 2;

  if (stagger)
    x += 0.5;

  y *= 0.75;
  x++; y++;

  draw.globalAlpha = 1;
  draw.fillStyle = '#07f';
  port = (port & CAMP_PORT_MASK) >> CAMP_PORT_BIT_SHIFT;
  draw.fillStyle = portColors[port];

  draw.beginPath();

  n = 0;
  switch (side)
  {
                         case 0: draw.lineTo((x+0.00) * tileWidth, (y+0.25) * tileHeight);
    if (++n == 2) break; case 1: draw.lineTo((x+0.50) * tileWidth, (y+0.00) * tileHeight);
    if (++n == 2) break; case 2: draw.lineTo((x+1.00) * tileWidth, (y+0.25) * tileHeight);
    if (++n == 2) break; case 3: draw.lineTo((x+1.00) * tileWidth, (y+0.75) * tileHeight);
    if (++n == 2) break; case 4: draw.lineTo((x+0.50) * tileWidth, (y+1.00) * tileHeight);
    if (++n == 2) break; case 5: draw.lineTo((x+0.00) * tileWidth, (y+0.75) * tileHeight);
    if (++n == 2) break;         draw.lineTo((x+0.00) * tileWidth, (y+0.25) * tileHeight);
  }
  draw.lineTo((x+.5)*tileWidth, (y+.5)*tileHeight);
  draw.fill();
}

function drawHands()
{
  var i;
  for (i=0; i<4; i++)
    drawHand(0, i*20 + tileFall * (game.h + 4), i);
}

function drawHand(x, y, player)
{
  var iRes, nRes, resources;
  resources = game.playerResources[player];
  for (iRes=0; iRes<resources.length; iRes++)
  {
    draw.fillStyle = tileColors[iRes%6];
    for (nRes=0; nRes<resources[iRes]; nRes++)
    {
      draw.fillRect(x, y, 5, 5);
      x += 6;
    }
  }
}

var dotsByNumber = {
  2: '\u2022', 12: '\u2022'
, 3: '\u2022\u2022', 11: '\u2022\u2022'
, 4: '\u2022\u2022\u2022', 10: '\u2022\u2022\u2022'
, 5: '\u2022\u2022\u2022\u2022', 9: '\u2022\u2022\u2022\u2022'
, 6: '\u2022\u2022\u2022\u2022\u2022', 8: '\u2022\u2022\u2022\u2022\u2022'
};

function drawLand(x, y, res, number)
{
  var stagger;

  stagger = y % 2;

  draw.strokeStyle = tileColors[res];
  draw.fillStyle = tileColors[res];
  draw.globalAlpha = 1;

  if (stagger)
    x += 0.5;

  y *= 0.75;

  x++; y++; /* make room for ports */
  draw.beginPath((x+0.00) * tileWidth, (y+0.25) * tileHeight);
  draw.lineTo   ((x+0.50) * tileWidth, (y+0.00) * tileHeight);
  draw.lineTo   ((x+1.00) * tileWidth, (y+0.25) * tileHeight);
  draw.lineTo   ((x+1.00) * tileWidth, (y+0.75) * tileHeight);
  draw.lineTo   ((x+0.50) * tileWidth, (y+1.00) * tileHeight);
  draw.lineTo   ((x+0.00) * tileWidth, (y+0.75) * tileHeight);
  draw.lineTo   ((x+0.00) * tileWidth, (y+0.25) * tileHeight);
  draw.fill();

  /* draw numbers */
  if (number)
  {
    draw.fillStyle = '#fff';
    draw.font = '12px Georgia';
    draw.textAlign = 'center';
    draw.globalAlpha = 1;
    draw.fillText(number, (x+0.5) * tileWidth, (y+0.5) * tileHeight);
    if (number != 6 && number != 8)
      draw.globalAlpha = 0.5;
    draw.fillText(dotsByNumber[number], (x+0.5) * tileWidth, (y+0.5) * tileHeight + 12);
  }
}

function drawCampsites()
{
  var x, y, campSite;
  for (y=0; y<(game.h+1)*2; y++)
  for (x=0; x<game.w; x++)
  {
    campSite = game.campSites[y * (game.w+1) + x];
    if (campSite != CAMP_VOID)
      drawCampsite(x, y, campSite);
  }
}

var RAINBOW = 'red orange yellow green blue purple'.split(' ');

function drawCampsite(x, y, campSite)
{
  var ox, oy;

  if (x < 0 || game.w*2 <= x || y < 0 || (game.h+1)*2 <= y)
    throw new Exception('Campsite ('+x+','+y+') out of bounds');

  ox = tileWidth  - 2.5;
  oy = tileHeight - 2.5;
  if (((y+1)&2)==0) ox += tileWidth / 2;
  if (y%2) oy += tileHeight * 0.25;

  if (campSite == CAMP_VOID)
  {
    return;
  }
  else if ((campSite & CAMP_FREE_MASK) == CAMP_FREE)
  {
    return;
  }
  else if ((campSite & CAMP_WHO_MASK) == CAMP_BLOCKED)
  {
    return;
  }

  draw.fillStyle = '#fff';
  draw.globalAlpha = 1;
  draw.fillRect(x * tileWidth + ox - 1, Math.floor(y/2) * tileHeight * .75 + oy - 1, 7, 7);

  draw.fillStyle = playerColors[campSite & CAMP_WHO_MASK];
  draw.globalAlpha = 1;
  draw.fillRect(x * tileWidth + ox, Math.floor(y/2) * tileHeight * .75 + oy, 5, 5);
}

function drawRoute(x, y, route)
{
  var ox, oy;

  if (x < 0 || game.w*2 <= x || y < 0 || (game.h+1)*2 <= y)
    throw new Exception('Route ('+x+','+y+') out of bounds');

  ox = tileWidth  - 2.5;
  oy = tileHeight - 2.5;
  if (((y+1)&2)==0) ox += tileWidth / 2;
  if (y%2) oy += tileHeight * 0.25;

  if (campSite == CAMP_VOID)
  {
    return;
  }
  else if ((campSite & CAMP_FREE_MASK) == CAMP_FREE)
  {
    return;
  }
  else if ((campSite & CAMP_WHO_MASK) == CAMP_BLOCKED)
  {
    return;
  }

  draw.fillStyle = '#fff';
  draw.globalAlpha = 1;
  draw.fillRect(x * tileWidth + ox - 1, Math.floor(y/2) * tileHeight * .75 + oy - 1, 7, 7);

  draw.fillStyle = playerColors[campSite & CAMP_WHO_MASK];
  draw.globalAlpha = 1;
  draw.fillRect(x * tileWidth + ox, Math.floor(y/2) * tileHeight * .75 + oy, 5, 5);
}

function getRoadIndex(x, y)
{
  if (y < 0 || y >= (game.h + 1) * 2 - 1 || x < 0 || x >= (y & 1 ? game.w : game.w * 2))
    throw new Exception('road index ('+x+','+y+') out of bounds');
  return Math.floor(y/2) * game.w * 3 + (y & 1 ? game.w * 2 : 0) + x;
}
function getRoad(x, y)
{
  return game.routes[getRoadIndex(x, y)];
}
function drawRoutes()
{
  var x, y, route, ox, oy;
  for (y=0; y<game.h*2+1; y++)
  for (x=0; x<(y&1?game.w:game.w*2); x++)
    drawRoute(x, y, getRoad(x, y));
}
function drawRoute(x, y, route)
{
  var player;
  if (route == CAMP_VOID)
    return;

  player = route & CAMP_WHO_MASK;

  draw.fillStyle =
  draw.strokeStyle =
    playerColors[player];

  if (y % 2 == 0)
  {
    draw.lineWidth = 2;
    if (((y&2)==0) != ((x&1)==0)) {
      draw.beginPath((x+3) / 2 * tileWidth, (y+2) / 2 * tileFall + 0.50 * tileHeight);
      draw.lineTo   ((x+2) / 2 * tileWidth, (y+2) / 2 * tileFall + 0.25 * tileHeight);
      draw.lineTo   ((x+3) / 2 * tileWidth, (y+2) / 2 * tileFall + 0.50 * tileHeight);
      draw.stroke();
    } else {
      draw.beginPath((x+2) / 2 * tileWidth, (y+2) / 2 * tileFall + 0.50 * tileHeight);
      draw.lineTo   ((x+3) / 2 * tileWidth, (y+2) / 2 * tileFall + 0.25 * tileHeight);
      draw.lineTo   ((x+2) / 2 * tileWidth, (y+2) / 2 * tileFall + 0.50 * tileHeight);
      draw.stroke();
    }
  }
  else
  {
    if (y & 2) x += 0.5;
    draw.fillRect((x+1) * tileWidth-1, (y+0.35) / 2 * tileFall + tileFall, 2, tileFall * 0.66);
  }
}

function resources()
{
  game.playerResources.forEach(function(rez, player) {
    rez.forEach(function(quantity, rezType) {
      console.log('player', player, '/', playerColors[player+1], 'has', quantity, RESOURCE_STR[rezType]);
    });
  });
}
