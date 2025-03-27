import pyttsx3
import speech_recognition as sr
import telebot
import os
import wikipedia

bot = telebot.TeleBot("token:)", parse_mode=None)
wikipedia.set_lang('uk')

#text to audio
@bot.message_handler(content_types=['text'])
def text_recognation(message):
	engine = pyttsx3.init()
	# delete file if it exists
	if os.path.exists("text.ogg"):
		os.remove("text.ogg")
	# save audio to .ogg format
	engine.save_to_file(message.text,'text.ogg')
	engine.say(message.text)
	engine.runAndWait()
	#open and send the result
	audio = open('text.ogg','rb')
	bot.send_voice(message.chat.id,audio)

#audio to text
@bot.message_handler(content_types=['voice'])
def audio_recognation(message):
	#first of all we need to save the voice on the PC
    #delete file if it exists
	if os.path.exists("voice.ogg"):
		os.remove("voice.ogg")
	if os.path.exists("audio.wav"):
		os.remove("audio.wav")
	#
	file_info =  bot.get_file(message.voice.file_id)
	downloaded_file = bot.download_file(file_info.file_path)
	with open('voice.ogg','wb') as new_file:
		new_file.write(downloaded_file)
	#convert .ogg to .wav
	#x = AudioSegment.from_file('voice.ogg')
	#x.export('audio.wav', format='wav')
	os.system(f'ffmpeg -i voice.ogg audio.wav')
	# recognize the audio to text
	recognizer = sr.Recognizer()
	speech = sr.AudioFile('audio.wav')
	with speech as source:
		recognizer.adjust_for_ambient_noise(source, duration=2)
		audio = recognizer.record(source)
		recognized_data = recognizer.recognize_google(audio,language='uk').lower()
		try:
			wiki_answer = wikipedia.summary(recognized_data,sentences=5)
		except:
			wiki_answer = f'На жаль, за пошуковим запитом "{recognized_data}" нічого не знайдено'
	bot.send_message(message.chat.id,wiki_answer) 

bot.infinity_polling()
