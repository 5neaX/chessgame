class ChessAgent():
    def __init__(self, *args, **kwargs):
        pass
    
    def __call__(self, board):
        return self.getAction(board)
    
    def getAction(self, board):
        assert False, "[E] Method `getAction` is abstract and not implemented."
        return
    
    pass

