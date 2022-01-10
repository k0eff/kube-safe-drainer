from src.controllers import drain, upgrade

class Controllers:

    def exec(self, fn):
        return getattr(self, fn)

    def drain(self, args):
        return drain.run(args)

    def upgrade(self, args):
        return upgrade.run(args)
