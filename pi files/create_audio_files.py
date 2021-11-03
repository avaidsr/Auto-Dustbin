from gtts import gTTS
#import os
tts = gTTS(text='Thank You!', lang='en', slow=False)
tts.save("thanks.mp3")
#os.system('mpeg321 good.mp3')