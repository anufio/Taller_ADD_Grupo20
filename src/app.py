import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "datos")
RESULTS_DIR = os.path.join(BASE_DIR, "resultados")
os.makedirs(RESULTS_DIR, exist_ok=True)

ARCHIVOS_PRUEBA = ["prueba_1.csv", "prueba_2.csv", "prueba_3.csv"]
METRICAS = {"Promedio": "mean", "Máximo": "max", "Mínimo": "min"}

def clasificar_consumo(valor):
    if valor >= 400:
        return "Consumo alto"
    elif valor >= 250:
        return "Consumo medio"
    return "Consumo bajo"

def cargar_csv(ruta):
    df = pd.read_csv(ruta)
    requeridas = {"Fecha","Edificio","Consumo_kWh","Temperatura","Personas"}
    faltantes = requeridas - set(df.columns)
    if faltantes:
        raise ValueError("Faltan columnas: " + ", ".join(sorted(faltantes)))
    return df

def calcular(df, edificio, metrica):
    datos = df[df["Edificio"] == edificio]
    if datos.empty:
        raise ValueError("No hay datos para el edificio seleccionado.")
    return float(datos["Consumo_kWh"].agg(METRICAS[metrica]))

def generar_datos_powerbi():
    tablas=[]
    for nombre in ARCHIVOS_PRUEBA:
        df=cargar_csv(os.path.join(DATA_DIR,nombre)).copy()
        df["Archivo_Prueba"]=nombre
        df["Nivel_Consumo"]=df["Consumo_kWh"].apply(clasificar_consumo)
        tablas.append(df)
    salida=pd.concat(tablas,ignore_index=True)
    ruta=os.path.join(RESULTS_DIR,"datos_powerbi.csv")
    salida.to_csv(ruta,index=False,encoding="utf-8-sig")
    return ruta,len(salida)

class EnergyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Energy Analyzer")
        self.geometry("760x700")
        self.resizable(False,False)
        self.df=None
        self.crear_ui()
        self.cargar_archivo(os.path.join(DATA_DIR,ARCHIVOS_PRUEBA[0]))

    def crear_ui(self):
        ttk.Label(self,text="Energy Analyzer",font=("Segoe UI",22,"bold")).pack(pady=(18,4))
        ttk.Label(self,text="Análisis de consumo energético").pack(pady=(0,14))
        frm=ttk.Frame(self,padding=15); frm.pack(fill="x")

        ttk.Label(frm,text="Archivo:").grid(row=0,column=0,sticky="w",padx=5,pady=5)
        self.archivo_var=tk.StringVar(value=ARCHIVOS_PRUEBA[0])
        self.archivo_combo=ttk.Combobox(frm,textvariable=self.archivo_var,values=ARCHIVOS_PRUEBA,state="readonly",width=28)
        self.archivo_combo.grid(row=0,column=1,sticky="w",padx=5,pady=5)
        self.archivo_combo.bind("<<ComboboxSelected>>",lambda e:self.cargar_archivo(os.path.join(DATA_DIR,self.archivo_var.get())))
        ttk.Button(frm,text="Cargar CSV",command=self.cargar_externo).grid(row=0,column=2,padx=8)

        ttk.Label(frm,text="Edificio:").grid(row=1,column=0,sticky="w",padx=5,pady=5)
        self.edificio_var=tk.StringVar()
        self.edificio_combo=ttk.Combobox(frm,textvariable=self.edificio_var,state="readonly",width=28)
        self.edificio_combo.grid(row=1,column=1,sticky="w",padx=5,pady=5)

        ttk.Label(frm,text="Métrica:").grid(row=2,column=0,sticky="w",padx=5,pady=5)
        self.metrica_var=tk.StringVar(value="Promedio")
        ttk.Combobox(frm,textvariable=self.metrica_var,values=list(METRICAS),state="readonly",width=28).grid(row=2,column=1,sticky="w",padx=5,pady=5)
        ttk.Button(frm,text="Analizar",command=self.analizar).grid(row=3,column=1,sticky="w",padx=5,pady=(12,5))

        self.resultado=tk.StringVar(value="Resultado: --")
        self.nivel=tk.StringVar(value="Nivel de consumo: --")
        ttk.Label(self,textvariable=self.resultado,font=("Segoe UI",15,"bold")).pack(pady=(8,2))
        ttk.Label(self,textvariable=self.nivel,font=("Segoe UI",12)).pack(pady=(0,10))

        ttk.Label(self,text="Vista rápida de datos",font=("Segoe UI",11,"bold")).pack(pady=(8,5))
        cols=("Fecha","Edificio","Consumo_kWh","Temperatura","Personas")
        self.tabla=ttk.Treeview(self,columns=cols,show="headings",height=10)
        for c in cols:
            self.tabla.heading(c,text=c)
            self.tabla.column(c,width=135 if c=="Edificio" else 115)
        self.tabla.pack(padx=20,fill="x")

        botones=ttk.Frame(self,padding=10); botones.pack()
        ttk.Button(botones,text="Generar datos para Power BI",command=self.exportar).grid(row=0,column=0,padx=6)
        ttk.Button(botones,text="Salir",command=self.destroy).grid(row=0,column=1,padx=6)

        self.estado=tk.StringVar(value="Listo.")
        ttk.Label(self,textvariable=self.estado).pack(pady=(3,10))

    def cargar_externo(self):
        ruta=filedialog.askopenfilename(filetypes=[("CSV","*.csv")])
        if ruta:
            self.archivo_var.set(os.path.basename(ruta))
            self.cargar_archivo(ruta)

    def cargar_archivo(self,ruta):
        try:
            self.df=cargar_csv(ruta)
            edificios=sorted(self.df["Edificio"].dropna().unique().tolist())
            self.edificio_combo["values"]=edificios
            if edificios:self.edificio_var.set(edificios[0])
            for x in self.tabla.get_children(): self.tabla.delete(x)
            for _,f in self.df.head(10).iterrows():
                self.tabla.insert("", "end", values=(f["Fecha"],f["Edificio"],f["Consumo_kWh"],f["Temperatura"],f["Personas"]))
            self.resultado.set("Resultado: --"); self.nivel.set("Nivel de consumo: --")
            self.estado.set("Archivo cargado: "+os.path.basename(ruta))
        except Exception as e:
            messagebox.showerror("Error",str(e))

    def analizar(self):
        try:
            r=calcular(self.df,self.edificio_var.get(),self.metrica_var.get())
            self.resultado.set(f"Resultado: {r:.2f} kWh")
            self.nivel.set("Nivel de consumo: "+clasificar_consumo(r))
        except Exception as e:
            messagebox.showerror("Error",str(e))

    def exportar(self):
        try:
            ruta,n=generar_datos_powerbi()
            messagebox.showinfo("Listo",f"Se generaron {n} registros.\n\n{ruta}")
            self.estado.set("Datos para Power BI generados correctamente.")
        except Exception as e:
            messagebox.showerror("Error",str(e))

if __name__=="__main__":
    EnergyApp().mainloop()
