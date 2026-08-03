from functions import listen, speak, wake, ollama_ ,get_intent,run

wake_word = wake()
if wake_word == "hey celebi":
    speak("Hello, i am say-la-bee")
    user_model = ollama_()
    command = listen()
    get_intent(command)
    run()
    # response = ollama.chat(
    #     model=user_model,
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": command
    #         }
    #     ]
    # )
    #
    # print(response["message"]["content"])