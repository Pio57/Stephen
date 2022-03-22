import os
import json

from chellenge_recognizer import ChallengeRecognizer

from datatypes_date_time.timex import Timex

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult, ComponentDialog
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, CardFactory, turn_context
from botbuilder.schema import InputHints, SuggestedActions, CardAction, ActionTypes, Attachment, HeroCard

from .InterruptDialog import InterruptDialog
from .BestPractices import BestPracticesDialog

class EditChallenge(InterruptDialog):
    challenges = {
                  "BP_HDD_HDQ": "Per il nostro agente i dati sono essenziali, quindi dobbiamo sicuramente avere una grande quantità di dati e sopratutto dati di qualità.Quindi oltre ad avere un grande dataset, dobbiamo applicare tutte quelle tecniche di data preparation per pulire al meglio il dataset",
                  "BP_NLP": "Per l'NLP dobbiamo tenere in considerazione l'intento ovvero le intenzioni dell'utente finale, le entità che sono i metadati dell'intento.\nSe può esserti utile puoi usare Language Understanding (LUIS),è un servizio di intelligenza artificiale conversazionale basato sul cloud che applica l'intelligenza di Machine Learning al testo in linguaggio naturale della conversazione di un utente per prevedere il significato generale ed estrarre informazioni pertinenti e dettagliate. ",
                  "BP_TEST":"Test",
                  "BP_M": "Per la manutenzione ci sono 3 fasi principali:\n\n- HyperCare, dove i bot vengono eseguiti sotto stretta sorveglianza.\n\n- Supporto\n\n- Miglioramenti minori",
                  "BP_DC": "La necessità di formazione continua può diventare costosa, con l'utilizzo di piattaforme di modellazione SaaS AI/ML questapuò essere in qualche modo evitata utilizzando soluzioni invece di assumere un team completo di data science per modellare e allenare un bot.\nInoltre possiamo optare per tool e framework open source per diminuire ancora di più questo costo di sviluppo.",
                  "BC_SC": "Per la sicurezza del bot:\n\n- Il bot deve scambiare dati utilizzando un protocollo HTTPS\n\n- Eliminare i messaggi contenenti i dati sensibili non appena non sono più necessari\n\n- La best practice prevede di archiviare le informazioni in uno stato sicuro per un certo periodo di tempo e poi di scartarle in un secondo momento dopo che hanno raggiunto il loro scopo\n\n-  Rafforzare il DB",
                  "BC_ML": "Usare algoritmi di machine learning per capire continuamente i diversi modi in cui i clienti pongono le domande",
                  "BC_RS": "Per l'usabilità deobbiamo rendere le conversazioni con il bot quanto più simili a quelle umane. Quindi le conversazioni dovrebbero essere naturali, creative ed emotive.",
                  "BP_I": "Per l'integrazione è consigliato utilizzare le API",
                  "BP_PC": "Per quanto riguarda i concetti di privacy ossiamo agire in più modi :\n\n- Autenticazione e autorizzazione : questo sicuramente quando si sta lavorando con i dati del cliente.\n\n- Crittografia end-to-end: che è molto comoda in quanto permette la comunicazione in cui solo le due parti possono leggere i messaggi.\n\n- Messaggi autodistruttivi: Utilizzati per andare ad eliminare tutti quei messaggi che contengono informazioni personali.",
                  "BP_A": "Per questa challenge dobbiamo prevedere che il bot offri sia un interfaccia visiva che audio, questo proprio per permettere l'utilizzo del bot a tutti i potenziali utenti, senza distinzione di capacità e competenze linguistiche",
                  "BP_N": "Una soluzione è costruire strategicamente, cioèidentifichiamo un obbiettivo specifico di ciascun bot, in modo da evitare che un bot faccia tantissime cose, e strutturare le iterazioniattorno all'azione che desideri che l'utente intraprenda.",
                  "BP_E": "Per affrontare l'etica ci viene consigliato:\n\n- Di essere TRASPARENTI con chi utilizza il bot(fargli capire che non sta interagendo con una vera persona)\n\n- Evitare di di rafforzare i ruoli di genere(evitare lo stereotipo della 'donna sottomessa')\n\n- Arte della comunicazione",
                  "BP_T_R": "\n\n- Imposta aspettative chiare su cosa può fare chi utilizza il bot\n\n- Rendi l'esperienza fluida\n\n- Rendere coerente ogni iterazione\n\n- Rassicurare gli utenti in merito alle proprie misure di sicurezza",
                  "BP_IN": "IN",
                  "BP_CC": "\n\n- Impostare un obiettivo per il chatbot\n\n- Dare una personalità al chatbot, anche in base ai clienti con cui si relaziona",
                  "BP_LUI": "Per comprendere gli intenti ci sono vari modi:\n\n- Usare alberi decisionali più forti\n\n- Applichiamo tecniche di Machine learning per la miglior comprensione dell'intendo dell'utente\n\n- NLP",
                  "BP_TLA": "Di solito un bot offre agli utenti contenuti informativi e interessanti, per divulgare ciò sicuramente le informazioni saranno tante e conviene inviare più messaggi brevi anzichè uno lungo.",
                  "BP_SE": "Si consiglia che se il bot non riesce ad esaudire una richiesta dell'utente, in quanto non è una richiesta comune, allora si drovrà passare il rapidamente il controllo ad un operatore umanoin modo da evitarre che l'esperienza del cliente ne risente.",
                  "BP_LIB": "E' importante che nel messaggio di presentazione il botelenchi in anticipo le sue funzioni, in modo che l'utente sappia interagire con esso.",
                  "BP_WA_WI": "Di solito i bot durante il loro utilizzo apprendono nuove informazioni, questi informazioni possono essere sibuone ma anche cattive.Per evitare che il bot apprenda nozioni cattive dobbiamo : \n\n- Riconoscere il problema.\n\n- Impiegare misure difensive e protettive (Come rigidi controlli di accesso, adottare soluzione di protezione della rete).\n\n- Monitorare e testare la sicurezza.",
                  "BP_U": "Per l'usabilità deobbiamo rendere le conversazioni con il bot quanto più simili a quelle umane.Quindi le conversazioni dovrebbero essere naturali, creative ed emotive.",
                  }

    def __init__(self, dialog_id: str = None):
        super(EditChallenge, self).__init__(
            dialog_id or EditChallenge.__name__
        )
        self.recognizer = ChallengeRecognizer()
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.first_step,
                    self.second_step,
                    self.third_step,
                    self.fourth_step
                ],
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def first_step( self, step_context: WaterfallStepContext ) -> DialogTurnResult:

        reply = MessageFactory.text("Vuoi modificare le best-practices di una challenge?, bene di che tipologia fa parte la challenge?")
        aree = ["Development challenges","Use challenges"]

        reply.attachments = [self.create_hero_card("Seleziona una macro-area...",aree)]

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=reply)
        )

    def create_hero_card(self, title, items) -> Attachment:
        button = []
        for i in items:
            button.append(CardAction(type=ActionTypes.im_back,title=i,value=i))
        herocard = HeroCard(title=title,buttons=button)
        return CardFactory.hero_card(herocard)

    async def second_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
            intent = await self.recognizer.recognize(step_context)

            if (intent == "DevelopmentChallenges"):
                reply = MessageFactory.text("")
                reply.attachments = [self.create_hero_card("Bene, di quale challenge si tratta?", BestPracticesDialog.developmentChallenges)]
            elif (intent == "UseChallenges"):
                reply = MessageFactory.text("")
                reply.attachments = [ self.create_hero_card("Bene, di quale challenge si tratta?",BestPracticesDialog.useChallenges)]
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=reply)
            )


    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        challenge = await self.recognizer.recognize(step_context)
        reply = MessageFactory.text("Inserisci la best-practice che vuoi aggiungere...")
        step_context.dialogs.__setattr__("editChallenge", challenge)
        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=reply)
        )

    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        best_practices = step_context.result
        name_challenge = step_context.dialogs.__getattribute__("editChallenge")
        BestPracticesDialog.challenges.__setitem__(name_challenge,BestPracticesDialog.challenges.get(name_challenge)+"\n\n"+best_practices)
        print(BestPracticesDialog.challenges.get(name_challenge))
        return await step_context.begin_dialog("MainDialog")
