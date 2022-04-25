from escavador.resources.endpoint import Endpoint
from escavador.resources.enums import TiposBusca
from escavador.resources.documento import Documento
from typing import Optional


class BuscaAssincrona(Endpoint):

    def get_processo(self, numero_unico: str, *, send_callback: Optional[bool] = None, wait: Optional[bool] = None,
                     autos: Optional[bool] = None, usuario: Optional[str] = None, senha: Optional[str] = None,
                     origem: Optional[str] = None) -> dict:
        """
        Cria uma busca assíncrona com o numero único, e busca por ele em todos os tribunais
        :param senha: a senha do advogado para o tribunal, obrigatório se autos == 1
        :param usuario: o usuário do advogado para o tribunal, obrigatório se autos == 1
        :param origem: sigla de um tribunal para fazer a busca, utilizado para forçar a busca em um tribunal diferente
        do tribunal do processo
        :param autos: opção para retornar os autos do processo
        :param wait: opção para esperar pelo resultado, espera no máximo 1 minuto
        :param send_callback: opção para mandar um callback com o resultado da busca
        :param numero_unico: o numero único do processo
        :return: dict
        """

        data = {
            'send_callback': send_callback,
            'wait': wait,
            'autos': autos,
            'usuario': usuario,
            'senha': senha,
            'origem': origem
        }

        return self.methods.post(f"processo-tribunal/{numero_unico}/async", data=data)

    def get_processo_por_nome(self, origem: str, nome: str, *, send_callback: Optional[bool] = None,
                              wait: Optional[bool] = None, permitir_parcial: Optional[bool] = None) -> dict:
        """
        Cria uma busca assíncrona no tribunal de origem baseada no nome enviado
        :param permitir_parcial: opção para não fazer a busca em todos os sistemas de um tribunal
        :param wait:  opção para esperar pelo resultado, espera no máximo 1 minuto
        :param send_callback: opção para mandar um callback com o resultado da busca
        :param origem: o tribunal onde a busca será realizada
        :param nome: o nome a ser buscado
        :return: dict
        """

        data = {
            'nome': nome,
            'permitir_parcial': permitir_parcial,
            'send_callback': send_callback,
            'wait': wait
        }

        return self.methods.post(f"tribunal/{origem.upper()}/busca-por-nome/async", data=data)

    def get_processo_por_documento(self, origem: str, numero_documento: str, *, send_callback: Optional[bool] = None,
                                   wait: Optional[bool] = None, permitir_parcial: Optional[bool] = None) -> dict:
        """
        Cria uma busca assíncrona no tribunal de origem baseada no numero de documento enviado
        :param permitir_parcial: opção para não fazer a busca em todos os sistemas de um tribunal
        :param wait:  opção para esperar pelo resultado, espera no máximo 1 minuto
        :param send_callback: opção para mandar um callback com o resultado da busca
        :param origem: o tribunal onde a busca será realizada
        :param numero_documento: o documento que será pesquisado
        :return: dict
        """

        data = {
            'numero_documento': numero_documento,
            'permitir_parcial': permitir_parcial,
            'send_callback': send_callback,
            'wait': wait
        }

        return self.methods.post(f"tribunal/{origem.upper()}/busca-por-documento/async", data=data)

    def get_processo_por_oab(self, origem: str, numero_oab: str, estado_oab: str, *,
                             send_callback: Optional[bool] = None, wait: Optional[bool] = None,
                             permitir_parcial: Optional[bool] = None) -> dict:
        """
        Cria uma busca assíncrona no tribunal de origem baseada nos dados de oab enviados
        :param permitir_parcial: opção para não fazer a busca em todos os sistemas de um tribunal
        :param wait:  opção para esperar pelo resultado, espera no máximo 1 minuto
        :param send_callback: opção para mandar um callback com o resultado da busca
        :param origem: o tribunal onde a busca será realizada
        :param numero_oab: o numero da oab que será pesquisado
        :param estado_oab: o estado da oab enviada
        :return: dict
        """

        data = {
            'numero_oab': numero_oab,
            'estado_oab': estado_oab,
            'permitir_parcial': permitir_parcial,
            'send_callback': send_callback,
            'wait': wait
        }

        return self.methods.post(f"tribunal/{origem.upper()}/busca-por-oab/async", data=data)

    def busca_em_lote(self, tipo_busca: TiposBusca, origens: list[str], *, send_callback: Optional[bool] = None,
                      numero_oab: Optional[str] = None, estado_oab: Optional[str] = None,
                      numero_documento: Optional[str] = None, nome: Optional[str] = None) -> dict:
        """
        Cria buscas do mesmo tipo para todos os tribunais enviados
        :param nome: o nome que será pesquisado
        :param numero_documento: o documento que será pesquisado
        :param estado_oab:  o estado da oab enviada
        :param numero_oab:  o numero da oab que será pesquisado
        :param send_callback: opção para mandar um callback com o resultado da busca
        :param origens: os tribunais onde a busca será realizada
        :param tipo_busca: the tipe of search, available types: busca_por_nome, busca_por_documento, busca_por_oab
        :return: dict
        """

        origens = [origem.upper() for origem in origens]

        data = {
            'tipo': tipo_busca.value,
            'tribunais': origens,
            'nome': nome,
            'numero_documento': numero_documento,
            'numero_oab': numero_oab,
            'estado_oab': estado_oab,
            'send_callback': send_callback
        }

        return self.methods.post("tribunal/async/lote", data=data)

    def get_todos_resultados(self) -> dict:
        """
        Retorna todos os resultados de busca
        :return: dict
        """

        return self.methods.get('async/resultados')

    def get_resultado(self, id_busca: int) -> dict:
        """
        Retorna um resultado de busca específico
        :param id_busca: id do resultado
        :return: dict
        """

        return self.methods.get(f'async/resultados/{id_busca}')

    def get_pdf(self, link_pdf: str, path: str, nome_arquivo: str) -> dict:
        """
        Baixa um pdf de autos de acordo com seu link e salva no caminho enviado, com o nome enviado
        :param nome_arquivo: nome do arquivo a ser criado
        :param link_pdf: link do documento
        :param path: caminho onde o pdf será salvo
        :return: dict
        """
        conteudo = self.methods.get(link_pdf)

        return Documento.get_pdf(conteudo, path, nome_arquivo)
