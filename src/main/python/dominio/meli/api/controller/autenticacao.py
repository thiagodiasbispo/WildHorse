import string
from random import sample

from dominio.meli.api.controller.comum import (
    SystemBaseAutenticationController,
    inserir_dados_query,
    validar_sucesso_requisicao,
)


class AutenticacaoController(SystemBaseAutenticationController):
    def __init__(self, url_autenticacao, url_token, client_id, client_secret, redirect_uri):
        super().__init__()
        self._client_id = client_id
        self._client_secret = client_secret
        self._url_autenticacao = url_autenticacao
        self._url_token = url_token
        self._redirect_uri = redirect_uri

    def get_url_autenticacao(self):
        random_state = "".join(sample(string.ascii_letters, 20))
        url = inserir_dados_query(
            self._url_autenticacao,
            response_type="code",
            client_id=self._client_id,
            state=random_state,
            redirect_uri=self._redirect_uri
        )
        return url

    # def _get_credenciais(self):
    #     credenciais_b64 = f"{self._client_id}:{self._client_secret}"
    #     credenciais_b64 = credenciais_b64.encode("ascii")
    #     credenciais_b64 = base64.b64encode(credenciais_b64)
    #     return bytes.decode(credenciais_b64)

    @validar_sucesso_requisicao
    def get_token(self, code):
        payload = {
            "grant_type": "authorization_code",
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "code": code,
            "redirect_uri": self._redirect_uri
        }
        headers = {"Content-Type": "application/json"}
        return self.post(self._url_token, payload, json=headers)

    @validar_sucesso_requisicao
    def refresh_token(self, refresh_token):
        dice = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        return self.post(self._url_token, {}, json=dice)
