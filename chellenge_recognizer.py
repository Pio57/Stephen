from botbuilder.core import Recognizer, RecognizerResult, TurnContext
from botbuilder.dialogs import WaterfallStepContext


class ChallengeRecognizer(Recognizer):
    challenges = {"Acknowledges challenge" : "AcknowledgesChallenge",
                  "Insert new challenge" : "InsertChallenge",
                  "Remove challenge" : "RemoveChallenge" ,
                  "Development challenges" : "DevelopmentChallenges",
                  "Use challenges" : "UseChallenges",
                  "High Dependence on Data/high data quality": "Per il nostro agente i dati sono essenziali, quindi dobbiamo sicuramente avere una grande quantità di dati e sopratutto dati di qualità.Quindi oltre ad avere un grande dataset, dobbiamo applicare tutte quelle tecniche di data preparation per pulire al meglio il dataset",
                  "NLP(Natural Language Processing)": "Per l'NLP dobbiamo tenere in considerazione l'intento ovvero le intenzioni dell'utente finale, le entità che sono i metadati dell'intento.\nSe può esserti utile puoi usare Language Understanding (LUIS),è un servizio di intelligenza artificiale conversazionale basato sul cloud che applica l'intelligenza di Machine Learning al testo in linguaggio naturale della conversazione di un utente per prevedere il significato generale ed estrarre informazioni pertinenti e dettagliate. ",
                  "Maintenance":"Per la manutenzione ci sono 3 fasi principali:\n\n- HyperCare, dove i bot vengono eseguiti sotto stretta sorveglianza.\n\n- Supporto\n\n- Miglioramenti minori",
                  "Development cost": "La necessità di formazione continua può diventare costosa, con l'utilizzo di piattaforme di modellazione SaaS AI/ML questapuò essere in qualche modo evitata utilizzando soluzioni invece di assumere un team completo di data science per modellare e allenare un bot.\nInoltre possiamo optare per tool e framework open source per diminuire ancora di più questo costo di sviluppo.",
                  "Secure data":"Per la sicurezza del bot:\n\n- Il bot deve scambiare dati utilizzando un protocollo HTTPS\n\n- Eliminare i messaggi contenenti i dati sensibili non appena non sono più necessari\n\n- La best practice prevede di archiviare le informazioni in uno stato sicuro per un certo periodo di tempo e poi di scartarle in un secondo momento dopo che hanno raggiunto il loro scopo\n\n-  Rafforzare il DB",
                  "Machine learning": "Usare algoritmi di machine learning per capire continuamente i diversi modi in cui i clienti pongono le domande",
                  "Respond slowly": "Per l'usabilità deobbiamo rendere le conversazioni con il bot quanto più simili a quelle umane. Quindi le conversazioni dovrebbero essere naturali, creative ed emotive.",
                  "Integration": "Per l'integrazione è consigliato utilizzare le API",
                  "Privacy concerns": "Per quanto riguarda i concetti di privacy ossiamo agire in più modi :\n\n- Autenticazione e autorizzazione : questo sicuramente quando si sta lavorando con i dati del cliente.\n\n- Crittografia end-to-end: che è molto comoda in quanto permette la comunicazione in cui solo le due parti possono leggere i messaggi.\n\n- Messaggi autodistruttivi: Utilizzati per andare ad eliminare tutti quei messaggi che contengono informazioni personali.",
                  "Accessibility":"Per questa challenge dobbiamo prevedere che il bot offri sia un interfaccia visiva che audio, questo proprio per permettere l'utilizzo del bot a tutti i potenziali utenti, senza distinzione di capacità e competenze linguistiche",
                  "Noise": "Una soluzione è costruire strategicamente, cioèidentifichiamo un obbiettivo specifico di ciascun bot, in modo da evitare che un bot faccia tantissime cose, e strutturare le iterazioniattorno all'azione che desideri che l'utente intraprenda.",
                  "Ethics": "Per affrontare l'etica ci viene consigliato:\n\n- Di essere TRASPARENTI con chi utilizza il bot(fargli capire che non sta interagendo con una vera persona)\n\n- Evitare di di rafforzare i ruoli di genere(evitare lo stereotipo della 'donna sottomessa')\n\n- Arte della comunicazione",
                  "Trust/reliability": "\n\n- Imposta aspettative chiare su cosa può fare chi utilizza il bot\n\n- Rendi l'esperienza fluida\n\n- Rendere coerente ogni iterazione\n\n- Rassicurare gli utenti in merito alle proprie misure di sicurezza",
                  "Interruption": "",
                  "Choosing a bot / Configuring a bot": "\n\n- Impostare un obiettivo per il chatbot\n\n- Dare una personalità al chatbot, anche in base ai clienti con cui si relaziona",
                  "Lack of understanding of intent": "Per comprendere gli intenti ci sono vari modi:\n\n- Usare alberi decisionali più forti\n\n- Applichiamo tecniche di Machine learning per la miglior comprensione dell'intendo dell'utente\n\n- NLP",
                  "Too long answers": "Di solito un bot offre agli utenti contenuti informativi e interessanti, per divulgare ciò sicuramente le informazioni saranno tante e conviene inviare più messaggi brevi anzichè uno lungo.",
                  "Solve everything": "Si consiglia che se il bot non riesce ad esaudire una richiesta dell'utente, in quanto non è una richiesta comune, allora si drovrà passare il rapidamente il controllo ad un operatore umanoin modo da evitarre che l'esperienza del cliente ne risente.",
                  "Lack of information about the bot": "E' importante che nel messaggio di presentazione il botelenchi in anticipo le sue funzioni, in modo che l'utente sappia interagire con esso.",
                  "Wrong actions/wrong information": "Di solito i bot durante il loro utilizzo apprendono nuove informazioni, questi informazioni possono essere sibuone ma anche cattive.Per evitare che il bot apprenda nozioni cattive dobbiamo : \n\n- Riconoscere il problema.\n\n- Impiegare misure difensive e protettive (Come rigidi controlli di accesso, adottare soluzione di protezione della rete).\n\n- Monitorare e testare la sicurezza.",
                  "Usability": "Per l'usabilità deobbiamo rendere le conversazioni con il bot quanto più simili a quelle umane.Quindi le conversazioni dovrebbero essere naturali, creative ed emotive.",
                  }

    async def recognize(self, step_context: WaterfallStepContext):
        if(self.challenges.keys().__contains__(step_context.result)):
            return self.challenges[step_context.result]
        return None
