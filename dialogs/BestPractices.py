
from chellenge_recognizer import ChallengeRecognizer

from datatypes_date_time.timex import Timex

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult, ComponentDialog
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from botbuilder.schema import InputHints, SuggestedActions, CardAction, ActionTypes

from .InterruptDialog import InterruptDialog

class BestPracticesDialog(InterruptDialog):
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

    async def first_step( self, step_context: WaterfallStepContext ) -> DialogTurnResult:
        reply = MessageFactory.text("Le challenge si dividono in due macro-aree.\n\n- Development challenges: qui ci sono tutte le challenge che vengono affrontate durante lo sviluppo.\n\n- Use challenges: qui invece ci sono tutte le challenge per l'utilizzo dei bot.\n\n Seleziona una macro-area...")

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
            intent = await self.recognizer.recognize(step_context)

            if(intent == "DevelopmentChallenges"):
                reply = MessageFactory.text("Ecco qui tutte le challende relative allo sviluppo dei bot:")

                reply.suggested_actions = SuggestedActions(
                    actions=[
                        CardAction(
                            title="High Dependence on Data/high data quality",
                            type=ActionTypes.im_back,
                            value="High Dependence on Data/high data quality",
                        ),
                        CardAction(
                            title="NLP(Natural Language Processing)",
                            type=ActionTypes.im_back,
                            value="NLP(Natural Language Processing)",
                        ),
                        CardAction(
                            title="Test of Bot/ChatBot",
                            type=ActionTypes.im_back,
                            value="Test of Bot/ChatBot",
                        ),
                        CardAction(
                            title="Maintenance",
                            type=ActionTypes.im_back,
                            value="Maintenance",
                        ),
                        CardAction(
                            title="Development cost",
                            type=ActionTypes.im_back,
                            value="Development cost",
                        ),
                        CardAction(
                            title="Secure data",
                            type=ActionTypes.im_back,
                            value="Secure data",
                        ),
                        CardAction(
                            title="Machine learning",
                            type=ActionTypes.im_back,
                            value="Machine learning",
                        ),
                        CardAction(
                            title="Respond slowly",
                            type=ActionTypes.im_back,
                            value="Respond slowly",
                        ),
                        CardAction(
                            title="Integration",
                            type=ActionTypes.im_back,
                            value="Integration",
                        ),
                    ]
                )
            elif (intent == "UseChallenges"):
                reply = MessageFactory.text("Ecco qui tutte le challende relative all'utilizzo dei bot:")

                reply.suggested_actions = SuggestedActions(
                    actions=[
                        CardAction(
                            title="Privacy concerns",
                            type=ActionTypes.im_back,
                            value="Privacy concerns",
                        ),
                        CardAction(
                            title="Accessibility",
                            type=ActionTypes.im_back,
                            value="Accessibility",
                        ),
                        CardAction(
                            title="Noise",
                            type=ActionTypes.im_back,
                            value="Noise",
                        ),
                        CardAction(
                            title="Ethics",
                            type=ActionTypes.im_back,
                            value="Ethics",
                        ),
                        CardAction(
                            title="Trust/reliability",
                            type=ActionTypes.im_back,
                            value="Trust/reliability",
                        ),
                        CardAction(
                            title="Interruption",
                            type=ActionTypes.im_back,
                            value="Interruption",
                        ),
                        CardAction(
                            title="Choosing a bot / Configuring a bot",
                            type=ActionTypes.im_back,
                            value="Choosing a bot / Configuring a bot",
                        ),
                        CardAction(
                            title="Lack of understanding of intent",
                            type=ActionTypes.im_back,
                            value="Lack of understanding of intent",
                        ),
                        CardAction(
                            title="Too long answers",
                            type=ActionTypes.im_back,
                            value="Too long answers",
                        ),
                        CardAction(
                            title="Solve everything",
                            type=ActionTypes.im_back,
                            value="Solve everything",
                        ),
                        CardAction(
                            title="Lack of information about the bot",
                            type=ActionTypes.im_back,
                            value="Lack of information about the bot",
                        ),
                        CardAction(
                            title="Wrong actions/wrong information",
                            type=ActionTypes.im_back,
                            value="Wrong actions/wrong information",
                        ),
                        CardAction(
                            title="Usability",
                            type=ActionTypes.im_back,
                            value="Usability",
                        ),
                  ]
                )
            else:
                return await step_context.prompt(
                     BestPracticesDialog.__name__,PromptOptions(prompt="", retry_prompt=""),
                )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=reply)
            )

    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
            res = await self.recognizer.recognize(step_context)
            if(res == None):
                return await step_context.reprompt_dialog(
                    BestPracticesDialog.__name__, PromptOptions(prompt="", retry_prompt=""),
                )
            reply = MessageFactory.text(res)

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
            return await step_context.end_dialog()

        if(step_context.result == "Ho bisogno di altre best-practices per una nuova challenge"):
            return await step_context.begin_dialog(BestPracticesDialog.__name__)
