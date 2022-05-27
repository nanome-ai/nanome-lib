import nanome


class FilesAPITest(nanome.PluginInstance):
    def on_run(self):
        self.request_directory(".", self.on_directory_received)  # Request all content of "." directory (where Nanome is installed)

    def on_directory_received(self, result):
        if result.error_code != nanome.util.DirectoryErrorCode.no_error:  # If API couldn't access directory, display error
            nanome.util.Logs.error("Directory request error:", str(result.error_code))
            return

        # For each entry in directory, display name and if directory
        for entry in result.entry_array:
            nanome.util.Logs.debug(entry.name, "Is Directory?", entry.is_directory)

        self.request_files(["./api_bad_test.txt", "api_test.txt"], self.on_files_received)  # Read two files

    def on_files_received(self, file_list):
        # For each file we read, display if error, and file content
        for file in file_list:
            nanome.util.Logs.debug("Error?", str(nanome.util.FileErrorCode(file.error_code)), "Content:", file.data)

        # Prepare to write file "api_test.txt", with content "AAAA"
        file = nanome.util.FileSaveData()
        file.path = "./api_test.txt"
        file.write_text("AAAA")
        self.save_files([file], self.on_save_files_result)  # Write file

    def on_save_files_result(self, result_list):
        # Check for writing errors
        for result in result_list:
            nanome.util.Logs.debug("Saving", result.path, "Error?", str(nanome.util.FileErrorCode(result.error_code)))


if __name__ == "__main__":
    plugin = nanome.Plugin("Example File API", "Test File API by reading current directory, reading api_test.txt and api_bad_test.txt and modifying api_test.txt", "Examples", False)
    plugin.set_plugin_class(FilesAPITest)
    plugin.run()
