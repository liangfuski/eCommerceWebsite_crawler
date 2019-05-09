from etsy_cookies import etsycookies

lua_script2 = """
function main(splash, args)
   local function search_for_shopping_button()
     shopping_fee_button = splash:select(splash.args.button)
         if  not shopping_fee_button then
             error('no such button is found')
         else
             shopping_fee_button:mouse_click()
         end
     assert (splash:wait(1))
     input = splash:select('input.estimate-postal-code.input.input-large-mweb')
         if not input then 
              error('no input is found')
          else 
              input:mouse_click()
              splash:send_text('90002')
         end
     end

splash.images_enabled = false
splash:init_cookies(args.cookies)   -- setting cookies so that the web is show in US format
assert (splash:go(args.url))
assert (splash:wait(1))
search_for_shopping_button()
assert (splash:wait(5))
splash:set_viewport_full()
local screenshot = splash:png()
return {
    html = splash:html(),
    screenshot = screenshot,
     har  = splash:har()}
end"""

splash_args2 = {
                    'lua_source': lua_script2,
                    'button': "#estimated-shipping-variant > div > div:nth-child(2) > div:nth-child(1) > div > div > button",
                    'input': 'splash.args.input',
                    'cookies': etsycookies
                }

'''
the button tag with text 'Get shipping cost is selected '
this button tag is depended on the location of the client, this assume 
if the client is from Taiwan , the button will be 'Taiwan' and the 
css path of it it become 'a.button-destination text-link-secondary text-link-underline'
input tag with a class name est...web is selected
'''
'''
button:contains('Get shipping cost') is a jquery locator , we have to use css selector instead as 
parameter of splash:select_all(splash.args.button). 

'''

lua_script1 = '''
function main(splash, args)
  splash:init_cookies(args.cookies)   -- setting cookies so that the web is show in US format 
  splash.images_enabled = false       -- turn off the image on a website 
  assert(splash:go(args.url))
  return {html = splash:html(),
          har  = splash:har()}
end
'''


