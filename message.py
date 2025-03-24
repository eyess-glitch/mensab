class Message:

    def __init__(self, sender: str, receiver: str, body: str):
        self.sender = sender
        self.receiver = receiver
        self.body = body

    def get_(self, attribute: str):
        if hasattr(self, attribute):
            return getattr(self, attribute)
        else:
            raise AttributeError(f"'Message' object has no attribute '{attribute}'")


