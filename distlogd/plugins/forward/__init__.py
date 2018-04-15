import distlogd

class Forward(distlogd.Plugin):
    def match(self, data):
        return True

    def handle(self, data):
        print(data)

def initialize(options):
    print(options)
    return Forward()
