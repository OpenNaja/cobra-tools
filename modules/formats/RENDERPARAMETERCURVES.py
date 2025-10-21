from generated.formats.renderparameters.structs.RenderParameterCurvesRoot import RenderParameterCurvesRoot
from modules.formats.BaseFormat import MemStructLoader


class RenderParameterCurvesLoader(MemStructLoader):
    target_class = RenderParameterCurvesRoot
    extension = ".renderparametercurves"

    # def create(self, file_path):
    #     # super().create(file_path)
    #     # print(self.header)
    #     self.header = self.target_class.from_xml_file(file_path, self.context)
    #     print(self.header)
    #     self.write_memory_data()
