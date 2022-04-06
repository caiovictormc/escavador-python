from escavador.resources.endpoint import Endpoint


class Saldo(Endpoint):

    def get(self) -> dict:
        """
        Retorna a quantidade de créditos do usuário
        :return: dict
        """
        return self.methods.get("quantidade-creditos")
