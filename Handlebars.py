import sublime
import sublime_plugin
import os
import subprocess
import thread
import functools


#   AsyncProcess class taken and modified from the Default Package
class AsyncProcess(object):

    def __init__(self, command, listener):

        self.listener = listener

        # Hide the console window on Windows
        startupinfo = None
        if os.name == "nt":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # Get the environment variables
        proc_env = os.environ.copy()

        # Create a subprocess with the command specified
        # As we want to use a shell behaviour we're passing args as string like command parameter
        self.proc = subprocess.Popen(command, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, startupinfo=startupinfo, env=proc_env,
            shell=True)

        if self.proc.stdout:
            # Create a new thread for read the process
            thread.start_new_thread(self.read_stdout, ())

        if self.proc.stderr:
            # Create a new thread for read any error
            thread.start_new_thread(self.read_stderr, ())

    def kill(self):
        if not self.killed:
            self.killed = True
            self.proc.kill()
            self.listener = None

    # Thread wating for success
    def read_stdout(self):
        while True:
            data = os.read(self.proc.stdout.fileno(), 2 ** 15)

            if data != "":
                if self.listener:
                    self.listener.on_data(self, data)
            else:
                self.proc.stdout.close()
                if self.listener:
                    # Once the process is done invoke the callback function
                    # from our listener (HandlebarsCommand)
                    self.listener.on_finished(self)
                break

    def read_stderr(self):
        while True:
            data = os.read(self.proc.stderr.fileno(), 2 ** 15)

            if data != "":
                if self.listener:
                    self.listener.on_data(self, data)
            else:
                self.proc.stderr.close()
                break


class HandlebarsCommand(sublime_plugin.TextCommand):
    """
    This class is used to compile HTML templates using the Handlebars engine.
    This is the version 0.1 of the same.
    """
    def run(self, edit):

        self.encoding = "utf-8"

        # Get the settings
        self.settings = sublime.load_settings('Handlebars.sublime-settings')

        self.file_name = self.view.file_name()
        file_extension = os.path.splitext(self.file_name)[1]

        # Verify the allowed extensions
        if not (file_extension in self.settings.get('allowed_extensions')):
            sublime.status_message("The provided file has an invalid extension")
            return

        handlebars_exec = self.settings.get('handlebars_exec')
        self.compiled_extension = self.settings.get('compiled_extension')

        compiler_options = ""
        for option in self.settings.get('compiler_options'):
            compiler_options = compiler_options + " " + option

        # Create the OS command
        osCommand = handlebars_exec + ' "' + self.file_name + '" ' + compiler_options + ' "' + self.file_name + self.compiled_extension + '"'

        sublime.status_message("Creating the template...")

        # Create the new process and threads
        try:
            self.proc = AsyncProcess(osCommand, self)
        except Exception, e:
            sublime.status_message(str(e).decode(self.encoding))
            self.append_data(None)

    def append_data(self, proc, data):

        if proc != self.proc:
            # a second call to exec has been made before the first one
            # finished, ignore it instead of intermingling the output.
            if proc:
                proc.kill()
            return

    def finish(self, proc):

        try:
            self.view.window().open_file(self.file_name + self.compiled_extension)
        except Exception, e:
            sublime.status_message(str(e).decode(self.encoding))

    # On data recived from the process
    def on_data(self, proc, data):
        sublime.set_timeout(functools.partial(self.append_data, proc, data), 0)

    # Once the new file has been created we just need to open it
    def on_finished(self, proc):
        sublime.set_timeout(functools.partial(self.finish, proc), 0)
