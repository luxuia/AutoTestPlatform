# -*- coding: utf-8 -*-
import sys, os
import shutil
import json
import uuid
import subprocess

"""
uiautomate use multithread init, see 
https://github.com/pywinauto/pywinauto/issues/472
"""
import warnings
warnings.simplefilter('ignore', UserWarning)
sys.coinit_flags = 2

from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt

from .ext import *
from .screenshot.screenshot import ScreenShootWindow

from source.core.help import G


EXPORT_PATH = '__export_res__'

class Main(QtWidgets.QMainWindow):

    def __init__(self,parent=None):
        QtWidgets.QMainWindow.__init__(self,parent)

        self.filename = ""

        self.changesSaved = True

        self.initUI()

    def initToolbar(self):

        self.newAction = QtWidgets.QAction(QtGui.QIcon("icons/new.png"),"New",self)
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.setStatusTip("Create a new document from scratch.")
        self.newAction.triggered.connect(self.new)

        self.openAction = QtWidgets.QAction(QtGui.QIcon("icons/open.png"),"Open file",self)
        self.openAction.setStatusTip("Open existing document")
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.open)

        self.saveAction = QtWidgets.QAction(QtGui.QIcon("icons/save.png"),"Save",self)
        self.saveAction.setStatusTip("Save document")
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.save)

        self.findAction = QtWidgets.QAction(QtGui.QIcon("icons/find.png"),"Find and replace",self)
        self.findAction.setStatusTip("Find and replace words in your document")
        self.findAction.setShortcut("Ctrl+F")
        self.findAction.triggered.connect(find.Find(self).show)

        self.cutAction = QtWidgets.QAction(QtGui.QIcon("icons/cut.png"),"Cut to clipboard",self)
        self.cutAction.setStatusTip("Delete and copy text to clipboard")
        self.cutAction.setShortcut("Ctrl+X")
        self.cutAction.triggered.connect(self.text.cut)

        self.copyAction = QtWidgets.QAction(QtGui.QIcon("icons/copy.png"),"Copy to clipboard",self)
        self.copyAction.setStatusTip("Copy text to clipboard")
        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.triggered.connect(self.text.copy)

        self.pasteAction = QtWidgets.QAction(QtGui.QIcon("icons/paste.png"),"Paste from clipboard",self)
        self.pasteAction.setStatusTip("Paste text from clipboard")
        self.pasteAction.setShortcut("Ctrl+V")
        self.pasteAction.triggered.connect(self.text.paste)

        self.undoAction = QtWidgets.QAction(QtGui.QIcon("icons/undo.png"),"Undo last action",self)
        self.undoAction.setStatusTip("Undo last action")
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.triggered.connect(self.text.undo)

        self.redoAction = QtWidgets.QAction(QtGui.QIcon("icons/redo.png"),"Redo last undone thing",self)
        self.redoAction.setStatusTip("Redo last undone thing")
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.triggered.connect(self.text.redo)

        dateTimeAction = QtWidgets.QAction(QtGui.QIcon("icons/calender.png"),"Insert current date/time",self)
        dateTimeAction.setStatusTip("Insert current date/time")
        dateTimeAction.setShortcut("Ctrl+D")
        dateTimeAction.triggered.connect(datetime.DateTime(self).show)

        wordCountAction = QtWidgets.QAction(QtGui.QIcon("icons/count.png"),"See word/symbol count",self)
        wordCountAction.setStatusTip("See word/symbol count")
        wordCountAction.setShortcut("Ctrl+W")
        wordCountAction.triggered.connect(self.wordCount)

        snapAction = QtWidgets.QAction(QtGui.QIcon('icons/image.png'), 'Snap Screen', self)
        snapAction.setStatusTip('Snap Screen')
        snapAction.setShortcut("Ctrl+Shift+S")
        snapAction.triggered.connect(self.snapWindow)

        runAction = QtWidgets.QAction(QtGui.QIcon('icons/indent.png'), "Run Script", self)
        runAction.setStatusTip("Run Script")
        runAction.setShortcut('Ctrl+Shift+R')
        runAction.triggered.connect(self.runScript)

        self.toolbar = self.addToolBar("Options")

        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.cutAction)
        self.toolbar.addAction(self.copyAction)
        self.toolbar.addAction(self.pasteAction)
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.findAction)
        self.toolbar.addAction(dateTimeAction)
        self.toolbar.addAction(wordCountAction)
        self.toolbar.addAction(snapAction)
        self.toolbar.addAction(runAction)

        self.addToolBarBreak()

    def initFormatbar(self):

        fontBox = QtWidgets.QFontComboBox(self)
        fontBox.currentFontChanged.connect(lambda font: self.text.setCurrentFont(font))

        fontSize = QtWidgets.QSpinBox(self)

        # Will display " pt" after each value
        fontSize.setSuffix(" pt")

        fontSize.valueChanged.connect(lambda size: self.text.setFontPointSize(size))

        fontSize.setValue(14)

        fontColor = QtWidgets.QAction(QtGui.QIcon("icons/font-color.png"),"Change font color",self)
        fontColor.triggered.connect(self.fontColorChanged)

        boldAction = QtWidgets.QAction(QtGui.QIcon("icons/bold.png"),"Bold",self)
        boldAction.triggered.connect(self.bold)

        italicAction = QtWidgets.QAction(QtGui.QIcon("icons/italic.png"),"Italic",self)
        italicAction.triggered.connect(self.italic)

        underlAction = QtWidgets.QAction(QtGui.QIcon("icons/underline.png"),"Underline",self)
        underlAction.triggered.connect(self.underline)

        strikeAction = QtWidgets.QAction(QtGui.QIcon("icons/strike.png"),"Strike-out",self)
        strikeAction.triggered.connect(self.strike)

        superAction = QtWidgets.QAction(QtGui.QIcon("icons/superscript.png"),"Superscript",self)
        superAction.triggered.connect(self.superScript)

        subAction = QtWidgets.QAction(QtGui.QIcon("icons/subscript.png"),"Subscript",self)
        subAction.triggered.connect(self.subScript)

        alignLeft = QtWidgets.QAction(QtGui.QIcon("icons/align-left.png"),"Align left",self)
        alignLeft.triggered.connect(self.alignLeft)

        alignCenter = QtWidgets.QAction(QtGui.QIcon("icons/align-center.png"),"Align center",self)
        alignCenter.triggered.connect(self.alignCenter)

        alignRight = QtWidgets.QAction(QtGui.QIcon("icons/align-right.png"),"Align right",self)
        alignRight.triggered.connect(self.alignRight)

        alignJustify = QtWidgets.QAction(QtGui.QIcon("icons/align-justify.png"),"Align justify",self)
        alignJustify.triggered.connect(self.alignJustify)

        indentAction = QtWidgets.QAction(QtGui.QIcon("icons/indent.png"),"Indent Area",self)
        indentAction.setShortcut("Ctrl+Tab")
        indentAction.triggered.connect(self.indent)

        dedentAction = QtWidgets.QAction(QtGui.QIcon("icons/dedent.png"),"Dedent Area",self)
        dedentAction.setShortcut("Shift+Tab")
        dedentAction.triggered.connect(self.dedent)

        backColor = QtWidgets.QAction(QtGui.QIcon("icons/highlight.png"),"Change background color",self)
        backColor.triggered.connect(self.highlight)

        self.formatbar = self.addToolBar("Format")

        self.formatbar.addWidget(fontBox)
        self.formatbar.addWidget(fontSize)

        self.formatbar.addSeparator()

        self.formatbar.addAction(fontColor)
        self.formatbar.addAction(backColor)

        self.formatbar.addSeparator()

        self.formatbar.addAction(boldAction)
        self.formatbar.addAction(italicAction)
        self.formatbar.addAction(underlAction)
        self.formatbar.addAction(strikeAction)
        self.formatbar.addAction(superAction)
        self.formatbar.addAction(subAction)

        self.formatbar.addSeparator()

        self.formatbar.addAction(alignLeft)
        self.formatbar.addAction(alignCenter)
        self.formatbar.addAction(alignRight)
        self.formatbar.addAction(alignJustify)

        self.formatbar.addSeparator()

        self.formatbar.addAction(indentAction)
        self.formatbar.addAction(dedentAction)

    def initMenubar(self):

        menubar = self.menuBar()

        file = menubar.addMenu("File")
        edit = menubar.addMenu("Edit")
        view = menubar.addMenu("View")

        # Add the most important actions to the menubar

        file.addAction(self.newAction)
        file.addAction(self.openAction)
        file.addAction(self.saveAction)

        edit.addAction(self.undoAction)
        edit.addAction(self.redoAction)
        edit.addAction(self.cutAction)
        edit.addAction(self.copyAction)
        edit.addAction(self.pasteAction)
        edit.addAction(self.findAction)

        # Toggling actions for the various bars
        toolbarAction = QtWidgets.QAction("Toggle Toolbar",self)
        toolbarAction.triggered.connect(self.toggleToolbar)

        formatbarAction = QtWidgets.QAction("Toggle Formatbar",self)
        formatbarAction.triggered.connect(self.toggleFormatbar)

        statusbarAction = QtWidgets.QAction("Toggle Statusbar",self)
        statusbarAction.triggered.connect(self.toggleStatusbar)

        view.addAction(toolbarAction)
        view.addAction(formatbarAction)
        view.addAction(statusbarAction)

    def initUI(self):

        self.text = QtWidgets.QTextEdit(self)

        # Set the tab stop width to around 33 pixels which is
        # more or less 8 spaces
        self.text.setTabStopWidth(33)

        self.initToolbar()
        self.initFormatbar()
        self.initMenubar()

        self.setCentralWidget(self.text)

        # Initialize a statusbar for the window
        self.statusbar = self.statusBar()

        # If the cursor position changes, call the function that displays
        # the line and column number
        self.text.cursorPositionChanged.connect(self.cursorPosition)

        # We need our own context menu for tables
        self.text.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text.customContextMenuRequested.connect(self.context)

        self.text.textChanged.connect(self.changed)

        self.highlighter = pyhighlighter.PythonHighlighter(self.text.document())

        self.snap = None

        self.setGeometry(100,100,1030,800)
        self.setWindowTitle("Writer")
        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))

    def changed(self):
        self.changesSaved = False

    def closeEvent(self,event):

        if self.changesSaved or self.text.toPlainText() == '':

            event.accept()

        else:

            popup = QtWidgets.QMessageBox(self)

            popup.setIcon(QtWidgets.QMessageBox.Warning)

            popup.setText("The document has been modified")

            popup.setInformativeText("Do you want to save your changes?")

            popup.setStandardButtons(QtWidgets.QMessageBox.Save   |
                                      QtWidgets.QMessageBox.Cancel |
                                      QtWidgets.QMessageBox.Discard)

            popup.setDefaultButton(QtWidgets.QMessageBox.Save)

            answer = popup.exec_()

            if answer == QtWidgets.QMessageBox.Save:
                self.save()

            elif answer == QtWidgets.QMessageBox.Discard:
                event.accept()

            else:
                event.ignore()

    def context(self,pos):

        # Grab the cursor
        cursor = self.text.textCursor()

        event = QtGui.QContextMenuEvent(QtGui.QContextMenuEvent.Mouse,QtCore.QPoint())

        self.text.contextMenuEvent(event)

    def toggleToolbar(self):

        state = self.toolbar.isVisible()

        # Set the visibility to its inverse
        self.toolbar.setVisible(not state)

    def toggleFormatbar(self):

        state = self.formatbar.isVisible()

        # Set the visibility to its inverse
        self.formatbar.setVisible(not state)

    def toggleStatusbar(self):

        state = self.statusbar.isVisible()

        # Set the visibility to its inverse
        self.statusbar.setVisible(not state)

    def new(self):

        spawn = Main()

        spawn.show()



    def open(self):

        import asyncio

        @asyncio.coroutine
        def compute(x, y):
            print("Compute %s + %s ..." % (x, y))
            yield from asyncio.sleep(10.0)
            return x + y
        
        @asyncio.coroutine
        def print_sum(x, y):
            print('before print sum', x, y)
            result = yield from compute(x, y)
            print("%s + %s = %s" % (x, y, result))
        
        self.loop = asyncio.get_event_loop()
        self.loop.call_soon(print_sum(1, 2), self.loop)

        # Get filename and show only .writer files
        #PYQT5 Returns a tuple in PyQt5, we only need the filename
        self.filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File',".","(*.writer)")[0]

        if self.filename:
            with open(self.filename,"rt") as file:
                self.text.setText(file.read())

    def dump_script_text(self):
        result = """
# We need the path to setup.py to be able to run
# the setup from a different folder
import os, sys
def setup_path(path = ""):
    # get the path to the setup file
    setup_path = os.path.abspath(os.path.split(__file__)[0])

    return os.path.join(setup_path, path)

sys.path.insert(0, setup_path('..'))

from source.core.api import *
from source.core.cv import *
from source.core.help import *
from source.core.win.win import Window

handle = sys.argv[1]
G.DEVICE = Window(handle=handle) 


"""
        
        textblock = self.text.document().firstBlock()
        
        while textblock.isValid():
            it = textblock.begin()
            while not it.atEnd():
                fragment = it.fragment()
                charformat = fragment.charFormat()
    
                if charformat.isImageFormat():
                    charformat = charformat.toImageFormat()
                    result += "Template('%s')" % charformat.name()
                else:
                    result += fragment.text()
                print(fragment.text())
                it += 1
            result += '\n'
            textblock = textblock.next()
            
        return result

    def save(self):

        # Only open dialog if there is no filename yet
        #PYQT5 Returns a tuple in PyQt5, we only need the filename
        if not self.filename:
          self.filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')[0]

        # 只能保存在项目目录下，保证python模块引用
        if self.filename and not self.filename.startswith(G.ROOT_PATH):
            return

        if self.filename:

            # Append extension if not there yet
            if not self.filename.endswith(".writer"):
              self.filename += ".writer"

            # We just store the contents of the text file along with the
            # format in html, which Qt does in a very nice way for us
            with open(self.filename,"wt", encoding='utf8') as file:
                file.write( self.text.toHtml() )

            pyname = self.filename.replace('.writer', '.py')

            with open(pyname, "wt", encoding='utf8') as file:
                file.write( self.dump_script_text() )

            self.changesSaved = True

            # move temp resource to project path
            #dirpath = self.filename.replace('.writer', '')
            #if not os.path.exists(dirpath) and os.path.exists(EXPORT_PATH):
            #    shutil.move(EXPORT_PATH, dirpath)

    def cursorPosition(self):

        cursor = self.text.textCursor()

        # Mortals like 1-indexed things
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()

        self.statusbar.showMessage("Line: {} | Column: {}".format(line,col))

    def wordCount(self):

        wc = wordcount.WordCount(self)

        wc.getText()

        wc.show()

    def insertImage(self):

        # Get image file name
        #PYQT5 Returns a tuple in PyQt5
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Insert image',".","Images (*.png *.xpm *.jpg *.bmp *.gif)")[0]

        if filename:

            # Create image object
            image = QtGui.QImage(filename)

            # Error if unloadable
            if image.isNull():

                popup = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                          "Image load error",
                                          "Could not load image file!",
                                          QtWidgets.QMessageBox.Ok,
                                          self)
                popup.show()

            else:

                cursor = self.text.textCursor()

                cursor.insertImage(image,filename)

    async def wait_lonmg():
        await asyncio.sleep(10)

    def snapWindow(self):

        G.DEVICE.set_foreground()

        if self.snap is not None:
            self.snap.destroy()

        self.snap = ScreenShootWindow()

        def _addImage(background, foreground, top, left, width, height):
            if not background.isNull():
                if not self.filename:
                    path = EXPORT_PATH
                else:
                    path = self.filename.replace('.writer', '')

                if not os.path.exists(path):
                    os.mkdir(path)

                suffix = 'png'
                pathstr = "%s/%s.%s"
                struuid = str(uuid.uuid4())
                name = pathstr % (path, struuid, suffix)

                for x, y in [(x, y) for x in range(background.width()) for y in range(background.height())]:
                    color = foreground.pixel(x, y)
                    # do mask if has color pixel
                    if (color & 0xFFFFFF) > 1:
                        background.setPixel(x, y, 0)

                background.save(name, suffix, 10)

                metadic = {
                    'top':top,
                    'left':left,
                    'width':left,
                    'height':height,
                    'path':name,
                    'name':struuid,
                }

                with open(name + ".meta", "wt", encoding='utf8') as file:
                    file.write(json.dumps(metadic))

                background = background.scaledToHeight(80)

                cursor = self.text.textCursor()
                cursor.insertImage(background, name)
                #cursor.insertImage(foreground, 'fore ' + name)

        self.snap.setSuccCallback(_addImage)
        self.snap.show()

    def getPyModuleByfilename(self, filename):
        print('try get pymodule by filename ' + filename)
        filename = filename.replace("\\", "/")
        if filename.startswith(G.ROOT_PATH):
            filename = filename.replace(G.ROOT_PATH, '')
            filename = filename.replace('/', '.')
            filename.replace('.py', '')

            if filename[0] == '.':
                filename = filename[1:]

            return filename

    def getPyPathByfilename(self, filename):
        filename = filename.replace("\\", "/")
        if filename.startswith(G.ROOT_PATH):
            filename = filename.replace(G.ROOT_PATH, '')

            if filename.endswith('.writer'):
                filename = filename.replace('.writer', '.py')

            if filename[0] == '/' :
                filename = filename[1:]

            return filename

    def runScript(self):
        #import importlib
        #modulepath = self.getPyModuleByfilename(self.filename)
        #if modulepath is not None:
        #    importlib.import_module(modulepath)

        pypath = self.getPyPathByfilename(self.filename)

        print('run script: python ', pypath)

        subprocess.run("python {} {}".format(pypath, G.DEVICE.handle))

    def fontColorChanged(self):

        # Get a color from the text dialog
        color = QtWidgets.QColorDialog.getColor()

        # Set it as the new text color
        self.text.setTextColor(color)

    def highlight(self):

        color = QtWidgets.QColorDialog.getColor()

        self.text.setTextBackgroundColor(color)

    def bold(self):

        if self.text.fontWeight() == QtGui.QFont.Bold:

            self.text.setFontWeight(QtGui.QFont.Normal)

        else:

            self.text.setFontWeight(QtGui.QFont.Bold)

    def italic(self):

        state = self.text.fontItalic()

        self.text.setFontItalic(not state)

    def underline(self):

        state = self.text.fontUnderline()

        self.text.setFontUnderline(not state)

    def strike(self):

        # Grab the text's format
        fmt = self.text.currentCharFormat()

        # Set the fontStrikeOut property to its opposite
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())

        # And set the next char format
        self.text.setCurrentCharFormat(fmt)

    def superScript(self):

        # Grab the current format
        fmt = self.text.currentCharFormat()

        # And get the vertical alignment property
        align = fmt.verticalAlignment()

        # Toggle the state
        if align == QtGui.QTextCharFormat.AlignNormal:

            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSuperScript)

        else:

            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)

        # Set the new format
        self.text.setCurrentCharFormat(fmt)

    def subScript(self):

        # Grab the current format
        fmt = self.text.currentCharFormat()

        # And get the vertical alignment property
        align = fmt.verticalAlignment()

        # Toggle the state
        if align == QtGui.QTextCharFormat.AlignNormal:

            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSubScript)

        else:

            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)

        # Set the new format
        self.text.setCurrentCharFormat(fmt)

    def alignLeft(self):
        self.text.setAlignment(Qt.AlignLeft)

    def alignRight(self):
        self.text.setAlignment(Qt.AlignRight)

    def alignCenter(self):
        self.text.setAlignment(Qt.AlignCenter)

    def alignJustify(self):
        self.text.setAlignment(Qt.AlignJustify)

    def indent(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        if cursor.hasSelection():

            # Store the current line/block number
            temp = cursor.blockNumber()

            # Move to the selection's end
            cursor.setPosition(cursor.anchor())

            # Calculate range of selection
            diff = cursor.blockNumber() - temp

            direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down

            # Iterate over lines (diff absolute value)
            for n in range(abs(diff) + 1):

                # Move to start of each line
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)

                # Insert tabbing
                cursor.insertText("\t")

                # And move back up
                cursor.movePosition(direction)

        # If there is no selection, just insert a tab
        else:

            cursor.insertText("\t")

    def handleDedent(self,cursor):

        cursor.movePosition(QtGui.QTextCursor.StartOfLine)

        # Grab the current line
        line = cursor.block().text()

        # If the line starts with a tab character, delete it
        if line.startswith("\t"):

            # Delete next character
            cursor.deleteChar()

        # Otherwise, delete all spaces until a non-space character is met
        else:
            for char in line[:8]:

                if char != " ":
                    break

                cursor.deleteChar()

    def dedent(self):

        cursor = self.text.textCursor()

        if cursor.hasSelection():

            # Store the current line/block number
            temp = cursor.blockNumber()

            # Move to the selection's last line
            cursor.setPosition(cursor.anchor())

            # Calculate range of selection
            diff = cursor.blockNumber() - temp

            direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down

            # Iterate over lines
            for n in range(abs(diff) + 1):

                self.handleDedent(cursor)

                # Move up
                cursor.movePosition(direction)

        else:
            self.handleDedent(cursor)

def guimain():

    app = QtWidgets.QApplication(sys.argv)

    main = Main()
    main.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    guimain()
