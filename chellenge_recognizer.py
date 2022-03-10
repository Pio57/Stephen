from botbuilder.core import Recognizer, RecognizerResult, TurnContext
from botbuilder.dialogs import WaterfallStepContext


class ChallengeRecognizer(Recognizer):
    challenges = {"High Dependence on Data/high data quality": "Per il nostro agente i dati sono essenziali, quindi dobbiamo sicuramente avere una grande quantità di dati e sopratutto dati di qualità.Quindi oltre ad avere un grande dataset, dobbiamo applicare tutte quelle tecniche di data preparation per pulire al meglio il dataset",
                  "NLP(Natural Language Processing)": "Per l'NLP dobbiamo tenere in considerazione l'intento ovvero le intenzioni dell'utente finale, le entità che sono i metadati dell'intento.",
                  3: 'i',
                  4: 'o',
                  5: 'u'}

    async def recognize(self, step_context: WaterfallStepContext):
        print("ciap")
        return self.challenges[step_context.result]
