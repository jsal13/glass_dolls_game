import blessed
from blessed import keyboard

t = blessed.Terminal()
for i in range(100):
    print(t.setaf(i) + "Hello!")
