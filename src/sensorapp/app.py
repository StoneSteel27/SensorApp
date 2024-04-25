"""
A Sensor Displaying Android App built with Beeware
"""
import socket
import time
import asyncio
import toga
from toga.style import Pack
from android.widget import Toast
from android.os import HandlerThread, Handler
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT, CENTER
from android.content import Context
from android.hardware import Sensor, SensorEvent, SensorEventListener, SensorManager
from java import dynamic_proxy
from java.lang import Runnable, Thread
import threading

port = 5678


# noinspection PyAttributeOutsideInit
class JavaFunc(dynamic_proxy(Runnable)):
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.func(*self.args, **self.kwargs)


class AccelerometerSocketListener(dynamic_proxy(SensorEventListener)):
    def set_app(self, app):
        self.app = app
        self.label_x = app.x_value
        self.label_y = app.y_value
        self.label_z = app.z_value
        self.streaming_mode = True
        self.count = 0
        self.i = 0
        self.j = 0

    def onSensorChanged(self, event):
        # Get the x, y, and z values of the accelerometer
        x = event.values[0]
        y = event.values[1]
        z = event.values[2]



    def onAccuracyChanged(self, sensor, accuracy):
        pass  # You can handle changes in the accuracy of the sensor

class AccelerometerUIListener(dynamic_proxy(SensorEventListener)):
    def set_app(self, app):
        self.app = app
        self.label_x = app.x_value
        self.label_y = app.y_value
        self.label_z = app.z_value
        self.streaming_mode = True
        self.j = 0

    def onSensorChanged(self, event):
        # Get the x, y, and z values of the accelerometer
        x = event.values[0]
        y = event.values[1]
        z = event.values[2]

        if self.app.connection:
            if self.j == 0:
                t = "Streaming..".rjust(20)
                self.app._impl.native.runOnUiThread(
                    JavaFunc(self.app.set_values, t,t,t))
                self.j = 1
            try:
                self.app.socket.send(f"{time.time()}:{x},{y},{z}".rjust(100).encode("utf-8"))
            except Exception as e:
                self.app._impl.native.runOnUiThread(JavaFunc(self.app.stop_connection))
                message = str(e).split("] ")[1]
                self.app._impl.native.runOnUiThread(JavaFunc(self.app.make_toast, message))


        if not self.app.connection:
            self.j = 0
            self.app._impl.native.runOnUiThread(
                    JavaFunc(self.app.set_values, f"{x:.2f}".rjust(30), f"{y:.2f}".rjust(30), f"{z:.2f}".rjust(30)))


    def onAccuracyChanged(self, sensor, accuracy):
        pass  # You can handle changes in the accuracy of the sensor here




class T(dynamic_proxy(Runnable)):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def run(self):
        if not self.app.connection:
            try:
                self.app._impl.native.runOnUiThread(JavaFunc(self.app.connecting))
                self.app.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.app.socket.connect((self.app.ip_input.value, port))
                self.app.socket.setblocking(False)
                self.app._impl.native.runOnUiThread(JavaFunc(self.app.initialize_connection))
            except Exception as e:
                message = str(e).split("] ")[1]
                self.app._impl.native.runOnUiThread(JavaFunc(self.app.make_toast, message))
                self.app._impl.native.runOnUiThread(JavaFunc(self.app.stop_connection))
        else:
            self.app._impl.native.runOnUiThread(JavaFunc(self.app.stop_connection))


class SensorApp(toga.App):
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.connection = False
        self.acc = None
        self.mHandlerThread = None

        self.main_window = toga.MainWindow(title="Sensor App")

        self.context = self._impl.native.getApplicationContext()

        main_box = toga.Box(style=Pack(direction=COLUMN, background_color="#313135"))
        self.nav_box = toga.Box()
        self.content_box = toga.Box(
            style=Pack(direction=COLUMN, alignment=CENTER, padding=(10, 20), background_color="black"))

        self.nav_button = toga.Button("Back to Home", style=Pack(background_color="#8585ad", color="#313135"),
                                      on_press=self.navigate)
        self.nav_box.add(self.nav_button)

        self.content_label = toga.Label("Accelerometer", style=Pack(color="white", text_align=CENTER, font_size=20))
        self.content = toga.Box(style=Pack(direction=COLUMN, background_color="#5A5A6C", alignment=CENTER, padding=30))
        content_font_size = 18

        label_style = Pack(text_align=LEFT, font_size=content_font_size, color="white")
        value_style = Pack(font_size=content_font_size, color="white", text_align=RIGHT)
        data_box_style = Pack(padding=(10, 10), alignment=CENTER)
        self.x_box = toga.Box(style=data_box_style)
        self.x_label = toga.Label("X :", style=label_style)
        self.x_value = toga.Label("5", style=value_style)

        self.y_box = toga.Box(style=data_box_style)
        self.y_label = toga.Label("Y :", style=label_style)
        self.y_value = toga.Label("5", style=value_style)

        self.z_box = toga.Box(style=data_box_style)
        self.z_label = toga.Label("Z :", style=label_style)
        self.z_value = toga.Label("5", style=value_style)

        self.x_box.add(self.x_label)
        self.x_box.add(self.x_value)
        self.y_box.add(self.y_label)
        self.y_box.add(self.y_value)
        self.z_box.add(self.z_label)
        self.z_box.add(self.z_value)

        self.content.add(self.x_box, self.y_box, self.z_box)
        self.content_box.add(self.content_label, self.content)
        info_box = toga.Box(style=Pack(direction=COLUMN, padding=(0, 20)))
        info_label1 = toga.Label("*Speed of Sensor is reduced to save App ",style=Pack(color="orange", text_align=LEFT,font_size=9))
        info_label2 = toga.Label("resources and will be increased while Streaming",
                                 style=Pack(color="orange", text_align=LEFT, font_size=9))
        info_box.add(info_label1, info_label2)
        self.content_box.add(info_box)
        self.ip_box = toga.Box(style=Pack(direction=COLUMN, padding=(0, 20)))
        self.ip_label = toga.Label("IP Address of Server :", style=Pack(font_size=16, padding_top=10, color="white"))
        self.ip_input = toga.TextInput(placeholder="Enter your Server IP",
                                       style=Pack(font_size=16, background_color="white",
                                                  color="black"))
        self.ip_button = toga.Button("Connect Server", style=Pack(background_color="#8585ad", color="#313135"),
                                     on_press=self.handle_client)
        self.con_box = toga.Box(style=Pack(direction=ROW, padding=(0, 20)))
        self.con_status_label = toga.Label("Connection Status:", style=Pack(font_size=14, color="white"))
        self.con_status = toga.Label("Disconnected", style=Pack(font_size=14, color="red"))
        self.con_box.add(self.con_status_label, self.con_status)

        self.ip_box.add(self.ip_label, self.ip_input, self.ip_button)
        self.content_box.add(self.ip_box, self.con_box)
        main_box.add(self.nav_box)
        main_box.add(self.content_box)

        self.start_accelerometer()

        self.main_window.content = main_box
        self.main_window.show()

    def navigate(self, widget):
        self.make_toast("Not Implemented yet")

    async def handle_client(self, widget):
        t = Thread(T(self))
        t.start()

    def start_accelerometer(self, mode=SensorManager.SENSOR_DELAY_NORMAL):
        self.sensor_manager = (self.app.context.getSystemService(Context.SENSOR_SERVICE))
        acc = self.sensor_manager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)
        self.acc = AccelerometerUIListener()
        self.acc.set_app(self)
        self.mHandlerThread = HandlerThread("AccelerometerUIListener")
        self.mHandlerThread.start()
        self.handler = Handler(self.mHandlerThread.getLooper())
        self.sensor_manager.registerListener(self.acc, acc, mode, self.handler)

    def stop_accelerometer(self):
        if self.acc:
            self.sensor_manager.unregisterListener(self.acc)
            self.acc = None

        if self.mHandlerThread:
            if self.mHandlerThread.isAlive():
                self.mHandlerThread.quitSafely()
                self.mHandlerThread = None

    def initialize_connection(self):
        self.connection = True
        if self.acc and self.mHandlerThread:
            self.stop_accelerometer()
            self.start_accelerometer(mode=SensorManager.SENSOR_DELAY_GAME)
        self.con_status.text = "Connected"
        self.con_status.style.update(color="green")
        self.ip_button.text = "Stop Connection"

    def connecting(self):
        self.con_status.text = "Connecting.."
        self.con_status.style.update(color="orange")

    def stop_connection(self):
        self.connection = False
        if self.acc and self.mHandlerThread:
            self.stop_accelerometer()
            self.start_accelerometer()
        self.con_status.text = "Disconnected"
        self.con_status.style.update(color="red")
        if self.socket:
            self.socket.close()
            self.socket = None
        self.ip_button.text = "Connect Server"

    def make_toast(self, text):
        #print(text)
        Toast.makeText(self.context, text, Toast.LENGTH_SHORT).show()

    def set_values(self, x, y, z):
        self.x_value.text = x
        self.y_value.text = y
        self.z_value.text = z


def main():
    return SensorApp()
