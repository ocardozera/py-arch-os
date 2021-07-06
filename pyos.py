import os
import curses
import pycfg
from pyarch import load_binary_into_memory
from pyarch import cpu_t

class os_t:
	def __init__ (self, cpu, memory, terminal):
		self.cpu = cpu
		self.memory = memory
		self.terminal = terminal

		self.terminal.enable_curses()

		self.console_str = ""
		self.command = ""
		self.terminal.console_print("this is the console, type the commands here\n")

	def printk(self, msg):
		self.terminal.kernel_print("kernel: " + msg + "\n")

	def panic (self, msg):
		self.terminal.end()
		self.terminal.dprint("kernel panic: " + msg)
		self.cpu.cpu_alive = False
		#cpu.cpu_alive = False

#1
	def interrupt_keyboard (self):
		key = self.terminal.get_key_buffer()

		if ((key >= ord('a')) and (key <= ord('z'))) or ((key >= ord('A')) and (key <= ord('Z'))) or ((key >= ord('0')) and (key <= ord('9'))) or (key == ord(' ')) or (key == ord('-')) or (key == ord('_')) or (key == ord('.')):
			self.console_str += chr(key) #junta a string do console com o que o usuario digitou
			self.terminal.console_print("\r" + self.console_str) #imprimir o que esta na variavel string do console
			
		
		elif (key == curses.KEY_BACKSPACE):
			self.console_str = self.console_str[:-1] #remove o ultimo caractere da string do console
			self.terminal.console_print("\r" + self.console_str) #imprimir o que esta na variavel string do console
			return

		elif (key == curses.KEY_ENTER) or (key == ord('\n')):
			if (self.console_str == "" or self.console_str.isspace()): #verifica se console_str esta vazio, ou se contem somente caracteres vazios
				self.terminal.console_print("Digite caracteres validos\n")
				self.console_str = "" #zera a string 
#1
#2
			else:
				self.terminal.console_print("\n")
				self.interrupt_command()
				self.console_str = "" #zera a string 
				
			return

	def interrupt_command(self):
		if(self.console_str == "exit"):
			self.panic()
		
		if(self.console_str[0:3] == "run"):
			self.command = self.console_str[4:]
			self.syscall()


	def handle_interrupt (self, interrupt):
		# 1
		if (interrupt == pycfg.INTERRUPT_KEYBOARD): #verificar se e interrupcao de teclado, caso seja, vai pro metodo
			self.interrupt_keyboard()
		elif (interrupt == pycfg.INTERRUPT_MEMORY_PROTECTION_FAULT):
			self.terminal.console_print("Interrupção de falha de proteção geral não implementada")
		elif (interrupt == pycfg.INTERRUPT_TIMER):
			self.terminal.console_print("Interrupção de temporizador não implementada")
		return

	def syscall (self):
		self.terminal.console_print("As chamadas de sistemas não foram implementadas.")
		self.command = ""
		return
#2

#Implementar a interrupcao do teclado (OK)
#Implementar o console de comandos. Devera haver 1 comando 
#para fechar o simulador e 1 comando para carregar um processo
#(este ultimo sendo um comando sem efeito pratico, apenas um placeholder)
#Deixar mensagens de interrupcoes/syscalls nao implementadas
