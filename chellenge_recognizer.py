from botbuilder.core import Recognizer, RecognizerResult, TurnContext
from botbuilder.dialogs import WaterfallStepContext


class ChallengeRecognizer(Recognizer):
    intents = {"Acknowledges challenge" : "AcknowledgesChallenge",
                  "Insert new challenge" : "InsertChallenge",
                  "Remove challenge" : "RemoveChallenge" ,
                  "Development challenges" : "DevelopmentChallenges",
                  "Use challenges" : "UseChallenges",
                  "High Dependence on Data/high data quality": "BP_HDD_HDQ",
                  "NLP(Natural Language Processing)": "BP_NLP",
                  "Test of Bot/ChatBot":"BP_TEST",
                  "Maintenance":"BP_M",
                  "Development cost": "BP_DC",
                  "Secure data":"BC_SC",
                  "Machine learning": "BC_ML",
                  "Respond slowly": "BC_RS",
                  "Integration": "BP_I",
                  "Privacy concerns": "BP_PC",
                  "Accessibility":"BP_A",
                  "Noise": "BP_N",
                  "Ethics": "BP_E",
                  "Trust/reliability": "BP_T_R",
                  "Interruption": "BP_IN",
                  "Choosing a bot / Configuring a bot": "BP_CC",
                  "Lack of understanding of intent": "BP_LUI",
                  "Too long answers": "BP_TLA",
                  "Solve everything": "BP_SE",
                  "Lack of information about the bot": "BP_LIB",
                  "Wrong actions/wrong information": "BP_WA_WI",
                  "Usability": "BP_U",
                  }

    async def recognize(self, step_context: WaterfallStepContext):
        if(self.intents.keys().__contains__(step_context.result)):
            return self.intents[step_context.result]
        return None
