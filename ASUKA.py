import os
import requests
import speech_recognition as sr

r = sr.Recognizer()

def transcribe_audio():
    while True:
        with sr.Microphone() as source:
            os.system('espeak-ng "En attente de la commande Asuka" -s 150 -v fr')
            print("En attente de la commande 'Asuka'...")

            # Attendre la commande "Asuka"
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio, language="fr-FR")
                if "asuka" in text.lower():
                    print("Asuka est activée. Posez votre question.")
                    os.system('espeak-ng "Asuka est activée. Posez votre question." -s 150 -v fr')

                    # Attendre la question de l'utilisateur
                    audio = r.listen(source)

                    # Convertir la question de l'utilisateur en texte
                    try:
                        question = r.recognize_google(audio, language="fr-FR")
                        print("Question de l'utilisateur: " + question)

                        # Appeler l'action personnalisée sur l'assistant Google avec la question de l'utilisateur
                        webhook_url = "https://MY_WEBHOOK_URL"
                        headers = {'Content-type': 'application/json'}
                        payload = {
                            "queryResult": {
                                "queryText": question
                            }
                        }
                        response = requests.post(webhook_url, headers=headers, json=payload)

                        # Récupérer la réponse générée par l'action personnalisée
                        response_data = response.json()
                        fulfillment_text = response_data['fulfillmentText']
                        media_url = response_data['payload']['google']['richResponse']['items'][1]['mediaResponse']['mediaObjects'][0]['contentUrl']

                        # Jouer la synthèse vocale de la réponse générée
                        os.system(f'ffplay -nodisp -autoexit "{media_url}"')

                    except sr.UnknownValueError:
                        # Si la question de l'utilisateur est incompréhensible
                        print("Je n'ai pas compris la question de l'utilisateur. Veuillez répéter.")
                        os.system('espeak-ng "Je n\'ai pas compris la question de l\'utilisateur. Veuillez répéter." -s 150 -v fr')

                elif "arrêt" in text.lower() or "stop" in text.lower():
                    # Si l'utilisateur veut arrêter le script
                    print("Asuka est mise en veille.")
                    os.system('espeak-ng "Asuka est mise en veille." -s 150 -v fr')
                    break

                else:
                    # Si la commande "Asuka" n'est pas reconnue
                    print("Commande inconnue. Veuillez dire 'Asuka' pour poser une question.")
                    os.system('espeak-ng "Commande inconnue. Veuillez dire Asuka pour poser une question." -s 150 -v fr')

            except sr.UnknownValueError:
                # Si la commande "Asuka" n'est pas reconnue
                print("Commande inconnue. Veuillez dire 'Asuka' pour poser une question.")
                os.system('espeak-ng "Commande inconnue. Veuillez dire Asuka pour poser une question." -s 150 -v fr')

# Transcrire l'audio
transcribe_audio()
