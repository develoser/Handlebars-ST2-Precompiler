Handlebars Precompiler for Sublime Text 2
==========================

This is a little plugin for [Sublime Text 2](http://www.sublimetext.com/2). You can precompile templates using the [Handlebars.js](http://handlebarsjs.com/) engine inside this cool IDE :)

## Install

* First of all you need to have installed and running [Nodejs](http://nodejs.org/download/)
* Next, install the [Handlebars](http://handlebarsjs.com/precompilation.html) npm package:

```
  $ npm install -g handlebars
```

* Finally just clone/download this repository into your Packages folder as *"Handlebars-ST2-Precompiler"*

## Usage

* Open a template with the default extension: **.hb, .handlebars or .html** *Note: You can add more extensions as you need.*
* If all are ok on right click you will see a new option in the context menu called: **Precompile with Handlebars**, select this option.
* A new precompiled file is created and opened in a new tab (with a **.js** extension, the same is also configurable).
* And thats all!

## Settings

The plugin comes with a few default options like following:

```
  {
  	"handlebars_exec" : "handlebars",
  	"allowed_extensions" : [".hb", ".hbs", ".handlebars", ".html"],
  	"compiler_options" : ["-m", "-f"],
  	"compiled_extension" : ".js"
  }
```

* **handlebars_exec**: This is the default command to run Handlebars
* **allowed_extensions**: This array contains all the allowed extensions by default. If your templates have a different one please add it here.
* **compiler_options**: This array contains the default options for Handlebars. Default are:```-m:``` Minimize and ```-f:``` ouput file.
* **compiled_extension**: Finally, if you want a different file for the output change it here.

You can modify any those options as you want.
