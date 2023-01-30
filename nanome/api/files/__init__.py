from . import messages, models  # noqa: F401

from nanome.util import simple_callbacks
from nanome._internal.enums import Commands, Messages


registered_commands = [
    (Commands.export_files_result, messages.ExportFiles(), simple_callbacks.simple_callback_arg),
    (Commands.print_working_directory_response, messages.PWD(), simple_callbacks.simple_callback_arg_unpack),
    (Commands.cd_response, messages.CD(), simple_callbacks.simple_callback_arg),
    (Commands.ls_response, messages.LS(), simple_callbacks.simple_callback_arg_unpack),
    (Commands.mv_response, messages.MV(), simple_callbacks.simple_callback_arg),
    (Commands.cp_response, messages.CP(), simple_callbacks.simple_callback_arg),
    (Commands.get_response, messages.Get(), simple_callbacks.simple_callback_arg_unpack),
    (Commands.put_response, messages.Put(), simple_callbacks.simple_callback_arg),
    (Commands.rm_response, messages.RM(), simple_callbacks.simple_callback_arg),
    (Commands.rmdir_response, messages.RMDir(), simple_callbacks.simple_callback_arg),
    (Commands.mkdir_response, messages.MKDir(), simple_callbacks.simple_callback_arg),
    (Commands.load_file_done, messages.LoadFileDone(), simple_callbacks.simple_callback_arg),
    (Commands.directory_response, messages.DirectoryRequest(), simple_callbacks.simple_callback_arg),
    (Commands.file_response, messages.FileRequest(), simple_callbacks.simple_callback_arg),
    (Commands.file_save_done, messages.FileSave(), simple_callbacks.simple_callback_arg),
]

registered_messages = [
    (Messages.print_working_directory, messages.PWD()),
    (Messages.cd, messages.CD()),
    (Messages.ls, messages.LS()),
    (Messages.mv, messages.MV()),
    (Messages.cp, messages.CP()),
    (Messages.get, messages.Get()),
    (Messages.put, messages.Put()),
    (Messages.rm, messages.RM()),
    (Messages.rmdir, messages.RMDir()),
    (Messages.mkdir, messages.MKDir()),
    (Messages.load_file, messages.LoadFile()),
    # Deprecated list
    (Messages.directory_request, messages.DirectoryRequest()),
    (Messages.file_request, messages.FileRequest()),
    (Messages.file_save, messages.FileSave()),
    (Messages.export_files, messages.ExportFiles()),
]
