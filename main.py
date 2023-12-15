import tkinter as tk
import numpy as np
import utils
from tkinter import *
from tkinter import messagebox



def stoi(s):
    if ((s[0] >= '0' and s[0] <= '9') or s[0] == '-'):
        return int(s)
    return s


# Tạo một đối tượng Tkinter window
window = tk.Tk()
window.title("Giải Bài toán quy hoạch tuyến tính")

# Tạo một khung nhập liệu
entry_frame = tk.Frame(window, padx=10, pady=10)
entry_frame.pack(side=tk.LEFT, padx=5, pady=5)

input2_label = tk.Label(entry_frame, text="Enter the number of variables", font=30)
input2_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
input2_entry = tk.Entry(entry_frame, width=20, font=30)
input2_entry.grid(row=0, column=1, padx=5, pady=5)



input_label = tk.Label(entry_frame, text="Enter the number of constraints", font=30)
input_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
input_entry = tk.Entry(entry_frame, width=20, font=30)
input_entry.grid(row=1, column=1, padx=5, pady=5)

#next_button = tk.Button(entry_frame, text="Next",font=30, command=next)
#next_button.grid(row=1, column=2, padx=0, pady=0)
button = tk.Button(entry_frame,  padx=10, pady=6 ,text="Next", bg='White', fg='Black',
                            command=lambda: next())
#button = tk.Button(window,  padx=3, pady=4 ,text="Next", bg='White', fg='Black', command=lambda:next())
button.grid(row=1, column=2, pady=5)



def next():
    # Tạo một đối tượng Tkinter window
    window2 = tk.Toplevel()
    window2.title("Solution")
    window2.geometry("800x500")
  


    # Tạo một khung nhập liệu
    
    #entry_frame2 = tk.Frame(window2, padx=10, pady=10)
    #entry_frame3= tk.Frame(window2)
    #entry_frame3.pack(side=tk.LEFT)
    #entry_frame2.pack(side=tk.LEFT, padx=5, pady=5)

    # Create a Tkinter variable
    tkvar = StringVar()

    # Dictionary with options
    choices = { 'Maximize','Minimize'}
    tkvar.set('') # set the default option

    popupMenu = OptionMenu(window2, tkvar, *choices)
    popupMenu.configure(width=10, font=30)



    objective_label0 = tk.Label(window2, text="Select objective", font=30)
    objective_label0.grid(row=0, column=0 ,sticky="w")
    popupMenu.grid(row = 0, column =1,sticky=N+W, columnspan=10)
    # on change dropdown value




    
    input=input_entry.get().strip()
    input = np.array(input, dtype=int)
    input2=input2_entry.get().strip()
    input2 = np.array(input2, dtype=int)
    
    #temp= 'min' 
    
    def change_dropdown(*args):
        global temp
        temp = ""
        if tkvar.get() =='Maximize':
            print('max')
            temp='max'
        if tkvar.get() =='Minimize':
            print('min')
            temp='min'

# link function to change dropdown
    tkvar.trace('w', change_dropdown)

    flag=2


    objective_label0 = tk.Label(window2, text="Objective", font=30)
    objective_label0.grid(row=0+flag, column=0, sticky="w")

    #objective_entry0 = tk.Entry(window2, width=5, font=30)
    #objective_entry0.grid(row=0+flag, column=1)

    
   
    objective_label=np.zeros(input2,dtype=object)
    objective_entry=np.zeros(input2,dtype=object) 
    for i in range(0,input2):
        
        
        objective_entry[i] = tk.Entry(window2, font=30,width=5)
        objective_entry[i].grid(row=0+flag, column=2*i+1)
        if i!=input2-1:
            objective_label[i] = tk.Label(window2, text=X+str(i+1)+' +', font=30)
        else:
            objective_label[i] = tk.Label(window2, text=X+str(i+1), font=30)

        objective_label[i].grid(row=0+flag, column=2*i+2, sticky="w")
        



    flag=flag+1
    # Tạo một nhãn cho khung nhập liệu tháng
    n=input+3
    constrain_label=np.zeros([input,input2+2],dtype=object)
    constraint_entry=np.zeros([input,input2+2],dtype=object)
    #tkvar2=np.zeros(n,dtype=object)
    for i in range(1,n):
        for j in range(input2+2):
            if i<n-2:
                constrain_label[i-1][j] = tk.Label(window2, text="Constraint "+str(i), font=30)
                constrain_label[i-1][j].grid(row=i+flag, column=0, sticky="w")
                constraint_entry[i-1][j] = tk.Entry(window2, font=30,width=5)
                constraint_entry[i-1][j].grid(row=i+flag, column=2*j+1)
                if j<=input2-2 :
                    constrain_label[i-1][j] = tk.Label(window2, text=X +str(j+1)+' +', font=30)
                    constrain_label[i-1][j].grid(row=i+flag, column=2*j+2, sticky="w")
                if j==input2-1 :
                    constrain_label[i-2][j] = tk.Label(window2, text=X +str(j+1), font=30)
                    constrain_label[i-2][j].grid(row=i+flag, column=2*j+2, sticky="w")
                if j==input2 :
                    constrain_label[i-2][j] = tk.Label(window2, text='', font=30)
                    constrain_label[i-2][j].grid(row=i+flag, column=2*j+2, sticky="w")



    n2=input2+4
    condition_label=np.zeros([input2,input2+2],dtype=object)
    condition_entry=np.zeros([input2,input2+2],dtype=object)
    #tkvar3=np.zeros([input2,input2+2],dtype=object)
    #tkvar2=np.zeros(n,dtype=object)
    for i in range(input2):
        for j in range(input2+2):
            if i<n-2:
                condition_label[i][j] = tk.Label(window2, text="Condition "+str(i+1), font=30)
                condition_label[i][j].grid(row=n2+i+flag, column=0, sticky="w")
                condition_entry[i][j] = tk.Entry(window2, font=30,width=5)
                condition_entry[i][j].grid(row=n2+i+flag, column=2*j+1)
                
                if (j < input2):
                    if (i == j): condition_entry[i][j].insert(0, "1")
                    else: condition_entry[i][j].insert(0, "0")
                    condition_entry[i][j].config(state=DISABLED)

                if (j == input2 + 1):
                    condition_entry[i][j].insert(0, "0")
                    condition_entry[i][j].config(state=DISABLED)


                if j<=input2-2 :
                    condition_label[i][j] = tk.Label(window2, text=X +str(j+1)+'+', font=30)
                    condition_label[i][j].grid(row=n2+i+flag, column=2*j+2, sticky="w")
                if j==input2-1 :
                    condition_label[i][j] = tk.Label(window2, text=X +str(j+1), font=30)
                    condition_label[i][j].grid(row=n2+i+flag, column=2*j+2, sticky="w")
                if j==input2 :
                    condition_label[i][j] = tk.Label(window2, text='', font=30)
                    condition_label[i][j].grid(row=n2+i+flag, column=2*j+2, sticky="w")



    

    # Tạo một nhãn cho khung nhập liệu số kw cũ



    n2=n2-1

    
    def calculate():
        z_entry.delete(0, tk.END)
        for i in range (input2):
            solution_entry[0][i].delete(0, tk.END)
        status_entry.delete(0, tk.END)
        # Lấy giá trị từ các đối tượng nhập liệu
        objectives=np.zeros([1,input2+1],dtype=object)
        constraints=np.zeros([input,input2+2],dtype=object)
        conditions=np.zeros([input2,input2+2],dtype=object)
        # print("conditions = ",conditions)
        # if (temp == ""):
        #     messagebox.showerror("Thông báo", "Chưa có temp")
        #     return
        try:
            objectives[0][0]=temp
        except:
            messagebox.showerror("Thông báo", "Objectives (min, max) is not define")
            return
        try:
            for i in range(0,input2):
                temp1=objective_entry[i].get().strip()
                objectives[0][i+1]=eval(temp1)
            print("objectives", objectives)
        except:
            messagebox.showerror("THông báo", "Objectives is incorrect")
            return

        try:
            for i in range(0,input):
                for j in range(input2+2):
                    temp1=constraint_entry[i][j].get().strip()
                    if temp1=='>=' or temp1=='<=' or temp1=='=' or temp1=='?':
                        constraints[i][j]=temp1
                    if temp1!='>=' and temp1!='<=' and temp1!='=' and temp1!='?':
                        constraints[i][j]=eval(temp1)
                    if j == input2  and  temp1!='>=' and temp1!='<=' and temp1!='=' and temp1!='?':
                        raise ValueError("Error constrains")
                    
            print("constraints", constraints)
        except:
            messagebox.showerror("Thông báo", "Constraints is incorrect")
            return

        try:  
            for i in range(0,input2):
                for j in range(input2+2):
                    
                    temp1=condition_entry[i][j].get().strip()
                    if temp1=='>=' or temp1=='<=' or temp1=='=' or temp1=='?':
                        conditions[i][j]=temp1
                    if temp1!='>=' and temp1!='<=' and temp1!='=' and temp1!='?':
                        conditions[i][j]=eval(temp1)
                    if j == input2  and  temp1!='>=' and temp1!='<=' and temp1!='=' and temp1!='?':
                        raise ValueError("Error condition")
                    
                        # if (j == input2 + 1):
                        #     try:
                        #         if (eval(temp1) == 0):
                        #             conditions[i][j]=eval(temp1)
                        #     except:
                        #         print("j = ",j)
                        #         messagebox.showerror("Thông báo", "conditions is incorrect0")
                        #         break
                        # else:
                        #     conditions[i][j]=eval(temp1)
        except:
            messagebox.showerror("Thông báo", "Conditions is incorrect")
            return
            
        print("condition1111 = ",conditions)


        objective_origin, constraint_origin, condition_origin=objectives.copy(), constraints.copy(), conditions.copy()
        # print("conditions_or = ", condition_origin)
        objectives, constraints, conditions = utils.check_condition(objectives, constraints, conditions)
        objectives, constraints, conditions = utils.check_constraint(objectives, constraints, conditions)
        objectives, constraints, conditions = utils.check_objective(objectives, constraints, conditions)
        A, b, c = utils.convert(objectives, constraints, conditions)

  
        check_x = utils.vec_check(condition_origin)
        print(check_x)
        print(A, b, c)
        
        z, solution,status = utils.find_proper_algorithm(A, b, c,check_x)
        print("solution111 = ",solution, "; type(solution)= ",type(solution))
        z, solution,status =utils.origin_solution(objective_origin, constraint_origin, condition_origin, conditions, z, solution, status,check_x)

        z_entry.insert(0, str(z))
        print("solution = ",solution, "; type(solution)= ",type(solution))
        # print("input2 = ", input2)


        for i in range (input2):
            if np.array_equal(solution, None):
                solution_entry[0][i].insert(i+1, "None")
            else:
                solution_entry[0][i].insert(i+1,  str(solution[i]))
        status_entry.insert(0, str(status))
       



    x = tk.Label(window2,text="")
    x.grid(row=n+n2+1+flag, column=0)
    flag=flag+1
    calculate_button = tk.Button(window2, text="Calculate",font=30, command=calculate)
    calculate_button.grid(row=n+n2+1+flag, column=0, padx=0, pady=0,sticky=S, columnspan=10)
    flag=flag+1
    x = tk.Label(window2,text="")
    x.grid(row=n+n2+1+flag, column=0)
    
    # Tạo một nút tính toán
    


    z_label = tk.Label(window2, text="Z", font=30)
    z_label.grid(row=n+n2+2+flag, column=0, sticky=E+W)

    z_entry = tk.Entry(window2,  font=30,width=5)
    z_entry.grid(row=n+n2+2+flag, column=1, columnspan=5,sticky=E+W)

    solution_label=np.zeros([1,input2],dtype=object)
    solution_entry=np.zeros([1,input2],dtype=object)
    solution_label[0][0] = tk.Label(window2, text="solution", font=30)
    solution_label[0][0].grid(row=n+n2+3+flag, column=0,sticky=E+W)
    for i in range (input2):

        solution_label[0][i] = tk.Label(window2, text='  '+X+str(i+1)+' =', font=30)
        solution_label[0][i].grid(row=n+n2+3+flag+1, column=2*i, sticky=N+E+S+W)

        solution_entry[0][i] = tk.Entry(window2, font=30,width=5)
        solution_entry[0][i].grid(row=n+n2+3+flag+1, column=2*i+1,sticky=N+E+S+W)

    status_label = tk.Label(window2, text="Status", font=30)
    status_label.grid(row=n+n2+4+flag+1, column=0, sticky=N+S)

    status_entry = tk.Entry(window2, font=30,width=48)
    status_entry.grid(row=n+n2+4+flag+1, column=1, columnspan=10)

    window2.mainloop()

window.mainloop()

   

