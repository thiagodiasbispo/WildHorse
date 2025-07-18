# Form implementation generated from reading ui file 'configuracoes.ui'
#
# Created by: PyQt6 UI code generator 6.9.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_FrmConfiguracoes(object):
    def setupUi(self, FrmConfiguracoes):
        FrmConfiguracoes.setObjectName("FrmConfiguracoes")
        FrmConfiguracoes.resize(715, 285)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(FrmConfiguracoes)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(parent=FrmConfiguracoes)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.TabPosition.West)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.TabShape.Triangular)
        self.tabWidget.setIconSize(QtCore.QSize(32, 32))
        self.tabWidget.setElideMode(QtCore.Qt.TextElideMode.ElideLeft)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tabBling = QtWidgets.QWidget()
        self.tabBling.setObjectName("tabBling")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tabBling)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gpbDadosAcessoAPI = QtWidgets.QGroupBox(parent=self.tabBling)
        self.gpbDadosAcessoAPI.setObjectName("gpbDadosAcessoAPI")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.gpbDadosAcessoAPI)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.RowWrapPolicy.DontWrapRows)
        self.formLayout.setObjectName("formLayout")
        self.cliendIdLabel = QtWidgets.QLabel(parent=self.gpbDadosAcessoAPI)
        self.cliendIdLabel.setObjectName("cliendIdLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.cliendIdLabel)
        self.edtClientId = QtWidgets.QLineEdit(parent=self.gpbDadosAcessoAPI)
        self.edtClientId.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.edtClientId.setCursorMoveStyle(QtCore.Qt.CursorMoveStyle.LogicalMoveStyle)
        self.edtClientId.setObjectName("edtClientId")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.edtClientId)
        self.clientSecretLabel = QtWidgets.QLabel(parent=self.gpbDadosAcessoAPI)
        self.clientSecretLabel.setObjectName("clientSecretLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.clientSecretLabel)
        self.edtClientSecret = QtWidgets.QLineEdit(parent=self.gpbDadosAcessoAPI)
        self.edtClientSecret.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.edtClientSecret.setObjectName("edtClientSecret")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.edtClientSecret)
        self.userIDLabel = QtWidgets.QLabel(parent=self.gpbDadosAcessoAPI)
        self.userIDLabel.setObjectName("userIDLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.userIDLabel)
        self.label_4 = QtWidgets.QLabel(parent=self.gpbDadosAcessoAPI)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_4)
        self.edtAuthorizationCode = QtWidgets.QLineEdit(parent=self.gpbDadosAcessoAPI)
        self.edtAuthorizationCode.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.edtAuthorizationCode.setObjectName("edtAuthorizationCode")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.edtAuthorizationCode)
        self.label_5 = QtWidgets.QLabel(parent=self.gpbDadosAcessoAPI)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_5)
        self.edtRedirectUri = QtWidgets.QLineEdit(parent=self.gpbDadosAcessoAPI)
        self.edtRedirectUri.setText("")
        self.edtRedirectUri.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.edtRedirectUri.setObjectName("edtRedirectUri")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.edtRedirectUri)
        self.label = QtWidgets.QLabel(parent=self.gpbDadosAcessoAPI)
        self.label.setObjectName("label")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.edtToken = QtWidgets.QLineEdit(parent=self.gpbDadosAcessoAPI)
        self.edtToken.setReadOnly(True)
        self.edtToken.setObjectName("edtToken")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.FieldRole, self.edtToken)
        self.label_2 = QtWidgets.QLabel(parent=self.gpbDadosAcessoAPI)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_2)
        self.edtRefreshToken = QtWidgets.QLineEdit(parent=self.gpbDadosAcessoAPI)
        self.edtRefreshToken.setReadOnly(True)
        self.edtRefreshToken.setObjectName("edtRefreshToken")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.ItemRole.FieldRole, self.edtRefreshToken)
        self.label_3 = QtWidgets.QLabel(parent=self.gpbDadosAcessoAPI)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3)
        self.edtValidadeToken = QtWidgets.QLineEdit(parent=self.gpbDadosAcessoAPI)
        self.edtValidadeToken.setReadOnly(True)
        self.edtValidadeToken.setObjectName("edtValidadeToken")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.ItemRole.FieldRole, self.edtValidadeToken)
        self.edtUserId = QtWidgets.QLineEdit(parent=self.gpbDadosAcessoAPI)
        self.edtUserId.setReadOnly(True)
        self.edtUserId.setObjectName("edtUserId")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.edtUserId)
        self.verticalLayout_3.addLayout(self.formLayout)
        self.verticalLayout.addWidget(self.gpbDadosAcessoAPI)
        self.tabWidget.addTab(self.tabBling, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnAbrirJanelaAutenticacao = QtWidgets.QPushButton(parent=FrmConfiguracoes)
        self.btnAbrirJanelaAutenticacao.setObjectName("btnAbrirJanelaAutenticacao")
        self.horizontalLayout.addWidget(self.btnAbrirJanelaAutenticacao)
        self.btnAtualizarToken = QtWidgets.QPushButton(parent=FrmConfiguracoes)
        self.btnAtualizarToken.setEnabled(False)
        self.btnAtualizarToken.setObjectName("btnAtualizarToken")
        self.horizontalLayout.addWidget(self.btnAtualizarToken)
        self.btnSalvar = QtWidgets.QPushButton(parent=FrmConfiguracoes)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icones/icones/salvar.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnSalvar.setIcon(icon)
        self.btnSalvar.setObjectName("btnSalvar")
        self.horizontalLayout.addWidget(self.btnSalvar)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(FrmConfiguracoes)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FrmConfiguracoes)

    def retranslateUi(self, FrmConfiguracoes):
        _translate = QtCore.QCoreApplication.translate
        FrmConfiguracoes.setWindowTitle(_translate("FrmConfiguracoes", "Configurações"))
        self.gpbDadosAcessoAPI.setTitle(_translate("FrmConfiguracoes", "Dados de acesso a API"))
        self.cliendIdLabel.setText(_translate("FrmConfiguracoes", "Cliend id:"))
        self.clientSecretLabel.setText(_translate("FrmConfiguracoes", "Client secret:"))
        self.userIDLabel.setText(_translate("FrmConfiguracoes", "User ID"))
        self.label_4.setText(_translate("FrmConfiguracoes", "Authorization code:"))
        self.label_5.setText(_translate("FrmConfiguracoes", "Redirect uri"))
        self.label.setText(_translate("FrmConfiguracoes", "Token:"))
        self.label_2.setText(_translate("FrmConfiguracoes", "Refresh token:"))
        self.label_3.setText(_translate("FrmConfiguracoes", "Validade do token:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabBling), _translate("FrmConfiguracoes", "Mercado Livre"))
        self.btnAbrirJanelaAutenticacao.setText(_translate("FrmConfiguracoes", "Abrir janela de autenticação"))
        self.btnAtualizarToken.setText(_translate("FrmConfiguracoes", "Atualizar token"))
        self.btnSalvar.setText(_translate("FrmConfiguracoes", "&Salvar"))
