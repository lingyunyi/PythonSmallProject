import copy


Golbals_WebUrl_Dict = {}

Golbals_SQL_Table_Data_List = []

Tem_Golbals_WebUrl_Dict = {}

Tem_Golbals_SQL_Table_Data_List = []


def clearGolbalsData():
    global Golbals_WebUrl_Dict
    global Golbals_SQL_Table_Data_List
    Golbals_WebUrl_Dict = {}
    Golbals_SQL_Table_Data_List = []

def clearTemplateData():
    global Golbals_WebUrl_Dict
    global Golbals_SQL_Table_Data_List
    Tem_Golbals_WebUrl_Dict = {}
    Tem_Golbals_SQL_Table_Data_List = []

def GolbalsData2TemplateData():
    global Tem_Golbals_WebUrl_Dict
    global Tem_Golbals_SQL_Table_Data_List
    Tem_Golbals_WebUrl_Dict = copy.deepcopy(Golbals_WebUrl_Dict)
    Tem_Golbals_SQL_Table_Data_List = copy.deepcopy(Golbals_SQL_Table_Data_List)
