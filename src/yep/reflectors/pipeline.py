"""Data model to represent yep pipelines."""

class YepPipeline:

    def __init__(self, name, config, file_path):
        self.name = name
        self.config = config
        self.file_path = file_path
        # variables that where optional arguments can be pulled from
        self.vars = {}
        # individual steps of the pipeline that form a chain of calls
        self.tasks = []
