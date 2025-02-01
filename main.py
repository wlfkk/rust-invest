import steammarket as sm
import time as time
import gspread
from datetime import datetime

def sheets_auth():
  gs = gspread.service_account(filename='secret.json')
  sh = gs.open_by_key('1jFAmcVoe21eJSLSGWANeccOdrUMOXKsNZFsp8gtIfDg')
  return sh

def get_items():
  sh = sheets_auth()
  worksheet = sh.worksheet('main')
  itemcolumn = worksheet.col_values(1)
  itemcolumn.pop(0)
  itemcolumn.pop()
  itemcolumn.pop()
  return itemcolumn

def put_arch():
  sh = sheets_auth()
  end = len(sh.worksheet('arch').col_values(1))+1
  st = sh.worksheet('main').col_values(5).pop()
  date = str(datetime.now().strftime("%Y-%m-%d"))
  sh.worksheet('arch').update_cell(end, 1, date)
  sh.worksheet('arch').update_cell(end, 2, st)

def item_price(name):
  item = sm.get_item(252490, name, currency='RUB')
  try:
    price=item['lowest_price']
    try:
      price_int = int(price.split(',')[0])
    except:
      price_int = int(price.split(' ')[0])
  except:
    price_int = 'error'
  return price_int

def main():
  sh = sheets_auth()
  worksheet = sh.worksheet('main')
  items = get_items()
  i = 1
  errnames = []
  for name in items:
    i = i + 1
    print('Processing item:', name)
    price = item_price(name)
    time.sleep(10)
    if price!='error':
      print('Got price:', price, 'for item:', name)
      worksheet.update_cell(i, 5, price)
    else:
      print('Got error during price discovering for item:', name)
      errnames.append(name)
  if len(errnames) > 0:
    print('Error on discovering item price for items:', errnames)
  put_arch()

main()
