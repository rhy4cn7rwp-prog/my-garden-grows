"""Run with python3 tests/browser_smoke.py; starts its own local server."""
import os
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright
root = Path(__file__).resolve().parents[1]
server = ThreadingHTTPServer(('127.0.0.1', 0), partial(SimpleHTTPRequestHandler, directory=str(root)))
Thread(target=server.serve_forever, daemon=True).start()
try:
 with sync_playwright() as p:
  browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
  page = browser.new_page(viewport={'width':390,'height':844}, is_mobile=True, has_touch=True, device_scale_factor=3)
  page.set_default_timeout(5000)
  assert page.evaluate('navigator.maxTouchPoints') > 0
  errors=[]
  page.on('pageerror', lambda e: errors.append(str(e)))
  page.goto(os.environ.get('PREVIEW_URL', f'http://127.0.0.1:{server.server_port}/development/'))
  page.get_by_role('button',name='Dream Shop',exact=True).tap()
  page.locator('.spot').first.tap()
  page.get_by_role('button',name='🎯 Choose this dream',exact=True).tap()
  assert page.evaluate('state.goal')==0
  page.get_by_role('button',name='Home',exact=True).tap()
  page.get_by_role('button',name='🧺 Market Supplies',exact=True).tap()
  page.locator('.spot').last.tap()
  assert 'Required for by-the-pound sales' in page.locator('body').inner_text()
  page.get_by_role('button',name='Close ✕',exact=True).tap()
  page.get_by_role('button',name='Home',exact=True).tap()
  page.get_by_role('button',name='Seed & Feed',exact=True).tap()
  page.get_by_role('button',name='Corn seeds',exact=True).tap()
  page.get_by_role('button',name='+',exact=True).tap()
  page.get_by_role('button',name='🛒 View basket',exact=True).tap()
  page.get_by_role('button',name='Pay at checkout',exact=True).tap()
  assert page.evaluate('state.cash')==48
  page.get_by_role('button',name='Close ✕',exact=True).tap()
  page.get_by_role('button',name='Home',exact=True).tap()
  page.get_by_role('button',name='My Garden',exact=True).tap()
  page.locator('.plot').first.tap()
  page.get_by_role('button',name='🌽 Corn (1)',exact=True).tap()
  page.get_by_role('button',name='🌱 Plant plan (1)',exact=True).tap()
  assert page.evaluate('state.plots[0].id')=='corn'
  for _ in range(5):
   page.get_by_role('button',name='💧 Water all',exact=True).tap()
   page.get_by_role('button',name='☀️ End day',exact=True).tap()
  page.locator('.plot').first.tap()
  page.get_by_role('button',name='🧺 Harvest',exact=True).tap()
  assert page.evaluate('state.inventory.corn')==2
  page.get_by_role('button',name='Close ✕',exact=True).tap()
  page.get_by_role('button',name='Home',exact=True).tap()
  page.get_by_role('button',name='Farmers Market',exact=True).tap()
  page.get_by_role('button',name='🧺 Arrange produce / open market',exact=True).tap()
  page.get_by_role('button',name='+',exact=True).tap()
  page.get_by_role('button',name='Open market',exact=True).tap()
  page.get_by_role('button',name='Welcome next customer',exact=True).tap()
  page.get_by_role('button',name='😊 Welcome! What can I get you?',exact=True).tap()
  page.get_by_role('button',name='🧺 Fill customer basket',exact=True).tap()
  page.get_by_role('button',name='+',exact=True).tap()
  page.locator('#total-answer').fill('3')
  page.get_by_role('button',name='⚖️ Check total / collect payment',exact=True).tap()
  page.get_by_role('button',name='💵 Count change',exact=True).tap()
  page.get_by_role('button',name='$1',exact=True).tap()
  page.get_by_role('button',name='$1',exact=True).tap()
  page.get_by_role('button',name='Give change',exact=True).tap()
  assert page.evaluate('state.cash')==51
  page.reload()
  assert page.evaluate('state.cash')==51
  page.evaluate("localStorage.setItem('mgg10','{broken')")
  page.reload()
  assert page.evaluate('state.cash')==51
  page.evaluate("localStorage.setItem('mgg10','{broken');localStorage.setItem('mgg10-backup','{broken')")
  page.reload()
  assert page.evaluate('state.cash')==50
  assert not errors, errors
  assert page.locator('.stage').evaluate('(e)=>getComputedStyle(e).backgroundImage.includes("assets/")')
  print('PASS: touch-only iPhone-sized viewport purchase → plan → water/grow → harvest → greet/order → calculate/pay/change → reload → corrupt-save recovery; no page errors')
  browser.close()
finally:
 server.shutdown()
