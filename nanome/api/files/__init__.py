from . import messages, models

from nanome.api import callbacks as base_callbacks
from nanome._internal.enums import Commands


registered_commands = [
    (Commands.export_files_result, messages.ExportFiles(), base_callbacks.simple_callback_arg),
    (Commands.print_working_directory_response, messages.PWD(), base_callbacks.simple_callback_arg_unpack),
    (Commands.cd_response, messages.CD(), base_callbacks.simple_callback_arg),
    (Commands.ls_response, messages.LS(), base_callbacks.simple_callback_arg_unpack),
    (Commands.mv_response, messages.MV(), base_callbacks.simple_callback_arg),
    (Commands.cp_response, messages.CP(), base_callbacks.simple_callback_arg),
    (Commands.get_response, messages.Get(), base_callbacks.simple_callback_arg_unpack),
    (Commands.put_response, messages.Put(), base_callbacks.simple_callback_arg),
    (Commands.rm_response, messages.RM(), base_callbacks.simple_callback_arg),
    (Commands.rmdir_response, messages.RMDir(), base_callbacks.simple_callback_arg),
    (Commands.mkdir_response, messages.MKDir(), base_callbacks.simple_callback_arg),
    (Commands.load_file_done, messages.LoadFileDone(), base_callbacks.simple_callback_arg),
    (Commands.directory_response, messages.DirectoryRequest(), base_callbacks.simple_callback_arg),
    (Commands.file_response, messages.FileRequest(), base_callbacks.simple_callback_arg),
    (Commands.file_save_done, messages.FileSave(), base_callbacks.simple_callback_arg),
]