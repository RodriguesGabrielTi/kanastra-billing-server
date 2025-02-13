class GovernmentId:
    def __init__(self, value: str):
        # Essa classe é importante para implementar uma validação mais robusta do id do documento, no nosso exemplo
        # Apenas iremos validar se o valor não é vazio
        if not value:
            raise ValueError("Government ID cannot be empty")
        self.value = value
