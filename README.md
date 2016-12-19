# sublime-maven-simple
this is a simple maven plugin for sublime Text 2

### install 
#### 1. copy this repository code to SublimeText2BasePath\Data\Packages
#### 2. restart sublime text 2

### configuration
#### 1. open file Maven.sublime-settings
 
```
{
	"m2_path": "F:\\.m2\\settings.xml",   //maven global settings file path
	"output_encode": "gbk"  //output text encode in sublime console window
}
```
#### 2. config command
 if you like hot-key to run maven command, you can config file: Default (\<your os type\>).sublime-keymap

### enable command list:

 * mvn clean compile
 * mvn clean install
 * mvn package
 * mvn run jar     //java -jar something.jar
