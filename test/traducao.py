from googletrans import Translator

translator = Translator()
input_text = 'This is a exemples of a text to translate. Using python script and for finish "Hello World"'

# Detectando automaticamente o idioma de entrada
detected_language = translator.detect(input_text).lang

# Traduzindo o texto para o português de Portugal
translation = translator.translate(input_text, src=detected_language, dest='pt')

print("Texto original:", input_text)
print("Tradução para pt-pt:", translation.text)
