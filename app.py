"""
app.py

Copyright (c) 2022 yoririn

This software is released under the MIT license.
See https://opensource.org/licenses/MIT

"""
import tkinter as tk
from tkinter import BooleanVar, StringVar, ttk
from tkinter import filedialog
import pandas as pd
import sys
import os
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# from matplotlib.backend_bases import key_press_handler

# plt.switch_backend("tkagg")

# IMAGES_PATH = pathlib.Path(__file__).parent / "images"
def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), "images", relative_path)

def make_divisors(n):
    multiplier = 10**len(str(n).split('.')[-1])
    n_bymultiplier = n*multiplier
    lower_divisors , upper_divisors = [], []
    i = 1
    while i*i <= n_bymultiplier:
        if n_bymultiplier % i == 0:
            lower_divisors.append(i)
            if i != n_bymultiplier // i:
                upper_divisors.append(n_bymultiplier//i)
        i += 1
    return [i/multiplier for i in lower_divisors + upper_divisors[::-1]]

# mpl.use("pgf") #set drawing driver (latexを使える
# # 文字に latex を利用するための設定
# config = {
#     "text.usetex": True,
#     "text.latex.preamble": "\n".join([r"\usepackage{siunitx}"]),
#     "pgf.preamble": "\n".join([r"\usepackage{siunitx}"])  # plots will use this preamble
#     #     'font.sans-serif':['DejaVu Serif', 'Bitstream Vera Serif', 'Computer Modern Roman', 'New Century Schoolbook', 'Century Schoolbook L', 'Utopia', 'ITC Bookman', 'Bookman', 'Nimbus Roman No9 L', 'Times New Roman', 'Times', 'Palatino', 'Charter', 'serif']
# }
# plt.rcParams.update(config)

class MyNavigationToolbar(NavigationToolbar2Tk):
    toolitems = [t for t in NavigationToolbar2Tk.toolitems[:-2]]

class ColormapsWindow(tk.Toplevel):
    def __init__(self, container):
        super().__init__(container)
        w = app.winfo_screenwidth()  # モニター横幅取得
        h = app.winfo_screenheight()  # モニター縦幅取得
        self.geometry("+" + str(w//4) + "+" + str(h//4))   # ウィンドウサイズ(幅x高さ)
        self.resizable(width=False, height=False)
        # gradient = np.linspace(1, 0, 256)
        # self.gradient = np.vstack((gradient, gradient)).T
        
        cmap_list = list(mpl.cm._colormaps._cmaps.keys())
        cm_num = int(len(cmap_list)/2)
        self.ncols = int(cm_num//3+1)
        # fig = self.plot_color_gradients(cmap_list)
        # self.frame.grid(padx=20, pady=20)
        # cms_canvas = FigureCanvasTkAgg(fig, master=self)
        # cms_canvas.draw()
        # cms_canvas.get_tk_widget().grid(column=0, row=0, sticky=tk.NSEW)
        self.background = tk.PhotoImage(file=resource_path("cm.png"))
        bg = tk.Label(self, image=self.background)
        bg.grid(column=0, row=0, sticky=tk.NSEW)
        self.cm_rbtns = [tk.Radiobutton(self, variable=app.input_frame.which_cm, value=cm, background="white") for cm in cmap_list[:cm_num]]
        [self.cm_rbtns[i].place(x=22+30*(i%self.ncols), y=26+200*(i//self.ncols), anchor=tk.CENTER) for i in range(cm_num)]

    def plot_color_gradients(self, cmap_list):
        # Create figure and adjust figure height to number of colormaps
        figw = (self.ncols + (self.ncols - 1) * 0.1) * 20
        figh = 40*3+480
        fig, axs = plt.subplots(nrows=3, ncols=self.ncols, figsize=(figw, figh), dpi=1)
        fig.subplots_adjust(top=1-40/figh, bottom=0, left=0, right=1, hspace=40/160)

        for i,cm in enumerate(cmap_list[:int(len(cmap_list)/2)]):
            axs[i//self.ncols,i%self.ncols].imshow(self.gradient, aspect='auto', cmap=plt.get_cmap(cm))

        # Turn off *all* ticks & spines, not just the ones with colormaps.
        for i in range(self.ncols*3):
            axs[i//self.ncols,i%self.ncols].set_axis_off()
        
        return fig

# class FigureFrame(ttk.Frame):
#     def __init__(self, container):
#         super().__init__(container)  # Generate canvas instance, Embedding fig in root
#         # self.df

class InputFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        # setup the grid layout manager
        # self.columnconfigure(
        #     [
        #         0,
        #     ],
        #     weight=1,
        # )
        self.columns_span = 4

        ## browse frame
        self.browse_frame = tk.LabelFrame(self, text="CSV File")
        # self.browse_frame = tk.LabelFrame(self, )
        self.browse_frame.grid(column=0, row=0, ipadx=5, ipady=3, sticky=tk.EW)
        self.browse_frame.columnconfigure( [0,],weight=1,)
        ## filepath entry
        self.filepath = tk.StringVar()
        self.filepath_label = ttk.Label(self.browse_frame, textvariable=self.filepath, wraplength=155)
        self.filepath_label.grid(column=0, row=0, sticky=tk.EW, padx=5, )
        self.filepath_label.focus()
        # self.filepath_delta_entry = ttk.Entry(self.browse_frame, textvariable=self.filepath_delta)
        # self.filepath_delta_entry.grid(column=1, row=1, sticky=tk.EW)
        ## browse button
        self.img_mglass = tk.PhotoImage(file=resource_path("mglass.png"))
        self.load_button = ttk.Button(self.browse_frame, image=self.img_mglass, command=self.master.browse_inputfile)
        self.load_button.grid(column=1, row=0, sticky=tk.E, padx=(0, 5), )

        ## setting frame
        self.setting_frame = tk.LabelFrame(self, text="Plot Setting")
        self.setting_frame.grid(column=0, row=1, ipadx=5, ipady=3, sticky=tk.EW)
        self.setting_frame.columnconfigure([0,], weight=1,)
        ## ticks frame
        self.axes_frame = ttk.LabelFrame(self.setting_frame, text="Axis Scale")
        self.axes_frame.grid(column=0, row=0, ipadx=5, ipady=3, sticky=tk.EW)
        self.axes_frame.columnconfigure([1,], weight=1,)
        self.xaxis_interval = tk.DoubleVar()
        self.yaxis_interval = tk.DoubleVar()
        self.xaxis_label = ttk.Label(self.axes_frame, text="x-Interval")
        self.xaxis_label.grid(column=0, row=0, sticky=tk.W)
        self.yaxis_label = ttk.Label(self.axes_frame, text="y-Interval")
        self.yaxis_label.grid(column=0, row=1, sticky=tk.W)
        self.xaxis_cbox = ttk.Combobox(self.axes_frame, state="readonly", textvariable=self.xaxis_interval)
        self.xaxis_cbox.grid(column=1, row=0, sticky=tk.E)
        self.yaxis_cbox = ttk.Combobox(self.axes_frame, state="readonly", textvariable=self.yaxis_interval)
        self.yaxis_cbox.grid(column=1, row=1, sticky=tk.E)
        ## colorscale_frame
        self.colorscale_frame = ttk.LabelFrame(self.setting_frame, text="Color Scale")
        self.colorscale_frame.grid(column=0, row=1, ipadx=5, ipady=3, sticky=tk.EW)
        self.colorscale_frame.columnconfigure([1,], weight=1,)
        self.scalemax_label = ttk.Label(self.colorscale_frame, text="Max")
        self.scalemax_label.grid(column=0, row=0, sticky=tk.W)
        self.scalemin_label = ttk.Label(self.colorscale_frame, text="Min")
        self.scalemin_label.grid(column=0, row=1, sticky=tk.W)
        self.scaleintervals_label = ttk.Label(self.colorscale_frame, text="Interval")
        self.scaleintervals_label.grid(column=0, row=2, sticky=tk.W)
        self.scalemax = tk.DoubleVar(value=None)
        self.scalemin = tk.DoubleVar(value=None)
        self.scalemax_entry = ttk.Entry(self.colorscale_frame, textvariable=self.scalemax)
        self.scalemax_entry.grid(column=1, row=0, sticky=tk.E)
        self.scalemin_entry = ttk.Entry(self.colorscale_frame, textvariable=self.scalemin)
        self.scalemin_entry.grid(column=1, row=1, sticky=tk.E)
        self.scaleinterval = tk.DoubleVar()
        self.scaleintervals_cbox = ttk.Combobox(self.colorscale_frame, state="readonly", postcommand=self.change_intervalslist, textvariable=self.scaleinterval)
        self.scaleintervals_cbox.grid(column=1, row=2, sticky=tk.E)
        ## axes labal frame
        self.label_frame = ttk.LabelFrame(self.setting_frame, text="Label")
        self.label_frame.grid(column=0, row=2, ipadx=5, ipady=3, sticky=tk.EW)
        self.label_frame.columnconfigure([1,], weight=1,)
        self.xlabel_label = ttk.Label(self.label_frame, text="x-Label")
        self.xlabel_label.grid(column=0, row=0, sticky=tk.W)
        self.xlabel = tk.StringVar(value="x")
        self.xlabel_entry = ttk.Entry(self.label_frame, textvariable=self.xlabel)
        self.xlabel_entry.grid(column=1, row=0, sticky=tk.E)
        self.ylabel_label = ttk.Label(self.label_frame, text="y-Label")
        self.ylabel_label.grid(column=0, row=1, sticky=tk.W)
        self.ylabel = tk.StringVar(value="y")
        self.ylabel_entry = ttk.Entry(self.label_frame, textvariable=self.ylabel)
        self.ylabel_entry.grid(column=1, row=1, sticky=tk.E)
        self.cbarlabel_label = ttk.Label(self.label_frame, text="Colorbar Label")
        self.cbarlabel_label.grid(column=0, row=2, sticky=tk.W)
        self.cbarlabel = tk.StringVar(value="z()")
        self.cbarlabel_entry = ttk.Entry(self.label_frame, textvariable=self.cbarlabel)
        self.cbarlabel_entry.grid(column=1, row=2, sticky=tk.E)
        ## fontsize
        self.font_frame = ttk.LabelFrame(self.setting_frame, text="Fontsize")
        self.font_frame.grid(column=0, row=3, ipadx=5, ipady=3, sticky=tk.EW)
        self.font_frame.columnconfigure([1,], weight=1,)
        self.labelsize_label = ttk.Label(self.font_frame, text="Axis Label")
        self.labelsize_label.grid(column=0, row=0, sticky=tk.W)
        self.labelsize = tk.IntVar(value=24)
        self.labelsize_sbox = ttk.Spinbox(self.font_frame, state="readonly", textvariable=self.labelsize, from_=1, to=30)
        self.labelsize_sbox.grid(column=1, row=0, sticky=tk.E)
        self.tickslabelsize_label = ttk.Label(self.font_frame, text="Ticks Label")
        self.tickslabelsize_label.grid(column=0, row=1, sticky=tk.W)
        self.tickslabelsize = tk.IntVar(value=12)
        self.tickslabelsize_sbox = ttk.Spinbox(self.font_frame, state="readonly", textvariable=self.tickslabelsize, from_=1, to=30)
        self.tickslabelsize_sbox.grid(column=1, row=1, sticky=tk.E)
        ## colormap
        self.which_cm = StringVar(value="magma")
        self.cm_frame = ttk.LabelFrame(self.setting_frame, text="Colormap")
        self.cm_frame.grid(column=0, row=4, ipadx=5, ipady=3, sticky=tk.EW)
        self.cm_button = ttk.Button(self.cm_frame, text="Select Colormap")
        self.cm_button["command"] = self.select_cm
        self.cm_button.grid(column=0,row=0)
        self.cm_reversed = BooleanVar()
        self.cm_check = ttk.Checkbutton(self.cm_frame, text='reversed', onvalue=True, offvalue=False, variable=self.cm_reversed)
        self.cm_check.grid(column=1, row=0)
        ## 3d
        self.is_3d = BooleanVar()
        self.threeD_check = ttk.Checkbutton(self.setting_frame, text='3D', onvalue=True, offvalue=False, variable=self.is_3d)
        self.threeD_check.grid(column=0, row=5, sticky=tk.W)
        ## shared option
        for child in self.setting_frame.winfo_children():
            child.grid_configure(padx=3, pady=3)
        # for child in self.winfo_children():
        #     child.configure(bg='white')

        ## button frame
        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(column=0, row=3, padx=5, ipadx=5, ipady=3, sticky=tk.EW)
        self.button_frame.columnconfigure([0,], weight=1,)
        ## plot button
        self.calculate_button = ttk.Button(self.button_frame, text="Plot")
        self.calculate_button["command"] = self.master.screen
        self.calculate_button.grid(column=0, row=0, sticky=tk.EW)
        ## save button
        self.img_save = tk.PhotoImage(file=resource_path("save.png"))
        self.save_button = ttk.Button(self.button_frame, image=self.img_save, command=self.save_image)
        self.save_button.grid(column=1, row=0, padx=(5, 0))

        
        ## shared option
        for child in self.winfo_children():
            child.grid_configure(pady=5)
        for frame in self.setting_frame.winfo_children():
            for child in frame.winfo_children():
                if isinstance(child, (ttk.Entry, ttk.Spinbox, ttk.Combobox)):
                    child["width"] = 10
                    child.grid_configure(sticky=tk.EW)
                if isinstance(child, (ttk.Label)):
                    child["width"] = 15

    def select_cm(self):
        '''モーダルダイアログボックスの作成'''
        dlg_modal = ColormapsWindow(app)
        dlg_modal.title("Select Colormap") # ウィンドウタイトル

        # モーダルにする設定
        dlg_modal.grab_set()        # モーダルにする
        dlg_modal.focus_set()       # フォーカスを新しいウィンドウをへ移す
        # dlg_modal.transient(app)   # タスクバーに表示しない

        # ダイアログが閉じられるまで待つ
        app.wait_window(dlg_modal)

    def save_image(self):
        savepath = filedialog.asksaveasfilename(
            filetypes = [
                ("PNG", ".png"),
                ("eps", ".eps"),
                ("JPEG", ".jpeg"), ("JPEG", ".jpg"),
                ("PDF", ".pdf"),
                ("PGF", ".pgf"),
                ("PS", ".ps"),
                ("RAW", ".raw"),
                ("RGBA", ".rgba"),
                ("SVG", ".svg"),
                ("SVGZ", ".svgz"),
                ("Tiff", ".tif"), ("Tiff", ".tiff")
            ],
            # title="",
            defaultextension="png",
            initialdir=os.path.expanduser("~/Documents")
        )
        plt.savefig(savepath, facecolor="white", bbox_inches="tight")

    def change_intervalslist(self):
        if("" in (self.scalemax.get(), self.scalemin.get())):
            return
        mm_range = self.scalemax.get()-self.scalemin.get()
        _ = make_divisors(mm_range)
        self.scaleintervals_cbox["values"] = [i for i in _ if mm_range/i < 21]

    # def view(self):
    #     df=pd.read_csv(self.filepath,header=None)
    #     # df_=file.parse(sheet_name=0,header=None)
    #     # df_.drop(df_k1_refbehind.index[[0]])
    #     df = df.dropna(axis=1)
    #     print(df)

#     # def preview_csv(self):
#     #     de
# # sheet_df_dictonary = pd.read_excel('toeic.xlsx', sheet_name=['Page024', skiprows=0)
    

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Csv Heatmapper")
        self.attributes('-alpha', 0.0)
        self.resizable(width=False, height=False)
        self.minsize(width=400, height=20)
        icon = tk.PhotoImage(file=resource_path("icon.png"))
        self.tk.call("wm", "iconphoto", self._w, icon)

        # layout on the root window
        self.columnconfigure(0, weight=1)
        # create the input frame
        self.figure_frame = tk.Frame(self, width=900, height=600, background="#E6E6FA")
        self.figure_frame.grid(column=1, row=0, sticky=tk.NSEW, padx=(0, 10), pady=10)
        self.input_frame = InputFrame(self)
        self.input_frame.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)
        self.analyzedvalues = tk.StringVar(value="Load a csv-like file.")
        self.statusbar = tk.Label(self, textvariable=self.analyzedvalues,bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.grid(column=0, row=1, columnspan=2, sticky=tk.EW)

        self.is_first = True
    def browse_inputfile(self):
        """
        Handle button click event
        """
        csvpath = filedialog.askopenfilename(
            filetypes=[
                ("CSV-like files", "*.csv"),
                ('CSV-like files', '*.xlsx'),
            ],
            title="load",
            initialdir=os.path.expanduser("~/Documents")
        )
        if(csvpath):
            if(os.path.splitext(csvpath)[-1].lower() == ".csv"):
                self.figure_frame.df = pd.read_csv(csvpath,header=None).dropna(axis=1)
            else:
                df_file = pd.ExcelFile(csvpath)
                self.figure_frame.df = df_file.parse(sheet_name=0,header=None).dropna(axis=1)
            # self.input_frame.df = df = df
            self.figure_frame.df_mean = self.figure_frame.df.mean().mean()
            self.figure_frame.df_max = self.figure_frame.df.max().max()
            self.figure_frame.df_min = self.figure_frame.df.min().min()
            self.analyzedvalues.set(f"Max: {self.figure_frame.df_max}, Min: {self.figure_frame.df_min}, Mean: {self.figure_frame.df_mean}")
            self.input_frame.filepath.set(csvpath)
            app.is_first = True #regard when csv is read as the first time
            self.screen()
        
    def screen(self):
        if((fig := self.plot()) == None):
            return
        try:
            figure_canvas = FigureCanvasTkAgg(fig, master=self.figure_frame)
            figure_canvas.draw()
            toolbar = MyNavigationToolbar(figure_canvas, self.figure_frame, pack_toolbar=False)
            toolbar.update()
            toolbar.grid(column=0, row=0, sticky=tk.EW)
            # figure_canvas.mpl_connect(
            #     "key_press_event", lambda event: print(f"you pressed {event.key}"))
            # figure_canvas.mpl_connect("key_press_event", key_press_handler)
            figure_canvas.get_tk_widget().grid(column=0, row=1, sticky=tk.NSEW)
            # plt.show()
        except ValueError as e: # Error(Latex) in drawing figure
            pass
            # print(traceback.format_exception(*sys.exc_info()))
            # figure_canvas = FigureCanvasTkAgg(fig, master=self.figure_frame)
    def plot(self):
        # path = self.input_frame.filepath.get()
        if((path := self.input_frame.filepath.get()) == ""):
            return None
        plt.close("all")

        df = self.figure_frame.df
        fig = plt.figure(figsize=(9,6), dpi=100)

        df_width = len(df.columns)
        df_height = len(df)
        # ax_ = ax_.ravel()
        # norm = mpl.colors.Normalize(df_min, 138)
        # cmax = df.max().max()
        # cmin = df.min().min()
        try:
            # cs_max = self.input_frame.scalemax.get()
            # cs_min = self.input_frame.scalemin.get()
            cmax = self.input_frame.scalemax.get()
            cmin = self.input_frame.scalemin.get()
        except:
            return None
        if(self.is_first): # set initial values
            self.is_first = False
            cmax = math.ceil(self.figure_frame.df_max)
            cmin = math.floor(self.figure_frame.df_min)
            cinterval = (cmax-cmin)/10
            x_interval = 1 if df_width < 5 else df_width//5
            y_interval = 1 if df_height < 4 else df_height//4
            self.input_frame.scalemax.set(cmax)
            self.input_frame.scalemin.set(cmin)
            self.input_frame.scaleinterval.set(cinterval)
            self.input_frame.xaxis_cbox.set(x_interval)
            self.input_frame.yaxis_cbox.set(y_interval)
            self.input_frame.change_intervalslist()
        elif('' in (cmax, cmin)):
            # When colorbar scale max or min have no value.
            return None
        elif(cmax <= cmin):
            return None
        else:
            self.input_frame.change_intervalslist()
            if((cinterval := self.input_frame.scaleinterval.get()) not in self.input_frame.scaleintervals_cbox["values"]):
                # cmax = self.input_frame.scalemax.get()
                # cmin = self.input_frame.scalemin.get()
                cinterval = (cmax-cmin)/10
                self.input_frame.scaleinterval.set(cinterval)
            # cmax = cs_max
            # cmin = cs_min
            # cinterval = self.input_frame.scaleinterval.get()
            x_interval = self.input_frame.xaxis_interval.get()
            y_interval = self.input_frame.yaxis_interval.get()

        cbar_step = int((cmax-cmin)/cinterval)
        cbar_norm = mpl.colors.Normalize(cmin, cmax)
        cmap = self.input_frame.which_cm.get()
        if(self.input_frame.cm_reversed.get()):
            cmap =cmap+"_r"
        
        if(self.input_frame.is_3d.get()):
            ax = fig.add_subplot(111, projection="3d")
            x = np.arange(1, df_width+1)
            y = np.arange(1, df_height+1)
            X, Y = np.meshgrid(x, y)
            ax.plot_surface(X, Y, df, cmap = cmap)
        else:
            ax = fig.add_subplot(111)
            extent = 0.5, df_width+0.5, df_height+0.5, 0.5
            ax.matshow(df, norm=cbar_norm, cmap=cmap, extent=extent)
            # # ax.matshow(df, norm=cbar_norm, cmap=cmap,)
            ax.xaxis.set_label_position('top')
            ax.yaxis.set_ticks_position('both')
        cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=cbar_norm, cmap=cmap),ax=ax,)
        cbar.ax.set_yticks([cmin+i*cinterval for i in range(cbar_step+1)])
        cbar.ax.set_yticklabels([fr"$\leq {float(cmin)}$"]+[f"${round(cmin+(i+1)*cinterval, 3)}$" for i in range(cbar_step-1)]+[fr"$\geq {float(cmax)}$"])
        ax.set_xticks([1]+[i for i in range(int(x_interval), df_width+1, int(x_interval))])
        ax.set_yticks([1]+[i for i in range(int(y_interval), df_height+1, int(y_interval))])
        labelsize = self.input_frame.labelsize.get()
        tickslabelsize = self.input_frame.tickslabelsize.get()
        cbar.ax.tick_params(axis='y', labelsize=tickslabelsize)
        ax.tick_params(axis='x', labelsize=tickslabelsize)
        ax.tick_params(axis='y', labelsize=tickslabelsize)
        cbar.set_label(fr"${(self.input_frame.cbarlabel.get())}$", fontsize=labelsize)
        ax.set_xlabel(fr"${(self.input_frame.xlabel.get())}$", fontsize=labelsize)
        ax.set_ylabel(fr"${(self.input_frame.ylabel.get())}$", fontsize=labelsize)
        

        _ = list(range(1,10))+[i for i in range(10, df_width, 5)]+[df_width] if df_width > 10 else list(range(1, df_width+1))
        self.input_frame.xaxis_cbox["values"] = [i for i in _ if df_width/i < 21]
        _ = list(range(1,10))+[i for i in range(10, df_height, 5)]+[df_height] if df_height > 10 else list(range(1, df_height+1))
        self.input_frame.yaxis_cbox["values"] = [i for i in _ if df_height/i < 21]

        return fig

def center(win):
        w = win.winfo_screenwidth()  # モニター横幅取得
        h = win.winfo_screenheight()  # モニター縦幅取得
        # w = int((w - float(re.split("[+]", win.geometry())[1]))/2)  # メイン画面横幅分調整
        # h = int((h - float(re.split("[+]", win.geometry())[2]))/2)  # メイン画面縦幅分調整
        win.geometry("+" + str(w//2-572) + "+" + str(h//2-310))  # 位置設定
        win.attributes('-alpha', 1.0)

def on_closing():
    app.quit()
    app.destroy()

if __name__ == "__main__":
    df = pd.DataFrame()
    app = App()
    center(app)
    
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
