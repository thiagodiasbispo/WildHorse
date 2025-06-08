import os
import traceback
from datetime import datetime
from pathlib import Path

from PyQt6.QtWidgets import QWidget

from apps.integrador_meli.controller import InserirCompatibilidadeController
from apps.integrador_meli.gui.ui.frm_inserir_compatibilidades_meli import Ui_FrmInserirCompatibilidadesMeli
from comum.assincrono import ExecutorAssincronaDeFuncaoGeradora
from comum.widget_models import TableDataframeModel
from comum.widget_utils import escolher_panilha_excel, mostrar_mensagem_erro_usuario_nao_autenticado, \
    mostrar_cursor_espera, restaurar_cursor
from dominio.meli.api.autenticacao_utils import usuario_esta_autenticado
from wild_horse.gui.widget.frm_barra_progresso_para_operacao_assincrona import FrmBarraProgressoParaExecucaoAssincrona


class FrmInserirCompatibilidadeMeli(QWidget):
    def __init__(self, *args, **kwargs):
        super(FrmInserirCompatibilidadeMeli, self).__init__(*args, **kwargs)
        self.ui = Ui_FrmInserirCompatibilidadesMeli()
        self.ui.setupUi(self)

        self.ui.btnAbrirPlanilhaCompatibilidade.clicked.connect(self._abrir_planilha_compatibilidade)
        self.ui.btnPlanilhaMarcaModelosAnos.clicked.connect(self._abrir_panilha_associacao_atributos)
        self.ui.btnInserirCompatibilidades.clicked.connect(self._inserir_compatibilidades)
        self._compatibilidade_controller = InserirCompatibilidadeController()

        # self.ui.tblCompatibilidades.setModel(TableDataframeModel())

    def _log_info(self, mensagem):
        mensagem = f"<font color='blue'>{mensagem}</font>"
        self._log_html(mensagem)

    def _log_error(self, mensagem):
        mensagem = f"<font color='red'>{mensagem}</font>"
        self._log_html(mensagem)

    def _log_html(self, mensagem):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.ui.txtLogs.appendHtml(f"{now} - {mensagem}")

    def _nova_compatibilidade_inserida(self, dados):
        sucesso, descricao, compat_result, mensagem = dados
        if sucesso:
            if compat_result:
                self._log_info(
                    f"{descricao}: {compat_result.created_compatibilities_count} compatibilidade(s) inserida(s).")
            else:
                self._log_info(f"{descricao}")
        else:
            self._log_error(f"{descricao}: Erro {mensagem}")

    def _carregamento_finalizado(self):
        self._log_info('Inserção finalizada!')

    def _criar_inseridor_compatibilidade(self):
        def inserir():
            print("Iniciando inserção de compatibilidades...")
            yield from self._compatibilidade_controller.inserir_compatibilidade_por_planilha(
                self.planilha_compatibilidade, self.planilha_associacao_atributos
            )

        gerador_anuncios = ExecutorAssincronaDeFuncaoGeradora(inserir)
        gerador_anuncios.erro_no_carregamento.connect(self._erro_no_carregamento)
        gerador_anuncios.carregamento_finalizado.connect(self._carregamento_finalizado)

        return gerador_anuncios

    def _criar_barra_progresso_de_insercao_anuncio(self, inseridor_compatibilidade):
        frm_barra_progresso = FrmBarraProgressoParaExecucaoAssincrona(inseridor_compatibilidade, parent=self,
                                                                      mensagem="Inserindo compatibilidades")
        return frm_barra_progresso

    def _erro_no_carregamento(self, mensagem):
        self._log_error(mensagem)

    def _inserir_compatibilidades(self):
        try:
            if not usuario_esta_autenticado():
                mostrar_mensagem_erro_usuario_nao_autenticado(self)
                return

            inseridor = self._criar_inseridor_compatibilidade()

            frm_barra_progresso = self._criar_barra_progresso_de_insercao_anuncio(inseridor)

            frm_barra_progresso.iniciar_carregamento_assincrono(
                callback_novos_dados_carregados=self._nova_compatibilidade_inserida)

        except Exception as e:
            self._log_error(str(e))
            traceback.print_exc()

    def _habilitar_botao_inserir_compatibilidades(self):
        habilitar = bool(self.planilha_compatibilidade) and bool(self.planilha_associacao_atributos)
        self.ui.btnInserirCompatibilidades.setEnabled(habilitar)

    def _abrir_planilha_compatibilidade(self):
        diretorio = os.getenv("USERPROFILE")

        if self.planilha_compatibilidade:
            diretorio = str(Path(self.planilha_compatibilidade).parent)

        arquivo = escolher_panilha_excel(self, titulo="Selecione a planilha de compatibilidade", directory=diretorio)

        if arquivo:
            self.ui.edtPlanilhaCompatibilidade.setText(arquivo)
            self._atualizar_tabela_compatibilidades()

        self._habilitar_botao_inserir_compatibilidades()

    def _atualizar_tabela_compatibilidades(self):
        try:
            self._log_info("Lendo planilha de compatibilidade...")
            self.repaint()
            mostrar_cursor_espera()
            df = self._compatibilidade_controller.ler_planilha_compatibilidade(self.planilha_compatibilidade)
            if not (model := self.ui.tblCompatibilidades.model()):
                self.ui.tblCompatibilidades.setModel(TableDataframeModel(df))
            else:
                model.set_df(df)
            self.ui.tblCompatibilidades.resizeColumnsToContents()
            self._log_info("Planilha de compatibilidade lida com sucesso!")
        except Exception as e:
            self._log_error("Erro ao ler planilha de compatibilidade: " + str(e))
        finally:
            restaurar_cursor()

    def _abrir_panilha_associacao_atributos(self):
        diretorio = os.getenv("USERPROFILE")

        if self.planilha_compatibilidade:
            diretorio = str(Path(self.planilha_compatibilidade).parent)
        elif self.planilha_associacao_atributos:
            diretorio = str(Path(self.planilha_associacao_atributos).parent)

        arquivo = escolher_panilha_excel(self, titulo="Selecione a planilha com relação de marca e modelo",
                                         directory=diretorio)

        if arquivo:
            self.ui.edtPlanilhaAssociacaoAtributos.setText(arquivo)

        self._habilitar_botao_inserir_compatibilidades()

    @property
    def planilha_compatibilidade(self):
        return self.ui.edtPlanilhaCompatibilidade.text().strip()

    @property
    def planilha_associacao_atributos(self):
        return self.ui.edtPlanilhaAssociacaoAtributos.text().strip()
