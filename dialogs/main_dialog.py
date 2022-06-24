# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, TurnContext, turn_context
from botbuilder.schema import InputHints, SuggestedActions, CardAction, ActionTypes, CardImage

from chellenge_recognizer import ChallengeRecognizer
from helpers.dialog_helper import DialogHelper
from helpers.luis_helper import LuisHelper, Intent

from .InsertChallenge import InsertChallenge
from .BestPractices import BestPracticesDialog
from .EditChallenge import EditChallenge

import random
import json
import torch
from recognize.model import NeuralNet
from recognize.NLTK_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('recognize/intentsChallenges.json', 'r') as f:
    intents = json.load(f)

FILE = "recognize/data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()


class MainDialog(ComponentDialog):
    def __init__(self, recognizer: ChallengeRecognizer):
        super(MainDialog, self).__init__(MainDialog.__name__)

        self.recognizer = recognizer

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(BestPracticesDialog(BestPracticesDialog.__name__))
        self.add_dialog(InsertChallenge(InsertChallenge.__name__))
        self.add_dialog(EditChallenge(EditChallenge.__name__))
        self.add_dialog(
            WaterfallDialog(
                "MainDialog", [self.initial_step, self.loop, self.options_step, self.choise_step, self.final_step]
            )
        )

        self.initial_dialog_id = "MainDialog"

    async def initial_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        reply = MessageFactory.text("")
        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=reply)
        )

    async def loop(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if(str(step_context.result).lower() == "menu" or str(step_context.result).lower() == "menù"):
            return await step_context.next(step_context)
        if (str(step_context.result).lower() == "cancel" or str(step_context.result).lower() == "quit" or str(step_context.result).lower() == "grazie" or str(step_context.result).lower() == "grazie per la risposta"):
            reply = MessageFactory.text("Spero di essere stato d'aiuto, alla prossima!!")
            await step_context._turn_context.send_activity(reply)
            return await step_context.end_dialog()
        else:
            sentence = str(step_context.result)
            sentence = tokenize(sentence)
            X = bag_of_words(sentence, all_words)
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X).to(device)

            output = model(X)

            _, predicted = torch.max(output, dim=1)
            tag = tags[predicted.item()]

            probs = torch.softmax(output, dim=1)
            prob = probs[0][predicted.item()]
            if prob.item() > 0.75:
                for intent in intents["intents"]:
                    if tag == intent["tag"]:
                        text = random.choice(intent['responses'])
                        reply = MessageFactory.text(text)
            else:
                reply = MessageFactory.text("Non ho capito...")
            await step_context._turn_context.send_activity(BestPracticesDialog.challenges[text])
            return await step_context.begin_dialog("MainDialog")

    async def options_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        reply = MessageFactory.text("Come posso esserti di aiuto?\n\n"
                                    "Queste sono mie potenzialità:\n\n- Acknowledges challenge: Stai sviluppando un bot, ti darò una mano a scoprire le best-practices che miglioreranno il tuo bot!"
                                    "\n\n- Insert challenges: sei un bravo sviluppatore di bot? Inserisci qui una nuova challenge con le relative best-practices in modo da aiutare tutta la community di sviluppaotri.")

        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="Acknowledges challenge",
                    type=ActionTypes.im_back,
                    value="Acknowledges challenge",
                ),
                CardAction(
                    title="Insert new challenge",
                    type=ActionTypes.im_back,
                    value="Insert new challenge",
                ),
                CardAction(
                    title="Edit challenge",
                    type=ActionTypes.im_back,
                    value="Edit challenge",
                ),
            ]
        )

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=reply)
        )


    async def choise_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        intent = await self.recognizer.recognize(step_context)
        selected: [str] = step_context.options if step_context.options is not None else []
        if(intent == "AcknowledgesChallenge"):
            return await step_context.begin_dialog(BestPracticesDialog.__name__)
        elif(intent == "InsertChallenge"):
            return await step_context.begin_dialog(InsertChallenge.__name__)
        elif (intent == "EditChallenge"):
            return await step_context.begin_dialog(EditChallenge.__name__)
        else:
            sentence = str(intent)
            sentence = tokenize(sentence)
            X = bag_of_words(sentence, all_words)
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X).to(device)

            output = model(X)

            _, predicted = torch.max(output, dim=1)
            tag = tags[predicted.item()]

            probs = torch.softmax(output, dim=1)
            prob = probs[0][predicted.item()]
            if prob.item() > 0.75:
                for intent in intents["intents"]:
                    if tag == intent["tag"]:
                        reply = MessageFactory.text(random.choice(intent['responses']))
            else:
                reply = MessageFactory.text("Non ho capito...")
            print(tag)
            await step_context._turn_context.send_activity(reply)
            return await step_context.begin_dialog("MainDialog")


    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        reply = MessageFactory.text("Spero di essere stato d'aiuto, alla prossima!")
        await step_context._turn_context.send_activity(reply)
        return await step_context.end_dialog()


