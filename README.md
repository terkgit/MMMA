# MyMediaMouseAssist

This project implements a tray application that allows users to control the system volume using mouse movements. The application supports different states, and the volume control is active only in the media state.

## Brief Description for Users
MyMediaMouseAssist provides a convenient way to control your system volume using your mouse. Once you run the app, an icon will appear in your system tray. Click the middle mouse button to switch to media mode and use the scroll wheel to adjust the volume. The application will automatically revert to normal mode after 2 seconds of inactivity.

## Features
- Control system volume using mouse scroll.
- Toggle between active, inactive, and media states.
- Custom tray icon indicating the current state.
- Idle timeout to automatically revert to the active state from the media state.

## Requirements
- Python 3.x
- The following Python libraries:
  - pystray
  - pillow
  - pynput
```
pip install pystray
pip install pillow
pip install pynput

```

## Script Overview

### Main Components

- **TrayStateMachine**: Handles the state transitions and tray icon updates.
- **create_image(text, color)**: Generates the tray icon image with specified text and color.
- **set_state(state)**: Sets the current state and updates the tray icon accordingly.
- **toggle_state(icon, item)**: Toggles between active and inactive states.
- **media_state()**: Activates the media state if the current state is active.
- **exit_app(icon, item)**: Stops the tray icon and signals the application to terminate.
- **on_clicked(x, y, button, pressed)**: Activates the media state when the middle mouse button is pressed.
- **on_scroll(x, y, dx, dy)**: Controls the volume when in media state using mouse scroll.
- **change_volume(key_code)**: Simulates volume key press and release.
- **start_idle_timer()**: Starts the timer to revert to the active state after idle timeout.
- **cancel_idle_timer()**: Cancels the idle timer.
- **return_to_active()**: Reverts to the active state from the media state.

### Logic Description for Developers

The application is built using a state machine design pattern with the following logic:

- **Initialization**: The `TrayStateMachine` class initializes the application with the active state. It sets up the tray icon using `pystray` and the global mouse listener using `pynput`.

- **State Management**:
  - **Active State**: Default state where the tray icon is green. The application listens for the middle mouse button click to transition to the media state.
  - **Inactive State**: User can toggle to this state where the tray icon turns red, indicating no actions are being monitored.
  - **Media State**: Activated by clicking the middle mouse button. The tray icon turns blue, allowing volume control via the scroll wheel. The application reverts to the active state after 2 seconds of inactivity.

- **Tray Icon**: The tray icon is created and managed using `pystray`. The icon updates based on the current state of the application, displaying different colors for each state.

- **Mouse Listener**: The global mouse listener is set up to monitor clicks and scrolls. The middle mouse button click transitions to the media state, and the scroll wheel controls the volume in the media state.

- **Volume Control**: Volume changes are simulated using `ctypes` to send virtual key codes for volume up and down.

- **Idle Timer**: An idle timer is implemented using `threading.Timer` to revert to the active state after a period of inactivity in the media state.

### Usage

- **Run the script**: Double-click the `volume_control_with_tray.pyw` file to start the application.
- **Tray Icon**:
  - The tray icon will appear in the system tray with an "M" symbol.
  - Right-click the icon to toggle between active and inactive states or to exit the application.
- **Volume Control**:
  - Press the middle mouse button to switch to media state.
  - Use the mouse scroll wheel to adjust the volume (up to increase, down to decrease).
  - The application will revert to the active state after 2 seconds of inactivity in the media state.

## Contributing

Feel free to submit issues or pull requests to improve the functionality or fix bugs.

## License

This project is licensed under the MIT License.
