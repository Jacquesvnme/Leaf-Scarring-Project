import eel

eel.init('templates')                     # Give folder containing web files

print("Establishing bridge...")
print("Connected...")

@eel.expose                         # Expose this function to Javascript
def handleinput(x):
    output = int(x) * 2
    eel.say_hello_js(output)                # Call a Javascript function

eel.start('index.html', size=(1000, 600))    # Start