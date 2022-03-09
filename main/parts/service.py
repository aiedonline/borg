import uuid;


class Service():
    def __init__(self):
        self.sessions = {};
    def new(self):
        session_id = str(uuid.uuid4());
        self.sessions[session_id] = str(uuid.uuid4());
        return self.sessions[session_id];
