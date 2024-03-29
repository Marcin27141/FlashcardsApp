import shutil
import os
from CLI.Exporters.BaseExporter import BaseExporter
from CLI.FileOperator import FileAlias
from datetime import datetime

class AllSetsExporter(BaseExporter):
    def __init__(self, export_info) -> None:
        super().__init__(export_info)
        self.name = self.name if self.name else self.get_default_archive_name()
        self.sets_to_export = self.get_all_sets()

    def export_sets(self):
        self.export_all_sets_to_archive()

    def get_all_sets(self):
        return self.controller.get_available_sets()

    def create_temporary_directory(self):
        TEMP_DIRECTORY = "temp_directory"
        temp_joined_directory = os.path.join(self.destination_directory, TEMP_DIRECTORY)
        self.FILE_OPERATOR.create_directory(temp_joined_directory)
        return temp_joined_directory        

    def get_content_directory_for_archive(self):
        temp_directory = self.create_temporary_directory()
        for flashcards_set in self.sets_to_export:
            filename = self.get_default_set_filename(flashcards_set.name)
            filename = f"{filename}.txt"
            set_text = self.get_set_to_text(flashcards_set)
            file_alias = FileAlias(temp_directory, filename)
            self.FILE_OPERATOR.write_to_file(file_alias, set_text)
        return temp_directory
        
    def export_all_sets_to_archive(self):
        DEFAULT_ARCHIVE_FORMAT = 'zip'
        file_alias = FileAlias(self.destination_directory, self.name)
        self.name = self.FILE_OPERATOR.get_nonduplicate_filename(file_alias, DEFAULT_ARCHIVE_FORMAT)
        content_directory_for_archive = self.get_content_directory_for_archive()
        archive_path = os.path.join(self.destination_directory, self.name)
        shutil.make_archive(archive_path, DEFAULT_ARCHIVE_FORMAT, content_directory_for_archive)
        shutil.rmtree(content_directory_for_archive)

    def get_default_archive_name(self):
        return "CreatedSets"