"""Click independently measured illustration landmarks, not hotspot element centers."""
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
# Pixel landmarks on the original 512px artwork: object center and two interior edges.
landmarks={
 'seeds': [('carrot','Carrots Seeds',94,322,34,70),('corn','Corn Seeds',181,322,34,70),
 ('beans','Green beans Seeds',268,322,34,70),('strawberry','Strawberries Seeds',358,322,38,70),
 ('cucumber','Cucumbers Seeds',448,322,34,70),('tomato','Tomatoes Seeds',94,443,34,70),
 ('lettuce','Lettuce Seeds',181,443,34,70),('radish','Radishes Seeds',268,443,34,70),
 ('onion','Onions Seeds',358,443,38,70),('potato','Potatoes Seeds',448,443,34,70)],
 'dream': [('ball','Soccer ball',74,204,34,60),('bike','Bicycle',150,405,130,90),
 ('tablet','Tablet',458,196,34,70),('guitar','Guitar',465,350,38,100),
 ('camera','Camera',360,385,50,70),('puppy','Puppy fund',346,261,60,55)],
 'supplies': [('table','Wooden market table',145,230,130,75),
 ('canopy','Striped shade canopy',366,230,140,80),
 ('bags','10 brown paper bags',161,374,80,85),('scale','Produce weighing scale',358,371,80,80)]
}
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(root)))
Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  clicks=0
  for width,height in [(320,740),(390,844),(768,1024),(1440,900)]:
   page=b.new_page(viewport={'width':width,'height':height});page.set_default_timeout(3000)
   errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto(f'http://127.0.0.1:{server.server_port}/development/')
   for scene,items in landmarks.items():
    page.evaluate('(scene)=>go(scene)',scene)
    box=page.locator('.stage').bounding_box()
    for id,title,x,y,w,h in items:
     for dx,dy in [(0,0),(-w/2,-h/2),(w/2,h/2)]:
      px=box['x']+(x+dx)/512*box['width'];py=box['y']+(y+dy)/512*box['height']
      # Assert the actual object landmark lands on the intended target, even with zoom/scaling.
      action=page.evaluate('([x,y])=>document.elementFromPoint(x,y)?.closest("button")?.getAttribute("onclick")',[px,py])
      assert action and f"'{id}'" in action,(width,scene,id,action)
      page.mouse.click(px,py)
      assert title in page.locator('.dialog h2').inner_text(),(width,scene,id)
      page.get_by_role('button',name='Close ✕',exact=True).click();clicks+=1
   assert not errors,errors
   page.screenshot(path=f'/tmp/garden-hotspots-{width}.png')
   page.close()
  # Verify packaged download runs without external asset requests.
  page=b.new_page();requests=[];page.on('request',lambda r:requests.append(r.url))
  page.goto(f'http://127.0.0.1:{server.server_port}/playtest/My-Garden-Grows-1.0.html')
  page.get_by_role('button',name='Seed & Feed',exact=True).click()
  page.get_by_role('button',name='Carrots seeds',exact=True).click()
  assert 'Carrots Seeds' in page.locator('.dialog h2').inner_text()
  assert len(requests)==1,requests
  print(f'PASS: {clicks} illustration-landmark taps at 320, 390, 768, 1440px; all 20 products; standalone playtest has no external requests')
  b.close()
finally:server.shutdown()
