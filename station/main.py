"""
Lager Factory demo project

Start reading with the STEPS variable at the bottom of the file
"""

import time
import sys
from lager import lager
from lager import INPUT
from lager import factory
from lager.factory import Step, get_secret

POWER_RAIL_ADC_CH = 0
LED_GPIO_READ_PIN = 0
MIN_LINE_VOLTAGE = 3.05
MAX_LINE_VOLTAGE = 3.25
START_SEQUENCE = b'New Lager PCB Demo.\r\n'
SERIAL_PATH = '/dev/ttyACM0'

STEP_SLEEP = 0

class EmptyStep(Step):
    """
        Step classes must subclass `lager.factory.Step` and implement a `run` function.
        The name of the step in the UI will be the name of the class, with spaces between capital
        letters.
        For example, this step will be called "Empty Step"
    """
    def run(self):
        """
            `self.log` behaves like print(), except the output goes to the operator's stdout/stderr
            textboxes

            `self.log("a string")` sends output to the stdout textbox
            `self.log("another string", file=sys.stderr)` sends output to the stderr textbox
        """
        self.log("This goes to stdout")
        self.log("This goes to stderr", file=sys.stderr)
        time.sleep(STEP_SLEEP)


class StepWithDisplayName(Step):
    """
        Steps can have an optional `DisplayName` property that overrides the default behavior
        of the display name matching the class name
    """
    DisplayName = 'This is a custom display name'
    def run(self):
        time.sleep(STEP_SLEEP)

class StepWithDescription(Step):
    """
        The description will appear as a bold header in the left pane of the operator UI.
        By default the description is just the step name; set the `Description` property to customize it.
    """
    Description = 'This is a custom description'
    def run(self):
        time.sleep(STEP_SLEEP)

class StepThatSetsState(Step):
    """
        `self.state` is a dictionary that maintains the state for an individual test run, across all steps.
    """
    def run(self):
        self.log("Setting state...")
        self.state['Foo'] = 'Bar'
        self.state['Baz'] = 42

class StepThatReadsState(Step):
    def run(self):
        self.log("Reading state...")
        foo = self.state['Foo']
        baz = self.state['Baz'] = 42
        self.log(f'Got foo: {foo} and baz: {baz}')


class StepThatCanFail(Step):
    """
        The return value of a step is used to indicate success or failure. If an exception is raised or
        an explicit False is returned, the step will be marked as failed (returning None explicitly or
        implicitly will count as a test success). If any steps fail, the run is considered to be a
        failure.

        By default, if a step fails, the entire test run will stop immediately. However,
        if you set the StopOnFail property to False, a failing step will not stop the entire run.
    """
    StopOnFail = False
    def run(self):
        self.log("This step fails")
        time.sleep(STEP_SLEEP)
        return False

class StepWithImage(Step):
    """
        The Image property can be used to display a fixed, static image during a step.

        The property must be set to the relative path of an image *in the repo used for the test*

    """
    Image = 'station/img/puppy.jpg'

    def run(self):
        time.sleep(STEP_SLEEP)

class StepWithLink(Step):
    """
        Steps can provide a link. This link will be displayed in the right pane of the operator
        UI during the step.
    """
    Link = 'https://www.example.com'
    def run(self):
        time.sleep(STEP_SLEEP)

class StepWithLinkText(Step):
    """
        To use custom text for your link, set Link to a tuple with the url as the first
        element and the text as the second
    """
    Link = ('https://www.example.com', 'This is the link text')
    def run(self):
        time.sleep(STEP_SLEEP)

class StepWithButtons(Step):
    """
        A set of buttons can be presented to the user with `self.present_buttons`.
        It takes a list of button specifiers. A button specifier can be either a string, or a 2-element
        tuple where the first element is the button text and the second is the value.

        The return value of `present_buttons` is the value of the button which the operator clicked.

        If the value of a button is `True`, it will be presented in green text. f the value is `False` it
        will be presented in red.
    """
    def run(self):
        response = self.present_buttons([
            'Button 1',
            'Button 2',
            'Button 3',
        ])
        self.log(f'You clicked: {response}')

        response = self.present_buttons([
            ('Button 4', 'Value 1'),
            ('This is green', True),
            ('Button 6', 42),
        ])
        self.log(f'You clicked: {response}')

class PassFailButtons(Step):
    """
        As a convenient shortcut, you can use `self.present_pass_fail_buttons` to show two
        buttons, one which is green and says "Pass", and the other which is red and says "Fail".
        The return value will be True if the operator clicks "Pass" and False if they click "Fail".
    """
    def run(self):
        response = self.present_pass_fail_buttons()
        self.log(f'You clicked: {response}')


class StepWithTextInput(Step):
    """
        You can use `self.present_text_input` to provide a text input box with prompt to the
        operator. The optional `size` parameter (default: 50) controls how many characters
        wide the input box is. The return value is the value typed by the operator.
    """
    def run(self):
        response = self.present_text_input("What is your name?", size=25)
        self.log(f'Your name is: {response}')

class StepWithRadios(Step):
    """
        `self.present_radios` can be used to present a radio input to the operator, requiring them to select
        exactly one. The first argument is the label/prompt for the input, and the second argument is the set
        of options. As with `present_buttons` it can be a list of strings, or a list of 2-element tuples

        The return value is a dictionary with keys 'name' and 'value'
    """
    def run(self):
        response = self.present_radios("Choose exactly 1", [
            "Choice 1",
            "Choice 2",
            "Choice 3",
        ])
        self.log(f'You selected: {response}')


class StepWithCheckBoxes(Step):
    """
        `self.present_checkboxes` can be used to present a checkbox input to the operator, which allows selecting
        multiple (or no) inputs. The first argument is the label/prompt for the input, and the second argument is the set
        of options. As with `present_buttons` it can be a list of strings, or a list of 2-element tuples

        The return value is a list of dictionaries of the selected items, each with keys 'name' and 'value'
    """
    def run(self):
        response = self.present_checkboxes("Choose as many as you want", [
            "Choice 1",
            "Choice 2",
            "Choice 3",
        ])
        self.log(f'You selected: {response}')

class StepWithSelect(Step):
    """
        `self.present_select` can be used to present a dropdown select input to the operator. The first argument
        is the label/prompt for the input, and the second argument is the set of options.
        As with `present_buttons` it can be a list of strings, or a list of 2-element tuples
        `allow_multiple` is an optional argument (default: False) that controls whether the operator is allowed
        to select multiple items.

        If `allow_multiple` is False (the default), the return value is a dictionary with 'name' and 'value' keys.
        If `allow_multiple` is True, the return value is a list of dictionaries with 'name' and 'value' keys.
    """
    def run(self):
        response = self.present_select("Choose from the dropdown", [
            "Choice 1",
            "Choice 2",
            "Choice 3",
        ], allow_multiple=True)
        self.log(f'You selected: {response}')

class StepThatReadsSecret(Step):
    """
        lager.factory.get_secret can be used to read a secret value from the environment.
        When running with `lager factory dev`, secrets can be set using `--secret FOO=BAR`
        In production, secrets can be configured at https://app.lagerdata.com/account/factory-secrets
        They will be stored in an encrypted keystore and automatically passed to your running factory
        instance.
    """
    def run(self):
        secret = get_secret('FOO')
        self.log(f'The secret is {secret}')
        time.sleep(3)

class ConnectToDut(Step):
    """
        The full range of Lager Python tools are available, for interacting with your DUT. See the documentation
        at https://docs.lagerdata.com/gateway-lager/device.html
    """
    def run(self):
        gateway = lager.Lager()
        self.state["gateway"] = gateway
        self.state["dut"] = gateway.connect(
            "at91samdgxx",
            interface="ftdi",
            transport="swd",
            speed=3000,
            ignore_if_connected=True,
        )


class Shutdown(Step):
    def run(self):
        """
            Perform de-initialization here
        """

# STEPS is a required top-level variable. It defines the series of steps that will comprise one factory run.
# It must be called STEPS. The steps will be executed in-order until a step fails, or the entire set of steps
# succeeds
STEPS = [
    EmptyStep,
    StepWithDisplayName,
    StepWithDescription,
    StepThatSetsState,
    StepThatReadsState,
    StepThatCanFail,
    StepWithImage,
    StepWithLink,
    StepWithLinkText,
    StepWithButtons,
    PassFailButtons,
    StepWithTextInput,
    StepWithRadios,
    StepWithCheckBoxes,
    StepWithSelect,
    StepThatReadsSecret,
    # ConnectToDut,
]

def main():
    """
        factory.run takes two arguments - the list of steps from above, and an optional keyword argument
        `finalizer_cls`. `finalizer_cls` is a step that will execute at the end of the factory run, regardless
        of success or failure. Use it to perform additional logging, close shared resources, or take any other
        actions that always need to happen at the end of a run.
    """
    factory.run(STEPS, finalizer_cls=Shutdown)


if __name__ == "__main__":
    main()
