# coding=UTF-8
import sublime, sublime_plugin, os, sys, subprocess, binascii
from os import path
try:
	import xml.etree.cElementTree as ElementTree
except Exception, e:
	import xml.etree.ElementTree as ElementTree 

from xml.dom.minidom import parse 
import xml.dom.minidom 

try:
    package_control_dir = os.getcwd()
except (ImportError) as e:
    package_control_dir = path.dirname(path.dirname(__file__))

POM_NS = "{http://maven.apache.org/POM/4.0.0}"

class MvnCommand(sublime_plugin.TextCommand):
	# 读取当前 POM 文件中的 project.build.finalname 节点值， 作为生成的可执行 java 包

	def getRunFileName(self):
		pomFileName = self.view.file_name();
		try: 
			tree = ElementTree.parse(pomFileName)     #打开xml文档 
			for builds in tree.findall("//%sbuild" % (POM_NS)):
				for build in builds:
					if build.tag == "%sfinalName" % (POM_NS):
						return build.text
		except Exception, _ex: 
			print 'ERROR: %s' % str(_ex)

		print "Error:cannot parse file:" + pomFileName + ", maybe you lost config the node: project.build.finalName"
		return ''

	def getPackaging(self):
		pomFileName = self.view.file_name();
		try: 
			tree = ElementTree.parse(pomFileName)     #打开xml文档 
			for packaging in tree.findall("//%spackaging" % (POM_NS)):
				return packaging.text
		except Exception, _ex: 
			print 'ERROR: %s' % str(_ex)

		print "Error:cannot parse file:" + pomFileName + ", maybe you lost config the node: project.packaging"
		return ''

	# 执行 cmd 命令，打印返回值
	@staticmethod
	def mvnCommand(self, cmd):
		settings = sublime.load_settings('Maven.sublime-settings')

		parameterPomFile = ' -f '+ self.view.file_name()
		parameterGs = ' -gs '+ settings.get('m2_path', '\.m2')
		outputEncode = settings.get('output_encode', 'gbk')
		command = 'mvn -e -Dmaven.test.skip '+cmd+parameterGs+parameterPomFile		
		try:
			subp=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			while subp.poll()==None:
				infos = subp.stdout.readline().strip()
				if len(infos) == 0:
					continue
				print infos.decode(outputEncode)
			print subp.returncode
		except Exception, _ex:
			print 'ERROR: %s' % str(_ex)

class MvnCleanCompileCommand(MvnCommand):
	def run(self, edit):
		self.mvnCommand(self, 'clean compile')

class MvnCleanInstallCommand(MvnCommand):
	def run(self, edit):
		self.mvnCommand(self, 'clean install')

class MvnPackageCommand(MvnCommand):
	def run(self, edit):
		self.mvnCommand(self, 'clean compile package')

class MvnRunJarCommand(MvnCommand):
	def run(self, edit):
		jarFileName = self.getRunFileName() + '.jar'
		jarFile = os.path.dirname(self.view.file_name()) + '/target/' + jarFileName;
		# print 'java -jar ' + jarFile
		# return
		output = os.popen('java -jar ' + jarFile, 'rw')
		print output.read() 
		# print jarFile



