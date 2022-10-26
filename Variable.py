from Symbol import SymbolType, Symbol


class Variable:
    def __init__(self, name: str):
        self.name = name
        self.symbol_value = Symbol(SymbolType.NOT_INITIALIZED, None)

    def __str__(self):
        return f"Variable {self.name}: {str(self.symbol_value)}"
