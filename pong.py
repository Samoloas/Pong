import paho.mqtt.client as paho
import time
import streamlit as st
import json
import os
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob

from gtts import gTTS

def on_publish(client, userdata, result):
    print("Data published successfully\n")
    pass  # Optional: Add further actions after successful publishing

def on_message(client, userdata, message):
    global message_received
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

broker = "broker.mqttdashboard.com"
port = 1883
client = paho.Client("Pong")
client.on_message = on_message

# Improved Connection Handling (consider persistent connection)
def connect_and_publish(recognized_text):
    client.connect(broker, port)
    poder = json.dumps({"poder": recognized_text})
    client.publish(topic, poder)  # Publish the message with the recognized power

st.title("Final Interfaces Multimodales")
st.subheader("Poderes Pong")

st.write("Activa tus poderes en Pong, recita el hechizo que deseas invocar")
st.write("J1")

image = Image.open('fuego.png')
st.image(image)
st.write("Fuego")
image = Image.open('shield.png')
st.image(image)
st.write("Barrera")


st.write("Toca el Botón y di el hechizo")
stt_button = Button(label="J1", width=200)

stt_button.js_on_event("button_click", CustomJS(code="""
 var recognition = new webkitSpeechRecognition();
 recognition.continuous = true;
 recognition.interimResults = true;
 
 recognition.onresult = function (e) {
 var value = "";
 for (var i = e.resultIndex; i < e.results.length; ++i) {
  if (e.results[i].isFinal) {
  value += e.results[i][0].transcript;
  }
 }
 if ( value != "") {
  document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
 }
 }
 recognition.start();
 """))

result = streamlit_bokeh_events(
    stt_button,  # Remove the non-breaking space here
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)


if result:
    if "GET_TEXT" in result:
        recognized_text = result.get("GET_TEXT")
        st.write("Reconocido:", recognized_text)

        # Publish the message with the recognized power
        connect_and_publish(recognized_text)

        # Consider adding post-processing or feedback after publishing


        

