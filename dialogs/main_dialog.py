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
from botbuilder.schema import InputHints, SuggestedActions, CardAction, ActionTypes

from booking_details import BookingDetails
from chellenge_recognizer import ChallengeRecognizer
from flight_booking_recognizer import FlightBookingRecognizer
from helpers.luis_helper import LuisHelper, Intent
from .booking_dialog import BookingDialog
from .BestPractices import BestPractices

class MainDialog(ComponentDialog):
    def __init__(self, recognizer: ChallengeRecognizer):
        super(MainDialog, self).__init__(MainDialog.__name__)

        self.recognizer = recognizer

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(BestPractices(BestPractices.__name__))
        self.add_dialog(
            WaterfallDialog(
                "WFDialog", [self.options_step, self.choise_step, self.final_step]
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def options_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        reply = MessageFactory.text("Here's what I can do\nChoose an option")

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
                    title="Remove challenge",
                    type=ActionTypes.im_back,
                    value="Remove challenge",
                ),
            ]
        )

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=reply)
        )

    async def choise_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        print(step_context.result)
        intent = await self.recognizer.recognize(step_context)
        if(intent == "AcknowledgesChallenge"):
            return await step_context.begin_dialog(BestPractices.__name__)
        else:
            return await step_context.prompt(
                MainDialog.__name__, PromptOptions(prompt="", retry_prompt=""),
            )
        """
        if intent == Intent.BOOK_FLIGHT.value and luis_result:
            # Show a warning for Origin and Destination if we can't resolve them.
            await MainDialog._show_warning_for_unsupported_cities(
                step_context.context, luis_result
            )

            # Run the BookingDialog giving it whatever details we have from the LUIS call.
            return await step_context.begin_dialog(self._booking_dialog_id, luis_result)

        if intent == Intent.GET_WEATHER.value:
            get_weather_text = "TODO: get weather flow here"
            get_weather_message = MessageFactory.text(
                get_weather_text, get_weather_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(get_weather_message)

        else:
            didnt_understand_text = (
                "Sorry, I didn't get that. Please try asking in a different way"
            )
            didnt_understand_message = MessageFactory.text(
                didnt_understand_text, didnt_understand_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(didnt_understand_message)

        return await step_context.next(None)
        """
    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        print("final step")
        """    
        # If the child dialog ("BookingDialog") was cancelled or the user failed to confirm,
        # the Result here will be null.
        if step_context.result is not None:
            result = step_context.result

            # Now we have all the booking details call the booking service.

            # If the call to the booking service was successful tell the user.
            # time_property = Timex(result.travel_date)
            # travel_date_msg = time_property.to_natural_language(datetime.now())
            msg_txt = f"I have you booked to {result.destination} from {result.origin} on {result.travel_date}"
            message = MessageFactory.text(msg_txt, msg_txt, InputHints.ignoring_input)
            await step_context.context.send_activity(message)

        prompt_message = "What else can I do for you?"
        return await step_context.replace_dialog(self.id, prompt_message)
"""
    @staticmethod
    async def _show_warning_for_unsupported_cities(
        context: TurnContext, luis_result: BookingDetails
    ) -> None:
        if luis_result.unsupported_airports:
            message_text = (
                f"Sorry but the following airports are not supported:"
                f" {', '.join(luis_result.unsupported_airports)}"
            )
            message = MessageFactory.text(
                message_text, message_text, InputHints.ignoring_input
            )
            await context.send_activity(message)
