class Graph:
    def __init__(self):
       self.data = {}
    
    def add(self, data):
        """adds data from a new dictionary to the graph"""
        
        self.data = self.data | data


