# ocr_to_messenger
Read characters from your PC screen and get alerted through a messenger on your phone if certain conditions are met

# Demo
https://youtu.be/cQge6o26k70

# Installation

- install PyCharmCommunity Edition from https://www.jetbrains.com/pycharm/download/other.html
- install python 3 https://www.python.org/downloads/windows/
- follow this https://www.jetbrains.com/pycharm/guide/tips/create-project-from-github/
- use https://github.com/mawwy/ocr_to_messenger.git as URL
- PyCharm asks you to install libraries from requirements.txt, do this
- alternatively follow https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html and install them yourself
- install google tesseract for the character recognition from https://github.com/UB-Mannheim/tesseract/wiki
- edit tesseract path in code if your system installed it to a different path
- on your phone download Telegram and start a conversation with @botfather or visit https://telegram.me/botfather follow his instructions until you get an access token from him
- enter that token into the code at line 18 (telegram_token = "123456:abcdefghjijjqnsadnqwemasdqo")
- Run your code in PyCharm via the menu in the top left https://www.jetbrains.com/help/pycharm/creating-and-running-your-first-python-project.html
- WoW needs to run fullscreen on your main screen for this to work 
- /pos messaged to your bot get you the current position
- /startalarm starts the alarm to spam you when your queue is done
- /stopalarm stops the alarm
- be productive or sleep while in queue

# WARNING
This code reads characters off the center area of your screen and sends them to a bot anyone could talk to. 
If you do not close PyCharm after your queue is done you could potentially leak personal information.

# CLOSE PYCHARM WHEN YOU START PLAYING!

I am not responsible for any harm done
