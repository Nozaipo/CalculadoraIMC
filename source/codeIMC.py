from PyQt6 import QtWidgets, uic, QtGui
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtWidgets import QDialog
import sys
from time import sleep

class Relatorio(QDialog):
	def __init__(self):
		super(Relatorio, self).__init__()
		uic.loadUi("layout/relatorio.ui",self)
		self.classificacao = None
		self.peso = None
		self.altura = None
		self.imc = None
		self.nome = None
		self.pesoIdeal = []
		self.descricoes = {
			"magreza": ["De acordo com a Organização Mundial da Saúde, seu IMC está abaixo do recomendado para a sua altura. Para atingir um valor de IMC normal, seu peso deve estar entre ", lambda x: f"< {x * 18.5:.1f} kg"],
			"normal": ["De acordo com a Organização Mundial da Saúde, seu IMC é considerado normal para a sua altura. Para manter o valor de IMC normal, seu peso pode variar entre ", lambda x: f"{x*18.5:.1f} e {x * 24.9:.1f} kg"],
			"sobrepeso": ["De acordo com a Organização Mundial da Saúde, seu IMC está acima do recomendado para a sua altura. Para atingir um valor de IMC normal, seu peso deve estar entre ", lambda x: f"{x * 24.9:.1f} e {x * 30:.1f} kg"],
			"obesidade": ["De acordo com a Organização Mundial da Saúde, seu IMC está acima do recomendado para a sua altura. Para atingir um valor de IMC normal, seu peso deve estar entre ", lambda x: f"> {x * 30:.1f} kg"]
		}

	def gerarRelatorio(self):

		janelas.widget(2).inicioRelatorio.setText(f"Olá, {self.nome}.\n\nSeu resultado foi {self.imc:.1f} kg/m²")

		magreza_label = janelas.widget(2).textoP_IDEAL_magreza
		magreza_descricao = self.descricoes['magreza']
		magreza_label.setText(magreza_descricao[1](self.altura))

		normal_label = janelas.widget(2).textoP_IDEAL_normal
		normal_descricao = self.descricoes['normal']
		normal_label.setText(normal_descricao[1](self.altura))

		sobrepeso_label = janelas.widget(2).textoP_IDEAL_sobrepeso
		sobrepeso_descricao = self.descricoes['sobrepeso']
		sobrepeso_label.setText(sobrepeso_descricao[1](self.altura))

		obesidade_label = janelas.widget(2).textoP_IDEAL_obesidade
		obesidade_descricao = self.descricoes['obesidade']
		obesidade_label.setText(obesidade_descricao[1](self.altura))

		janelas.widget(2).inicioDescricao.setText(self.descricoes[self.classificacao][0] + normal_descricao[1](self.altura))

		if self.classificacao == 'magreza':
			for i in (janelas.widget(2).textoMagreza, janelas.widget(2).textoIMC_magreza, janelas.widget(2).textoP_IDEAL_magreza):
				i.setStyleSheet('border-bottom: 1px solid rgb(200, 200, 255);background-color: rgba(255, 215, 196,0.85);color: rgba(33,33,33,1);')
		elif self.classificacao == 'normal':
			for i in (janelas.widget(2).textoNormal, janelas.widget(2).textoIMC_normal, janelas.widget(2).textoP_IDEAL_normal):
				i.setStyleSheet('border-bottom: 1px solid rgb(200, 200, 255);background-color: rgba(175, 255, 200, 0.8);color: rgba(33,33,33,1);')
		elif self.classificacao == 'sobrepeso':
			for i in (janelas.widget(2).textoSobrepeso, janelas.widget(2).textoIMC_sobrepeso, janelas.widget(2).textoP_IDEAL_sobrepeso):
				i.setStyleSheet('border-bottom: 1px solid rgb(200, 200, 255);background-color: rgba(255, 215, 196,0.85);color: rgba(33,33,33,1);')
		else:
			for i in (janelas.widget(2).textoObesidade, janelas.widget(2).textoIMC_obesidade, janelas.widget(2).textoP_IDEAL_obesidade):
				i.setStyleSheet('border-bottom: 1px solid rgb(200, 200, 255);background-color: rgba(255, 215, 196,0.85);color: rgba(33,33,33,1);')

class TelaCarregamento(QDialog):
	def __init__(self):
		super(TelaCarregamento, self).__init__()
		uic.loadUi("layout/carregando.ui",self)

	def rodar_carregamento(self):
		self.thread = QThread()
		self.girarCirculoCarregamento = girarCirculoCarregamento()
		self.girarCirculoCarregamento.moveToThread(self.thread)

		self.thread.started.connect(self.girarCirculoCarregamento.executar)
		self.girarCirculoCarregamento.concluido.connect(self.thread.quit)
		self.girarCirculoCarregamento.concluido.connect(self.girarCirculoCarregamento.deleteLater)
		self.thread.finished.connect(self.thread.deleteLater)
		self.girarCirculoCarregamento.atualizar.connect(self.atualizarRoda)
		self.thread.start()

	def atualizarRoda(self, texto):
		self.rodaroda.setStyleSheet(texto)

class girarCirculoCarregamento(QObject):
	concluido = pyqtSignal()
	atualizar = pyqtSignal(str)
	def executar(self):
		cores = ['white'] * 4
		base = "border-color:white; border-width: 5px;\
				border-style:solid solid solid solid;\
				border-radius: 50px;\
				border-color:"
		for _ in range(3):
			for i in range(4):
				cores[(i+1)%4] = 'rgb(135,135,255)'
				texto = base + f"{' '.join(cores)}"
				self.atualizar.emit(texto)
				cores = ['white'] * 4
				sleep(0.08)
			sleep(0.04)
		janelas.setCurrentIndex(janelas.currentIndex()+1)
		self.concluido.emit()

class PaginaInicial(QtWidgets.QMainWindow, Relatorio, TelaCarregamento):
	def __init__(self):
		super(PaginaInicial, self).__init__()
		uic.loadUi("layout/pagina-inicial.ui", self)
		self.camposTexto = [self.nomeInput, self.pesoInput, self.alturaInput]
		self.main()
		self.show()

	def main(self):
		janelas.setWindowTitle("Calculadora de IMC")
		janelas.setWindowIcon(QtGui.QIcon('icon.png'))
		self.calcularIMC.clicked.connect(self.CalcularIMC)

	def CalcularIMC(self):
		validador = [ 
			self.validarNome(self.nomeInput.text()),
			self.validarPeso(self.pesoInput.text()),
			self.validarAltura(self.alturaInput.text()),
			self.validarSexo([self.radioBMulher, self.radioBHomem])
		]

		if all(validador):
			self.nome = self.nomeInput.text()
			tam_altura = len(str(self.alturaInput.text()))
			self.peso = float(self.pesoInput.text())
			self.altura = float(self.alturaInput.text()) / 100 if tam_altura == 6 else float(self.alturaInput.text())
			self.imc = self.peso / (self.altura ** 2)

			if self.imc < 18.5:
				self.classificacao = "magreza"
			elif self.imc > 18.5 and self.imc <= 24.9:
				self.classificacao = 'normal'
			elif self.imc > 24.9 and self.imc <= 29.9:
				self.classificacao = 'sobrepeso'
			else:
				self.classificacao = 'obesidade'


			self.gerarRelatorio()
			janelas.widget(1).rodar_carregamento()
			janelas.setCurrentIndex(janelas.currentIndex()+1)

	def validarNome(self, nome):

		if nome == "":
			self.nomeErro.setStyleSheet("font-size:12px;color: rgb(255,0,0)")
			return False
		else:
			self.nomeErro.setStyleSheet("font-size:12px;color: rgb(33,33,33)")
			return True

	def validarSexo(self, sexo):
		casos = map(lambda x: x.isChecked(), sexo)

		if not any(casos):
			self.sexoErro.setStyleSheet("font-size:12px;color: rgb(255,0,0)")
			return False
		else:
			self.sexoErro.setStyleSheet("font-size:12px;color: rgb(33,33,33)")
			return True

	def validarPeso(self, peso):
		try:
			peso = peso.replace(",", ".")
			peso = float(peso)
			if peso < 0:
				raise ValueError
			self.pesoInput.setText(f"{peso:.2f}")
			self.pesoErro.setStyleSheet("font-size:12px;color: rgb(33,33,33)")
			return True
		except:
			self.pesoErro.setStyleSheet("font-size:12px;color: rgb(255,0,0)")
			return False

	def validarAltura(self, altura):
		try:
			altura = altura.replace(",", ".")
			altura = float(altura)
			if altura < 0:
				raise ValueError
			self.alturaInput.setText(f"{altura:.2f}")
			self.alturaErro.setStyleSheet("font-size:12px;color: rgb(33,33,33)")
			return True
		except:
			self.alturaErro.setStyleSheet("font-size:12px;color: rgb(255,0,0)")
			return False

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	janelas = QtWidgets.QStackedWidget()
	paginaInicial = PaginaInicial()
	telaCarregar = TelaCarregamento()
	relatorio = Relatorio()
	janelas.addWidget(paginaInicial)
	janelas.addWidget(telaCarregar)
	janelas.addWidget(relatorio)
	janelas.setFixedHeight(560)
	janelas.setFixedWidth(360)
	janelas.setCurrentIndex(0)
	janelas.show()
	app.exec()