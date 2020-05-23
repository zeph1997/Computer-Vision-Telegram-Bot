import telebot
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionResultDimensionUnit
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

TOKEN = "<Telegram API Token>"

bot = telebot.TeleBot(TOKEN)

sub_key = "<Your Subscription Key>"
endpoint = "<Your Endpoint URL>"

computervision_client = ComputerVisionClient(endpoint,CognitiveServicesCredentials(sub_key))

@bot.message_handler(commands=["start"])
def start_up_message(m):
    bot.send_message(m.chat.id,"Hello! I am Recycable Bot! Send me a picture of the item in question and I will tell you if it is recycable or not!")


@bot.message_handler(content_types=["photo"])
def receive_photo(m):
    bot.send_message(m.chat.id,"received photo")
    image_url = bot.get_file_url(m.photo[0].file_id)
    image_result = computervision_client.detect_objects(image_url)
    if len(image_result.objects) == 0:
        bot.send_message(m.chat.id,"I am unable to identify what is in the picture. Please take another picture.")
    else:
        maxConfidence = 0
        outputItem = ""
        for item in image_result.objects:
            if item.confidence > maxConfidence:
                outputItem = item.object_property
                maxConfidence = item.confidence
        bot.send_message(m.chat.id,f"I am {maxConfidence*100:.2f}% confident that this is: {outputItem}")

bot.polling()