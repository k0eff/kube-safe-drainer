import src.controllers.drain as drain

class Controllers:

    def get(self, fn):
        return getattr(self, fn)

    def drain(self, args):
        return drain.run(args)


