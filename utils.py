import numpy as np
import pandas as pd
from fractions import Fraction

def vec_check(condition_origin):
    check_x =[]
    for i in range(len(condition_origin)):
        if condition_origin[:,-2][i]=='?':
            check_x.append(i)
            check_x.append(i)
        else:
            check_x.append(i) 
    return check_x

def check_condition(objective, constraint, condition):
    
    condition2=condition
    flag1=0
    flag2=0
    flag3=0
    for i in range(condition2.shape[0]):
        for j in range(condition2.shape[1]):
            if np.diag(condition2)[i] == 1:
                if condition2[i][j] == '<='and condition2[:,-1][i] == 0  :
                    objective[:,i+1+flag2] = objective[:,i+1+flag2]*-1
                    constraint[:,i+flag2]=constraint[:,i+flag2]*-1
                    condition[i][j] = '>='
                    flag1=flag1+1
                elif condition2[i][j] == '>='and condition2[:,-1][i] == 0  :
                    flag3=flag3+1
                elif condition[:,-1][i] != 0 :
                    temp_objective=pd.DataFrame(objective)
                    newcol=np.vstack([temp_objective.iloc[:,2*i+1-flag1-flag3],temp_objective.iloc[:,2*i+1-flag1-flag3]*-1])
                    temp_objective.insert(2*i+1-flag1-flag3,None,newcol[0].T)
                    temp_objective.insert(2*i+2-flag1-flag3,None,newcol[1].T)
                    temp_objective.drop(labels=2*i+1-flag1-flag3,axis=1,inplace=True)
                    objective=temp_objective
                    objective=temp_objective.values
                    
                    temp_constraint=pd.DataFrame(constraint)
                    newrow=np.zeros(temp_constraint.shape[1],dtype=np.object)
                    newrow[i-flag1-flag3:]=condition2[i,:]                    
                    temp_constraint.loc[temp_constraint.shape[0]+1]=newrow
                    #constraint= np.vstack([constraint, newrow])
                    newcol=np.vstack([temp_constraint.iloc[:,2*i-flag1-flag3],temp_constraint.iloc[:,2*i-flag1-flag3]*-1])
                    temp_constraint.insert(2*i-flag1-flag3,None,newcol[0].T)
                    temp_constraint.insert(2*i+1-flag1-flag3,None,newcol[1].T)
                    temp_constraint.drop(labels=2*i-flag1-flag3,axis=1,inplace=True)
                    constraint=temp_constraint.values
                    
                    
                    newcol=np.zeros(condition.shape[0],dtype=np.object)
                    newrow=np.zeros(condition.shape[1]+1,dtype=np.object)
                    temp_condition=pd.DataFrame(condition)
                    temp_condition.insert(condition.shape[1]-2,None,newcol.T)
                    temp_condition.loc[condition.shape[0]]=newrow
                    temp_condition.iloc[-1,condition.shape[1]-1]='>='
                    temp_condition.iloc[-1,condition.shape[1]-2]=1
                    temp_condition.iloc[i,condition.shape[1]]=0
                    temp_condition.iloc[i,condition.shape[1]-1]='>='
                    condition = np.array(temp_condition)
                    
                    flag2=flag2+1
                elif condition2[i][j] == '?'and condition2[:,-1][i] == 0:
                    temp_objective=pd.DataFrame(objective)
                    newcol=np.vstack([temp_objective.iloc[:,2*i+1-flag1-flag3],temp_objective.iloc[:,2*i+1-flag1-flag3]*-1])
                    temp_objective.insert(2*i+1-flag1-flag3,None,newcol[0].T)
                    temp_objective.insert(2*i+2-flag1-flag3,None,newcol[1].T)
                    temp_objective.drop(labels=2*i+1-flag1-flag3,axis=1,inplace=True)
                    objective=temp_objective
                    objective=temp_objective.values
                    
                    temp_constraint=pd.DataFrame(constraint)
                    
                    #constraint= np.vstack([constraint, newrow])
                    newcol=np.vstack([temp_constraint.iloc[:,2*i-flag1-flag3],temp_constraint.iloc[:,2*i-flag1-flag3]*-1])
                    temp_constraint.insert(2*i-flag1-flag3,None,newcol[0].T)
                    temp_constraint.insert(2*i+1-flag1-flag3,None,newcol[1].T)
                    temp_constraint.drop(labels=2*i-flag1-flag3,axis=1,inplace=True)
                    constraint=temp_constraint.values
                    
                    
                    newcol=np.zeros(condition.shape[0],dtype=np.object)
                    newrow=np.zeros(condition.shape[1]+1,dtype=np.object)
                    temp_condition=pd.DataFrame(condition)
                    temp_condition.insert(condition.shape[1]-2,None,newcol.T)
                    temp_condition.loc[condition.shape[0]]=newrow
                    temp_condition.iloc[-1,condition.shape[1]-1]='>='
                    temp_condition.iloc[-1,condition.shape[1]-2]=1
                    temp_condition.iloc[i,condition.shape[1]]=0
                    temp_condition.iloc[i,condition.shape[1]-1]='>='
                    condition = np.array(temp_condition)
                    
                    flag2=flag2+1
                
    return objective,constraint,condition

def check_constraint(objective, constraint, condition):
    constraint2=constraint
    k=constraint.shape[1]-2
    flag=0
    for i in range(constraint2.shape[0]):
        if constraint[i-flag][k] == ">=":
            constraint[i-flag,:]=constraint[i-flag,:]*-1
            constraint[i-flag][k] = "<="
            
        if constraint2[:,k][i] == "=":
            newrow=np.vstack([constraint[i-flag],constraint[i-flag]*-1])
            newrow[0][k]='<='
            newrow[1][k]='<='
            temp_constraint=pd.DataFrame(constraint)
            #temp_constraint = temp_constraint.drop(labels=i, axis=0)
            temp_constraint.loc[temp_constraint.shape[0]+1]=newrow[0]
            temp_constraint.loc[temp_constraint.shape[0]+2]=newrow[1]
            temp_constraint = temp_constraint.drop(labels=i-flag, axis=0)
            flag=flag+1
                    
            constraint=temp_constraint.values
    return objective,constraint,condition

def check_objective(objective, constraint, condition):
    if objective[0][0]=='max':
        objective=objective*-1
        objective[0][0]='min'
        print("1objectives = ",objective)
        print("1constraints = ",constraint)
        print("1conditions = ",condition)        
    return objective, constraint, condition



# A: ma trận chứa hệ của của các biến trong các ràng buộc
# b: mảng chứa các giá trị bi
# c: mảng chứa hệ số các biến trong hàm mục tiêu

def get_solution(z,c_n,T,basis,b_n,check_x,m,n):

    #Xây dựng hàm lấy kết quả
    c_n = np.round(c_n,3)
    z = round(z,3)
    
    #Thiết lập solu là một ma trận có chiều là (số biến * số biến + 1 (tính cả b đứng đầu))
    solu = np.zeros((len(c_n),len(c_n)+1))
    #Thiết lập ma trận T với các vị trí của biến cơ sở = 0
    for i in range(len(basis)):
        T[i,int(basis[i])] = 0
    #Lấy vị trí của các biến không có trên hàm mục tiêu
    solu_temp = []
    free = []
    
    for i in range(len(c_n)):
        if(c_n[i]==0):
            solu_temp.append(i)
    
    #Lấy biến tự do
    for i in range(len(solu_temp)):
        if solu_temp[i] in basis:
            continue
        else:
            free.append(solu_temp[i])

    #Xây dựng ma trận để xét các nghiệm tối ưu
    for i in range(m):
        for j in range(len(solu_temp)):
            if(T[i,solu_temp[j]]!=0):
                solu[int(basis[i]),solu_temp[j]+1] = -T[i,solu_temp[j]]
        solu[int(basis[i]),0] = b_n[i]


    x = [0]*n
    #Trường hợp có nghiệm duy nhất

    for i in range(len(check_x)):
        if (solu[i,1:] != np.zeros(len(solu))).any():
            x[i] = solu[i,:].tolist()
        else:
            x[i] = round(solu[i,0],3)

    #Trường hợp có nghiệm duy nhất nhưng các biến được chuyển đổi từ các biến tự do
    status = "Only solution."
    for i in range(len(x)):
        if(type(x[i])!= np.float64):
            for j in range(len(check_x)):
                if(check_x[j]==check_x[i] and i!=j):
                    x[i][j+1] = 0
    
    #Trường hợp có vô số nghiệm
    for i in range(len(check_x)):
        if(type(x[i])!= np.float64):
            
            # print("x[i]= ",x[i])
            if(x[i][1:] != [0]*len(solu)):
                status = "Infinitive solution."
                continue
            else:
                x[i] = round(x[i][0],3)
    
    # print("x_final = ",x)
    return z, x, status

def leaving_index(c):
    for i, c_i in enumerate(c):
        if c_i < 0:
            return i
    return None

def bland_method(A, b, c,check_x):
    b = b.astype(np.float64)
    m, n = A.shape

    # Khởi tạo biến giá trị tối ưu
    z = 0 
    status = "" #Biến chứa trạng thái bài toán
    # Tính ma trận bổ sung
    T = np.hstack((A, np.eye(m)))
    c_n = np.concatenate((c, np.zeros(m)))
    b_n = b.copy()
    
    # Copy biến ban đầu để so sánh
    A_cop = T.copy()
    c_cop = c_n.copy()
    b_cop = b.copy()
    
    # Tính biến cơ sở ban đầu
    basis = list(range(n, n + m))
    # Chuyển về dạng chuẩn tắc
    while True:
        
        # Tìm biến vào
        j = leaving_index(c_n)
        if j == None:
            break
            
        # Tìm biến ra
        ratios = [float('inf')] * m
        for i in range(m):
            if T[i, j] > 0:
                ratios[i] = b_n[i] / T[i, j]
        
        i = np.argmin(ratios)

        # Kiểm tra bài toán không giới nội
        if ratios[i] == float('inf'):
            status = "Unbounded."
            return -np.inf, None, status
        
        # Tính giá trị tối ưu
        z += c_n[j] / T[i, j] * b_n[i]
    
        # Cập nhật ma trận
        basis[i] = j
        
        for k in range(m):
            if k != i:
                b_n[k] -= T[k, j]/T[i,j] * b_n[i]
                T[k, :] -=  T[k, j] / T[i,j] * T[i, :]
        
        b_n[i] /= T[i, j]
        T[i, :] /= T[i, j]       
        c_n -= c_n[j] * T[i, :]
        
        # Kiểm tra thuật toán có hoàn thành hay không 
        # Nếu Từ vựng mới trùng với từ vựng ban đầu thì dừng thuật toán
        if (c_n == c_cop).all() and (T == A_cop).all() and (b_n == b_cop).all():
            status = "Infinite repeat."
            return None, None, status

    z,x1,status = get_solution(z,c_n,T,basis,b_n,check_x,m,n)

                           
    return z, x1, status 




def dantzig_method(A, b, c,check_x):
    b = b.astype(np.float64)
    m, n = A.shape

    # Khởi tạo biến giá trị tối ưu
    z = 0 
    status = "" # Biến chứa trạng thái bài toán
    # Tính ma trận bổ sung
    T = np.hstack((A, np.eye(m)))
    c_n = np.concatenate((c, np.zeros(m)))
    b_n = b.copy()
    
    # Copy biến ban đầu để so sánh
    A_cop = T.copy()
    c_cop = c_n.copy()
    b_cop = b.copy()
    
    # Tính biến cơ sở ban đầu
    basis = list(range(n, n + m))
    # Chuyển về dạng chuẩn tắc
    while True:
        # Tìm biến vào
        j = np.argmin(c_n)
        
        if c_n[j] >= 0:
            break
            
        # Tìm biến ra
        ratios = [float('inf')] * m
        for i in range(m):
            if T[i, j] > 0:
                ratios[i] = b_n[i] / T[i, j]
        
        i = np.argmin(ratios)

        # Kiểm tra bài toán không giới nội
        if ratios[i] == float('inf'):
            status = "Unbounded."
            return -np.inf, None, status
        
        # Tính giá trị tối ưu
        z += c_n[j] / T[i, j] * b_n[i]
        # Cập nhật ma trận
        basis[i] = j
        
        for k in range(m):
            if k != i:
                b_n[k] -= T[k, j]/T[i,j] * b_n[i]
                T[k, :] -=  T[k, j] / T[i,j] * T[i, :]
        
        b_n[i] /= T[i, j]
        T[i, :] /= T[i, j]       
        c_n -= c_n[j] * T[i, :]
        # Kiểm tra thuật toán có hoàn thành hay không 
        # Nếu Từ vựng mới trùng với từ vựng ban đầu thì dừng thuật toán
        if (c_n == c_cop).all() and (T == A_cop).all() and (b_n == b_cop).all():
            status = "Infinite repeat."
            return None, None, status

    z,x,status = get_solution(z,c_n,T,basis,b_n, check_x,m,n)
                           
    return z, x, status

def check_phase1(b_n_o, T_o, c1_o, basis_o, ratios_o,i,j,m,c_cop,A_cop,b_cop,z_o):
    status = ""
    # print("Đã vào vòng lặp mới")
    b_n = b_n_o.copy()
    T = T_o.copy()
    c1 = c1_o.copy()
    basis = basis_o.copy()
    ratios = ratios_o.copy()
    z = z_o.copy()
    
    while(True):
    # Kiểm tra bài toán không giới nội hoặc từ vựng tối ưu
        if ratios[i] == float('inf'):
            status = "Unbounded."
            return z,b_n, T, c1, basis, status

        # Tính giá trị tối ưu
        z += c1[j] / T[i, j] * b_n[i]
        # Cập nhật ma trận
        basis[i] = j

        for k in range(m):
            if k != i:
                b_n[k] -= T[k, j]/T[i,j] * b_n[i]
                T[k, :] -=  T[k, j] / T[i,j] * T[i, :]

        b_n[i] /= T[i, j]
        T[i, :] /= T[i, j]       
        c1 -= c1[j] * T[i, :]
        # Kiểm tra thuật toán có hoàn thành hay không 
        # Nếu Từ vựng mới trùng với từ vựng ban đầu thì dừng thuật toán
        if (c1 == c_cop).all() and (T == A_cop).all() and (b_n == b_cop).all():
            status = "Infinite repeat."
            return z,b_n, T, c1, basis, status
        j = np.argmin(c1)
        if c1[j] >= 0:
            break

    #Kiểm tra bài toán có nghiệm khi hoàn thành phase 1
    if np.array_equal(c1,c_cop) == False:
        status = "No solution."
    if (status == "No solution."):
        return z_o,b_n_o,T_o,c1_o,basis_o,status
    return z,b_n, T, c1, basis, status
def two_phases(A,b,c,check_x):
    b = b.astype(np.float64)
    m, n = A.shape
    # Khởi tạo biến giá trị tối ưu
    z = 0
    status = ""
    # Tính ma trận bổ sung có chứa x0
    c1 = np.concatenate((np.ones(1), np.zeros(m+n)))
    new_col = (-1*np.ones(m)).reshape(-1, 1)
    T = np.hstack((new_col,np.hstack((A, np.eye(m)))))
    b_n = b.copy()

    # Copy biến ban đầu để so sánh
    A_cop = T.copy()
    c_cop = c1.copy()
    b_cop = b.copy()

    # Tính biến cơ sở ban đầu
    basis = list(range(n+1, n + m+1))

    #Chọn biến vào
    j = 0
    #Tìm biến ra
    i = np.argmin(b_n)

    
    # Tính giá trị tối ưu
    z += c1[j] / T[i, j] * b_n[i]
    # Cập nhật ma trận
    basis[i] = j
    
    for k in range(m):
        if k != i:
            b_n[k] -= T[k, j]/T[i,j] * b_n[i]
            T[k, :] -=  T[k, j] / T[i,j] * T[i, :]
    
    b_n[i] /= T[i, j]
    T[i, :] /= T[i, j]       
    c1 -= c1[j] * T[i, :]

    #phase 1
    #Thử trường hợp phase 1 là bland
    while True:
        # Tìm biến vào
        j = np.argmin(c1)
        if c1[j] >= 0:
            break
            
        # Tìm biến ra
        ratios = [float('inf')] * m
        for i in range(m):
            if T[i, j] > 0:
                ratios[i] = b_n[i] / T[i, j]
        
        i = np.argmin(ratios)
        i_out = []
        for it in range(m):
            if (ratios[it] == b_n[i] / T[i, j]):
                i_out.append(it)

        # Tìm biến ra phù hợp
        if (len(i_out) > 1):
            for it in range(len(i_out)):
                i = i_out[it]
                z, b_n, T, c1, basis, status = check_phase1(b_n,T, c1,basis,ratios,i,j,m,c_cop,A_cop,b_cop,z)
                if status != "No solution.":
                    i = i_out[it]
                    break

        # Kiểm tra bài toán không giới nội hoặc từ vựng tối ưu
        if ratios[i] == float('inf'):
            status = "Unbounded."
            return -np.inf, None, status
        
        # Tính giá trị tối ưu
        z += c1[j] / T[i, j] * b_n[i]
        # Cập nhật ma trận
        basis[i] = j
        
        for k in range(m):
            if k != i:
                b_n[k] -= T[k, j]/T[i,j] * b_n[i]
                T[k, :] -=  T[k, j] / T[i,j] * T[i, :]
        
        b_n[i] /= T[i, j]
        T[i, :] /= T[i, j]       
        c1 -= c1[j] * T[i, :]
        # Kiểm tra thuật toán có hoàn thành hay không 
        # Nếu Từ vựng mới trùng với từ vựng ban đầu thì dừng thuật toán
        if (c1 == c_cop).all() and (T == A_cop).all() and (b_n == b_cop).all():

            status = "Infinite repeat."
            return None, None, status
        
    #Kiểm tra bài toán có nghiệm khi hoàn thành phase 1
    if np.array_equal(c1,c_cop) == False:
        status = "No solution."
        return None, None, status
    
    #Thiết lập hàm mục tiêu cho phase 2
    c_n = np.zeros(m+n) # trường hợp các biến trên hàm mục tiêu không đủ
    s = len(c_n)-len(c)
    c_temp = np.concatenate((c,np.zeros(s)))
    c_n +=c_temp
    #loại bỏ x0
    T = T[:, 1:]
    T_z = T.copy()
    for i in range(m):
        if basis[i] <= n:
            T_z[i,basis[i]-1] = 0 # làm mất biến thay vào khi thêm vào hàm mục tiêu
            c_n[basis[i]-1] = 0
            c_n -= c[basis[i]-1] * T_z[i,:] #vì basis có tính 0
            z += c[basis[i]-1] * b_n[i]
    # #Cập nhật giá trị z cho phase 2
    #Cập nhật lại basis
    basis -= np.ones(len(basis))
    #phase 2
    while True:
        b_n_st = b_n.copy
        T_st = T.copy
        c_n_st = c1.copy
        basis_st = basis.copy
        # Tìm biến vào
        j = np.argmin(c_n)
        
        if c_n[j] >= 0:
            break
            
        # Tìm biến ra
        ratios = [float('inf')] * m
        for i in range(m):
            if T[i, j] > 0:
                ratios[i] = b_n[i] / T[i, j]
        
        i = np.argmin(ratios)

        # Kiểm tra bài toán không giới nội
        if ratios[i] == float('inf'):
            status = "Unbounded."
            return -np.inf, None, status
        
        # Tính giá trị tối ưu
        z += c_n[j] / T[i, j] * b_n[i]
        
        # Cập nhật ma trận
        basis[i] = j
        
        for k in range(m):
            if k != i:
                b_n[k] -= (T[k, j]/T[i,j]) * b_n[i]
                T[k, :] -=  T[k, j] / T[i,j] * T[i, :]
        
        b_n[i] /= T[i, j]
        T[i, :] /= T[i, j]
        c_n -= c_n[j] * T[i, :]
        # Kiểm tra thuật toán có hoàn thành hay không 
        # Nếu Từ vựng mới trùng với từ vựng ban đầu thì dừng thuật toán
        if np.array_equal(c_n, c_cop) and np.array_equal(T, A_cop) and np.array_equal(b_n, b_cop):
            status = "Infinite repeat."
            x_b, z_b, status_b = bland_method(T_st,b_n_st,c_n_st)
            if (x_b == None and z == None):
                status = "No solution."
                return None, None, status
            return x_b,z_b,status

   
    z, x, status = get_solution(z,c_n,T,basis,b_n,check_x,m,n)
         
    return z, x, status 



def convert(objective, constraint, condition):
    print('objective = ',objective)
    c = objective[:,1:]
    print("c = ",c)
    c = c.flatten()
    print("c = ", c,"; type(c) = ",type(c))
    c = c.astype(np.float64)
    
    b = constraint[:, -1]
    b = b.astype(np.float64)
    
    A = np.delete(constraint, [-1,-2], axis = 1)
    A = A.astype(np.float64)
    return A, b, c

# Hàm chọn thuật toán phù hợp
def find_proper_algorithm(A, b, c,check_x):
    if np.any(b == 0):
        print("1")
        z, x, status = bland_method(A, b, c,check_x)
    elif np.any(b < 0):
        print("2")
        z, x, status = two_phases(A, b, c,check_x)
    else:
        print("3")
        z, x, status = dantzig_method(A, b, c,check_x)
    return z, x, status

# Hàm trả về kết quả của bài toán QHTT ban đầu
def origin_solution(objective_origin, constraint_origin, condition_origin,condition, z, x, status,check_x):
    if z == None:
        return z, x, status
    x_origin = np.zeros(constraint_origin.shape[1]-2,dtype=object)

    if objective_origin[0][0] == 'max':
        z = -z
    else:
        z = z

    if x is not None:
        m = condition.shape[0]
        i = 0
        k = 0
        while i < m:
            
            j = i + 1
            #if np.float64
            if condition_origin[:,-2][k]=='?':
                #Trường hợp nghiệm tự do có vô số nghiệm
                print("type(x[i]) = ",type(x[i]),"; type(x[i+1]) = ",type(x[i+1]),"; i = ",i)
                if((type(x[i])!= float and type(x[i]) != np.float64) or ( type(x[i+1])!= float and type(x[i+1])!= np.float64)):
                    # for j in range(len(check_x)):
                    #     if(check_x[j]==check_x[i] and i!=j):
                    #         x[i][j+1] = 0
                    if(type(x[i])!= float and type(x[i])!= np.float64 ):
                        print("000type(x[i]) = ",type(x[i]),"; x[i] = ",x[i],"; i = ",i)
                        x[k] = str(round(x[i][0],3))
                    else:
                        print("111type(x[i+1]) = ",type(x[i+1]),"; x[i+1] = ",x[i+1],"; i = ",i)
                        x[k] = str(round(-x[i][0],3))
                    if(x[i][1:] != [0]*(len(x[i])-1)):
                        for j in range(1,len(x[i])):
                            if(x[i][j]!=0):
                                x[k] += "+"
                                x[k] += str(round(x[i][j],3))+"*t{{{}}}".format(j-1)
                    i+=2
                else:
                    x_origin[k] = round((x[i]-x[j]),3)
                    i += 2
            elif condition_origin[:,-2][k]=='<=':
                #Trường hợp nghiệm có điều kiện <= và vô số nghiệm
                if(type(x[i])!= float and type(x[i])!= np.float64):
                    x_origin[k] = str((-x[i][0]))
                    if(x[i][1:] != [0]*(len(x[i])-1)):
                        for j in range(1,len(x[i])):
                            if(x[i][j]!=0):
                                x_origin[k] += "+"
                                x_origin[k] += str(round(x[i][j],3))+"*t{{{}}}".format(j-1)
                    i+=1
                else:
                    x_origin[k] = -round(x[i],3)
                    i += 1
            elif condition_origin[:,-2][k]=='>=':
                #Trường hợp nghiệm có điều kiện >= và vô số nghiệm
                if(type(x[i])!= float and type(x[i])!= np.float64):
                    x_origin[k] = str(round(x[i][0],3))
                    if(x[i][1:] != [0]*(len(x[i])-1)):
                        for j in range(1,len(x[i])):
                            if(x[i][j]!=0):
                                print("x[i][j] = ",x[i][j])
                                x_origin[k] += "+"
                                x_origin[k] += str(round(x[i][j],3))+"*t{{{}}}".format(j-1)
                    i+=1
                else:
                    x_origin[k] = round(x[i],3)
                    i += 1
            #else
            #Trường hợp vô số nghiệm
            k += 1
        
        return z, x_origin, status

    else:
        x_origin = x
                
    return z, x_origin, status