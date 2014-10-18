facebook-shenanigans

OVERVIEW

Currently, this project only contains code to cheat one's way to the top of a
Facebook "poke war." Sign into your Facebook account in the command line, 
provide a list of people who the program has permission to poke, and then 
anyone who pokes your Facebook account will automatically be poked back.

INSTRUCTIONS

To start auto-poking people, open two tabs in Terminal and navigate to the
directory containing the fb_session.py and autopoke.py files.

In one tab, type "python fb_session.py 1234" to start the fb_session socket 
server on port 1234. You will be prompted for your Facebook login credentials. 
If the API can authenticate you successfully, then you should see a message
indicating that a server has started on port 1234.

In the other tab, type "python autopoke.py 1234 2" to start the autopoke
script. With these arguments, it will check for new pokes every two seconds
and poke people back through the fb_session server running on port 1234.

You will be prompted to enter the names of people who the program has
permission to poke back. Please use your victims-- I mean, friends full names,
as they are shown on Facebook. For example, to allow my autopoke script to
poke Bob Jones, I would enter "Bob Jones" at the "We can poke: " prompt.

Then work on something else productive while people get frustrated trying to 
poke you.

FILES

fb_session.py

fb_session uses Facebook's HTTP API to log in with the provided account
credentials. A Requests session is created, allowing further HTTP requests
with Facebook without requiring an additional login. A socket server is then
created to allow processes to send requests through this session.

autopoke.py

autopoke.py sends HTTP requests through an active fb_session server. The script
parses Facebook's HTML responses to find recent pokes, and then sends a GET
request to poke those accounts back. This repeats until the process is
terminated.

NOTES

Running the session in a separate process seems, and indeed is, an unecessary
layer of complexity. I made this design choice when debugging the Facebook
API so as to avoid needing to log in over a hundred times in the scope of a
day. Initially, the session existed within autopoke.py, but I quickly
ran up against a Facebook security setting that began imposing a Captcha
whenever I tried to log in. The fb_session server allowed me to keep one
connection open while debugging the autopoke.py file, where most of the tricky
code was.

Going forward, I will likely remove the socket server element to this code and
instead save cookie data to disk to avoid the login bombardment issue. Still,
it was fun to learn how to use socket servers in Python.