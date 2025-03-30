from tkinter import Tk,Label,Frame,Entry,Button,messagebox,simpledialog,filedialog
from tkinter.ttk import Combobox
import time
from PIL import Image,ImageTk
import autotable_creation
import random
import sqlite3
import gmail
from tkintertable import TableCanvas,TableModel 
import re


win=Tk()      #window created
win.title("My Project")
win.state("zoomed")
win.resizable(width=False,height=False)  
win.configure(bg="powder blue")

# first pass parent'win' & bg is here to match the window color 
header_title=Label(win,text="Banking Automation",font=('arial',50,'bold','underline'),bg='powder blue')  
header_title.pack()      #window text at top center

current_date=time.strftime('%d-%b-%y')
header_date=Label(win,text=current_date,font=('arial',20,'bold'),bg='powder blue',fg='blue')
header_date.pack(pady=10)    #pady used for lowerdown the text

footer_title=Label(win,text="By:Prashant Yadav\nEmail:Prashant16doc@gmail.com",font=('arial',25,'bold','underline'),bg=('powder blue'))
footer_title.pack(side='bottom')

Image
img=Image.open('D:\\SQL 2024\\logo.jpg').resize((250,150))
bitmap_image=ImageTk.PhotoImage(img,master=win)  #convert into bitmap bcz of Tk,widget
logo_label=Label(win,image=bitmap_image)
logo_label.place(relx=0,rely=0)


def main_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)   #second small window
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.75)
    
    def reset():
        acn_entry.delete(0,'end')
        pass_entry.delete(0,'end')
        acn_entry.focus()
    
    def login_click():
        global uacn
        uacn=acn_entry.get()  #get is used to retrieved text from user
        upass=pass_entry.get()
        urole=role_cb.get()

        if len(uacn)==0 or len(uacn)==0:
            messagebox.showerror('login',"ACN or PASS can't be empty")
            return
        uacn=int(uacn) 

        if uacn==0 and upass=='admin' and urole=='Admin':
            frm.destroy()
            welcome_admin_screen()
        
        elif urole=='User':
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select * from users where users_acno=? and users_pass=?',(uacn,upass))
            tup=cur_obj.fetchone()
            if tup==None:
                messagebox.showerror('login','invalid ACN/PASS')
            else:
                global uname
                uname=tup[2]
                frm.destroy()
                welcome_user_screen()
           # messagebox.showerror('login','Invalid ACN/PASS') #first agr for name of box 
        else:
            messagebox.showerror('login','invalid user')
            

    #account
    acn_label=Label(frm,font=('arial',20,'bold'),text='ACCOUNT NO.',bg='pink')
    acn_label.place(relx=.25,rely=.1)
    acn_entry=Entry(frm,font=('arial',20,'bold'),bd=5) # bd is border
    acn_entry.place(relx=.4,rely=.1)
    acn_entry.focus()  #for the cursor
    #passowrd
    pass_label=Label(frm,font=('arial',20,'bold'),text='PASSword',bg='pink')
    pass_label.place(relx=.25,rely=.2)
    pass_entry=Entry(frm,font=('arial',20,'bold'),bd=5,show='*') # bd is border
    pass_entry.place(relx=.4,rely=.2)
    #role
    role_label=Label(frm,font=('arial',20,'bold'),text='Role',bg='pink')
    role_label.place(relx=.25,rely=.3)
    role_cb=Combobox(frm,font=('arial',20,'bold'),values=['User','Admin'])
    role_cb.current(0)   #indexing of value 
    role_cb.place(relx=.4,rely=.3)
    #button
    login_btn=Button(frm,text='Login',font=('arial',20,'bold'),bg='powder blue',bd=5,command=login_click)
    login_btn.place(relx=.4,rely=.42)
    
    reset_btn=Button(frm,text='Reset',command=reset,font=('arial',20,'bold'),bg='powder blue',bd=5)
    reset_btn.place(relx=.52,rely=.42)

    forgot_btn=Button(frm,width=16,text='Forgot Password',font=('arial',20,'bold'),bg='powder blue',bd=5,command=forgot_password_screen)
    forgot_btn.place(relx=.4,rely=.55)

#admin login window
def welcome_admin_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)   #second small window
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.75)

    def logout_click():
        resp=messagebox.askyesno('logout','Do you want to logout,Kindly confirm?')
        if resp:
            frm.destroy()
            main_screen()


    def create_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.05,relwidth=.6,relheight=.6)
            
            
        # insert into sqlite tables 
        def open_acn():
            uname=name_entry.get()
            umob=mob_entry.get()
            uemail=email_entry.get()
            uadhar=adhar_entry.get()
            uadd=add_entry.get()
            ubal=0
            upass=str(random.randint(100000,999999))

            if len(uname)==0 or len(umob)==0 or len(uemail)==0 or len(uadhar)==0:
                messagebox.showerror('create','Empty Fields are not allowed')
                return
            
            if not re.fullmatch('[a-zA-Z]+',uname):
                messagebox.showerror('create','Kindly enter the vaild Name')
                return
            
            if not re.fullmatch('[6-9][0-9]{9}',umob):
                messagebox.showerror('create','Kindly enter the vaild Mob number')
                return

            if not re.fullmatch('[a-z0-9_.]+@[a-z]+[.][a-z]+',uemail):
                messagebox.showerror('create','Kindly enter the vaild Email')
                return
            
            if not re.fullmatch('[0-9]{12}',uadhar):
                messagebox.showerror('create','Kindly enter the vaild Adhar')
                return
            
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('insert into users(users_pass,users_name,users_mob,users_add,users_email,users_bal,users_adhar,users_opendate) values(?,?,?,?,?,?,?,?)',(upass,uname,umob,uadd,uemail,ubal,uadhar,current_date))
            con_obj.commit()
            con_obj.close()
            #send acn no. through gmail
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select max(users_acno)from users')
            tup=cur_obj.fetchone()
            uacn=tup[0]
            con_obj.close()

            #gmail
            try:
                gmail_con=gmail.GMail('pyadav1672002@gmail.com','zncx tihq sbel eyxk')
                umsg=f'''Hello,{uname}
                Welcome to ABC bank 
                Your ACN is :{uacn}
                Your pass is :{upass}
                Kindly change your password when you login first time
                thanks'''
                msg=gmail.Message(to=uemail,subject='Account',text=umsg)
                gmail_con.send(msg)
                messagebox.showinfo('open acn','account created and kindly check your email for acn/pass')
            except Exception as e:
                print(e)
                messagebox.showerror('open acn','something went wrong')      

        #inner frame title
        title_ifrm=Label(ifrm,font=('arial',15,'bold'),text='This is create user screen',bg='white',fg='purple')
        title_ifrm.pack()

         #name label and entry
        name_label=Label(ifrm,font=('arial',15,'bold'),text='Name',bg='white',fg='black')
        name_label.place(relx=.05,rely=.2)
        name_entry=Entry(ifrm,font=('arial',20,),bd=5,bg='white') # bd is border
        name_entry.place(relx=.05,rely=.27)
        name_entry.focus()
        #mob label and entry
        mob_label=Label(ifrm,font=('arial',15,'bold'),text='MOB',bg='white',fg='black')
        mob_label.place(relx=.05,rely=.4)
        mob_entry=Entry(ifrm,font=('arial',20,),bd=5,bg='white') # bd is border
        mob_entry.place(relx=.05,rely=.47)
        #email label adn entry
        email_label=Label(ifrm,font=('arial',15,'bold'),text='Email',bg='white',fg='black')
        email_label.place(relx=.5,rely=.2)
        email_entry=Entry(ifrm,font=('arial',20,),bd=5,bg='white') # bd is border
        email_entry.place(relx=.5,rely=.27)
        #adhar label and entry
        adhar_label=Label(ifrm,font=('arial',15,'bold'),text='Adhar',bg='white',fg='black')
        adhar_label.place(relx=.5,rely=.4)
        adhar_entry=Entry(ifrm,font=('arial',20,),bd=5,bg='white') # bd is border
        adhar_entry.place(relx=.5,rely=.47)
        #address label and entry
        add_label=Label(ifrm,font=('arial',15,'bold'),text='Address',bg='white',fg='black')
        add_label.place(relx=.05,rely=.6)
        add_entry=Entry(ifrm,font=('arial',20,),bd=5,bg='white') # bd is border
        add_entry.place(relx=.05,rely=.67)

        #button
        open_btn=Button(ifrm,command=open_acn,text='Open ',font=('arial',20,'bold'),bg='light green',bd=5)
        open_btn.place(relx=.5,rely=.7)
 
        reset_btn=Button(ifrm,text='Reset',font=('arial',20,'bold'),bg='red',bd=5,fg="black")
        reset_btn.place(relx=.65,rely=.7)


    def view_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.05,relwidth=.6,relheight=.6)
        
        #inner frame title
        title_ifrm=Label(ifrm,font=('arial',15,'bold'),text='This is view user screen',bg='white',fg='purple')
        title_ifrm.pack()

         #transaction table
        data={}
        conobj=sqlite3.connect("bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select * from users")
        tups=curobj.fetchall()
        i=1
        for tup in tups:
            data[str(i)]={'Acno':tup[0],'Balance':tup[6],'Adhar':tup[7],'Opendate':tup[8],'Email':tup[3],'Mob':tup[5]}
            i+=1
        model = TableModel()
        model.importDict(data)

        table_frm=Frame(ifrm)
        table_frm.place(relx=.1,rely=.1,relwidth=7)

        table = TableCanvas(table_frm, model=model,editable=False)
        table.show()

        

    def delete_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.05,relwidth=.6,relheight=.6)
        
        #inner frame title
        title_ifrm=Label(ifrm,font=('arial',15,'bold'),text='This is delete user screen',bg='white',fg='purple')
        title_ifrm.pack()

        def delete_db():
            uacn=acn_entry.get()
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('delete from users where users_acno=?',(uacn,))
            cur_obj.execute('delete from txn where txn_acno=?',(uacn,))
            con_obj.commit()
            con_obj.close()
            messagebox.showinfo('Delete',f'user with Acn {uacn} deleted') 

        
        #account label and entry
        acn_label=Label(ifrm,font=('arial',15,'bold'),text='Account No.',bg='white',fg='black')
        acn_label.place(relx=.2,rely=.3)
        acn_entry=Entry(ifrm,font=('arial',20,),bd=5,bg='white') # bd is border
        acn_entry.place(relx=.2,rely=.37)
        acn_entry.focus()

        #button
        delete_btn=Button(ifrm,text='Delete',command=delete_db,font=('arial',20,'bold'),bg='red',bd=5,fg="black")
        delete_btn.place(relx=.5,rely=.6)
  
       
    wel_label=Label(frm,font=('arial',20,'bold'),text='WELCOME ADMIN',bg='pink',fg='blue')
    wel_label.place(relx=.0,rely=.0)

    # function is defined before the logout_btn button because the button needs to know what function to execute when clicked    
    logout_btn=Button(frm,command=logout_click,text='Logout',font=('arial',20,'bold'),bg='powder blue',bd=5)
    logout_btn.place(relx=.9,rely=.0)
 
    create_btn=Button(frm,command=create_click,width=12,text='Create User',font=('arial',20,'bold'),bg='green',bd=5,fg="white")
    create_btn.place(relx=.0,rely=.1)

    view_btn=Button(frm,command=view_click,width=12,text='View user',font=('arial',20,'bold'),bg='grey',bd=5,fg="white")
    view_btn.place(relx=.0,rely=.30)

    delete_btn=Button(frm,command=delete_click,width=12,text='Delete User',font=('arial',20,'bold'),bg='powder blue',bd=5,fg="white")
    delete_btn.place(relx=.0,rely=.50)


def forgot_password_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)   
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.75)

    def back_click():
        frm.destroy()
        main_screen()

    def get_password():
        ucan=acn_entry.get()
        uemail=email_entry.get()
        umob=mob_entry.get()
        con_obj=sqlite3.connect(database='bank.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute('select users_name,users_pass from users where users_acno=? and users_email=? and users_mob=?',(ucan,uemail,umob))
        tup=cur_obj.fetchone()
        con_obj.close()
        if tup==None:
            messagebox.showerror('forgot pass','Invlaid Details')
        else:
            try:
                gmail_con=gmail.GMail('pyadav1672002@gmail.com','zncx tihq sbel eyxk')
                umsg=f'''Hello,{tup[0]}
                Welcome to ABC bank 
                Your pass is :{tup[1]}
                thanks'''
                msg=gmail.Message(to=uemail,subject='Account',text=umsg)
                gmail_con.send(msg)
                messagebox.showinfo('forgot password','kindly check your email for pass')
            except Exception as e:
                print(e)
                messagebox.showerror('forgot password','something went wrong')      

    back_btn=Button(frm,command=back_click,text='Back',font=('arial',20,'bold'),bg='powder blue',bd=5)
    back_btn.place(relx=.9,rely=.0)


    #account
    acn_label=Label(frm,font=('arial',20,'bold'),text='ACCOUNT NO.',bg='pink')
    acn_label.place(relx=.25,rely=.1)
    acn_entry=Entry(frm,font=('arial',20,'bold'),bd=5) # bd is border
    acn_entry.place(relx=.4,rely=.1)
    acn_entry.focus()  #for the cursor
    #Email
    email_label=Label(frm,font=('arial',20,'bold'),text='Email',bg='pink')
    email_label.place(relx=.25,rely=.2)
    email_entry=Entry(frm,font=('arial',20,'bold'),bd=5) # bd is border
    email_entry.place(relx=.4,rely=.2)
    #mob
    mob_label=Label(frm,font=('arial',20,'bold'),text='MOb',bg='pink')
    mob_label.place(relx=.25,rely=.3)
    mob_entry=Entry(frm,font=('arial',20,'bold'),bd=5,show='*') # bd is border
    mob_entry.place(relx=.4,rely=.3)

    #button
    submit_btn=Button(frm,command=get_password,text='Submit',font=('arial',20,'bold'),bg='powder blue',bd=5)
    submit_btn.place(relx=.5,rely=.42)
    
#user login window
def welcome_user_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)  
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.75)

    def logout_click():
        resp=messagebox.askyesno('logout','Do you want to logout,Kindly confirm?')
        if resp:
            frm.destroy()
            main_screen()
        

    def check_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.05,relwidth=.6,relheight=.7)
        
        #showing the data
        con_obj=sqlite3.connect(database='bank.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute('select users_bal,users_opendate,users_adhar from users where users_acno=? ',(uacn,))
        tup=cur_obj.fetchone()
        con_obj.close()

        lbl_bal=Label(ifrm,text=f'Available Balance:\t{tup[0]}',font=('arial',18,'bold'),fg='blue',bg='white')
        lbl_bal.place(relx=.2,rely=.2)

        lbl_opendate=Label(ifrm,text=f'Available Balance:\t{tup[1]}',font=('arial',18,'bold'),fg='blue',bg='white')
        lbl_opendate.place(relx=.2,rely=.4)

        lbl_adhar=Label(ifrm,text=f'Available Balance:\t{tup[2]}',font=('arial',18,'bold'),fg='blue',bg='white')
        lbl_adhar.place(relx=.2,rely=.6)


        #inner frame title
        title_ifrm=Label(ifrm,font=('arial',15,'bold'),text='This is Check Balance screen',bg='white',fg='purple')
        title_ifrm.pack()

    def update_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.05,relwidth=.6,relheight=.7)
        
        #inner frame title
        title_ifrm=Label(ifrm,font=('arial',15,'bold'),text='This is Update screen',bg='white',fg='purple')
        title_ifrm.pack()

        #update the user details
        def update_details():
            uname=name_entry.get()
            umob=mob_entry.get()
            uemail=email_entry.get()
            upass=pass_entry.get()
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('update users set users_name=?,users_pass=?,users_email=?,users_mob=? where users_acno=?',(uname,upass,uemail,umob,uacn))
            con_obj.commit()
            con_obj.close()
            messagebox.showinfo('update','deatils updated')


        #show the details of the user for update
        con_obj=sqlite3.connect(database='bank.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute('select * from users where users_acno=?',(uacn,))
        tup=cur_obj.fetchone()
        con_obj.close()

         #name label and entry
        name_label=Label(ifrm,font=('arial',15,'bold'),text='Name',bg='white',fg='black')
        name_label.place(relx=.05,rely=.2)
        name_entry=Entry(ifrm,font=('arial',20,),bd=5,bg='white') # bd is border
        name_entry.place(relx=.05,rely=.27)
        name_entry.insert(0,tup[2])
        name_entry.focus()
        #mob label and entry
        mob_label=Label(ifrm,font=('arial',15,'bold'),text='MOB',bg='white',fg='black')
        mob_label.place(relx=.05,rely=.4)
        mob_entry=Entry(ifrm,font=('arial',20,),bd=5,bg='white') # bd is border
        mob_entry.place(relx=.05,rely=.47)
        mob_entry.insert(0,tup[3])
        #email label adn entry
        email_label=Label(ifrm,font=('arial',15,'bold'),text='Email',bg='white',fg='black')
        email_label.place(relx=.5,rely=.2)
        email_entry=Entry(ifrm,font=('arial',20,),bd=5,bg='white') # bd is border
        email_entry.place(relx=.5,rely=.27)
        email_entry.insert(0,tup[5])
        #pass label and entry
        pass_label=Label(ifrm,font=('arial',15,'bold'),text='Password',bg='white',fg='black')
        pass_label.place(relx=.5,rely=.4)
        pass_entry=Entry(ifrm,font=('arial',20,),bd=5,bg='white') # bd is border
        pass_entry.place(relx=.5,rely=.47)
        pass_entry.insert(0,tup[1])
        
        #button
        update_btn=Button(ifrm,command=update_details,text='Update Details',font=('arial',20,'bold'),bg='powder blue',bd=5)
        update_btn.place(relx=.3,rely=.7)
 

    def deposit_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.05,relwidth=.6,relheight=.7)
        
        #inner frame title
        title_ifrm=Label(ifrm,font=('arial',15,'bold'),text='This is Deposit screen',bg='white',fg='purple')
        title_ifrm.pack()

        def deposit_db():
            uamt=float(amt_entry.get())
            #user balance fetch
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select users_bal from users where users_acno=?',(uacn,))
            ubal=cur_obj.fetchone()[0]
            con_obj.close()


            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('UPDATE users SET users_bal = users_bal + ? WHERE users_acno = ?', (uamt, uacn))
            con_obj.commit()
            con_obj.close()
            #insert into transaction table
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_updatebal) values(?,?,?,?,?)',(uacn,'Cr(+)',time.strftime('%d-%b-%Y-%r'),uamt,ubal+uamt))
            con_obj.commit()
            con_obj.close()

            messagebox.showinfo('deposit',f'amount {uamt} deposited and updated bal {ubal+uamt}')

        
        amt_label=Label(ifrm,font=('arial',15,'bold'),text='Deposite Amount',bg='white',fg='black')
        amt_label.place(relx=.2,rely=.3)
        amt_entry=Entry(ifrm,font=('arial',20,),bd=5,bg='white') # bd is border
        amt_entry.place(relx=.2,rely=.37)
        amt_entry.focus()

        #button
        deposit_btn=Button(ifrm,command=deposit_db,text='Deposit',font=('arial',20,'bold'),bg='light green',bd=5,fg="black")
        deposit_btn.place(relx=.5,rely=.6)


    def withdraw_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.05,relwidth=.6,relheight=.7)
        
        #inner frame title
        title_ifrm=Label(ifrm,font=('arial',15,'bold'),text='This is Withdraw screen',bg='white',fg='purple')
        title_ifrm.pack()

        def withdraw_db():
            uamt=float(amt_entry.get())
            #user balance fetch
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select users_bal from users where users_acno=?',(uacn,))
            ubal=cur_obj.fetchone()[0]
            con_obj.close()

            if ubal>=uamt:
                con_obj=sqlite3.connect(database='bank.sqlite')
                cur_obj=con_obj.cursor()
                cur_obj.execute('UPDATE users SET users_bal = users_bal - ? WHERE users_acno = ?', (uamt, uacn))
                con_obj.commit()
                con_obj.close()
                #insert into transaction table
                con_obj=sqlite3.connect(database='bank.sqlite')
                cur_obj=con_obj.cursor()
                cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_updatebal) values(?,?,?,?,?)',(uacn,'Dr(-)',time.strftime('%d-%b-%Y-%r'),uamt,ubal-uamt))
                con_obj.commit()
                con_obj.close()

                messagebox.showinfo('withdraw',f'amount {uamt} withdraw and updated bal {ubal-uamt}')
            else:
                messagebox.showerror('withdraw',f'Insuffient Bal{ubal}')


        amt_label=Label(ifrm,font=('arial',15,'bold'),text='Withdraw Amount',bg='white',fg='black')
        amt_label.place(relx=.2,rely=.3)
        amt_entry=Entry(ifrm,font=('arial',20,),bd=5,bg='white') # bd is border
        amt_entry.place(relx=.2,rely=.37)
        amt_entry.focus()

        #button
        deposit_btn=Button(ifrm,command=withdraw_db,text='Withdraw',font=('arial',20,'bold'),bg='light green',bd=5,fg="black")
        deposit_btn.place(relx=.5,rely=.6)

    def transfer_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.05,relwidth=.6,relheight=.7)
        
        #inner frame title
        title_ifrm=Label(ifrm,font=('arial',15,'bold'),text='This is Transfer screen',bg='white',fg='purple')
        title_ifrm.pack()

        def transfer_db():
            uamt=float(amt_entry.get())
            toacn=int(to_entry.get())
            #user balance fetch
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select users_bal,users_email from users where users_acno=?',(uacn,))
            tup=cur_obj.fetchone()
            ubal=tup[0]
            uemail=tup[1]
            con_obj.close()

            if ubal>=uamt:
                #check user exist or not
                con_obj=sqlite3.connect(database='bank.sqlite')
                cur_obj=con_obj.cursor()
                cur_obj.execute('select * from users where users_acno=?',(toacn,))
                tup=cur_obj.fetchone()
                cur_obj.close()

                if tup==None:
                    messagebox.showinfo('Transfer','To ACN does not exist')
  
                else:
                    #generate OTP
                    otp=random.randint(1000,9999)
                    try:
                        gmail_con=gmail.GMail('pyadav1672002@gmail.com','zncx tihq sbel eyxk')
                        umsg=f'''Hello,{uname}
                        Welcome to ABC bank 
                        Your OTP is :{otp}
                        Kindly verify this otp to complete your txn
                        thanks'''
                        msg=gmail.Message(to=uemail,subject='Account',text=umsg)
                        gmail_con.send(msg)
                        messagebox.showinfo('txn','we have send otp to your registered email')
                        
                        #otp box
                        uotp=simpledialog.askinteger("OTP","Enter OTP")
                        if otp==uotp:
                            #DMl querry (Debit from sender, Credit to receiver)
                            con_obj=sqlite3.connect(database='bank.sqlite')
                            cur_obj=con_obj.cursor()
                            cur_obj.execute('UPDATE users SET users_bal = users_bal - ? WHERE users_acno = ?', (uamt, uacn))
                            cur_obj.execute('UPDATE users SET users_bal = users_bal + ? WHERE users_acno = ?', (uamt, toacn))
                            con_obj.commit()
                            con_obj.close()
                                
                            #fetch toacn balance
                            tobal=tup[6]

                            #run dml querry for transaction records (Dr. & Cr.)
                            con_obj=sqlite3.connect(database='bank.sqlite')
                            cur_obj=con_obj.cursor()
                            cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_updatebal) values(?,?,?,?,?)',(uacn,'Dr(-)',time.strftime('%d-%b-%Y-%r'),uamt,ubal-uamt))
                            cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_updatebal) values(?,?,?,?,?)',(toacn,'Cr(+)',time.strftime('%d-%b-%Y-%r'),uamt,tobal))
                            con_obj.commit()
                            con_obj.close()

                            

                            messagebox.showinfo('Transfer',f'amount {uamt} Transfered and updated bal {ubal-uamt}')
                        else:
                            messagebox.showerror("txn","Something went wrong")
                    except Exception as e:
                        print(e)
                        messagebox.showerror('txn','something went wrong')      
            else:
                messagebox.showerror('withdraw',f'Insuffient Bal{ubal}')



        to_label=Label(ifrm,font=('arial',15,'bold'),text='To ACN',bg='white',fg='black')
        to_label.place(relx=.25,rely=.3)
        to_entry=Entry(ifrm,font=('arial',20,),bd=5,bg='white') # bd is border
        to_entry.place(relx=.4,rely=.3)
        to_entry.focus()

        amt_label=Label(ifrm,font=('arial',15,'bold'),text='Amount',bg='white',fg='black')
        amt_label.place(relx=.25,rely=.5)
        amt_entry=Entry(ifrm,font=('arial',20,),bd=5,bg='white') # bd is border
        amt_entry.place(relx=.4,rely=.5)

        #button
        transfer_btn=Button(ifrm,command=transfer_db,text='Transfer',font=('arial',20,'bold'),bg='light green',bd=5,fg="black")
        transfer_btn.place(relx=.6,rely=.7)


    def history_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.05,relwidth=.6,relheight=.7)
        
        #transaction table
        data={}
        conobj=sqlite3.connect("bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select * from txn where txn_acno=?",(uacn,))
        tups=curobj.fetchall()
        i=1
        for tup in tups:
            data[str(i)]={'Txn Amt':tup[4],'Txn Type':tup[2],'Updated Bal':tup[5],'Txn Date':tup[3],'Txn Id':tup[0]}
            i+=1
        model = TableModel()
        model.importDict(data)

        table_frm=Frame(ifrm)
        table_frm.place(relx=.1,rely=.1,relwidth=7)

        table = TableCanvas(table_frm, model=model,editable=False)
        table.show()

        #inner frame title
        title_ifrm=Label(ifrm,font=('arial',15,'bold'),text='This is History screen',bg='white',fg='purple')
        title_ifrm.pack()


    wel_label=Label(frm,font=('arial',20,'bold'),text=f'Welcome,{uname.capitalize()}',bg='pink',fg='blue')
    wel_label.place(relx=.0,rely=.0)
    # function is defined before the logout_btn button because the button needs to know what function to execute when clicked    
    logout_btn=Button(frm,command=logout_click,text='Logout',font=('arial',20,'bold'),bg='powder blue',bd=5)
    logout_btn.place(relx=.9,rely=.0)
    
    #Buttons
    check_btn=Button(frm,command=check_click,width=14,text='Check Balance',font=('arial',20,'bold'),bg='green',bd=5,fg="white")
    check_btn.place(relx=.0,rely=.1)

    update_btn=Button(frm,command=update_click,width=14,text='Update Details',font=('arial',20,'bold'),bg='grey',bd=5,fg="white")
    update_btn.place(relx=.0,rely=.25)

    deposit_btn=Button(frm,command=deposit_click,width=14,text='Deposit Amount',font=('arial',20,'bold'),bg='powder blue',bd=5,fg="white")
    deposit_btn.place(relx=.0,rely=.40)

    withdraw_btn=Button(frm,command=withdraw_click,width=14,text='Withdraw Amount',font=('arial',20,'bold'),bg='navy blue',bd=5,fg="white")
    withdraw_btn.place(relx=.0,rely=.55)

    transfer_btn=Button(frm,command=transfer_click,width=14,text='Tranfer Amount',font=('arial',20,'bold'),bg='dark orange',bd=5,fg="white")
    transfer_btn.place(relx=.0,rely=.7)

    history_btn=Button(frm,command=history_click,width=14,text='Txn History',font=('arial',20,'bold'),bg='yellow',bd=5,fg="black")
    history_btn.place(relx=.0,rely=.85)

main_screen()
win.mainloop() #window launch