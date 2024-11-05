import time
from pynput import mouse

class StateMachine:
    def __init__(self):
        self.current_state = IdleState(self)
        print(f"Starting in {self.current_state.__class__.__name__}")
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()

    def on_click(self, x, y, button, pressed):
        self.current_state.on_click(x, y, button, pressed)

    def change_state(self, new_state):
        print(f"Entering {new_state.__class__.__name__}")
        self.current_state = new_state

class State:
    def __init__(self, machine):
        self.machine = machine

    def on_click(self, x, y, button, pressed):
        pass

class IdleState(State):
    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.middle and pressed:
            self.machine.change_state(ActiveState(self.machine))

class ActiveState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.start_time = time.time()

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.middle and not pressed:
            elapsed_time = time.time() - self.start_time
            print(f"Active time: {elapsed_time:.2f} seconds")
            if elapsed_time < 1.0:
                self.machine.change_state(IdleState(self.machine))
            else:
                self.machine.change_state(CooldownState(self.machine))

class CooldownState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.start_time = time.time()

    def on_click(self, x, y, button, pressed):
        pass  # Do nothing on click

    def execute(self):
        if time.time() - self.start_time >= 2:
            self.machine.change_state(IdleState(self.machine))

if __name__ == "__main__":
    state_machine = StateMachine()
    while True:
        if isinstance(state_machine.current_state, CooldownState):
            state_machine.current_state.execute()
        time.sleep(0.1)
