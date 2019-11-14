#defines a single leg
from nanome.util import Logs
class FuzzerCommand(object):
    def __init__(self, fuzzer_info):
        self.done = False
        self.fuzzer_info = fuzzer_info
        Logs.message("Selected Command:", self.get_name())
        Logs.inc_tab()

    def get_name(self):
        return self._get_name()
    
    def get_done(self):
        return self.done

    def rules(self):
        Logs.message("Checking rules...")
        Logs.inc_tab()
        success = self._rules()
        if not success:
            Logs.message("failed")
        else:
            Logs.message("success")
        Logs.dec_tab()
        return success

    def run(self):
        Logs.message("Running...")
        Logs.inc_tab()
        result = self._run()
        return result

    def finish(self):
        self.done = True
        Logs.dec_tab()
        Logs.message("Finished Command:", self.get_name())
        Logs.dec_tab()


    def _get_name(self):
        raise NotImplementedError()

    def _get_done(self):
        raise NotImplementedError()
    
    def _rules(self, FuzzerInfo):
        raise NotImplementedError()

    def _run(self, FuzzerInfo):
        raise NotImplementedError()

class ExampleCommand(FuzzerCommand):
    def __init__(self):
        FuzzerCommand.__init__(self)
        self.done = False

    def _get_name(self):
        return "Example"

    def _rules(self, FuzzerInfo):
        return True

    def _run(self, FuzzerInfo):
        pass