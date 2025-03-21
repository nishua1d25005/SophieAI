from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import speech_recognition as sr
import pyttsx3
import requests
from plyer import tts, notification, filechooser, clipboard
from jnius import autoclass
import os

# Access Android-specific features
Intent = autoclass('android.content.Intent')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Environment = autoclass('android.os.Environment')
MediaPlayer = autoclass('android.media.MediaPlayer')
WifiManager = autoclass('android.net.wifi.WifiManager')
AudioManager = autoclass('android.media.AudioManager')
BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
CameraManager = autoclass('android.hardware.camera2.CameraManager')

class SophieApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.label = Label(text="Tap the button and speak...", font_size=20)
        self.button = Button(text="Listen", font_size=24, on_press=self.listen_command)

        layout.add_widget(self.label)
        layout.add_widget(self.button)

        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.media_player = MediaPlayer()
        self.audio_manager = PythonActivity.mActivity.getSystemService("audio")
        self.camera_manager = PythonActivity.mActivity.getSystemService("camera")
        self.wifi_manager = PythonActivity.mActivity.getApplicationContext().getSystemService(PythonActivity.mActivity.WIFI_SERVICE)
        self.bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()

        return layout

    def speak(self, text):
        """ Make Sophie respond with speech and display text """
        self.label.text = f"Sophie: {text}"
        tts.speak(text)  # Uses Plyer to speak

    def listen_command(self, instance):
        """ Capture voice and process command """
        self.label.text = "Listening..."
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            command = self.recognizer.recognize_google(audio).lower()
            self.label.text = f"You said: {command}"
            self.process_command(command)
        except sr.UnknownValueError:
            self.speak("I didn't understand that.")
        except sr.RequestError:
            self.speak("Speech service is down.")

    def process_command(self, command):
        """ Process user commands """
        if "hello" in command:
            self.speak("Hello! How can I assist you?")

        elif "time" in command:
            from datetime import datetime
            self.speak(f"The time is {datetime.now().strftime('%I:%M %p')}")

        elif "weather" in command:
            self.speak("Fetching weather data...")
            weather = self.get_weather()
            self.speak(weather)

        elif "volume up" in command:
            self.adjust_volume("up")

        elif "volume down" in command:
            self.adjust_volume("down")

        elif "turn on wifi" in command:
            self.toggle_wifi(True)

        elif "turn off wifi" in command:
            self.toggle_wifi(False)

        elif "turn on bluetooth" in command:
            self.toggle_bluetooth(True)

        elif "turn off bluetooth" in command:
            self.toggle_bluetooth(False)

        elif "turn on flashlight" in command:
            self.toggle_flashlight(True)

        elif "turn off flashlight" in command:
            self.toggle_flashlight(False)

        elif "copy to clipboard" in command:
            self.copy_to_clipboard(command.replace("copy to clipboard", "").strip())

        elif "paste from clipboard" in command:
            text = clipboard.paste()
            self.speak(f"Pasting: {text}")

        elif "open" in command:
            self.open_app(command.replace("open", "").strip())

        elif "move file" in command:
            self.move_file()

        elif "delete file" in command:
            self.delete_file()

        elif "rename file" in command:
            self.rename_file()

        elif "play music" in command:
            self.play_music()

        elif "pause music" in command:
            self.pause_music()

        elif "resume music" in command:
            self.resume_music()

        else:
            self.speak("I'm still learning!")

    def get_weather(self):
        """ Fetch weather from OpenWeatherMap (replace 'your_api_key' with actual key) """
        API_KEY = "your_openweathermap_api_key_here"
        city = "your_city_here"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        try:
            weather_data = requests.get(url).json()
            temp = weather_data["main"]["temp"]
            desc = weather_data["weather"][0]["description"]
            return f"The current temperature in {city} is {temp}°C with {desc}."
        except:
            return "Couldn't fetch the weather."

    def adjust_volume(self, direction):
        """ Adjust volume up or down """
        if direction == "up":
            self.audio_manager.adjustVolume(AudioManager.ADJUST_RAISE, AudioManager.FLAG_SHOW_UI)
            self.speak("Volume increased")
        else:
            self.audio_manager.adjustVolume(AudioManager.ADJUST_LOWER, AudioManager.FLAG_SHOW_UI)
            self.speak("Volume decreased")

    def toggle_wifi(self, state):
        """ Turn WiFi on or off """
        self.wifi_manager.setWifiEnabled(state)
        status = "enabled" if state else "disabled"
        self.speak(f"WiFi {status}")

    def toggle_bluetooth(self, state):
        """ Turn Bluetooth on or off """
        if state:
            self.bluetooth_adapter.enable()
            self.speak("Bluetooth enabled")
        else:
            self.bluetooth_adapter.disable()
            self.speak("Bluetooth disabled")

    def toggle_flashlight(self, state):
        """ Turn Flashlight on or off """
        camera_id = self.camera_manager.getCameraIdList()[0]
        if state:
            self.camera_manager.setTorchMode(camera_id, True)
            self.speak("Flashlight turned on")
        else:
            self.camera_manager.setTorchMode(camera_id, False)
            self.speak("Flashlight turned off")

    def copy_to_clipboard(self, text):
        """ Copy text to clipboard """
        clipboard.copy(text)
        self.speak("Text copied to clipboard")

    def open_app(self, app_name):
        """ Open apps based on user command """
        intent = Intent(Intent.ACTION_MAIN)
        intent.addCategory(Intent.CATEGORY_LAUNCHER)
        context = PythonActivity.mActivity.getApplicationContext()
        package_manager = context.getPackageManager()
        app_list = package_manager.getInstalledApplications(0)

        for app in app_list:
            if app_name.lower() in app.loadLabel(package_manager).lower():
                intent.setPackage(app.packageName)
                PythonActivity.mActivity.startActivity(intent)
                self.speak(f"Opening {app_name}")
                return

        self.speak("App not found")

    def move_file(self):
        """ Move a file using file chooser """
        filechooser.open_file(on_selection=self.move_file_selected)

    def move_file_selected(self, selection):
        """ Handle file move operation """
        if selection:
            new_path = os.path.join(Environment.getExternalStorageDirectory().getAbsolutePath(), "NewFolder", os.path.basename(selection[0]))
            os.rename(selection[0], new_path)
            self.speak("File moved successfully")

    def delete_file(self):
        """ Delete a file """
        filechooser.open_file(on_selection=self.delete_file_selected)

    def delete_file_selected(self, selection):
        """ Handle file delete operation """
        if selection:
            os.remove(selection[0])
            self.speak("File deleted successfully")

    def rename_file(self):
        """ Rename a file """
        filechooser.open_file(on_selection=self.rename_file_selected)

    def rename_file_selected(self, selection):
        """ Handle file rename operation """
        if selection:
            new_name = "renamed_file.txt"
            os.rename(selection[0], os.path.join(os.path.dirname(selection[0]), new_name))
            self.speak("File renamed successfully")

if __name__ == "__main__":
    SophieApp().run()
