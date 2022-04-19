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
			"magreza": ["De acordo com a Organização Mundial da Saúde, seu IMC está abaixo do recomendado para a sua altura.\nPara atingir um valor de IMC normal, seu peso deve estar entre ", lambda x: f"< {x * 18.5:.1f} kg"],
			"normal": ["De acordo com a Organização Mundial da Saúde, seu IMC é considerado normal para a sua altura.\nPara manter o valor de IMC normal, seu peso pode variar entre ", lambda x: f"{x*18.5:.1f} a {x * 24.9:.1f} kg"],
			"sobrepeso": ["De acordo com a Organização Mundial da Saúde, seu IMC está acima do recomendado para a sua altura.\nPara atingir um valor de IMC normal, seu peso deve estar entre ", lambda x: f"{x * 24.9:.1f} a {x * 29.9:.1f} kg"],
			"obesidade1": ["De acordo com a Organização Mundial da Saúde, seu IMC está acima do recomendado para a sua altura.\nPara atingir um valor de IMC normal, seu peso deve estar entre ", lambda x: f"{x * 30:.1f} a {x * 34.9:.1f} kg"],
			"obesidade2": ["De acordo com a Organização Mundial da Saúde, seu IMC está acima do recomendado para a sua altura.\nPara atingir um valor de IMC normal, seu peso deve estar entre ", lambda x: f"{x * 35:.1f} a {x * 39.9:.1f} kg"],
			"obesidade3": ["De acordo com a Organização Mundial da Saúde, seu IMC está acima do recomendado para a sua altura.\nPara atingir um valor de IMC normal, seu peso deve estar entre ", lambda x: f"> {x * 40:.1f} kg"]
		}

	def gerarRelatorio(self):

		textoSaudacao = f"Olá, {self.nome}.\n\nSeu resultado foi {self.imc:.1f} kg/m²"

		janelas.widget(2).inicioRelatorio.setText(textoSaudacao)

		magreza_label = janelas.widget(2).textoP_IDEAL_magreza
		magreza_descricao = self.descricoes['magreza']
		magreza_label.setText(magreza_descricao[1](self.altura))

		normal_label = janelas.widget(2).textoP_IDEAL_normal
		normal_descricao = self.descricoes['normal']
		normal_label.setText(normal_descricao[1](self.altura))

		sobrepeso_label = janelas.widget(2).textoP_IDEAL_sobrepeso
		sobrepeso_descricao = self.descricoes['sobrepeso']
		sobrepeso_label.setText(sobrepeso_descricao[1](self.altura))

		obesidade1_label = janelas.widget(2).textoP_IDEAL_obesidade1
		obesidade1_descricao = self.descricoes['obesidade1']
		obesidade1_label.setText(obesidade1_descricao[1](self.altura))

		obesidade2_label = janelas.widget(2).textoP_IDEAL_obesidade2
		obesidade2_descricao = self.descricoes['obesidade2']
		obesidade2_label.setText(obesidade2_descricao[1](self.altura))

		obesidade3_label = janelas.widget(2).textoP_IDEAL_obesidade3
		obesidade3_descricao = self.descricoes['obesidade3']
		obesidade3_label.setText(obesidade3_descricao[1](self.altura))

		janelas.widget(2).inicioDescricao.setText(self.descricoes[self.classificacao][0] + normal_descricao[1](self.altura))

		textoDescricao = '\n\n' + janelas.widget(2).inicioDescricao.text() + '\n\n'
		textoDescResultado = f"{'CLASSIFICAÇÃO':^20}|{'IMC':^20}|{'PESO IDEAL':^20}\n"

		if self.classificacao == 'magreza':
			textoResultado = f"{janelas.widget(2).textoMagreza.text():^20}|{janelas.widget(2).textoIMC_magreza.text():^20}|{janelas.widget(2).textoP_IDEAL_magreza.text():^20}"
			for i in (janelas.widget(2).textoMagreza, janelas.widget(2).textoIMC_magreza, janelas.widget(2).textoP_IDEAL_magreza):
				i.setStyleSheet('border-bottom: 1px solid rgb(200, 200, 255);background-color: rgba(255, 215, 196,0.85);color: rgba(33,33,33,1);')
		elif self.classificacao == 'normal':
			textoResultado = f"{janelas.widget(2).textoNormal.text():^20}|{janelas.widget(2).textoIMC_normal.text():^20}|{janelas.widget(2).textoP_IDEAL_normal.text():^20}"
			for i in (janelas.widget(2).textoNormal, janelas.widget(2).textoIMC_normal, janelas.widget(2).textoP_IDEAL_normal):
				i.setStyleSheet('border-bottom: 1px solid rgb(200, 200, 255);background-color: rgba(175, 255, 200, 0.8);color: rgba(33,33,33,1);')
		elif self.classificacao == 'sobrepeso':
			textoResultado = f"{janelas.widget(2).textoSobrepeso.text():^20}|{janelas.widget(2).textoIMC_sobrepeso.text():^20}|{janelas.widget(2).textoP_IDEAL_sobrepeso.text():^20}"
			for i in (janelas.widget(2).textoSobrepeso, janelas.widget(2).textoIMC_sobrepeso, janelas.widget(2).textoP_IDEAL_sobrepeso):
				i.setStyleSheet('border-bottom: 1px solid rgb(200, 200, 255);background-color: rgba(255, 215, 196,0.85);color: rgba(33,33,33,1);')
		elif self.classificacao == 'obesidade1':
			textoResultado = f"{janelas.widget(2).textoObesidade1.text():^20}|{janelas.widget(2).textoIMC_obesidade1.text():^20}|{janelas.widget(2).textoP_IDEAL_obesidade1.text():^20}"
			for i in (janelas.widget(2).textoObesidade1, janelas.widget(2).textoIMC_obesidade1, janelas.widget(2).textoP_IDEAL_obesidade1):
				i.setStyleSheet('border-bottom: 1px solid rgb(200, 200, 255);background-color: rgba(255, 215, 196,0.85);color: rgba(33,33,33,1);')
		elif self.classificacao == 'obesidade2':
			textoResultado = f"{janelas.widget(2).textoObesidade2.text():^20}|{janelas.widget(2).textoIMC_obesidade2.text():^20}|{janelas.widget(2).textoP_IDEAL_obesidade2.text():^20}"
			for i in (janelas.widget(2).textoObesidade2, janelas.widget(2).textoIMC_obesidade2, janelas.widget(2).textoP_IDEAL_obesidade2):
				i.setStyleSheet('border-bottom: 1px solid rgb(200, 200, 255);background-color: rgba(255, 215, 196,0.85);color: rgba(33,33,33,1);')
		else:
			textoResultado = f"{janelas.widget(2).textoObesidade3.text():^20}|{janelas.widget(2).textoIMC_obesidade3.text():^20}|{janelas.widget(2).textoP_IDEAL_obesidade3.text():^20}"
			for i in (janelas.widget(2).textoObesidade3, janelas.widget(2).textoIMC_obesidade3, janelas.widget(2).textoP_IDEAL_obesidade3):
				i.setStyleSheet('border-bottom: 1px solid rgb(200, 200, 255);background-color: rgba(255, 215, 196,0.85);color: rgba(33,33,33,1);')

		with open(f"Relatório - {self.nome}.txt", 'w') as relatorio:
			relatorio.write(textoSaudacao + textoDescricao + textoDescResultado + textoResultado)

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
			elif self.imc > 30 and self.imc <= 34.9:
				self.classificacao = 'obesidade1'
			elif self.imc > 35 and self.imc <= 39.9:
				self.classificacao = 'obesidade2'
			else:
				self.classificacao = 'obesidade3'




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