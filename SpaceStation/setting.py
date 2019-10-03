import copy,time


class Setting(object):

    def __init__(self):
        self.Golbals_WebUrl_Dict = {}
        self.Golbals_SQL_Table_Data_List = []
        self.Tem_Golbals_WebUrl_Dict = {}
        self.Tem_Golbals_SQL_Table_Data_List = []

    def clearGolbalsData(self):
        self.Golbals_WebUrl_Dict = {}
        self.Golbals_SQL_Table_Data_List = []

    def clearTemplateData(self):
        self.Tem_Golbals_WebUrl_Dict = {}
        self.Tem_Golbals_SQL_Table_Data_List = []

    def GolbalsData2TemplateData(self):
        self.Tem_Golbals_WebUrl_Dict = copy.deepcopy(self.Golbals_WebUrl_Dict)
        self.Tem_Golbals_SQL_Table_Data_List = copy.deepcopy(self.Golbals_SQL_Table_Data_List)


a = Setting()
# a.clearGolbalsData()
# a.Tem_Golbals_WebUrl_Dict
a.GolbalsData2TemplateData()