
import tkinter as tk
import tkinter.messagebox
import pickle
import random
import string
from PIL import ImageFont, ImageDraw, Image


def login():

    # String
    name = str_username.get()
    password = str_password.get()
    sys_identityCode = str_sys_identityCode
    usr_identityCode = str_usr_identityCode.get()


    if usr_identityCode != sys_identityCode:
        tk.messagebox.showinfo(title='Error', message='identity code wrong,please try again')
        str_usr_identityCode.set('')

    else:
        '''
        Open usrs_info
         If usrs_info not found then create usrs_info.pickle with {admin : admin}
        '''
        try:
            with open('usrs_info.pickle', 'rb')as usr_file:
                usrs_info = pickle.load(usr_file)
        except FileNotFoundError:
            with open('usrs_info.pickle', 'wb')as usr_file:
                usrs_info = {'admin': 'admin'}
                pickle.dump(usrs_info, usr_file)
        # If 如果用戶名在usrs_info内=密碼符合name=登錄成功else密碼錯誤
        '''
        if name in usrs info:if password match with usrs = login else error 
        '''
        if name in usrs_info:
            if password == usrs_info[name]:
                tk.messagebox.showinfo(title='Welcome',message='hi, '+ name)
            else:
                tk.messagebox.showinfo(title='Error',message='your password is wrong')
                # Clear entry box
                str_password.set('')
                str_usr_identityCode.set('')
        # If usr name not in usrs_info > signup func
        else:
            is_sign_up = tk.messagebox.askyesno('Hi', 'you have not sign up yet.sign up now')
            # Clear entry box
            str_username.set('')
            str_password.set('')
            str_usr_identityCode.set('')
            if is_sign_up:
                signup()


# Func: signup
def signup():

    def sing_up_done():
        # Usrs detail string
        new_nm           = str_newName.get()
        new_pwd          = str_newPassword.get()
        new_confirmpwd   = str_pwdConfirm.get()

        '''
        make usrs_info as variable 
        If new password not match with confirm password: error
        '''
        with open('usrs_info.pickle', 'rb')as usr_file:
            exist_usr_info = pickle.load(usr_file)
        if new_pwd != new_confirmpwd:
            tk.messagebox.showinfo(title='Error', message='Password and confirm password must be the same')
            # Clear entry box
            str_newPassword.set('')
            str_pwdConfirm.set('')

        # If usr name already exist
        elif new_nm in exist_usr_info:
            tk.messagebox.showinfo(title='Error', message='The user has already signed up')
            str_newName.set('')
        # Successfully signup
        else:
            # Write new detail into exist_usr_info
            exist_usr_info[new_nm] = new_pwd
            with open('usrs_info.pickle', 'wb')as usr_file:
                pickle.dump(exist_usr_info, usr_file)
            # Welcome window
            tk.messagebox.showinfo(title='Welcome', message='you have successfully done register ')
            # Close welcome window
            window_signup.destroy()

    # Build up SIGNUP windown
    window_signup = tk.Toplevel(window)
    window_signup.geometry('350x200')
    window_signup.title('signup')

    # String
    str_newName = tk.StringVar()
    str_newPassword = tk.StringVar()
    str_pwdConfirm = tk.StringVar()

    # Create new_name, new_Password, pwd_Confirm Text
    # Name
    tk.Label(window_signup, text='User name              :').place(x=40,y=30)
    new_name = tk.Entry(window_signup, textvariable=str_newName)
    new_name.place(x=150, y=30)
    # Password
    tk.Label(window_signup, text='Password                :').place(x=40, y=70)
    new_Password = tk.Entry(window_signup, textvariable=str_newPassword)
    new_Password.place(x=150, y=70)
    # Confirm password
    tk.Label(window_signup, text='Confirm Password :').place(x=40, y=110)
    pwd_Confirm = tk.Entry(window_signup, textvariable=str_pwdConfirm)
    pwd_Confirm.place(x=150, y=110)

    # Confirm signup button
    confirm_signup = tk.Button(window_signup, text='sign up', command=sing_up_done)
    confirm_signup.place(x=150,y=150)


# Identity code
def create_identity_code():
    def randomChar():
        key = random.choice(string.ascii_letters)
        identifying_code.append(key)

        return key

    def randomColor():
        # return 3val that 0~255(hex)
        # In case if three return 255 at same time so I set blue maximum at 200 make sure no white hex
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 200)

    # Identity code picture size
    width = 30 * 4
    height = 30

    # Image.new(mode, size(w&h), color=0)
    # Img detail
    IMG = Image.new('RGB', (width, height), (255, 255, 255))

    # Font detail
    font = ImageFont.truetype('arial.ttf', size=15)
    draw = ImageDraw.Draw(IMG)
    # Background
    for x in range(width):
        for y in range(height):
            # White
            draw.point((x, y), fill=(255, 255, 255))
    # Create 4words
    for i in range(4):
        # ImageDraw.Draw.text((x,y), text, fill=*, font=*, anchor=None)
        draw.text((30 * i, 10), randomChar(), fill=randomColor(), font=font)
    # Save as identitycode.gif
    IMG.save('identitycode.gif', 'gif')





#main
# Build up  main Window
window = tk.Tk()
window.title('Login')
window.geometry('450x250')

# Identity code
# Record identity code for identifying
identifying_code = []
# Creat identity code
create_identity_code()

# String
str_username = tk.StringVar()
str_username.set('example@gmail.com')
str_password = tk.StringVar()
str_usr_identityCode = tk.StringVar()
str_sys_identityCode = ''.join(identifying_code)

# Text
tk.Label(window, text='User name     :').place(x=100, y=30)
tk.Label(window, text='Password       :').place(x=100, y=70)
tk.Label(window, text='IdentifyCode :').place(x=100, y=110)

# Create Entry box of user name,user password and user identitycode
user_name = tk.Entry(window, textvariable=str_username).place(x=180, y=30)
user_password = tk.Entry(window, show='*', textvariable=str_password).place(x=180, y=70)
user_identifycode = tk.Entry(window, textvariable=str_usr_identityCode).place(x=180, y=110)

# Place identity code
canvas = tk.Canvas(window, height=30, width=600)
image_file = tk.PhotoImage(file='identitycode.gif')
image = canvas.create_image(80, 0, anchor='nw', image=image_file)
canvas.place(x=100, y=135)

# Create register and login button
register_button = tk.Button(window, text='register now', command=signup).place(x=100, y=190)
login_button = tk.Button(window, text='Login', command=login).place(x=300, y=190)

# Run main windown
window.mainloop()



