from gtts import gTTS
from playsound import playsound
audio='rent.mp3'
language='en'
sp=gTTS(text="Hello Everyone.  This is a  Rent Management System Project based on Django. There are 3 models. Rent, Landlord and Tenant. ", lang=language, slow=False)
sp.save(audio)
playsound(audio)