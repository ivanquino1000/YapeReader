import threading
import asyncio
import re
#import pygame
import pyttsx3
from datetime import datetime
import winrt.windows.foundation.metadata as metadata
import winrt.windows.system.diagnostics as diagnostics
import winrt.windows.ui.notifications.management as NotificationManager
import winrt.windows.ui.notifications as Notifications


if metadata.ApiInformation.is_type_present("Windows.UI.Notifications.Management.UserNotificationListener"):
    print("Windows.System.AppDiagnosticInfo type was found")
else:
    print("Windows.System.AppDiagnosticInfo type was NOT found")

# Listener = NoticationManager.UserNotificationListenerAccessStatus


# def play_sound(file_path):
#     pygame.mixer.init()
#     pygame.mixer.music.load(file_path)
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)
#     pygame.mixer.quit()
def text_to_speech(text, language='es'):
    engine = pyttsx3.init()
    try:
        engine.setProperty('rate', 150)
        engine.setProperty('voice', f'{language}')
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"An error occurred in text-to-speech: {e}")
    finally:
        engine.stop()
        
    
# def text_to_speech(text, language='es'):
#     engine = pyttsx3.init()

#     # Set the language for text-to-speech
#     engine.setProperty('rate', 150)  # Speed of speech
#     engine.setProperty('voice', f'{language}')
    
#     engine.say(text)
#     engine.runAndWait()
    
    
def extract_info(input_string):
    # Define a regular expression pattern to capture the name and payment amount
    pattern = re.compile(r'Yape! (.*?) te envió un pago por S/ (\d*\.?\d*)')

    
    # Use the pattern to search for matches in the input string
    match = pattern.search(input_string)
    
    # Check if a match was found
    if match:
        # Extract the name and payment amount from the matched groups
        name = match.group(1)
        amount = match.group(2)
        
        return name, f"S/ {amount}"

    return None, None

# ! Notification Listener - Request Access
async def test():
        listener = NotificationManager.UserNotificationListener.get_current()
        result = await  listener.request_access_async()

        if result == NotificationManager.UserNotificationListenerAccessStatus.ALLOWED:
            print("Access granted. Ready to receive notifications.")
            notifs = await listener.get_notifications_async(Notifications.NotificationKinds.TOAST)
            #print(type(notifs),notifs.get_at(0).app_info.display_info.display_name)
            #now = datetime.now()
            #print(now.day)
            i=0
            #properties = dir(notifs.get_at(0).creation_time)
            #for prop in properties:
            #print(dir(notifs.get_at(0).notification))
            #print(notifs.get_at(0).creation_time.universal_time.real)
            
            
            for n in notifs:
                # ! App Name Checker - "Chrome" 
                appName = n.app_info.display_info.display_name
                if appName  != "Google Chrome":
                    print(appName)
                    continue 
                
                #print(i,n.app_info.display_info.display_name)
                # ! Allowed Notification - Yape OR Noti Sender
                
                NotifMainDiv = n.notification.visual.bindings[0].get_text_elements()[0].text
                NotifDetailsDiv = n.notification.visual.bindings[0].get_text_elements()[1].text
                
                MsgIdPattern = re.compile(r"\bYape\b|\bNoti Sender\b",)
                
                
                #re.search(r"\bYape\b|\bNoti Sender\b",)
                
                if not bool(MsgIdPattern.search(NotifMainDiv)):
                    continue 
                
                sound_file_path = "C:\\Users\\EQUIPO\\Downloads\\yapefx.mp3"

                
                name, amount = extract_info(NotifDetailsDiv)
                print(f"Name: {name}, Amount: {amount}")
                #play_sound(sound_file_path)
                
                
                #threading.Thread(target=play_sound, args=(sound_file_path,)).start()
                t = threading.Thread(target=text_to_speech, args=(f"{name} pagó {amount} Soles",))
                t.start()
                t.join()
                
                #text_to_speech((f"{name} pagó {amount} Soles",))    
                i+=1


            
        else:
            print("Access denied. Unable to receive notifications.")




# Run the event loop
asyncio.run(test())