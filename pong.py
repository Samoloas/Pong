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

st.title("Final Interfaces multimodales")
st.subheader("Poderes Pong")

st.write("activa tus poderes en pong, recita el hechizo que deseas invocar")
st.write("J1")

image = Image.open('fuego.png')
st.image(image)
st.write("Fuego")
image = Image.open('shield.png')
st.image(image)
st.write("barrera")


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
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:  # Removed the non-breaking space here
        st.write(result.get("GET_TEXT"))
        if "GET_TEXT" == "fuego" or "barrera":
            # MQTT Broker Configuration
            broker = "broker.mqttdashboard.com"  # Replace with your broker address
            port = 1883  # Replace with your broker port
            topic = "pong-commands"  # Replace with your topic name

            # Create MQTT client
            client = paho.Client("pong-player")

            # Define on_publish callback
            def on_publish(client, userdata, mid, status):
                if status == 0:
                    print("Message published successfully")
                else:
                    print("Failed to publish message")

            # Connect to MQTT broker
            client.connect(broker, port)

            # Prepare message to publish
            poder = json.dumps({"poder": result.get("GET_TEXT")})

            # Publish message to the topic
            client.publish(topic, poder)

            # Disconnect from MQTT broker
            client.disconnect()

