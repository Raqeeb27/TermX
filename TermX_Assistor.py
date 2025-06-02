import asyncio
import json
import os
import subprocess
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Label, Input, Select
from textual.containers import Container, Vertical, Horizontal
from textual.reactive import var
from textual import on
from textual.screen import ModalScreen
from textual.widgets import RichLog, ProgressBar # For displaying output clearly

# --- Helper Functions for Termux API Commands ---


# Helper to run a Termux API command and return its output
def run_termux_command(command_name: str, *args, input_text: str = None) -> str:
    """
    Runs a termux-api command and captures its output.

    Args:
        command_name: The base name of the termux-api command (e.g., "torch", "battery-status").
        *args: Additional arguments for the command (e.g., "-n", "phone_number").
        input_text: Optional text to pass to the command's stdin.

    Returns:
        The stripped standard output of the command, or an error message.
    """
    # Define the full path to the termux-api executable base
    TERMUX_BIN_PATH = "/data/data/com.termux/files/usr/bin/"
    full_command_path = os.path.join(TERMUX_BIN_PATH, f"termux-{command_name}") # Use f-string for clarity

    command_list = [full_command_path] + list(args)

    try:
        process = subprocess.run(
            command_list, # Pass the list of arguments correctly
            capture_output=True,
            text=True,
            check=True,
            input=input_text
        )
        return process.stdout.strip()
    except FileNotFoundError:
        return f"Error: Command '{full_command_path}' not found. Please ensure termux-api package is installed and the command exists."
    except subprocess.CalledProcessError as e:
        # Provide more detailed error info for debugging
        return (
            f"Error executing '{' '.join(command_list)}':\n"
            f"Return Code: {e.returncode}\n"
            f"STDOUT: {e.stdout.strip() if e.stdout else '[No stdout]'}\n"
            f"STDERR: {e.stderr.strip() if e.stderr else '[No stderr]'}"
        )
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# --- Custom Modal Dialogs for Input/Confirmation ---

class MessageDialog(ModalScreen[None]):
    """A simple dialog to display a message."""
    def __init__(self, title: str, message: str) -> None:
        super().__init__()
        self.title = title
        self.message = message

    def compose(self) -> ComposeResult:
        yield Container(
            Static(self.title, classes="dialog-title"),
            Static(self.message, classes="dialog-content"),
            Button("OK", id="ok_button", variant="primary"),
            classes="dialog-box"
        )

    @on(Button.Pressed, "#ok_button")
    def on_ok_button_pressed(self) -> None:
        self.dismiss(None)

class InputDialog(ModalScreen[str]):
    """A dialog to get text input."""
    def __init__(self, title: str, prompt: str, default: str = "") -> None:
        super().__init__()
        self.title = title
        self.prompt = prompt
        self.default = default

    def compose(self) -> ComposeResult:
        yield Container(
            Static(self.title, classes="dialog-title"),
            Static(self.prompt, classes="dialog-content"),
            Input(value=self.default, id="input_field"),
            Horizontal(
                Button("OK", id="ok_button", variant="primary"),
                Button("Cancel", id="cancel_button", variant="default"),
                classes="dialog-buttons"
            ),
            classes="dialog-box"
        )

    @on(Button.Pressed, "#ok_button")
    def on_ok_button_pressed(self) -> None:
        input_value = self.query_one("#input_field", Input).value
        self.dismiss(input_value)

    @on(Button.Pressed, "#cancel_button")
    def on_cancel_button_pressed(self) -> None:
        self.dismiss(None) # Dismiss with None if cancelled

class ConfirmationDialog(ModalScreen[bool]):
    """A dialog to get Yes/No confirmation."""
    def __init__(self, title: str, message: str) -> None:
        super().__init__()
        self.title = title
        self.message = message

    def compose(self) -> ComposeResult:
        yield Container(
            Static(self.title, classes="dialog-title"),
            Static(self.message, classes="dialog-content"),
            Horizontal(
                Button("Yes", id="yes_button", variant="primary"),
                Button("No", id="no_button", variant="default"),
                classes="dialog-buttons"
            ),
            classes="dialog-box"
        )

    @on(Button.Pressed, "#yes_button")
    def on_yes_button_pressed(self) -> None:
        self.dismiss(True)

    @on(Button.Pressed, "#no_button")
    def on_no_button_pressed(self) -> None:
        self.dismiss(False)

# --- Main Termux API TUI App ---

class TermuxApiApp(App):
    """A Textual app for Termux API commands."""

    display_message = var("Welcome to Termux API TUI!")

    # Store a reference to the RichLog for output
    log_output: RichLog

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    # --- CSS Styling ---
    CSS = """
    Screen {
        background: #1e1e1e;
        color: white;
        layout: vertical;
        align: center middle;
    }

    #header {
        background: blue;
        color: white;
        text-align: center;
        padding: 1 0;
        width: 100%;
    }

    #menu-container {
        layout: grid;
        grid-size: 2; /* 2 columns */
        grid-rows: auto;
        grid-columns: 1fr 1fr;
        grid-gutter: 2;
        width: 90%;
        height: auto; /* Let content dictate height */
        padding: 1;
        border: solid #6a0dad; /* Purple border */
        margin-top: 2;
    }

    .menu-button {
        width: 100%; /* Take full grid cell width */
        height: 3;
        background: #2a2a2a;
        color: white;
        border: solid dodgerblue;
        text-align: center;
    }

    .menu-button:hover {
        background: dodgerblue;
    }

    #output-log {
        border: panel green;
        width: 90%;
        height: 30%; /* Give it enough height for output */
        margin-top: 2;
        background: #333333;
        padding: 1;
    }

    /* Styles for the modal dialogs */
    .dialog-box {
        background: #333333;
        border: thick $primary;
        width: 60%;
        height: auto;
        padding: 2;
        align: center middle;
        layout: vertical;
    }

    .dialog-title {
        text-align: center;
        text-style: bold;
        color: $primary;
        margin-bottom: 1;
    }

    .dialog-content {
        text-align: center;
        margin-bottom: 2;
        padding: 0 2; /* Add horizontal padding for text */
    }

    .dialog-buttons {
        layout: horizontal;
        align: center middle;
        margin-top: 1;
        width: 100%;
    }

    .dialog-buttons Button {
        margin: 0 1;
    }

   Input {
        width: 80%;
        /* Remove 'margin: 1 auto;' - centering will be handled by the parent container's layout */
        margin-top: 1; /* You can keep explicit vertical margins if needed */
        margin-bottom: 1;
        background: #444444;
        color: white;
        border: round #666666;
        text-align: left;
    }
    Input:focus {
        border: round dodgerblue;
    }
    """

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(id="header")
        yield Label("Termux API Quick Access Menu", classes="instruction-label")
        yield Container(
            Button("1. Toggle Torch", id="btn_torch", classes="menu-button"),
            Button("2. Battery Status", id="btn_battery", classes="menu-button"),
            Button("3. Send SMS", id="btn_sms", classes="menu-button"),
            Button("4. Set Brightness", id="btn_brightness", classes="menu-button"),
            Button("5. Toggle Wi-Fi", id="btn_wifi_toggle", classes="menu-button"),
            Button("6. Scan Wi-Fi", id="btn_wifi_scan", classes="menu-button"),
            Button("7. Control Volume", id="btn_volume", classes="menu-button"),
            Button("8. Device Info", id="btn_device_info", classes="menu-button"),
            Button("9. Play Beep", id="btn_beep", classes="menu-button"),
            Button("0. Exit", id="btn_exit", variant="error", classes="menu-button"),
            id="menu-container"
        )
        # Use RichLog for better display of multi-line output
        self.log_output = RichLog(id="output-log", auto_scroll=True, max_lines=100)
        yield self.log_output
        yield Footer()

    def on_mount(self) -> None:
        """Called after the app is mounted and widgets are composed."""
        self.log_output.write("[bold green]Welcome to Termux API TUI![/bold green]")
        self.log_output.write("Select an option above to run a command.")

    # --- Button Event Handlers ---

    @on(Button.Pressed, "#btn_torch")
    async def toggle_torch(self) -> None:
        self.log_output.write("[blue]Toggling torch...[/blue]")
        result = run_termux_command("torch")
        self.log_output.write(f"[green]Torch status: {result}[/green]")
        await self.push_screen(MessageDialog("Torch Toggled", f"Torch command executed.\nResult: {result}"))

    @on(Button.Pressed, "#btn_battery")
    async def show_battery_status(self) -> None:
        self.log_output.write("[blue]Fetching battery status...[/blue]")
        result = run_termux_command("battery-status")
        try:
            parsed_json = json.dumps(json.loads(result), indent=2)
            display_text = f"[green]Battery Info:[/green]\n[white]{parsed_json}[/white]"
        except json.JSONDecodeError:
            display_text = f"[red]Error parsing JSON:[/red]\n{result}"

        self.log_output.write(display_text)
        await self.push_screen(MessageDialog("Battery Status", display_text))

    @on(Button.Pressed, "#btn_sms")
    async def send_sms(self) -> None:
        self.log_output.write("[blue]Initiating SMS send...[/blue]")
        number = await self.push_screen_and_wait(
            InputDialog("Send SMS", "Enter phone number (e.g., +1234567890):")
        )
        if number is None:
            self.log_output.write("[yellow]SMS sending cancelled.[/yellow]")
            return

        message = await self.push_screen_and_wait(
            InputDialog("Send SMS", "Enter message:")
        )
        if message is None:
            self.log_output.write("[yellow]SMS sending cancelled.[/yellow]")
            return

        confirm = await self.push_screen_and_wait(
            ConfirmationDialog("Confirm SMS", f"Send SMS to {number} with message:\n'{message}'?")
        )

        if confirm:
            self.log_output.write(f"[blue]Sending SMS to {number} with message: '{message}'[/blue]")
            result = run_termux_command("sms-send", "-n", number, message)
            self.log_output.write(f"[green]SMS command result: {result}[/green]")
            await self.push_screen(MessageDialog("SMS Status", f"SMS command issued.\nResult: {result}"))
        else:
            self.log_output.write("[yellow]SMS sending cancelled.[/yellow]")

    @on(Button.Pressed, "#btn_brightness")
    async def set_brightness(self) -> None:
        self.log_output.write("[blue]Setting screen brightness...[/blue]")
        # Attempt to get current brightness for default value
        current_brightness_info = run_termux_command("brightness")
        current_brightness_level = "128" # Default if fetching fails
        try:
            # Simple regex to extract number assuming 'level":X' format
            import re
            match = re.search(r'level":(\d+)', current_brightness_info)
            if match:
                current_brightness_level = match.group(1)
        except Exception:
            pass # Ignore if we can't parse it

        level_str = await self.push_screen_and_wait(
            InputDialog("Set Brightness", "Enter brightness level (0-255):", default=current_brightness_level)
        )
        if level_str is None:
            self.log_output.write("[yellow]Brightness setting cancelled.[/yellow]")
            return

        try:
            level = int(level_str)
            if not (0 <= level <= 255):
                await self.push_screen(MessageDialog("Error", "Invalid brightness level. Please enter a number between 0 and 255."))
                self.log_output.write("[red]Invalid brightness level.[/red]")
                return
        except ValueError:
            await self.push_screen(MessageDialog("Error", "Invalid input. Please enter a numeric value."))
            self.log_output.write("[red]Invalid brightness input (not a number).[/red]")
            return

        self.log_output.write(f"[blue]Setting brightness to {level}...[/blue]")
        result = run_termux_command("brightness", str(level))
        self.log_output.write(f"[green]Brightness command result: {result}[/green]")
        await self.push_screen(MessageDialog("Brightness Set", f"Brightness set to {level}.\nResult: {result}"))

    @on(Button.Pressed, "#btn_wifi_toggle")
    async def toggle_wifi(self) -> None:
        self.log_output.write("[blue]Toggling Wi-Fi...[/blue]")
        confirm_enable = await self.push_screen_and_wait(
            ConfirmationDialog("Wi-Fi Control", "Do you want to [bold green]enable[/bold green] Wi-Fi?\n(Choose No to [bold red]disable[/bold red])")
        )

        if confirm_enable is True: # User chose Yes
            self.log_output.write("[blue]Enabling Wi-Fi...[/blue]")
            result = run_termux_command("wifi-enable", "true")
            self.log_output.write(f"[green]Wi-Fi enable command result: {result}[/green]")
            await self.push_screen(MessageDialog("Wi-Fi Status", f"Wi-Fi enabled (command issued).\nResult: {result}"))
        elif confirm_enable is False: # User chose No
            self.log_output.write("[blue]Disabling Wi-Fi...[/blue]")
            result = run_termux_command("wifi-enable", "false")
            self.log_output.write(f"[green]Wi-Fi disable command result: {result}[/green]")
            await self.push_screen(MessageDialog("Wi-Fi Status", f"Wi-Fi disabled (command issued).\nResult: {result}"))
        else: # User cancelled
            self.log_output.write("[yellow]Wi-Fi toggle cancelled.[/yellow]")


    @on(Button.Pressed, "#btn_wifi_scan")
    async def scan_wifi(self) -> None:
        self.log_output.write("[blue]Scanning for Wi-Fi networks...[/blue]")
        result = run_termux_command("wifi-scaninfo")
        try:
            parsed_json = json.dumps(json.loads(result), indent=2)
            display_text = f"[green]Available Wi-Fi Networks:[/green]\n[white]{parsed_json}[/white]"
        except json.JSONDecodeError:
            display_text = f"[red]Error parsing JSON:[/red]\n{result}"

        self.log_output.write(display_text)
        await self.push_screen(MessageDialog("Wi-Fi Scan Results", display_text))


    @on(Button.Pressed, "#btn_volume")
    async def control_volume(self) -> None:
        self.log_output.write("[blue]Controlling volume...[/blue]")
        stream_options = [
            ("alarm", "Alarm volume"),
            ("media", "Media playback volume"),
            ("ring", "Ringtone volume"),
            ("system", "System sounds volume"),
            ("voice_call", "Voice call volume"),
        ]

        # Use Select widget for choosing stream (Textual's equivalent to dialog --menu)
        stream_select = Select(
            options=stream_options,
            prompt="Select a volume stream",
            id="volume_stream_select"
        )
        # This will block until a selection is made
        stream = await self.push_screen_and_wait(stream_select)

        if stream is None:
            self.log_output.write("[yellow]Volume control cancelled.[/yellow]")
            return

        percentage_str = await self.push_screen_and_wait(
            InputDialog("Set Volume", f"Enter volume percentage (0-100) for '{stream}':", default="50")
        )

        if percentage_str is None:
            self.log_output.write("[yellow]Volume control cancelled.[/yellow]")
            return

        try:
            percentage = int(percentage_str)
            if not (0 <= percentage <= 100):
                await self.push_screen(MessageDialog("Error", "Invalid percentage. Please enter a number between 0 and 100."))
                self.log_output.write("[red]Invalid volume percentage.[/red]")
                return
        except ValueError:
            await self.push_screen(MessageDialog("Error", "Invalid input. Please enter a numeric value."))
            self.log_output.write("[red]Invalid volume input (not a number).[/red]")
            return

        self.log_output.write(f"[blue]Setting {stream} volume to {percentage}%...[/blue]")
        result = run_termux_command("volume", stream, str(percentage))
        self.log_output.write(f"[green]Volume command result: {result}[/green]")
        await self.push_screen(MessageDialog("Volume Set", f"{stream} volume set to {percentage}%.\nResult: {result}"))

    @on(Button.Pressed, "#btn_device_info")
    async def show_device_info(self) -> None:
        self.log_output.write("[blue]Fetching device information...[/blue]")
        # Using telephony-deviceinfo as an example, other API commands like info might exist.
        result = run_termux_command("telephony-deviceinfo")
        try:
            parsed_json = json.dumps(json.loads(result), indent=2)
            display_text = f"[green]Device Details:[/green]\n[white]{parsed_json}[/white]"
        except json.JSONDecodeError:
            display_text = f"[red]Error parsing JSON:[/red]\n{result}"

        self.log_output.write(display_text)
        await self.push_screen(MessageDialog("Device Info", display_text))

    @on(Button.Pressed, "#btn_beep")
    async def play_beep(self) -> None:
        self.log_output.write("[blue]Playing a short beep sound...[/blue]")
        # No direct beep command, using toast for visual feedback
        result = run_termux_command("toast", "Beep!", "-g", "bottom") # '-g bottom' places toast at bottom
        # Alternatively, for an audible beep using TTS:
        # result = run_termux_command("tts-speak", "Beep")
        self.log_output.write(f"[green]Beep command result: {result}[/green]")
        await self.push_screen(MessageDialog("Beep Played", f"Beep command executed.\nResult: {result}"))


    @on(Button.Pressed, "#btn_exit")
    async def exit_app(self) -> None:
        self.log_output.write("[yellow]Exiting Termux API Menu. Goodbye![/yellow]")
        await self.push_screen(MessageDialog("Exiting", "Exiting Termux API Menu. Goodbye!"))
        self.exit("User exited.")

    # --- Actions (for key bindings) ---
    def action_quit(self) -> None:
        self.exit()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

if __name__ == "__main__":
    app = TermuxApiApp()
    app.run()
