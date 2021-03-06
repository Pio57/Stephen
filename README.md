# Stephen

 ![alt text](https://i.pinimg.com/originals/36/b2/7c/36b27cb0ad7592535d6a939368e4a3ea.gif) 

Stephen è un chatbot che si occupa di assistere i programmatori durante lo 
sviluppo di un bot, cercando di rispondere a quante più domande possibili.

Questo bot è stato realizzato tramite [Azure Bot Framework](https://dev.botframework.com), e sono state implementate:

- Più conversazioni utilizzando i Dialogs
- Gestite le interruzioni dell'utente come "Help" o "Cancel".

## Architettura del Bot 

![](img/BotArchitecture.png)

## Prerequisiti 

### Python
[Python](https://www.python.org/downloads/) versione 3.10.

```bash
#Verificare la versione di pyhon 
Python --version
```

## Per eseguire il Bot in locale

- Clonare il repository
```bash
git https://github.com/Pio57/Stephen.git
```
- Aprire un terminale nella cartella del progetto clonato
- Nel terminale digitare `pip install -r requirements.txt`
- Avviare il bot tramite `python app.py`



## Testare il Bot 

Per testare il bot è stato usato [Bot Framework Emulator](https://github.com/microsoft/botframework-emulator) è un'applicazione desktop che consente agli sviluppatori di bot di testare ed eseguire il debug dei loro bot su localhost o in esecuzione in remoto attraverso un canale.

### Connettere il bot a  Bot Framework Emulator

- Avvia Bot Framework Emulator
- File -> Open Bot
- Inserire l'URL : `http://localhost:3978/api/messages`

## Documentazione

Al seguente link è riportata tutta la documentazione prodotta durante la fase di
analisi in letteratura : [Data extraction](https://docs.google.com/spreadsheets/d/17tolV3Zc31x7tGw9ly5XD17nF1s1NVqw/edit?usp=sharing&ouid=110944671384119523236&rtpof=true&sd=true)