import uuid, json, os;

class JsonHelper():
    def write(self, path, data):
        if type(data) != type(""):
            data = json.dumps(data);
        path_file = "/tmp/" + str(uuid.uuid4());
        try:
            with open(path_file, "w") as f:
                f.write(data);
                f.close();
            os.rename(path_file, path);
            return True;
        except:
            return False;
    def read(self, path, default=None):
        if not os.path.exists(path):
            return default;
        return json.loads(open(path, "r").read());

