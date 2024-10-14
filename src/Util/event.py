"""
This script contains the implementation of an event class used to invoke lists of commands.
"""
from typing import Callable

class Event():
    def __init__(self) -> None:
        self.listeners = []

    def invoke(self,*args):
        """ Calls all listeners simultaneously. Listeners are functions. 
        """
        [listener(*args) for listener in self.listeners]
    
    def add_listener(self,command:Callable):
        if not self.is_listening(command): self.listeners.append(command)

    def remove_listener(self,command:Callable):
        if self.is_listening(command=command): self.listeners.remove(command)

    def is_listening(self,command:Callable):
        return command in self.listeners
    
    def remove_all(self):
        self.listeners = []