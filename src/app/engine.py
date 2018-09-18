"""
@Description: Singleton with the "Engine" of the application
"""
class Engine(object):
    # Instance of the class
    instance = None

    # Main class of the singleton
    class __Engine(object):
        def __init__(self, args):
            self.args = args

        """
        @description: Train the offline phase and start the webapp
        """
        def start(self):
            # Avoid circular dependencies
            from .hbase import get_hist
            from .model import get_model
            from .process import start_stream, get_stats

            # Retrieve data from HBase for training as Spark DataFrame
            df = get_hist()

            # Train a model with the data
            self.model = get_model(df)

        def __str__(self):
            return repr(self)
    
    # Singleton methods to retrieve the class
    def __init__(self, args = None):
        if not Engine.instance:
            Engine.instance = Engine.__Engine(args)
    def __getattr__(self, name):
        return getattr(self.instance, name)