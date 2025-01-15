import tkinter as tk
from src.database import ViolenceDetectionDatabase
import webbrowser

class LabellingApp(tk.Tk):
    def __init__(self, tableName):

        # window setup
        super().__init__()
        self.title("")
        self.geometry("1000x400")

        # layout
        self.columnconfigure((0, 1), weight=1, uniform="a")
        self.rowconfigure((0, 1, 2, 3), weight=1, uniform="a")

        # label data 
        self.tableName = tableName
        self.labelData = LabellingApp.get_label_data()
        self.labelDataIndex = -1

        # variables 
        self.transcriptVar = tk.StringVar()
        self.linkVar = tk.StringVar()
        self.timeframeVar = tk.StringVar()
        self.remainingVar = tk.StringVar()

        self.update_variables()

        # widgets
        DataInformationLabel(self, self.transcriptVar, 0, 0, 1, 2)
        linkLabel = DataInformationLabel(self, self.linkVar, 0, 1, 1, 2)
        DataInformationLabel(self, self.timeframeVar, 0, 2, 1, 2)
        tk.Label(self, textvariable=self.remainingVar, anchor="e").grid(column=1, row=0, sticky="ne")

        linkLabel.bind("<Button-1>", lambda x: webbrowser.open_new_tab(self.linkVar.get()))

        ActionButton(self, "Violent", 0, 3, lambda: self.update_database(1))
        ActionButton(self, "Non-Violent", 1, 3, lambda: self.update_database(0))
        self.mainloop()
    
    def get_label_data(self):
        with ViolenceDetectionDatabase() as VDdb:
            return VDdb.select_all(self.tableName, "violence IS ?", (None,))
    
    def update_variables(self):
        self.labelDataIndex += 1
        if self.labelDataIndex < len(self.labelData): # Check if there are more entries
            self.transcriptVar.set(self.labelData[self.labelDataIndex][2])
            self.linkVar.set(self.labelData[self.labelDataIndex][1])
            self.timeframeVar.set(self.labelData[self.labelDataIndex][0])
            self.remainingVar.set(len(self.labelData) - self.labelDataIndex)

        else:
            print("All data labeled.")
            self.quit()  # Optionally close the app when finished
    
    def update_database(self, isViolent):
        with ViolenceDetectionDatabase() as VDdb:
            VDdb.update_case(self.timeframeVar.get(), violence=isViolent)
        self.update_variables()


class DataInformationLabel(tk.Label):
    def __init__(self, parent, var, column, row, rowspan, columnspan):
        super().__init__(master=parent, textvariable = var, wraplength=900)
        self.grid(column=column, row=row, rowspan=rowspan, sticky="nsew", columnspan=columnspan)


class ActionButton(tk.Button):
    def __init__(self, parent, text, col, row, command):
        super().__init__(master=parent, text=text, command=command)
        self.grid(column=col, row=row, sticky="nsew")


if __name__ == "__main__":
    l = LabellingApp("YalıÇapkını")