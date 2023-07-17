import tkinter as tk
import pandas as pd
from PIL import ImageGrab
from tkinter import messagebox
from datetime import datetime
import csv
import tkinter.colorchooser


def btnLoadClick():
    if (entry_row.get()=="")|(entry_col.get()==""):
        messagebox.showwarning(title="error", message="행 수, 열 수를 입력해주세요")
        return
    if (entry_row.get().isdigit()==False)|(entry_col.get().isdigit()==False)|(entry_row.get()=='0')|(entry_col.get()=='0'):
        messagebox.showwarning(title="invalid data", message="행 수, 열 수를 자연수로 입력해주세요")
        return
    if entry_load.get()=="":
        messagebox.showwarning(title="error", message="파일명을 입력해주세요")
        return
    
    global nrow
    nrow=int(entry_row.get())
    
    global ncol
    ncol=int(entry_col.get())
    
    filename=entry_load.get()+'.csv'
    
    global df
    try:
        df=pd.read_csv(filename)
    except:
        messagebox.showwarning(title="error", message="파일 load 실패")
        return
    
    if df.shape[0]%2==1:
        messagebox.showwarning(title="error", message="data 갯수 홀수")
        return
    
    if df.shape[1]!=(1+2*nrow*ncol):
        messagebox.showwarning(title="error", message="invalid data")
        return
    
    global nLeg
    nLeg=int(df.shape[0]/2)

    lb_before.delete(0,tk.END)
    lb_after.delete(0,tk.END)

    for i in range(nLeg):
        lb_before.insert(i, int(df.iloc[i].values[0]))
        lb_after.insert(i, int(df.iloc[i+nLeg].values[0]))
    
    tempB=[[[df.iloc[Leg].values[1 + 2*n], df.iloc[Leg].values[1 + 2*n +1]] for n in range(nrow*ncol)] for Leg in range(nLeg)]
    tempA=[[[df.iloc[Leg+nLeg].values[1 + 2*n], df.iloc[Leg+nLeg].values[1 + 2*n +1]] for n in range(nrow*ncol)] for Leg in range(nLeg)]

    for Leg in range(nLeg): #y값 기준 내림차순 정렬
        tempB[Leg].sort(key = lambda x : -x[1])
        tempA[Leg].sort(key = lambda x : -x[1])
        
    global B
    global A
    B=[[[[tempB[Leg][row*ncol+col][0], tempB[Leg][row*ncol+col][1]] for col in range(ncol)] for row in range(nrow)] for Leg in range(nLeg)]
    A=[[[[tempA[Leg][row*ncol+col][0], tempA[Leg][row*ncol+col][1]] for col in range(ncol)] for row in range(nrow)] for Leg in range(nLeg)]

    for Leg in range(nLeg):
        for row in  range(nrow): #x값 기준 오름차순 정렬
            B[Leg][row].sort(key = lambda x : x[0])
            A[Leg][row].sort(key = lambda x : x[0])
    
    Bxmin = [0] * nLeg
    Bxmax = [0] * nLeg
    Bymin = [0] * nLeg
    Bymax = [0] * nLeg

    Axmin = [0] * nLeg
    Axmax = [0] * nLeg
    Aymin = [0] * nLeg
    Aymax = [0] * nLeg

    Bcx = [0] * nLeg
    Bcy = [0] * nLeg
    Acx = [0] * nLeg
    Acy = [0] * nLeg

    for Leg in range(nLeg):

        Bxmin[Leg] = B[Leg][row][0][0]
        Bxmax[Leg] = B[Leg][row][0][0]
        Bymin[Leg] = B[Leg][row][0][1]
        Bymax[Leg] = B[Leg][row][0][1]

        Axmin[Leg] = A[Leg][row][0][0]
        Axmax[Leg] = A[Leg][row][0][0]
        Aymin[Leg] = A[Leg][row][0][1]
        Aymax[Leg] = A[Leg][row][0][1]

        for row in range(nrow):
            for col in range(1,ncol):
                if B[Leg][row][col][0] < Bxmin[Leg]: Bxmin[Leg] = B[Leg][row][col][0]
                if B[Leg][row][col][0] > Bxmax[Leg]: Bxmax[Leg] = B[Leg][row][col][0]
                if B[Leg][row][col][1] < Bymin[Leg]: Bymin[Leg] = B[Leg][row][col][1]
                if B[Leg][row][col][1] > Bymax[Leg]: Bymax[Leg] = B[Leg][row][col][1]

                if A[Leg][row][col][0] < Axmin[Leg]: Axmin[Leg] = A[Leg][row][col][0]
                if A[Leg][row][col][0] > Axmax[Leg]: Axmax[Leg] = A[Leg][row][col][0]
                if A[Leg][row][col][1] < Aymin[Leg]: Aymin[Leg] = A[Leg][row][col][1]
                if A[Leg][row][col][1] > Aymax[Leg]: Aymax[Leg] = A[Leg][row][col][1]
        
        Bcx[Leg] = (Bxmin[Leg] + Bxmax[Leg])/2
        Bcy[Leg] = (Bymin[Leg] + Bymax[Leg])/2
        Acx[Leg] = (Axmin[Leg] + Axmax[Leg])/2
        Acy[Leg] = (Aymin[Leg] + Aymax[Leg])/2

        for row in range(nrow):
            for col in range(ncol):
                B[Leg][row][col][0] = B[Leg][row][col][0] - Bcx[Leg]
                B[Leg][row][col][1] = B[Leg][row][col][1] - Bcy[Leg]
                A[Leg][row][col][0] = A[Leg][row][col][0] - Acx[Leg]
                A[Leg][row][col][1] = A[Leg][row][col][1] - Acy[Leg]
    """
    D=[[[0] for _ in range(ncol*nrow)] for _ in range(nLeg)]
    Dp=[[[0] for _ in range(ncol*nrow)] for _ in range(nLeg)]

    for Leg in range(nLeg):
        for row in range(nrow):
            for col in range(ncol):
                D[Leg][row*ncol+col]=((B[Leg][row][col][0]-A[Leg][row][col][0])**2 + (B[Leg][row][col][1]-A[Leg][row][col][1])**2)**(1/2)
                Dp[Leg][row*ncol+col]=100*D[Leg][row*ncol+col]/(((B[Leg][row][col][0])**2 + (B[Leg][row][col][1])**2)**(1/2))
    """
    
    try:
        f=open(entry_load.get()+'_output.csv','w',newline='')
    except:
        messagebox.showwarning(title="error", message="close the output file")
        return
    
    writer=csv.writer(f)

    writer.writerow(['X strain (%)'])
    writer.writerow('LEG'+str(Leg+1) for Leg in range(nLeg))

    xstrain=[0]*nLeg
    for Leg in range(nLeg):
        xstrain[Leg] = xstrain[Leg] + ((A[Leg][0][0][0]-B[Leg][0][0][0])/B[Leg][0][0][0]) *100
        xstrain[Leg] = xstrain[Leg] + ((A[Leg][0][ncol-1][0]-B[Leg][0][ncol-1][0])/B[Leg][0][ncol-1][0])*100
        xstrain[Leg] = xstrain[Leg] + ((A[Leg][nrow-1][0][0]-B[Leg][nrow-1][0][0])/B[Leg][nrow-1][0][0])*100
        xstrain[Leg] = xstrain[Leg] + ((A[Leg][nrow-1][ncol-1][0]-B[Leg][nrow-1][ncol-1][0])/B[Leg][nrow-1][ncol-1][0])*100
        xstrain[Leg] = xstrain[Leg]/4
    
    writer.writerow(str(round(xstrain[Leg],4)) for Leg in range(nLeg))
    writer.writerow(['avg'])

    temp=0
    for Leg in range(nLeg):
        temp = temp + xstrain[Leg]
    temp = temp / nLeg

    writer.writerow([str(round(temp,4))])
    writer.writerow([''])

    writer.writerow(['Y strain (%)'])
    writer.writerow('LEG'+str(Leg+1) for Leg in range(nLeg))

    ystrain=[0]*nLeg
    for Leg in range(nLeg):
        ystrain[Leg] = ystrain[Leg] + ((A[Leg][0][0][1]-B[Leg][0][0][1])/B[Leg][0][0][1])*100
        ystrain[Leg] = ystrain[Leg] + ((A[Leg][0][ncol-1][1]-B[Leg][0][ncol-1][1])/B[Leg][0][ncol-1][1])*100
        ystrain[Leg] = ystrain[Leg] + ((A[Leg][nrow-1][0][1]-B[Leg][nrow-1][0][1])/B[Leg][nrow-1][0][1])*100
        ystrain[Leg] = ystrain[Leg] + ((A[Leg][nrow-1][ncol-1][1]-B[Leg][nrow-1][ncol-1][1])/B[Leg][nrow-1][ncol-1][1])*100
        ystrain[Leg] = ystrain[Leg]/4
    
    writer.writerow(str(round(ystrain[Leg],4)) for Leg in range(nLeg))
    writer.writerow(['avg'])

    temp=0
    for Leg in range(nLeg):
        temp = temp + ystrain[Leg]
    temp = temp / nLeg

    writer.writerow([str(round(temp,4))])
    writer.writerow([''])
    """
    for Leg in range(nLeg):
        writer.writerow(['LEG'+str(Leg+1)+' displacement(mm)'])
        for row in range(nrow):
            writer.writerow('P'+str(col) for col in range(row*ncol+1,row*ncol+ncol+1))
            writer.writerow(str(round(D[Leg][col],6)) for col in range(row*ncol,row*ncol+ncol))
        writer.writerow([''])
    
    for Leg in range(nLeg):
        writer.writerow(['LEG'+str(Leg+1)+' displacement(%)'])
        for row in range(nrow):
            writer.writerow('P'+str(col) for col in range(row*ncol+1,row*ncol+ncol+1))
            writer.writerow(str(round(Dp[Leg][col],4)) for col in range(row*ncol,row*ncol+ncol))
        writer.writerow([''])
    """
    temp1=[]
    temp2=[]
    for Leg in range(nLeg):
        writer.writerow(['LEG'+str(Leg+1)+' B'])
        for row in range(nrow):
            del temp1[0:]
            del temp2[0:]
            for col in range(ncol) :
                temp1.append('X'+str(col+1+row*ncol))
                temp1.append('Y'+str(col+1+row*ncol))
                temp2.append(B[Leg][row][col][0])
                temp2.append(B[Leg][row][col][1])    
            writer.writerow(temp1)
            writer.writerow(temp2)
        writer.writerow([''])

        writer.writerow(['LEG'+str(Leg+1)+' A'])
        for row in range(nrow):
            del temp1[0:]
            del temp2[0:]
            for col in range(ncol) :
                temp1.append('X'+str(col+1+row*ncol))
                temp1.append('Y'+str(col+1+row*ncol))
                temp2.append(A[Leg][row][col][0])
                temp2.append(A[Leg][row][col][1])    
            writer.writerow(temp1)
            writer.writerow(temp2)
        writer.writerow([''])
    """
    for Leg in range(nLeg):
        writer.writerow(['LEG'+str(Leg+1)+' X displacement(mm)'])
        for row in range(nrow):
            writer.writerow('X'+str(col) for col in range(row*ncol+1,row*ncol+ncol+1))
            writer.writerow(str((A[Leg][row][col][0]-B[Leg][row][col][0])) for col in range(ncol))
        writer.writerow([''])

        writer.writerow(['LEG'+str(Leg+1)+' X strain(%)'])
        temp=0
        
        for row in range(nrow):
            writer.writerow('X'+str(col) for col in range(row*ncol+1,row*ncol+ncol+1))
            writer.writerow(str(((A[Leg][row][col][0]-B[Leg][row][col][0])/B[Leg][row][col][0])*100) for col in range(ncol))
            temp=temp+abs((A[Leg][row][col][0]-B[Leg][row][col][0])/B[Leg][row][col][0])*100
        
        temp = temp + ((A[Leg][0][0][0]-B[Leg][0][0][0])/B[Leg][0][0][0])*100
        temp = temp + ((A[Leg][0][ncol-1][0]-B[Leg][0][ncol-1][0])/B[Leg][0][ncol-1][0])*100
        temp = temp + ((A[Leg][nrow-1][0][0]-B[Leg][nrow-1][0][0])/B[Leg][nrow-1][0][0])*100
        temp = temp + ((A[Leg][nrow-1][ncol-1][0]-B[Leg][nrow-1][ncol-1][0])/B[Leg][nrow-1][ncol-1][0])*100
        temp = temp/4
        writer.writerow(['average : '+str(round(temp,4))+'%'])
        writer.writerow([''])

        writer.writerow(['LEG'+str(Leg+1)+' Y displacement(mm)'])
        for row in range(nrow):
            writer.writerow('Y'+str(col) for col in range(row*ncol+1,row*ncol+ncol+1))
            writer.writerow(str((A[Leg][row][col][1]-B[Leg][row][col][1])) for col in range(ncol))
        writer.writerow([''])

        writer.writerow(['LEG'+str(Leg+1)+' Y strain(%)'])
        temp=0
        for row in range(nrow):
            writer.writerow('Y'+str(col) for col in range(row*ncol+1,row*ncol+ncol+1))
            writer.writerow(str(((A[Leg][row][col][1]-B[Leg][row][col][1])/B[Leg][row][col][1])*100) for col in range(ncol))
            temp=temp+((A[Leg][row][col][1]-B[Leg][row][col][1])/B[Leg][row][col][1])*100
        temp=temp/(nrow*ncol)
        writer.writerow(['average : '+str(temp)])
        writer.writerow([''])
    """
    f.close()

    global dcs    
    if nrow>ncol: dcs=600/nrow
    else: dcs=600/ncol

    w=dcs*ncol
    h=dcs*nrow

    canvas.place(x=25, y=95, width=w, height=h)

    for i in range(nrow+1):
        canvas.create_line((0,i*dcs),(w,i*dcs),fill="gray",dash=(2,1))
        
    for j in range(ncol+1):
        canvas.create_line((j*dcs,0),(j*dcs,h),fill="gray",dash=(2,1))

    global xmp, ymp
    xmp=[0] * ncol
    ymp=[0] * nrow

    global minscale, maxscale
    minscale = 0

    for row in range(nrow):
        ymax=B[0][row][0][1]
        ymin=B[0][row][0][1]
        for Leg in range(nLeg):
            for col in range(ncol):
                if B[Leg][row][col][1] > ymax : ymax = B[Leg][row][col][1]
                if A[Leg][row][col][1] > ymax : ymax = A[Leg][row][col][1]
                if B[Leg][row][col][1] < ymin : ymin = B[Leg][row][col][1]
                if A[Leg][row][col][1] < ymin : ymin = A[Leg][row][col][1]
        if (ymax-ymin) > minscale : minscale = (ymax-ymin)
        ymp[row]=(ymax + ymin)/2
    
    for col in range(ncol):
        xmin=B[0][0][col][0]
        xmax=B[0][0][col][0]
        for Leg in range(nLeg):
            for row in range(nrow):
                if B[Leg][row][col][0] > xmax : xmax = B[Leg][row][col][0]
                if A[Leg][row][col][0] > xmax : xmax = A[Leg][row][col][0]
                if B[Leg][row][col][0] < xmin : xmin = B[Leg][row][col][0]
                if A[Leg][row][col][0] < xmin : xmin = A[Leg][row][col][0]
        if (xmax-xmin) > minscale : minscale = (xmax-xmin)
        xmp[col]=(xmax + xmin)/2
    
    maxscale=415/ncol
    if 515/nrow < maxscale : maxscale = 515/nrow

    label_minscale.config(text="minscale : %.4fmm" % minscale)
    label_maxscale.config(text="maxscale : %.4fmm" % maxscale)

    global dB,dA
    dB=[[[[0] *2 for _ in range(ncol)] for _ in range(nrow)] for _ in range(nLeg)]
    dA=[[[[0] *2 for _ in range(ncol)] for _ in range(nrow)] for _ in range(nLeg)]

    global LineB, LineA
    LineB=[[[[0]*2 for _ in range(ncol)] for _ in range(nrow)] for _ in range(nLeg)]
    LineA=[[[[0]*2 for _ in range(ncol)] for _ in range(nrow)] for _ in range(nLeg)]

    global colorB, colorA
    colorB=['']*nLeg
    colorA=['']*nLeg

    def changecolorB(event):
        Leg=lb_before.curselection()[0]
        if LineB[Leg][0][0][0]!=0:
            colorB[Leg]=tkinter.colorchooser.askcolor()[1]
            for col in range(ncol):
                for row in range(nrow-1):
                    canvas.delete(LineB[Leg][row][col][0])
                    LineB[Leg][row][col][0]=canvas.create_line(dB[Leg][row][col],dB[Leg][row+1][col],fill=colorB[Leg])
            for row in range(nrow):
                for col in range(ncol-1):
                    canvas.delete(LineB[Leg][row][col][1])
                    LineB[Leg][row][col][1]=canvas.create_line(dB[Leg][row][col],dB[Leg][row][col+1],fill=colorB[Leg])
            lb_before.itemconfig(Leg,{'fg':colorB[Leg]})
        else:
            colorB[Leg]=tkinter.colorchooser.askcolor()[1]
    def changecolorA(event):
        Leg=lb_after.curselection()[0]
        if LineA[Leg][0][0][0]!=0:
            colorA[Leg]=tkinter.colorchooser.askcolor()[1]
            for col in range(ncol):
                for row in range(nrow-1):
                    canvas.delete(LineA[Leg][row][col][0])
                    LineA[Leg][row][col][0]=canvas.create_line(dA[Leg][row][col],dA[Leg][row+1][col],fill=colorA[Leg])
            for row in range(nrow):
                for col in range(ncol-1):
                    canvas.delete(LineA[Leg][row][col][1])
                    LineA[Leg][row][col][1]=canvas.create_line(dA[Leg][row][col],dA[Leg][row][col+1],fill=colorA[Leg])
            lb_after.itemconfig(Leg,{'fg':colorA[Leg]})
        else:
            colorA[Leg]=tkinter.colorchooser.askcolor()[1]
    lb_before.bind('<Double-1>',changecolorB)
    lb_after.bind('<Double-1>',changecolorA)

    global lw
    lw=1

    entry_scale.config(state='normal')
    button_scale.config(state='normal')
    entry_width.config(state='normal')
    button_width.config(state='normal')

def btnInitClick():
    
    for Leg in range(nLeg):
        if LineB[Leg][0][0][0]!=0:
            for col in range(ncol):
                for row in range(nrow-1):
                    #canvas.delete(LineB[Leg][row][col][0])
                    LineB[Leg][row][col][0]=0
            for row in range(nrow):
                for col in range(ncol-1):
                    #canvas.delete(LineB[Leg][row][col][1])
                    LineB[Leg][row][col][1]=0
            lb_before.itemconfig(Leg,{'fg':'black'})
        if LineA[Leg][0][0][0]!=0:
            for col in range(ncol):
                for row in range(nrow-1):
                    #canvas.delete(LineA[Leg][row][col][0])
                    LineA[Leg][row][col][0]=0
            for row in range(nrow):
                for col in range(ncol-1):
                    #canvas.delete(LineA[Leg][row][col][1])
                    LineA[Leg][row][col][1]=0
            lb_after.itemconfig(Leg,{'fg':'black'})
    
    canvas.delete(tk.ALL)
    lb_before.delete(0,tk.END)
    lb_after.delete(0,tk.END)
    entry_scale.delete(0,tk.END)
    entry_width.delete(0,tk.END)
    global lw
    lw=1
    entry_scale.config(state='disabled')

    label_minscale.config(text="minscale")
    label_maxscale.config(text="maxscale")

    button_scale.config(state='disabled')
    button_draw.config(state='disabled')
    button_hide.config(state='disabled')
    button_save.config(state='disabled')

    entry_width.config(state='disabled')
    button_width.config(state='disabled')

def btnApplyClick():

    global scale
    try:
        scale=float(entry_scale.get())
    except:
        messagebox.showwarning(title="error", message="scale error")
        return
    """
    if (scale<minscale)|(scale>maxscale):
        messagebox.showwarning(title="error", message="scale : %.4f~%.4f" % (minscale,maxscale))
        return
    """

    for Leg in range(nLeg):
        if LineB[Leg][0][0][0]!=0:
            for col in range(ncol):
                for row in range(nrow-1):
                    canvas.delete(LineB[Leg][row][col][0])
                    LineB[Leg][row][col][0]=0
            for row in range(nrow):
                for col in range(ncol-1):
                    canvas.delete(LineB[Leg][row][col][1])
                    LineB[Leg][row][col][1]=0
            lb_before.itemconfig(Leg,{'fg':'black'})
        if LineA[Leg][0][0][0]!=0:
            for col in range(ncol):
                for row in range(nrow-1):
                    canvas.delete(LineA[Leg][row][col][0])
                    LineA[Leg][row][col][0]=0
            for row in range(nrow):
                for col in range(ncol-1):
                    canvas.delete(LineA[Leg][row][col][1])
                    LineA[Leg][row][col][1]=0
            lb_after.itemconfig(Leg,{'fg':'black'})
    lb_before.select_clear(0,tk.END)
    lb_after.select_clear(0,tk.END)

    for Leg in range(nLeg):
        for row in range(nrow):
            for col in range(ncol):
                dB[Leg][row][col][0] = (col+0.5)*dcs + ((B[Leg][row][col][0]-xmp[col])/scale)*dcs
                dA[Leg][row][col][0] = (col+0.5)*dcs + ((A[Leg][row][col][0]-xmp[col])/scale)*dcs
                dB[Leg][row][col][1] = (row+0.5)*dcs + ((ymp[row]-B[Leg][row][col][1])/scale)*dcs
                dA[Leg][row][col][1] = (row+0.5)*dcs + ((ymp[row]-A[Leg][row][col][1])/scale)*dcs
    
    button_save.config(state='normal')
    button_draw.config(state='normal')
    button_hide.config(state='normal')
    button_init.config(state='normal')

 

def btnDrawClick():
    #global lw
    #lw=1
    G=[0]*nLeg

    for i in range(nLeg):
        G[i]=int(round(255*i/nLeg,0))
        if G[i]<16 :
            if colorB[i]=='': colorB[i]='#000'+hex(G[i])[2:]+'ff'
            if colorA[i]=='': colorA[i]='#ff0'+hex(G[i])[2:]+'00'
        else : 
            if colorB[i]=='': colorB[i]='#00'+hex(G[i])[2:]+'ff'
            if colorA[i]=='': colorA[i]='#ff'+hex(G[i])[2:]+'00'
    
    
    if (len(lb_before.curselection())==0)&(len(lb_after.curselection())==0):
        messagebox.showwarning(title="error", message="표시할 데이타를 선택해주세요")
        return
    
    if len(lb_before.curselection())>0:
        for i in range(len(lb_before.curselection())):
            Leg=lb_before.curselection()[i]
            if LineB[Leg][0][0][0]==0:
                for col in range(ncol):
                    for row in range(nrow-1):
                        LineB[Leg][row][col][0]=canvas.create_line(dB[Leg][row][col],dB[Leg][row+1][col],fill=colorB[Leg],width=lw)
                for row in range(nrow):
                    for col in range(ncol-1):
                        LineB[Leg][row][col][1]=canvas.create_line(dB[Leg][row][col],dB[Leg][row][col+1],fill=colorB[Leg],width=lw)
            lb_before.itemconfig(Leg,{'fg':colorB[Leg]})
        lb_before.select_clear(0,tk.END)
    
    if len(lb_after.curselection())>0:
        for i in range(len(lb_after.curselection())):
            Leg=lb_after.curselection()[i]
            if LineA[Leg][0][0][0]==0:
                for col in range(ncol):
                    for row in range(nrow-1):
                        LineA[Leg][row][col][0]=canvas.create_line(dA[Leg][row][col],dA[Leg][row+1][col],fill=colorA[Leg],width=lw)
                for row in range(nrow):
                    for col in range(ncol-1):
                        LineA[Leg][row][col][1]=canvas.create_line(dA[Leg][row][col],dA[Leg][row][col+1],fill=colorA[Leg],width=lw)
            lb_after.itemconfig(Leg,{'fg':colorA[Leg]})
        lb_after.select_clear(0,tk.END)



def btnHideClick():
    if (len(lb_before.curselection())==0)&(len(lb_after.curselection())==0):
        messagebox.showwarning(title="error", message="숨길 데이타를 선택해주세요")
        return
    
    if len(lb_before.curselection())>0:
        for i in range(len(lb_before.curselection())):
            Leg=lb_before.curselection()[i]
            if (LineB[Leg][0][0][0]!=0):
                for col in range(ncol):
                    for row in range(nrow-1):
                        canvas.delete(LineB[Leg][row][col][0])
                        LineB[Leg][row][col][0]=0
                for row in range(nrow):
                    for col in range(ncol-1):
                        canvas.delete(LineB[Leg][row][col][1])
                        LineB[Leg][row][col][1]=0
            lb_before.itemconfig(Leg,{'fg':'black'})
        lb_before.select_clear(0,tk.END)
    
    if len(lb_after.curselection())>0:
        for i in range(len(lb_after.curselection())):
            Leg=lb_after.curselection()[i]
            if (LineA[Leg][0][0][0]!=0):
                for col in range(ncol):
                    for row in range(nrow-1):
                        canvas.delete(LineA[Leg][row][col][0])
                        LineA[Leg][row][col][0]=0
                for row in range(nrow):
                    for col in range(ncol-1):
                        canvas.delete(LineA[Leg][row][col][1])
                        LineA[Leg][row][col][1]=0
            lb_after.itemconfig(Leg,{'fg':'black'})
        lb_after.select_clear(0,tk.END)

def btnWidthClick():
    global lw
    try:
        w=float(entry_width.get())
    except:
        messagebox.showwarning(title="error", message="line width error")
        return
    
    if w<=0:
        messagebox.showwarning(title="error", message="line width > 0")
        return
    
    lw=w

    for Leg in range(nLeg):
        if LineB[Leg][0][0][0]!=0:
            for col in range(ncol):
                for row in range(nrow-1):
                    canvas.delete(LineB[Leg][row][col][0])
                    LineB[Leg][row][col][0]=canvas.create_line(dB[Leg][row][col],dB[Leg][row+1][col],fill=colorB[Leg],width=lw)
            for row in range(nrow):
                for col in range(ncol-1):
                    canvas.delete(LineB[Leg][row][col][1])
                    LineB[Leg][row][col][1]=canvas.create_line(dB[Leg][row][col],dB[Leg][row][col+1],fill=colorB[Leg],width=lw)
            
        if LineA[Leg][0][0][0]!=0:
            for col in range(ncol):
                for row in range(nrow-1):
                    canvas.delete(LineA[Leg][row][col][0])
                    LineA[Leg][row][col][0]=canvas.create_line(dA[Leg][row][col],dA[Leg][row+1][col],fill=colorA[Leg],width=lw)
            for row in range(nrow):
                for col in range(ncol-1):
                    canvas.delete(LineA[Leg][row][col][1])
                    LineA[Leg][row][col][1]=canvas.create_line(dA[Leg][row][col],dA[Leg][row][col+1],fill=colorA[Leg],width=lw)
        


def btnSaveClick():
    x = win.winfo_rootx()*1.25 + 25*1.25
    y = win.winfo_rooty()*1.25 + 95*1.25
    w = dcs*ncol*1.25 + x
    h = dcs*nrow*1.25 + y
    box=(x,y,w,h)
    img=ImageGrab.grab(box)
    now=datetime.now()
    time=now.strftime("%Y%m%d_%H%M%S")
    img.save(time+'_scale='+str(scale)+'mm.png')



win=tk.Tk()
win.geometry('900x700+50+50')
win.title("PNL 수축 v1.3")

label_row=tk.Label(win, text="행 수 :")
entry_row=tk.Entry(win)
label_col=tk.Label(win, text="열 수 :")
entry_col=tk.Entry(win)
label_row.place(x=5,y=5,width=50,height=20)
entry_row.place(x=55,y=5,width=50,height=20)
label_col.place(x=5,y=25,width=50,height=20)
entry_col.place(x=55,y=25,width=50,height=20)

label_load=tk.Label(win, text="파일명 :")
entry_load=tk.Entry(win)
label_csv=tk.Label(win, text=".csv")
button_load=tk.Button(win, text="load", command=btnLoadClick)
label_load.place(x=5,y=50,width=50,height=20)
entry_load.place(x=55,y=50,width=100,height=20)
label_csv.place(x=155,y=50,width=30,height=20)
button_load.place(x=190,y=50,width=40,height=20)

entry_row.insert(0,'5')
entry_col.insert(0,'5')
entry_load.insert(0,'input')

label_minscale=tk.Label(win,text="minscale")
label_maxscale=tk.Label(win,text="maxscale")
label_minscale.place(x=250,y=5,width=150,height=20)
label_maxscale.place(x=250,y=25,width=150,height=20)

label_scale=tk.Label(win, text="scale :")
label_scale.place(x=250,y=50,width=60,height=20)
entry_scale=tk.Entry(win)
entry_scale.place(x=310,y=50,width=60,height=20)
entry_scale.config(state='disabled')
label_mm=tk.Label(win, text="mm")
label_mm.place(x=370,y=50,width=30,height=20)
button_scale=tk.Button(win, text="적용", command=btnApplyClick)
button_scale.place(x=405,y=50,width=50,height=20)
button_scale.config(state='disabled')

button_draw=tk.Button(win, text="표시", command=btnDrawClick)
button_hide=tk.Button(win, text="숨기기", command=btnHideClick)
button_draw.place(x=700, y=75, width=50, heigh=20)
button_hide.place(x=760, y=75, width=50, heigh=20)
button_draw.config(state='disabled')
button_hide.config(state='disabled')

label_width=tk.Label(win, text="선굵기 :")
entry_width=tk.Entry(win)
button_width=tk.Button(win, text="적용", command=btnWidthClick)
label_width.place(x=650,y=40,width=60,height=20)
entry_width.place(x=710,y=40,width=60,height=20)
button_width.place(x=775,y=40,width=45,height=20)
entry_width.config(state='disabled')
button_width.config(state='disabled')

button_save=tk.Button(win, text="저장", command=btnSaveClick)
button_save.place(x=500,y=50,width=60,height=20)
lb_before=tk.Listbox(win, exportselection=False, selectmode='extended')
lb_after=tk.Listbox(win, exportselection=False, selectmode='extended')
lb_before.place(x=700, y=100, width=100, height=290)
lb_after.place(x=700, y=400, width=100, height=290)
button_save.config(state='disabled')

button_init=tk.Button(win, text="초기화", command=btnInitClick)
button_init.place(x=500,y=5,width=60,height=20)
button_init.config(state='disabled')

canvas=tk.Canvas(win, relief="solid", bg="white", bd=1)



win.mainloop()