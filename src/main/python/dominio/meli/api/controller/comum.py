import json
import time
from typing import Type, Callable

from apiclient import APIClient, JsonResponseHandler, exceptions, HeaderAuthentication
from apiclient.error_handlers import BaseErrorHandler
from apiclient.exceptions import UnexpectedError
from apiclient.request_formatters import BaseRequestFormatter
from apiclient.request_strategies import RequestStrategy
from apiclient.response import RequestsResponse
from apiclient.utils.typing import OptionalDict, OptionalJsonType
from pydantic import BaseModel
from requests import Response

from dominio.meli.api.controller.exception import (
    RequisicaoNaoFoiExecutadaComSucessoException,
)


class APontalPreCreatedJsonRequestFormatter(BaseRequestFormatter):
    """No action request formatter."""

    content_type = "application/json"

    @classmethod
    def format(cls, data: str) -> str:
        return data


class CustomResponseHandler(JsonResponseHandler):
    @staticmethod
    def get_request_data(response: Response) -> OptionalJsonType:
        json_response = super().get_request_data(response)
        json_response = response_or_exception_if_failure(json_response)

        del json_response["message"]
        del json_response["success"]

        return json_response


def atualizar_lista_de_parametros(parametros_iniciais: dict, **outros_parametros):
    parametros_iniciais.update(
        {k: v for k, v in outros_parametros.items() if v is not None}
    )
    return parametros_iniciais


def inserir_dados_query(url: str, **dados_filtro) -> str:
    """
        Cria uma nova url adicionando os parâmetros de paginação ou parâmetros de filtro na url passada como argumento
        Exemplos:
            >>> inserir_dados_query("/v1/clientes", page=1, per_page=10)
            >>> "/v1/clientes?page=1&per_page=10"

    :param url: URL original, sem filtros
    :param dados_filtro: Todos os parâmetros de filtro.

    :return: str
    """
    if not dados_filtro:
        return url

    parametros_query = [
        f"{nome}={valor}" for nome, valor in dados_filtro.items() if valor is not None
    ]
    parametros_query = "&".join(parametros_query)
    return f"{url}?{parametros_query}"


def response_or_exception_if_failure(response):
    if "error" in response:
        raise RequisicaoNaoFoiExecutadaComSucessoException(
            response["error"]["description"]
        )
    return response


def validar_sucesso_requisicao(funcao):
    def decorator(*args, **kwargs):
        response = funcao(*args, **kwargs)
        return response_or_exception_if_failure(response)

    return decorator


def converter_resultado(model: Type[BaseModel]):
    def inner_func(func):
        def decorator(*args, **kwargs):
            data = func(*args, **kwargs)
            data = get_dados_requisicao(data)
            if isinstance(data, dict):
                return model.model_validate(data)
            return [model.model_validate(d) for d in data]

        return decorator

    return inner_func


from pydantic.json import pydantic_encoder


def pydantic_custom_encoder(**kwargs):
    def base_encoder(obj):
        if isinstance(obj, BaseModel):
            return obj.model_dump(**kwargs)
        else:
            return pydantic_encoder(obj)

    return base_encoder


class APSystemErrorHandler(BaseErrorHandler):
    @staticmethod
    def get_exception(response: Response) -> exceptions.APIRequestError:
        status_code = response.get_status_code()
        exception_class = exceptions.UnexpectedError

        if 300 <= status_code < 400:
            exception_class = exceptions.RedirectionError
        elif 400 <= status_code < 500:
            exception_class = exceptions.ClientError
        elif 500 <= status_code < 600:
            exception_class = exceptions.ServerError

        json_response = json.loads(response.get_raw_data())
        mensagem = get_mensagem_erro(json_response)

        try:
            mensagem = f"Mensagem da API Meli: {mensagem}"
        except ValueError:
            pass

        return exception_class(
            message=(
                f"{status_code} Erro: {response.get_status_reason()} "
                f"URL: {response.get_requested_url()} "
                f"\n\n{mensagem}"
            ),
            status_code=status_code,
            info=response.get_raw_data(),
        )


class CustomRequestStrategy(RequestStrategy):
    def _make_request(
            self,
            request_method: Callable,
            endpoint: str,
            params: OptionalDict = None,
            headers: OptionalDict = None,
            data: OptionalDict = None,
            **kwargs,
    ) -> Response:
        """Make the request with the given method.

        Delegates response parsing to the response handler.
        """
        try:
            response = RequestsResponse(
                request_method(
                    endpoint,
                    params=self._get_request_params(params),
                    headers=self._get_request_headers(headers),
                    auth=self._get_username_password_authentication(),
                    data=self._get_formatted_data(data),
                    timeout=self._get_request_timeout(),
                    **kwargs,
                )
            )
        except Exception as error:
            raise UnexpectedError(
                f"Erro ao acessar o endpoint:' {endpoint}'.\n\nVerifique sua conexão com a Internet."
            ) from error
        else:
            self._check_response(response)
        return self._decode_response_data(response)


class RequisitionAwaiter:
    def __init__(self, tempo_espera:0.1):
        self.__last_requisition = None
        self.tempo_espera = tempo_espera

    def _await(self):
        if not self.__last_requisition:
            self.__last_requisition = time.time()
            return

        agora = time.time()
        if agora - self.__last_requisition < self.tempo_espera:
            time.sleep(self.tempo_espera - (agora - self.__last_requisition))

        self.__last_requisition = time.time()


class SystemBaseControllerAutenticated(APIClient, RequisitionAwaiter):
    def __init__(self, token):
        RequisitionAwaiter.__init__(self, tempo_espera=.4)
        authentication_method = HeaderAuthentication(token=token, scheme="Bearer")

        response_handler = JsonResponseHandler
        request_formatter = APontalPreCreatedJsonRequestFormatter
        error_handler = APSystemErrorHandler

        super().__init__(
            authentication_method=authentication_method,
            response_handler=response_handler,
            request_formatter=request_formatter,
            error_handler=error_handler,
            request_strategy=CustomRequestStrategy(),
        )

    def get(self, endpoint: str, params: OptionalDict = None, **kwargs):
        self._await()
        return super().get(endpoint, params, **kwargs)

    def put(
            self,
            endpoint: str,
            data: str | dict | BaseModel,
            params: OptionalDict = None,
            **kwargs,
    ):
        self._await()
        return super().put(endpoint, data=data, params=params, **kwargs)

    def post(
            self,
            endpoint: str,
            data: str | dict | BaseModel,
            params: OptionalDict = None,
            **kwargs,
    ):
        self._await()
        return super().post(endpoint, data=data, params=params, **kwargs)



class SystemBaseAutenticationController(APIClient, RequisitionAwaiter):
    def __init__(self):
        RequisitionAwaiter.__init__(self, tempo_espera=.4)
        authentication_method = None
        response_handler = JsonResponseHandler
        request_formatter = APontalPreCreatedJsonRequestFormatter
        error_handler = APSystemErrorHandler


        super().__init__(
            authentication_method=authentication_method,
            response_handler=response_handler,
            request_formatter=request_formatter,
            error_handler=error_handler,
        )
        self.__last_requisition = None


    def post(
            self,
            endpoint: str,
            data: str | dict | BaseModel,
            params: OptionalDict = None,
            **kwargs,
    ):
        self._await()
        return super().post(endpoint, data, params, **kwargs)

    def get(self, endpoint: str, params: OptionalDict = None, **kwargs):
        self._await()
        return super().get(endpoint, params, **kwargs)

    def put(
            self,
            endpoint: str,
            data: str | dict | BaseModel,
            params: OptionalDict = None,
            **kwargs,
    ):
        self._await()
        return super().put(endpoint, data, params, **kwargs)

    def patch(
            self,
            endpoint: str,
            data: str | dict | BaseModel,
            params: OptionalDict = None,
            **kwargs,
    ):
        self._await()
        return super().patch(endpoint, data, params, **kwargs)

    def delete(self, endpoint: str, params: OptionalDict = None, **kwargs):
        self._await()
        return super().delete(endpoint, params, **kwargs)


# def get_dados_paginacao(response):
#     return response["pagination"]


def get_dados_requisicao(response):
    return response


def get_mensagem_erro(response):
    return response["message"]
