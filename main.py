import datetime
import os

from flask import Flask, request, render_template, session, redirect
import pymysql
app = Flask(__name__)
conn = pymysql.connect(host="localhost", user="root", password="Gujjarlapudi@2021", db="desk")
cursor = conn.cursor()

conn2 = pymysql.connect(host="localhost", user="root", password="Gujjarlapudi@2021", db="desk")
cursor2 = conn2.cursor()

app.secret_key = 'fjsfdfd'
admin_username = 'admin'
admin_password = 'admin'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = APP_ROOT+'/static/images'


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")

@app.route("/admin_login1", methods=['post'])
def admin_login1():
    admin_username = request.form.get("user_name")
    admin_password = request.form.get("password")
    if admin_username == 'admin' and admin_password == 'admin':
        session['role'] = 'Admin'
        return render_template("admin_home_page.html")
    else:
        return render_template("msg.html", message="invalid login details")

@app.route("/admin_home_page")
def admin_home_page():
    return render_template("admin_home_page.html")


@app.route("/add_work_space")
def add_work_space():
    return render_template("add_work_space.html")

@app.route("/add_work_space1", methods=['post'])
def add_work_space1():
    work_space_name = request.form.get("work_space_name")
    image = request.files.get("image")
    path = APP_ROOT + "/" + image.filename
    image.save(path)
    address = request.form.get("address")
    count = cursor.execute("select * from work_space where work_space_name = '" + str(work_space_name) + "' and address = '"+str(address)+"'")
    if count == 0:
        cursor.execute("insert into work_space(work_space_name,address,image) value('"+str(work_space_name)+"', '"+str(address)+"', '"+str(image.filename)+"')")
        conn.commit()
        return render_template("admin_msg.html", message="Work Space added successfully")
    else:
        return render_template("admin_msg.html", message="Work Space already exist")

@app.route("/view_work_space")
def view_work_space():
    work_space_name = request.args.get('work_space_name')
    work_space_id = request.args.get('work_space_id')
    if work_space_name == None:
        work_space_name = ''
    if work_space_id == None:
        query = "select * from work_space where work_space_name like '%"+str(work_space_name)+"%'"
    else:
        query = "select * from work_space where work_space_id='"+str(work_space_id)+"' and work_space_name like '%"+str(work_space_name)+"%'"
    cursor.execute(query)
    work_spaces = cursor.fetchall()
    return render_template("view_work_space.html", work_spaces=work_spaces, work_space_name=work_space_name,work_space_id=work_space_id)

@app.route("/add_block")
def add_block():
    work_space_id = request.args.get("work_space_id")
    if work_space_id==None:
        work_space_id = ''
    query = "select * from work_space"
    cursor.execute(query)
    work_spaces = cursor.fetchall()
    return render_template("add_block.html", work_spaces=work_spaces, work_space_id=work_space_id, str=str)

@app.route("/add_block1", methods=['post'])
def add_block1():
    block_name = request.form.get("block_name")
    work_space_id = request.form.get("work_space_id")
    image = request.files.get("image")
    path = APP_ROOT + "/" + image.filename
    image.save(path)
    count = cursor.execute("select * from block where block_name = '" + str(block_name) + "' and work_space_id = '"+str(work_space_id)+"'")
    if count == 0:
        cursor.execute("insert into block(block_name,work_space_id,image) value('" + str(block_name) + "', '"+str(work_space_id)+"', '"+str(image.filename)+"')")
        conn.commit()
        return render_template("admin_msg.html", message="Block added successfully")
    else:
        return render_template("admin_msg.html", message="Block is already exist in the respective Work Space")


@app.route("/view_blocks")
def view_blocks():
    work_space_id = request.args.get("work_space_id")
    block_name = request.args.get("block_name")
    if block_name == None:
        block_name = ''
    if work_space_id == None:
        query = "select * from block where block_name like '%"+str(block_name)+"%'"
    else:
        query = "select * from block where work_space_id='"+str(work_space_id)+"' and block_name like '%"+str(block_name)+"%'"
    cursor.execute(query)
    blocks = cursor.fetchall()
    return render_template("view_blocks.html", blocks=blocks,work_space_id=work_space_id,block_name=block_name,get_work_space_by_work_space_id=get_work_space_by_work_space_id, get_work_spaces=get_work_spaces, str=str)

def get_work_space_by_work_space_id(work_space_id):
    cursor.execute("select * from work_space where work_space_id= '"+str(work_space_id)+"'")
    work_spaces = cursor.fetchall()
    print(work_spaces)
    return work_spaces[0]

def get_work_spaces():
    cursor.execute("select * from work_space")
    work_spaces = cursor.fetchall()
    print(work_spaces)
    return work_spaces

def get_work_spaces_by_block_id(block_id):
    cursor.execute("select * from work_space where work_space_id in(select work_space_id from block where block_id='"+str(block_id)+"')")
    work_space = cursor.fetchall()
    return work_space[0]


def get_block_by_block():
    cursor.execute("select * from block")
    blocks = cursor.fetchall()
    print(blocks)
    return blocks


@app.route("/add_floor")
def add_floor():
    block_id = request.args.get("block_id")
    work_space_id = ''
    blocks = []
    if block_id != None:
        query1 = "select * from block where block_id='"+str(block_id)+"'"
        cursor.execute(query1)
        blocks = cursor.fetchall()
        work_space_id = blocks[0][3]
        query1 = "select * from block where work_space_id='"+str(work_space_id)+"'"
        cursor.execute(query1)
        blocks = cursor.fetchall()
    return render_template("add_floor.html", blocks=blocks, get_work_spaces_by_block_id=get_work_spaces_by_block_id,
                           get_work_spaces=get_work_spaces, work_space_id=work_space_id,str=str, block_id=block_id)


@app.route("/add_floor1", methods=['post'])
def add_floor1():
    floor_no = request.form.get("floor_no")
    image = request.files.get("image")
    path = APP_ROOT + "/" + image.filename
    image.save(path)
    block_id = request.form.get("block_id")
    count = cursor.execute("select * from floors where floor_no = '" + str(floor_no) + "' and block_id = '"+str(block_id)+"'")
    if count == 0:
        cursor.execute("insert into floors(floor_no,block_id,image) value('" + str(floor_no) + "', '"+str(block_id)+"', '"+str(image.filename)+"')")
        conn.commit()
        return render_template("admin_msg.html", message="Floor is Added Successfully")
    else:
        return render_template("admin_msg.html", message="Floor is Already Exist in the Respective Block")


@app.route("/view_floors")
def view_floors():
    work_space_id = request.args.get("work_space_id")
    block_id = request.args.get("block_id")
    floor_no = request.args.get("floor_no")
    if work_space_id == None:
        work_space_id = ""
    if block_id == None:
        block_id = ""
    if floor_no == None:
        floor_no = ""
    if work_space_id == "" and block_id == "" and floor_no == "":
        query = "select * from floors"
    elif work_space_id == "" and block_id == "" and floor_no != "":
        query = "select * from floors where floor_no='"+str(floor_no)+"'"
    elif work_space_id == "" and block_id != "" and floor_no == "":
        query = "select * from floors where block_id='"+str(block_id)+"'"
    elif work_space_id != "" and block_id == "" and floor_no == "":
        query = "select * from floors where block_id in(select block_id from block where work_space_id='"+str(work_space_id)+"')"
    elif work_space_id != "" and block_id != "" and floor_no == "":
        query = "select * from floors where block_id='"+str(block_id)+"'"
    elif work_space_id == "" and block_id != "" and floor_no != "":
        query = "select * from floors where floor_no='"+str(floor_no)+"' and block_id='"+str(block_id)+"'"
    elif work_space_id != "" and block_id == "" and floor_no != "":
        query = "select * from floors where floor_no='"+str(floor_no)+"'"
    elif work_space_id != "" and block_id != "" and floor_no != "":
        query = "select * from floors where floor_no='"+str(floor_no)+"' and block_id='"+str(block_id)+"'"
    cursor.execute(query)
    print(query)
    floors = cursor.fetchall()
    return render_template("view_floors.html", floors=floors, get_block_by_block_id=get_block_by_block_id, get_work_space_by_work_space_id=get_work_space_by_work_space_id, get_block_by_block=get_block_by_block, get_work_spaces=get_work_spaces, work_space_id=work_space_id, block_id=block_id, floor_no=floor_no, str=str)

def get_block_by_block_id(block_id):
    cursor.execute("select * from block where block_id= '"+str(block_id)+"'")
    blocks = cursor.fetchall()
    print(blocks)
    return blocks[0]

@app.route("/get_floors_by_block_id")
def get_floors_by_block_id():
    block_id = request.args.get('block_id')
    cursor.execute("select * from floors where block_id= '" + str(block_id) + "'")
    floors = cursor.fetchall()
    return render_template("display_floors.html", floors=floors)

@app.route("/add_desk")
def add_desk():
    floor_id = request.args.get('floor_id')
    block_id = ''
    work_space_id = ''
    blocks = []
    floors = []
    if floor_id != None:
        cursor.execute("select * from floors where floor_id='"+str(floor_id)+"'")
        floors = cursor.fetchall()
        block_id = floors[0][3]
        cursor.execute("select * from block where block_id='" + str(block_id) + "'")
        blocks = cursor.fetchall()
        work_space_id = blocks[0][3]

        cursor.execute("select * from block where work_space_id='" + str(work_space_id) + "'")
        blocks = cursor.fetchall()

        cursor.execute("select * from floors where block_id='" + str(block_id) + "'")
        floors = cursor.fetchall()

    return render_template("add_desk.html", work_space_id=work_space_id, floor_id=floor_id, block_id=block_id, blocks=blocks, floors=floors, get_work_spaces=get_work_spaces, str=str)

def get_blocks():
    cursor.execute("select * from block")
    blocks = cursor.fetchall()
    return blocks

@app.route("/get_work_spaces")
def get_work_spaces2():
    cursor.execute("select * from work_space")
    work_spaces = cursor.fetchall()
    conn.commit()
    return render_template("get_work_spaces.html", work_spaces=work_spaces)

@app.route("/get_blocks")
def get_blocks():
    work_space_id = request.args.get('work_space_id')
    cursor.execute("select * from block where work_space_id='"+str(work_space_id)+"'")
    blocks = cursor.fetchall()
    conn.commit()
    return render_template("get_blocks.html", blocks=blocks)


@app.route("/get_floor")
def get_floor():
    block_id = request.args.get('block_id')
    cursor.execute("select * from floors where block_id='"+str(block_id)+"'")
    floors = cursor.fetchall()
    conn.commit()
    return render_template("get_floor.html", floors=floors)


@app.route("/add_desk1", methods=['post'])
def add_desk1():
    desk_title = request.form.get("desk_title")
    charge_per_day = request.form.get("charge_per_day")
    image = request.files.get("image")
    path = APP_ROOT + "/" + image.filename
    image.save(path)
    floor_id = request.form.get("floor_id")
    number_of_desks = request.form.get("number_of_desks")
    count = cursor.execute("select * from desk where desk_title = '" + str(desk_title) + "' and floor_id = '"+str(floor_id)+"'")
    if count == 0:
        cursor.execute("insert into desk(desk_title,charge_per_day,status,floor_id,image,number_of_desks) value('" + str(desk_title) + "', '" + str(charge_per_day) + "', 'Opened', '"+str(floor_id)+"', '"+str(image.filename)+"', '"+str(number_of_desks)+"')")
        conn.commit()
        return render_template("admin_msg.html", message="Desk is Added Successfully")
    else:
        return render_template("admin_msg.html", message="Desk is Already Exist in the Respective Floor")


@app.route("/view_desks")
def view_desks():
    floor_id = request.args.get('floor_id')
    block_id = ''
    work_space_id = ''
    blocks = []
    floors = []
    if floor_id != None:
        cursor.execute("select * from floors where floor_id='" + str(floor_id) + "'")
        floors = cursor.fetchall()
        block_id = floors[0][3]
        cursor.execute("select * from block where block_id='" + str(block_id) + "'")
        blocks = cursor.fetchall()
        work_space_id = blocks[0][3]

        cursor.execute("select * from block where work_space_id='" + str(work_space_id) + "'")
        blocks = cursor.fetchall()

        cursor.execute("select * from floors where block_id='" + str(block_id) + "'")
        floors = cursor.fetchall()

    return render_template("view_desks.html", work_space_id=work_space_id, floor_id=floor_id, block_id=block_id, blocks=blocks, floors=floors, get_work_spaces=get_work_spaces, str=str)

def get_floor_by_floor_id(floor_id):
    print("select * from floors where floor_id= '"+str(floor_id)+"'")
    cursor.execute("select * from floors where floor_id= '"+str(floor_id)+"'")
    floors = cursor.fetchall()
    print(floors)
    return floors[0]

@app.route("/get_desks")
def get_desks():
    work_space_id = request.args.get('work_space_id')
    block_id = request.args.get('block_id')
    floor_id = request.args.get('floor_id')
    desk_title = request.args.get('desk_title')

    print(work_space_id)
    query = "select * from desk where desk_title like '%"+str(desk_title)+"%'"
    if floor_id != '':
        query = "select * from desk where desk_title like '%" + str(desk_title) + "%' and floor_id='"+str(floor_id)+"'"
    elif block_id != '':
        query = "select * from desk where desk_title like '%" + str(desk_title) + "%' and floor_id in (select floor_id from floors where block_id='"+str(block_id)+"')"
    elif work_space_id != '':
        query = "select * from desk where desk_title like '%" + str(desk_title) + "%' and floor_id in (select floor_id from floors where block_id in (select block_id from block where work_space_id='"+str(work_space_id)+"'))"
    print(query)
    cursor2.execute(query)
    desks = cursor2.fetchall()
    conn2.commit()
    return render_template("get_desks.html", desks=desks, get_floor_by_floor_id=get_floor_by_floor_id, get_block_by_block_id=get_block_by_block_id, get_work_space_by_work_space_id=get_work_space_by_work_space_id)

@app.route("/employee_registration")
def employee_registration():
    return render_template("employee_registration.html")


@app.route("/employee_registration1", methods=['post'])
def employee_registration1():
    name = request.form.get("name")
    phone = request.form.get("phone")
    email = request.form.get("email")
    password = request.form.get("password")
    gender = request.form.get("gender")
    age = request.form.get("age")
    occupation = request.form.get("occupation")
    address = request.form.get("address")
    count = cursor.execute("select * from employee where email='"+str(email)+"'")
    if count > 0:
        return render_template("msg.html", message="This Email Already Taken by Another Employee")
    count = cursor.execute("select * from employee where phone='" + str(phone) + "'")
    if count > 0:
        return render_template("msg.html", message="This Phone Number Already Taken by Another Employee")
    cursor.execute("insert into employee(employee_name,phone,email,password,address,occuption,gender,age) values('" + str(name) + "', '" + str(phone) + "', '" + str(email) + "', '" + str(password) + "', '" + str(address) + "', '" + str(occupation) + "', '" + str(gender) + "', '" + str(age) + "')")
    conn.commit()
    return render_template("msg.html", message="Employee  Registered Successfully")



@app.route("/employee_login")
def employee_login():
    return render_template("employee_login.html")


@app.route("/employee_login1", methods=['post'])
def employee_login1():
    email = request.form.get("email")
    password = request.form.get("password")
    count = cursor.execute("select * from employee where email= '" + str(email) + "' and password= '" + str(password) + "'")
    employees = cursor.fetchall()
    if count > 0:
        employee = employees[0]
        session["employee_id"] = employee[0]
        session["role"] = 'employee'
        return redirect("/employee_home_page")
    else:
        return render_template("msg.html", message="invalid login")


@app.route("/employee_home_page")
def employee_home_page():
    return render_template("employee_home_page.html")


@app.route("/book_desk")
def book_desk():
    desk_id = request.args.get("desk_id")
    cursor.execute("select * from desk where desk_id = '"+str(desk_id)+"'")
    desk = cursor.fetchall()
    desk_title = desk[0][2]
    return render_template("book_desk.html", desk_id=desk_id, desk_title=desk_title)

@app.route("/book_desk1", methods=['post'])
def book_desk1():
    desk_id = request.form.get("desk_id")
    desk_title = request.form.get("desk_title")
    form_date_time = request.form.get("form_date_time")
    to_date_time = request.form.get("to_date_time")
    cursor.execute("select * from desk where desk_id = '" + str(desk_id) + "'")
    desk = cursor.fetchall()
    form_date_time = form_date_time.replace('T', ' ')
    to_date_time = to_date_time.replace('T', ' ')
    print(form_date_time)
    form_date_time = datetime.datetime.strptime(form_date_time, "%Y-%m-%d %H:%M")
    to_date_time = datetime.datetime.strptime(to_date_time, "%Y-%m-%d %H:%M")
    diff = to_date_time - form_date_time
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    print(hours, minutes, seconds)
    if hours > 0:
        days = days + 1
    return render_template("book_desk1.html", desk=desk, int=int, desk_title=desk_title, form_date_time=form_date_time, to_date_time=to_date_time, days=days, desk_id=desk_id,is_desk_booked=is_desk_booked)

@app.route("/book_desk2")
def book_desk2():
    employee_id = session["employee_id"]
    desk_id = request.args.get("desk_id")
    print(desk_id)
    no_of_days = request.args.get("no_of_days")
    form_date_time = request.args.get("form_date_time")
    to_date_time = request.args.get("to_date_time")
    no_of_desks = request.args.get("no_of_desks")
    desk_title = request.args.get("desk_title")
    selected_desks = []
    cursor.execute("select * from desk where desk_id = '"+str(desk_id)+"'")
    desk = cursor.fetchall()
    charge_per_day = desk[0][3]
    total_amount = int(charge_per_day)*int(no_of_days)
    for i in range(1, int(no_of_desks)):
        desk_number = request.args.get(str(i))
        print(desk_number)
        if desk_number!=None:
            selected_desks.append(i)
    desk_numbers = len(selected_desks)
    print(desk_numbers)
    cursor.execute("insert into employee_booking(status,date,from_date_time,to_date_time,desk_id,employee_id) values('Payment Pending', now(), '"+str(form_date_time)+"', '"+str(to_date_time)+"', '"+str(desk_id)+"', '"+str(employee_id)+"')")
    employee_booking_id = cursor.lastrowid
    conn.commit()
    for selected_desk in selected_desks:
        cursor.execute("insert into booking_desk(desk_numbers,employee_booking_id) values('"+str(selected_desk)+"', '"+str(employee_booking_id)+"')")
        conn.commit()

    cursor.execute("select * from employee_booking where employee_booking_id='"+str(employee_booking_id)+"'")
    employee_booking = cursor.fetchall()
    amount_to_be_payed = int(total_amount)*int(desk_numbers)
    return render_template("book_desk2.html", amount_to_be_payed=amount_to_be_payed, desk_id=desk_id, total_amount=total_amount, desk=desk, no_of_days=no_of_days, charge_per_day=charge_per_day, desk_numbers=desk_numbers, employee_booking=employee_booking, int=int)


@app.route("/book_desk3")
def book_desk3():
    employee_id = session["employee_id"]
    desk_id = request.args.get("desk_id")
    print(desk_id)
    amount_to_be_payed = request.args.get("amount_to_be_payed")
    print(amount_to_be_payed)
    cursor.execute("update employee_booking set status = 'Desk Booked', total_amount = '"+str(amount_to_be_payed)+"' where desk_id='"+str(desk_id)+"' and employee_id='"+str(employee_id)+"'")
    conn.commit()
    return render_template("employee_msg.html", message="Desks Booked Successfully")

@app.route("/view_employee_bookings")
def view_employee_bookings():
    status = request.args.get('status')
    desk_id = request.args.get('desk_id')
    query = ""
    role = session['role']
    if role == 'employee':
        employee_id = session["employee_id"]
        if status == 'Booked':
            query = "select * from employee_booking where employee_id='"+str(employee_id)+"' and status='Desk Booked'"
        elif status == 'History':
            query = "select * from employee_booking where employee_id='"+str(employee_id)+"' and status='Cancelled'"
    elif role != 'employee':
        query = "select * from employee_booking where desk_id='"+str(desk_id)+"'"
    cursor.execute(query)
    employee_bookings = cursor.fetchall()
    return render_template("view_employee_bookings.html", employee_bookings=employee_bookings, get_desk_by_employee_booking=get_desk_by_employee_booking, get_floor_by_floor_id=get_floor_by_floor_id, get_block_by_block_id=get_block_by_block_id, get_work_space_by_work_space_id=get_work_space_by_work_space_id, get_booked_desks_by_employee_booking_id=get_booked_desks_by_employee_booking_id, get_employee_by_employee_id=get_employee_by_employee_id)

def get_desk_by_employee_booking(desk_id):
    cursor.execute("select * from desk where desk_id='"+str(desk_id)+"'")
    desk = cursor.fetchall()
    print(desk)
    return desk[0]

def get_booked_desks_by_employee_booking_id(employee_booking_id):
    cursor.execute("select * from booking_desk where employee_booking_id='"+str(employee_booking_id)+"'")
    booking_desk = cursor.fetchall()
    print(booking_desk)
    return booking_desk

def get_employee_by_employee_id(employee_id):
    cursor.execute("select * from employee where employee_id='" + str(employee_id) + "'")
    employee = cursor.fetchall()
    print(employee)
    return employee[0]

@app.route("/cancel_booking")
def cancel_booking():
    employee_booking_id = request.args.get("employee_booking_id")
    cursor.execute("update employee_booking set status = 'Cancelled' where employee_booking_id='"+str(employee_booking_id)+"'")
    conn.commit()
    return render_template("employee_msg.html", message="Booking Cancelled Successfully")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

def is_desk_booked(desk_id,from_date_time,to_date_time,i):
    query = "select * from booking_desk where desk_numbers='"+str(i)+"' and  employee_booking_id in (select employee_booking_id from employee_booking where status='Desk Booked' and desk_id='"+str(desk_id)+"' and ((('"+str(from_date_time)+"'>= from_date_time and '"+str(from_date_time)+"'<= to_date_time) and ('"+str(to_date_time)+"'>= from_date_time and '"+str(to_date_time)+"'>= to_date_time)) or (('"+str(from_date_time)+"'<= from_date_time and '"+str(from_date_time)+"'<= to_date_time) and ('"+str(to_date_time)+"'>= from_date_time and '"+str(to_date_time)+"'<= to_date_time)) or (('"+str(from_date_time)+"'<= from_date_time and '"+str(from_date_time)+"'<= to_date_time) and ('"+str(to_date_time)+"'>= from_date_time and '"+str(to_date_time)+"'>= to_date_time)) or (('"+str(from_date_time)+"'>= from_date_time and '"+str(from_date_time)+"'<= to_date_time) and ('"+str(to_date_time)+"'>= from_date_time and '"+str(to_date_time)+"'<= to_date_time))) )"
    print(query)
    cursor.execute(query)
    employee_bookings = cursor.fetchall()
    print(len(employee_bookings))
    if len(employee_bookings) > 0:
        return True
    else:
        return False
app.run(debug=True)