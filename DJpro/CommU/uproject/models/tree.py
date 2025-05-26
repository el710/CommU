"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""

class UtemTreeBase():
    '''
        Operative base of utems for user
    '''
    def __init__(self):
        self._base = []
        self.counter = 0
    
    def __iter__(self):
        self.counter = 0
        return self
    
    def __next__(self):
        if self.counter < len(self._base):
            ind = self.counter
            self.counter += 1
            return self._base[ind]
                
        raise StopIteration() ## method 'for' will catch this exception

    def len(self):
        return len(self._base)

    def add(self, utem_id, utem_type, parent_id=None):
        '''
            Create & save 
        '''
        item = {"id": utem_id,
                "type": utem_type,
                "parent": parent_id
                }
        self._base.append(item)

    def read(self, utem_id=None):
        '''
            Find and return
            if utem_id == None return first
        '''
        if utem_id:
            for item in self._base:
                if item["id"] == utem_id:
                    return item
        else:
            if self.len() > 0:
                return self._base[0]
        return None
    
    def get_list(self):
        return [{"id": item["id"], "type": item["type"]} for item in self._base]

    def edit(self, utem_id, new_parent_id):
        for item in self._base:
            if item["id"] == utem_id:
                item["parent"] = new_parent_id
                

    def delete(self, utem_id):
        """
            Delete item by id
        """
        for item in self._base:
            if item["id"] == utem_id:
                self._base.remove(item)
        

if __name__ == "__main__":

    tree = UtemTreeBase()

    tree.add("a")
    tree.add("b")
    tree.add("c")

    print(tree.__next__())

    print(tree.read())

    print(tree.__iter__())

    print(tree.__next__())



