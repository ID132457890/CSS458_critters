class AnalyticsReporting(object):
    def __init__(self, model):
        self.model = model
        self.analyzers = [ConsoleAnalyzer(model)]

    def turn_analyze(self):
        for analyzer in self.analyzers:
            analyzer.turn_analyze()

    def round_analyze(self):
        for analyzer in self.analyzers:
            analyzer.round_analyze()

    def finish_analyze(self):
        for analyzer in self.analyzers:
            analyzer.finish_analyze()

class ConsoleAnalyzer(object):
    def __init__(self, model):
        self.model = model

    def turn_analyze(self):
        pass

    def round_analyze(self):
        pass

    def finish_analyze(self):
        pass