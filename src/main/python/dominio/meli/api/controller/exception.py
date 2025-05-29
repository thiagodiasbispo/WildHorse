class APSystemBaseException(Exception):
    pass

class UsuarioNaoAutenticadoError(APSystemBaseException):
    pass


class RequisicaoNaoFoiExecutadaComSucessoException(APSystemBaseException):
    pass


class DadosInsconsistentesException(APSystemBaseException):
    pass
