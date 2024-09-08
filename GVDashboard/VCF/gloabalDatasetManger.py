from typing import Callable, Any
from VCF.filterInfo import DataSetInfo

class GlobalDatasetManager():
    """Holds a static record of all datasets created. Used to avoid unesesary searching and copying of datasets"""
    _datasets = [] # Holds a list of all existing datasets
    _listeners = []

    def register(dataset:DataSetInfo):
        """Register a dataset for global access"""
        GlobalDatasetManager._datasets.append(dataset)
        GlobalDatasetManager.__call_listeners()

    def deregister(dataset:DataSetInfo):
        """Remove a dataset from global access and delete references to it"""
        GlobalDatasetManager._datasets.remove(dataset)
        GlobalDatasetManager.__call_listeners()

    def reconfigure(datasets:list[DataSetInfo]):
        """Remove all datasets that do not appear in the given list"""
        GlobalDatasetManager._datasets = datasets
        GlobalDatasetManager.__call_listeners()

    def add_listener(command:Callable[[list[DataSetInfo]], Any]):
        """
        Add an update event listener to the dataset list to call a command when the list is updated.
        """
        GlobalDatasetManager._listeners.append(command)

    def remove_listener(command:Callable[[list[DataSetInfo]], Any]):
        """
        Remove event listener and stop listening for command
        """
        if command in GlobalDatasetManager._listeners:
            GlobalDatasetManager._listeners.remove(command)

    def __call_listeners():
        for listener in GlobalDatasetManager._listeners:
            listener(GlobalDatasetManager._datasets)
