from chellenge_recognizer import ChallengeRecognizer

from datatypes_date_time.timex import Timex

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult, ComponentDialog
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from botbuilder.schema import InputHints, SuggestedActions, CardAction, ActionTypes
from .cancel_and_help_dialog import CancelAndHelpDialog
from .date_resolver_dialog import DateResolverDialog

class BestPractices(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(BestPractices, self).__init__(
            dialog_id or BestPractices.__name__
        )
        self.recognizer = ChallengeRecognizer()
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(DateResolverDialog(DateResolverDialog.__name__))
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

    async def first_step( self, step_context: WaterfallStepContext ) -> DialogTurnResult:
        reply = MessageFactory.text("select the challenges macro area")

        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="Development challenges",
                    type=ActionTypes.im_back,
                    value="Development challenges",
                ),
                CardAction(
                    title="Use challenges",
                    type=ActionTypes.im_back,
                    value="Use challenges",
                ),
            ]
        )

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=reply)
        )

    async def second_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
            reply = MessageFactory.text("select the challenge")
            intent = await self.recognizer.recognize(step_context)
            print(intent)
            if(intent == "DevelopmentChallenges"):
                reply.suggested_actions = SuggestedActions(
                    actions=[
                        CardAction(
                            title="High Dependence on Data/high data quality",
                            type=ActionTypes.im_back,
                            value="High Dependence on Data/high data quality",
                        ),
                        CardAction(
                            title="Use challenges",
                            type=ActionTypes.im_back,
                            value="Use challenges",
                        ),
                    ]
                )


            if (intent == "UseChallenges"):
                print("Hai scelto Use challenges")
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=reply)
            )

    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
            print(step_context.result)
            res = await self.recognizer.recognize(step_context)
            reply = MessageFactory.text("select the challenge"+res)

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
                ]
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=reply)
            )

    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if(step_context.result == "ok, grazie per la risposta"):
            print("sono qui")
            return await step_context.end_dialog(BestPractices.__name__)
        if(step_context.result == "Ho bisogno di altre best-practices per una nuova challenge"):
            return await step_context.begin_dialog(BestPractices.__name__)
