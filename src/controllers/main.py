from src.controllers import drain

class Controllers:

    def exec(self, fn):
        return getattr(self, fn)

    def drain(self, args):
        return drain.run(args)

