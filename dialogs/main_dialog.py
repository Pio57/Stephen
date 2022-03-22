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
from flight_booking_recognizer import FlightBookingRecognizer
from helpers.luis_helper import LuisHelper, Intent
from .InsertChallenge import InsertChallenge
from .BestPractices import BestPracticesDialog
from .EditChallenge import EditChallenge


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
                "MainDialog", [self.options_step, self.choise_step, self.final_step]
            )
        )

        self.initial_dialog_id = "MainDialog"

    async def options_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        reply = MessageFactory.text("Eccomi come posso esserti di aiuto?\n\n"
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
        if(intent == "AcknowledgesChallenge"):
            return await step_context.begin_dialog(BestPracticesDialog.__name__)
        elif(intent == "InsertChallenge"):
            return await step_context.begin_dialog(InsertChallenge.__name__)
        elif (intent == "EditChallenge"):
            return await step_context.begin_dialog(EditChallenge.__name__)
        else:
            return await step_context.prompt(
                MainDialog.__name__, PromptOptions(prompt="", retry_prompt=""),
            )

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        reply = MessageFactory.text("Spero di essere stato d'aiuto, alla prossima!!")
        await step_context._turn_context.send_activity(reply)
        return await step_context.end_dialog()


