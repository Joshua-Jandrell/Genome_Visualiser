from typing import Callable, Any
from VCF.filterInfo import DataSetInfo

class GlobalDatasetManager():
    """Holds a static record of all datasets created. Used to avoid unesesary searching and copying of datasets"""
    _datasets = [] # Holds a list of all existing datasets: should not be shared
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

    def get_datasets()->list[DataSetInfo]:
        """
        Returns a list of all registered datasets.\n
        WARNING: Do not store any reference any datasets from this list as this will prevent datasets from being deleted.
        """
        return GlobalDatasetManager._datasets

    def add_listener(command:Callable[[list[str]], Any]):
        """
        Add an update event listener to the dataset list to call a command when the list is updated.\n
        The listener should accept a list of datasets name strings.
        """
        GlobalDatasetManager._listeners.append(command)

    def remove_listener(command:Callable[[list[str]], Any]):
        """
        Remove event listener and stop listening for command
        """
        if command in GlobalDatasetManager._listeners:
            GlobalDatasetManager._listeners.remove(command)

    def get_dataset_names()->list[str]:
        """Returns a list of all dataset names."""
        return [dataset.get_dataset_name() for dataset in GlobalDatasetManager._datasets]
    
    def get_dataset_by_name(dataset_name:str)->DataSetInfo:
        """
        Returns a dataset with the given input name (if any)\n
        WARNING: Do not keep a reference to the returned dataset as this will prevent data from being deleted.
        """
        return next(dataset for dataset in GlobalDatasetManager._datasets if dataset_name == dataset.get_dataset_name())

    def __call_listeners():
        dataset_names = GlobalDatasetManager.get_dataset_names()
        for listener in GlobalDatasetManager._listeners:
            listener(dataset_names)
