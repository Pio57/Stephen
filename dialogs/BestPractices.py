import os
import json

from chellenge_recognizer import ChallengeRecognizer

from datatypes_date_time.timex import Timex

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult, ComponentDialog
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, CardFactory
from botbuilder.schema import InputHints, SuggestedActions, CardAction, ActionTypes, Attachment, HeroCard

from .InterruptDialog import InterruptDialog


class BestPracticesDialog(InterruptDialog):
    challenges = {
        "BP_HDD_HDQ": "Per il nostro agente i dati sono essenziali, quindi dobbiamo sicuramente avere una grande quantità di dati e sopratutto dati di qualità.Quindi oltre ad avere un grande dataset, dobbiamo applicare tutte quelle tecniche di data preparation per pulire al meglio il dataset",
        "BP_NLP": "Per il Natural language processing (NLP) bisogna considerare l'intento ovvero le intenzioni dell'utente finale, le entità che sono i metadati dell'intento.\n\nSe può esserti utile puoi usare Language Understanding (LUIS),è un servizio di intelligenza artificiale conversazionale basato sul cloud che applica l'intelligenza di Machine Learning al testo in linguaggio naturale della conversazione di un utente per prevedere il significato generale ed estrarre informazioni pertinenti e dettagliate. ",
        "BP_TEST": "Per testare un agente può essere utile seguire questi punti:\n\n- Definire i casi d'uso: elencando tutte le domende e le risposte per coprire ogni scenario.\n\n- Testare il flusso di conversazione del bot.\n\n- Testare i bot sulle frasi di interruzione dell'utente.\n\n- Testare quanto l'interfaccia risulta intuitiva.\n\n Alcuni tool che possono esserti di aiuto sono:\n\n- Zypnos.\n\n- TestyourBot.\n\n- Bot Testing.\n\n- Dimon.",
        "BP_M": "Per la manutenzione ci sono 3 fasi principali:\n\n- HyperCare, dove i bot vengono eseguiti sotto stretta sorveglianza.\n\n- Supporto\n\n- Miglioramenti minori",
        "BP_DC": "La necessità di formazione continua può diventare costosa, con l'utilizzo di piattaforme di modellazione SaaS AI/ML questapuò essere in qualche modo evitata utilizzando soluzioni invece di assumere un team completo di data science per modellare e allenare un bot.\nInoltre possiamo optare per tool e framework open source per diminuire ancora di più questo costo di sviluppo.",
        "BC_SC": "Per la sicurezza del bot:\n\n- Il bot deve scambiare dati utilizzando un protocollo HTTPS\n\n- Eliminare i messaggi contenenti i dati sensibili non appena non sono più necessari\n\n- La best practice prevede di archiviare le informazioni in uno stato sicuro per un certo periodo di tempo e poi di scartarle in un secondo momento dopo che hanno raggiunto il loro scopo\n\n-  Rafforzare il DB",
        "BC_ML": "Usare algoritmi di machine learning per capire continuamente i diversi modi in cui i clienti pongono le domande",
        "BC_RS": "Per l'usabilità deobbiamo rendere le conversazioni con il bot quanto più simili a quelle umane. Quindi le conversazioni dovrebbero essere naturali, creative ed emotive.",
        "BP_I": "Per l'integrazione è consigliato utilizzare le API",
        "BP_PC": "Per quanto riguarda i concetti di privacy si può agire in più modi :\n\n- Autenticazione e autorizzazione : questo sicuramente quando si lavora con dati sensibili del cliente.\n\n- Crittografia end-to-end: la quale è molto comoda. Essa, appunto, permette che i messaggi vengano letti solo dalle due parti che comunicano.\n\n- Messaggi autodistruttivi: Utilizzati per eliminare tutti quei messaggi che contengono informazioni personali.",
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
    developmentChallenges = ["High Dependence on Data/high data quality", "NLP(Natural Language Processing)",
                             "Test of Bot/ChatBot", "Maintenance", "Development cost", "Secure data",
                             "Machine learning", "Respond slowly", "Integration"]

    useChallenges = ["Privacy concerns", "Accessibility", "Noise", "Ethics", "Trust/reliability", "Interruption",
                     "Choosing a bot / Configuring a bot", "Lack of understanding of intent", "Too long answers",
                     "Solve everything", "Lack of information about the bot", "Wrong actions/wrong information",
                     "Usability"]

    def __init__(self, dialog_id: str = None):
        super(BestPracticesDialog, self).__init__(
            dialog_id or BestPracticesDialog.__name__
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
                    self.fourth_step,
                ],
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def first_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        reply = MessageFactory.text(
            "Le challenge si dividono in due macro-aree.\n\n- Development challenges: qui ci sono tutte le challenge che vengono affrontate durante lo sviluppo.\n\n- Use challenges: qui invece ci sono tutte le challenge per l'utilizzo dei bot.\n\n ")
        aree = ["Development challenges", "Use challenges"]

        reply.attachments = [self.create_hero_card("Seleziona una macro-area...", aree)]

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=reply)
        )

    def create_hero_card(self, title, items) -> Attachment:
        button = []
        for i in items:
            button.append(CardAction(type=ActionTypes.im_back, title=i, value=i))
        herocard = HeroCard(title=title, buttons=button)
        return CardFactory.hero_card(herocard)

    async def second_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        intent = await self.recognizer.recognize(step_context)

        if (intent == "DevelopmentChallenges"):
            reply = MessageFactory.text("")
            reply.attachments = [self.create_hero_card("Ecco qui tutte le challende relative allo sviluppo dei bot:",
                                                       self.developmentChallenges)]

        elif (intent == "UseChallenges"):
            reply = MessageFactory.text("Ecco qui tutte le challende relative all'utilizzo dei bot:")
            reply.attachments = [
                self.create_hero_card("Ecco qui tutte le challende relative all'utilizzo dei bot:", self.useChallenges)]

        else:
            return await step_context.prompt(
                BestPracticesDialog.__name__, PromptOptions(prompt="", retry_prompt=""),
            )
        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=reply)
        )

    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        res = await self.recognizer.recognize(step_context)
        if (res == None):
            return await step_context.reprompt_dialog(
                BestPracticesDialog.__name__, PromptOptions(prompt="", retry_prompt=""),
            )
        bp = self.challenges[res]
        reply = MessageFactory.text(bp)

        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="ok, grazie per la risposta",
                    type=ActionTypes.im_back,
                    value="ok, grazie per la risposta",
                ),
                CardAction(
                    title="Ho bisogno di altre best-practices per una nuova challenge",
                    type=ActionTypes.im_back,
                    value="Ho bisogno di altre best-practices per una nuova challenge",
                ),
                CardAction(
                    title="Torna al menù principale",
                    type=ActionTypes.im_back,
                    value="Torna al menù principale",
                ),
            ]
        )
        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=reply)
        )

    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if (step_context.result == "ok, grazie per la risposta"):
            return await step_context.end_dialog()

        elif (step_context.result == "Ho bisogno di altre best-practices per una nuova challenge"):
            return await step_context.begin_dialog(BestPracticesDialog.__name__)

        elif (step_context.result == "Torna al menù principale"):
            return await step_context.begin_dialog("MainDialog")