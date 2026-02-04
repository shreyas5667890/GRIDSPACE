#import libraries
from flask import Flask, redirect, render_template, flash, request, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import uuid
from werkzeug.utils import secure_filename
import os
import shutil

app = Flask(__name__)

app.secret_key = "apartment_rental"

#code for connection
app.config['MYSQL_HOST'] = 'localhost' #hostname
app.config['MYSQL_USER'] = 'root' #username
app.config['MYSQL_PASSWORD'] = 'Lucifer@1234' #password
#in my case password is null so i am keeping empty
app.config['MYSQL_DB'] = 'gridspace' #database name
# Intialize MySQL
mysql = MySQL(app)
           
@app.route('/')
def home() :
    return render_template('welcome.html')
    
    
@app.route('/AdminLogin', methods=['GET', 'POST'])
def AdminLogin() :
    error = None
    if request.method == 'POST' and 'adminUsername' in request.form and 'adminPass' in request.form and 'securityPass' in request.form:
        if request.form['adminUsername'] != 'admin' or \
                request.form['adminPass'] != 'secret@123' or \
                request.form['securityPass'] != '12345678':
            error = 'Invalid credentials'
        else:
            flash('You have logged in successfully!!')
            return redirect(url_for('AdminDashboard'))
    return render_template('AdminLogin.html', error=error)


@app.route('/AdminLogout')
def AdminLogout() :
    log2 = ''
    log2 = 'You have logged out successfully!!'
    return render_template('AdminLogin.html', log2=log2)


@app.route('/TenantLogin', methods=['GET', 'POST'])
def TenantLogin() :
    error = None
    user_type = request.args.get('type', 'tenant')  # Default to tenant, can be 'owner'
    if request.method == 'POST' and 'username' in request.form and 'pswd1' in request.form :
        username = request.form['username']
        password = request.form['pswd1']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # First check if it's an owner
        cursor.execute('SELECT * FROM OWNER WHERE EMAIL = % s AND PASSWORD = % s', (username, password, ))
        owner_account = cursor.fetchone()
        if owner_account:
            # Create session data for owner
            session['loggedin'] = True
            session['id'] = owner_account['OWNER_ID']
            session['username'] = owner_account['EMAIL']
            session['user_type'] = 'owner'
            session['owner_name'] = owner_account['OWNER_NAME']
            # Redirect to owner dashboard
            flash('You have logged in successfully!!')
            return redirect(url_for('OwnerDashboard'))
        
        # Then check if it's a tenant
        cursor.execute('SELECT * FROM TENANT WHERE EMAIL = % s AND PSWD = % s', (username, password, ))
        account = cursor.fetchone()
        # If account exists in TENANT table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['T_ID']
            session['username'] = account['EMAIL']
            session['user_type'] = 'tenant'
            # Redirect to home page
            flash('You have logged in successfully!!')
            return redirect(url_for('TenantDashboard'))
        else:
            # Account doesnt exist or username/password incorrect
            error = ' Invalid Username or Password !!'
    return render_template('TenantLogin.html', error=error)


@app.route('/Logout')
def Logout() :
    # Remove session data, this will log the user out
    user_type = session.get('user_type', 'tenant')
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('user_type', None)
    session.pop('owner_name', None)
    # Redirect to login page
    log = ''
    log = 'You have logged out successfully!!'
    if user_type == 'owner':
        return render_template('TenantLogin.html', log=log, user_type='owner')
    return render_template('TenantLogin.html', log=log)


@app.route('/Register', methods=['GET','POST'])
def Register():
    msg1 = ''
    log = ''
    #applying empty validation
    if request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form and 'phNo' in request.form and 'dob' in request.form and 'occupation' in request.form and 'gender' in request.form and 'email' in request.form and 'pswd' in request.form:
        #passing HTML form data into python variable
        fname = request.form['firstname']
        lname = request.form['lastname']
        ph = request.form['phNo']
        dob = request.form['dob']
        gender = request.form['gender']
        occupation = request.form['occupation']
        email = request.form['email']
        pswd = request.form['pswd']
        if len(ph) != 10 :
            msg1 = 'Phone No. must be of 10 digits!!'
            return render_template('TenantRegister.html', msg1=msg1)
        #creating variable for connection
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #query to check given data is present in database or no
        cursor.execute('SELECT * FROM TENANT WHERE EMAIL = % s', (email,))
        #fetching data from MySQL
        result = cursor.fetchone()
        if result:
            msg1 = 'Email already exists !'
        else:
            #executing query to insert new data into MySQL
            cursor.execute('INSERT INTO TENANT VALUES (% s, % s, NULL , % s, % s, % s , % s , % s , NULL, % s)', (fname, lname, ph, email, gender ,dob, occupation,pswd))
            mysql.connection.commit()
            #displaying message
            log = 'You have successfully registered !'
            return render_template('TenantLogin.html', log=log)          
    elif request.method == 'POST':
        msg1 = 'Please fill out the form !'
    return render_template('TenantRegister.html', msg1=msg1)


@app.route('/TenantRegister')
def tregister() :
    return render_template('TenantRegister.html')


#----------- ADMIN DASHBOARD----------------


@app.route('/AdminDashboard')
def AdminDashboard() :
    occ_apts=''
    unocc_apts=''
    t_tenants=''
    t_users=''
    #creating variable for connection
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
    cursor.execute('SELECT COUNT(T_ID) AS T_USERS FROM TENANT')
    mysql.connection.commit()
    result1=cursor.fetchone()
    t_users = result1['T_USERS'] 
    cursor.execute('SELECT COUNT(T_ID) AS T_TENANTS FROM TENANT WHERE ROOM_NO IS NOT NULL')
    mysql.connection.commit()
    result2=cursor.fetchone()
    t_tenants = result2['T_TENANTS'] 
    cursor.execute('SELECT COUNT(ROOM_NO) AS T_APTS FROM APARTMENT WHERE APT_STATUS = "Occupied"')
    mysql.connection.commit()
    result3=cursor.fetchone()
    occ_apts = result3['T_APTS'] 
    cursor.execute('SELECT COUNT(ROOM_NO) AS T_APTS FROM APARTMENT WHERE APT_STATUS = "Unoccupied"')
    mysql.connection.commit()
    result4=cursor.fetchone()
    unocc_apts = result4['T_APTS']  
    tot_apt = unocc_apts + occ_apts  
    cursor.execute('SELECT COUNT(BLOCK_NO) AS T_BLOCK FROM APARTMENT_BLOCK')
    mysql.connection.commit()
    result5=cursor.fetchone()
    tot_blck = result5['T_BLOCK']
    cursor.execute('SELECT SUM(R.RENT_FEE) AS T_RENT FROM RENT AS R, RENT_STATUS AS S WHERE R.RENT_ID = S.RENT_ID AND S.R_STATUS = "Paid"')
    mysql.connection.commit()
    result6=cursor.fetchone()
    tot_rent = result6['T_RENT'] 
    if tot_rent == None :
        tot_rent = 0
    return render_template('AdminDashboard.html', occ_apts=occ_apts, unocc_apts=unocc_apts, t_tenants=t_tenants, t_users=t_users, tot_apt=tot_apt, tot_blck=tot_blck, tot_rent=tot_rent)

@app.route('/OwnerDashboard')
def OwnerDashboard() :
    if 'loggedin' not in session or session.get('user_type') != 'owner':
        return redirect(url_for('TenantLogin'))
    occ_apts=''
    unocc_apts=''
    owner_id = session['id']
    owner_name = session.get('owner_name', 'Owner')
    #creating variable for connection
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
    cursor.execute('SELECT COUNT(ROOM_NO) AS T_APTS FROM APARTMENT WHERE APT_STATUS = "Occupied" AND OWNER_ID = %s', (owner_id,))
    mysql.connection.commit()
    result3=cursor.fetchone()
    occ_apts = result3['T_APTS'] 
    cursor.execute('SELECT COUNT(ROOM_NO) AS T_APTS FROM APARTMENT WHERE APT_STATUS = "Unoccupied" AND OWNER_ID = %s', (owner_id,))
    mysql.connection.commit()
    result4=cursor.fetchone()
    unocc_apts = result4['T_APTS']  
    tot_apt = unocc_apts + occ_apts  
    cursor.execute('SELECT SUM(R.RENT_FEE) AS T_RENT FROM RENT AS R, RENT_STATUS AS S, TENANT AS T, APARTMENT AS A WHERE R.RENT_ID = S.RENT_ID AND S.R_STATUS = "Paid" AND R.T_ID = T.T_ID AND T.ROOM_NO = A.ROOM_NO AND A.OWNER_ID = %s', (owner_id,))
    mysql.connection.commit()
    result6=cursor.fetchone()
    tot_rent = result6['T_RENT'] 
    if tot_rent == None :
        tot_rent = 0
    return render_template('OwnerDashboard.html', occ_apts=occ_apts, unocc_apts=unocc_apts, tot_apt=tot_apt, tot_rent=tot_rent, owner_name=owner_name)

@app.route('/OwnerRooms', methods=['POST','GET'])
def OwnerRooms() :
    if 'loggedin' not in session or session.get('user_type') != 'owner':
        return redirect(url_for('TenantLogin'))
    owner_id = session['id']
    block_id=''
    msg2=''
    msg3=''
    aptTitle = ''
    description = ''
    area = ''
    Rent=0
    Room = 0
    #creating variable for connection
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Handle POST request for adding apartment
    if request.method == 'POST' and 'room' in request.form and 'block' in request.form and 'status' in request.form and 'rentPerMonth' in request.form:
        #passing HTML form data into python variable
        Room = request.form['room']
        Block = request.form['block']
        Status = request.form['status']
        Rent = request.form['rentPerMonth']
        Location = request.form['location']
        aptTitle = request.form['apartmentTitle'] 
        description = request.form.get('desc')
        area = request.form['area']
        file1 = request.files['hall']
        file2 = request.files['kitchen']
        file3 = request.files['bedroom']
        file4 = request.files['extra']
        path = 'static/images/apartment'+Room
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
        file1.save(os.path.join('static/images/apartment'+Room, secure_filename(file1.filename)))
        file2.save(os.path.join('static/images/apartment'+Room, secure_filename(file2.filename)))
        file3.save(os.path.join('static/images/apartment'+Room, secure_filename(file3.filename)))
        file4.save(os.path.join('static/images/apartment'+Room, secure_filename(file4.filename)))
        #query to check given data is present in database or no
        cursor.execute('SELECT * FROM APARTMENT WHERE ROOM_NO = % s', (Room,))
        #fetching data from MySQL
        result = cursor.fetchone()
        if result:
            msg2 = 'Apartment already exists !'
        else:
            #executing query to insert new data into MySQL
            cursor.execute('INSERT INTO APARTMENT_BLOCK (BLOCK_NAME, LOCATION) VALUES (%s, %s)', (Block, Location))
            mysql.connection.commit()
            block_id = cursor.lastrowid 
            mysql.connection.commit()
            cursor.execute('INSERT INTO APARTMENT VALUES ( % s,%s, % s, % s, %s)', (Room, block_id,Rent, Status, owner_id))
            mysql.connection.commit()
            cursor.execute('INSERT INTO APARTMENT_DETAILS VALUES (% s, % s, % s, % s)', (Room, aptTitle, area, description))
            mysql.connection.commit()
            Image_url = 'images/apartment'+Room
            cursor.execute('INSERT INTO APARTMENT_PHOTOS VALUES (% s, % s, %s, %s, %s, %s)', (Room, Image_url, file1.filename, file2.filename, file3.filename, file4.filename))
            mysql.connection.commit()
            #displaying message
            msg2 = 'You have successfully added an Apartment !'
    elif request.method == 'POST':
        msg2 = 'Please fill out the form !'
    
    cursor.execute('SELECT APT_TITLE, A.ROOM_NO, AREA, RENT_PER_MONTH, APARTMENT_DESC, A.APT_STATUS, O.OWNER_NAME FROM APARTMENT AS A, APARTMENT_DETAILS AS AD, OWNER AS O WHERE A.ROOM_NO = AD.ROOM_NO AND A.OWNER_ID = O.OWNER_ID AND A.OWNER_ID = %s', (owner_id,))
    mysql.connection.commit()
    msg3=cursor.fetchall()
    
    cursor.execute('SELECT * FROM APARTMENT_PHOTOS')
    mysql.connection.commit()
    img_url = cursor.fetchall()
    return render_template('OwnerRooms.html', msg2=msg2, msg3=msg3, img_url=img_url)

@app.route('/OwnerUpdateApartment', methods=['GET','POST'])
def OwnerUpdateApartment():
    if 'loggedin' not in session or session.get('user_type') != 'owner':
        return redirect(url_for('TenantLogin'))
    owner_id = session['id']
    msg2=''
    msg3=''
    #creating variable for connection
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #applying empty validation
    if request.method == 'POST' and 'room1' in request.form and 'status1' in request.form and 'rentPerMonth1' in request.form :
        #passing HTML form data into python variable
        Room1 = request.form['room1']
        Status1 = request.form['status1']
        Rent1 = request.form['rentPerMonth1']
        area1 = request.form['up_area']
        title1 = request.form['up_title']
        #query to check given data is present in database and belongs to owner
        cursor.execute('SELECT * FROM APARTMENT WHERE ROOM_NO = % s AND OWNER_ID = %s', (Room1, owner_id))
        #fetching data from MySQL
        result = cursor.fetchone()
        if result:
            #executing query to update new data into MySQL
            cursor.execute('UPDATE APARTMENT SET RENT_PER_MONTH = % s, APT_STATUS = % s WHERE ROOM_NO = % s AND OWNER_ID = %s',(Rent1,Status1,Room1, owner_id))
            mysql.connection.commit()
            cursor.execute('UPDATE APARTMENT_DETAILS SET AREA = % s, APT_TITLE = % s WHERE ROOM_NO = % s',(area1,title1,Room1))
            mysql.connection.commit()
            msg2 = 'Apartment updated successfully!'
        else:
            msg2 = 'Apartment doesn\'t exist or you don\'t have permission to update it!'
    elif request.method == 'POST':
        msg2 = 'Please fill out the form !'
    cursor.execute('SELECT APT_TITLE, A.ROOM_NO, AREA, RENT_PER_MONTH, APARTMENT_DESC, A.APT_STATUS, O.OWNER_NAME FROM APARTMENT AS A, APARTMENT_DETAILS AS AD, OWNER AS O WHERE A.ROOM_NO = AD.ROOM_NO AND A.OWNER_ID = O.OWNER_ID AND A.OWNER_ID = %s', (owner_id,))
    mysql.connection.commit()
    msg3=cursor.fetchall() 
    cursor.execute('SELECT * FROM APARTMENT_PHOTOS')
    mysql.connection.commit()
    img_url = cursor.fetchall()
    return render_template('OwnerRooms.html', msg2=msg2,msg3=msg3,img_url=img_url)


@app.route('/OwnerDeleteApartment', methods=['GET','POST'])
def OwnerDeleteApartment() :
    if 'loggedin' not in session or session.get('user_type') != 'owner':
        return redirect(url_for('TenantLogin'))
    owner_id = session['id']
    msg2=''
    msg3=''
    #creating variable for connection
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #applying empty validation
    if request.method == 'POST' and 'room2' in request.form :
        #passing HTML form data into python variable
        Room2 = request.form['room2']
        #query to check given data is present in database and belongs to owner
        cursor.execute('SELECT * FROM APARTMENT WHERE ROOM_NO = % s AND OWNER_ID = %s', (Room2, owner_id))
        #fetching data from MySQL
        result = cursor.fetchone()
        if result:
            #executing query to delete apartment
            cursor.execute('SELECT PATHNAME FROM APARTMENT_PHOTOS WHERE ROOM_NO = % s',(Room2,))
            mysql.connection.commit()
            path = cursor.fetchone()
            if path:
                pathname = 'static/'+path['PATHNAME']
                shutil.rmtree(pathname, ignore_errors=False, onerror=None)
            cursor.execute('DELETE FROM APARTMENT WHERE ROOM_NO = % s AND OWNER_ID = %s',(Room2, owner_id))
            mysql.connection.commit()
            msg2 = 'Apartment deleted successfully!'
        else:
            msg2 = 'Apartment doesn\'t exist or you don\'t have permission to delete it!'
    elif request.method == 'POST':
        msg2 = 'Please fill out the form !'
    cursor.execute('SELECT APT_TITLE, A.ROOM_NO, AREA, RENT_PER_MONTH, APARTMENT_DESC, A.APT_STATUS, O.OWNER_NAME FROM APARTMENT AS A, APARTMENT_DETAILS AS AD, OWNER AS O WHERE A.ROOM_NO = AD.ROOM_NO AND A.OWNER_ID = O.OWNER_ID AND A.OWNER_ID = %s', (owner_id,))
    mysql.connection.commit()
    msg3=cursor.fetchall() 
    cursor.execute('SELECT * FROM APARTMENT_PHOTOS')
    mysql.connection.commit()
    img_url = cursor.fetchall()
    return render_template('OwnerRooms.html', msg2=msg2,msg3=msg3,img_url=img_url)

@app.route('/TotalUsers')
def TotalUsers() :
    msg5=''   
    #creating variable for connection
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT FNAME, LNAME, GENDER, PH_NO, EMAIL, ROOM_NO FROM TENANT')
    mysql.connection.commit()
    msg5=cursor.fetchall()
    return render_template('TotalUsers.html', msg5=msg5)

@app.route('/TotalOwners')
def TotalOwners() :
    msg7=''   
    #creating variable for connection
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT OWNER_ID, OWNER_NAME, PHONE, EMAIL FROM OWNER')
    mysql.connection.commit()
    msg7=cursor.fetchall()
    return render_template('TotalOwners.html', msg7=msg7)


@app.route('/tenantReport', methods=['GET','POST'])
def tenantReport() :
    tenantReport=''
    msg6=''
    #creating variable for connection
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #applying empty validation
    if request.method == 'POST' and 'tid' in request.form :
        #passing HTML form data into python variable
        T_ID = request.form['tid']
        #query to check given data is present in database or no
        cursor.execute('SELECT * FROM TENANT WHERE T_ID = % s', (T_ID,))
        #fetching data from MySQL
        result = cursor.fetchone()
        if result:
            #executing query to insert new data into MySQL
            cursor.execute('DELETE FROM TENANT WHERE T_ID = % s',(T_ID,))
            mysql.connection.commit()
        else:
            msg6 = 'Tenant doesn\'t exists !'
    elif request.method == 'POST':
        msg6 = 'Please fill out the details !'
    cursor.execute('SELECT T_ID, FNAME, LNAME, GENDER, PH_NO, EMAIL, ROOM_NO FROM TENANT WHERE ROOM_NO IS NOT NULL')
    mysql.connection.commit()
    tenantReport=cursor.fetchall()
    return render_template('tenantReport.html', msg6=msg6,tenantReport=tenantReport)


@app.route('/ApartmentRooms', methods=['POST','GET'])
def ApartmentRooms() :
    block_id=''
    msg2=''
    msg3=''
    aptTitle = ''
    description = ''
    area = ''
    Rent=0
    Room = 0
    #creating variable for connection
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #applying empty validation
    if request.method == 'POST' and 'room' in request.form and 'block' in request.form and 'status' in request.form and 'rentPerMonth' in request.form:
        #passing HTML form data into python variable
        Room = request.form['room']
        Block = request.form['block']
        Status = request.form['status']
        Rent = request.form['rentPerMonth']
        Location = request.form['location']
        aptTitle = request.form['apartmentTitle'] 
        description = request.form.get('desc')
        area = request.form['area']
        Owner_ID = request.form.get('owner_id', None)  # Get owner_id from form if provided
        if not Owner_ID:
            if 'loggedin' in session and session.get('user_type') == 'owner':
                Owner_ID = session['id']
            else:
                # For admin or when not logged in, get first available owner
                cursor.execute('SELECT OWNER_ID FROM OWNER LIMIT 1')
                default_owner = cursor.fetchone()
                if default_owner:
                    Owner_ID = default_owner['OWNER_ID']
                else:
                    msg2 = 'No owner found. Please create an owner first!'
                    cursor.execute('SELECT APT_TITLE, A.ROOM_NO, AREA, RENT_PER_MONTH, APARTMENT_DESC, O.OWNER_NAME FROM APARTMENT AS A, APARTMENT_DETAILS AS AD, OWNER AS O WHERE A.ROOM_NO = AD.ROOM_NO AND A.OWNER_ID = O.OWNER_ID AND A.APT_STATUS = "Unoccupied"')
                    mysql.connection.commit()
                    msg3=cursor.fetchall()
                    cursor.execute('SELECT * FROM APARTMENT_PHOTOS')
                    mysql.connection.commit()
                    img_url = cursor.fetchall()
                    return render_template('ApartmentRooms.html',msg2=msg2,msg3=msg3,img_url=img_url)
        file1 = request.files['hall']
        file2 = request.files['kitchen']
        file3 = request.files['bedroom']
        file4 = request.files['extra']
        path = 'static/images/apartment'+Room
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
        file1.save(os.path.join('static/images/apartment'+Room, secure_filename(file1.filename)))
        file2.save(os.path.join('static/images/apartment'+Room, secure_filename(file2.filename)))
        file3.save(os.path.join('static/images/apartment'+Room, secure_filename(file3.filename)))
        file4.save(os.path.join('static/images/apartment'+Room, secure_filename(file4.filename)))
        #query to check given data is present in database or no
        cursor.execute('SELECT * FROM APARTMENT WHERE ROOM_NO = % s', (Room,))
        #fetching data from MySQL
        result = cursor.fetchone()
        if result:
            msg2 = 'Apartment already exists !'
        else:
            #executing query to insert new data into MySQL
            cursor.execute('INSERT INTO APARTMENT_BLOCK (BLOCK_NAME, LOCATION) VALUES (%s, %s)', (Block, Location))
            mysql.connection.commit()
            block_id = cursor.lastrowid 
            mysql.connection.commit()
            cursor.execute('INSERT INTO APARTMENT VALUES ( % s,%s, % s, % s, %s)', (Room, block_id,Rent, Status, Owner_ID))
            mysql.connection.commit()
            cursor.execute('INSERT INTO APARTMENT_DETAILS VALUES (% s, % s, % s, % s)', (Room, aptTitle, area, description))
            mysql.connection.commit()
            Image_url = 'images/apartment'+Room
            cursor.execute('INSERT INTO APARTMENT_PHOTOS VALUES (% s, % s, %s, %s, %s, %s)', (Room, Image_url, file1.filename, file2.filename, file3.filename, file4.filename))
            mysql.connection.commit()
            #displaying message
            msg2 = 'You have successfully added an Apartment !'
    elif request.method == 'POST':
        msg2 = 'Please fill out the form !'
    cursor.execute('SELECT APT_TITLE, A.ROOM_NO, AREA, RENT_PER_MONTH, APARTMENT_DESC, O.OWNER_NAME FROM APARTMENT AS A, APARTMENT_DETAILS AS AD, OWNER AS O WHERE A.ROOM_NO = AD.ROOM_NO AND A.OWNER_ID = O.OWNER_ID AND A.APT_STATUS = "Unoccupied"')
    mysql.connection.commit()
    msg3=cursor.fetchall()
    
    cursor.execute('SELECT * FROM APARTMENT_PHOTOS')
    mysql.connection.commit()
    img_url = cursor.fetchall()
    return render_template('ApartmentRooms.html',msg2=msg2,msg3=msg3,img_url=img_url)


@app.route('/UpdateApartment', methods=['GET','POST'])
def UpdateApartment():
    msg2=''
    msg3=''
    #creating variable for connection
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #applying empty validation
    if request.method == 'POST' and 'room1' in request.form and 'status1' in request.form and 'rentPerMonth1' in request.form :
        #passing HTML form data into python variable
        Room1 = request.form['room1']
        Status1 = request.form['status1']
        Rent1 = request.form['rentPerMonth1']
        area1 = request.form['up_area']
        title1 = request.form['up_title']
        #query to check given data is present in database or no
        cursor.execute('SELECT * FROM APARTMENT WHERE ROOM_NO = % s', (Room1,))
        #fetching data from MySQL
        result = cursor.fetchone()
        if result:
            #executing query to insert new data into MySQL
            cursor.execute('UPDATE APARTMENT SET RENT_PER_MONTH = % s, APT_STATUS = % s WHERE ROOM_NO = % s',(Rent1,Status1,Room1))
            mysql.connection.commit()
            cursor.execute('UPDATE APARTMENT_DETAILS SET AREA = % s, APT_TITLE = % s WHERE ROOM_NO = % s',(area1,title1,Room1))
            mysql.connection.commit()
        else:
            msg2 = 'Apartment doesn\'t exists !'
    elif request.method == 'POST':
        msg2 = 'Please fill out the form !'
    cursor.execute('SELECT APT_TITLE, A.ROOM_NO, AREA, RENT_PER_MONTH, APARTMENT_DESC, O.OWNER_NAME FROM APARTMENT AS A, APARTMENT_DETAILS AS AD, OWNER AS O WHERE A.ROOM_NO = AD.ROOM_NO AND A.OWNER_ID = O.OWNER_ID AND A.APT_STATUS = "Unoccupied"')
    mysql.connection.commit()
    msg3=cursor.fetchall() 
    cursor.execute('SELECT * FROM APARTMENT_PHOTOS')
    mysql.connection.commit()
    img_url = cursor.fetchall()
    return render_template('ApartmentRooms.html', msg2=msg2,msg3=msg3,img_url=img_url)


@app.route('/DeleteApartment', methods=['GET','POST'])
def DeleteApartment() :
    msg2=''
    msg3=''
    #creating variable for connection
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #applying empty validation
    if request.method == 'POST' and 'room2' in request.form :
        #passing HTML form data into python variable
        Room2 = request.form['room2']
        #query to check given data is present in database or no
        cursor.execute('SELECT * FROM APARTMENT WHERE ROOM_NO = % s', (Room2,))
        #fetching data from MySQL
        result = cursor.fetchone()
        if result:
            #executing query to insert new data into MySQL
            cursor.execute('SELECT PATHNAME FROM APARTMENT_PHOTOS WHERE ROOM_NO = % s',(Room2,))
            mysql.connection.commit()
            path = cursor.fetchone()
            pathname = 'static/'+path['PATHNAME']
            shutil.rmtree(pathname, ignore_errors=False, onerror=None)
            cursor.execute('DELETE FROM APARTMENT WHERE ROOM_NO = % s',(Room2,))
            mysql.connection.commit()
        else:
            msg2 = 'Apartment doesn\'t exists !'
    elif request.method == 'POST':
        msg2 = 'Please fill out the form !'
    cursor.execute('SELECT APT_TITLE, A.ROOM_NO, AREA, RENT_PER_MONTH, APARTMENT_DESC, O.OWNER_NAME FROM APARTMENT AS A, APARTMENT_DETAILS AS AD, OWNER AS O WHERE A.ROOM_NO = AD.ROOM_NO AND A.OWNER_ID = O.OWNER_ID AND A.APT_STATUS = "Unoccupied"')
    mysql.connection.commit()
    msg3=cursor.fetchall() 
    cursor.execute('SELECT * FROM APARTMENT_PHOTOS')
    mysql.connection.commit()
    img_url = cursor.fetchall()
    return render_template('ApartmentRooms.html', msg2=msg2,msg3=msg3,img_url=img_url)


@app.route('/RentStatus')
def RentStatus() :
    rent_status=''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT FNAME, LNAME, T.ROOM_NO, RENT_PER_MONTH, DUE_DATE, R_STATUS, LATE_FEE FROM RENT AS R, APARTMENT AS A, RENT_STATUS AS RS, TENANT AS T WHERE R.RENT_ID = RS.RENT_ID AND T.T_ID = R.T_ID AND A.ROOM_NO = T.ROOM_NO')
    mysql.connection.commit()
    rent_status=cursor.fetchall()
    # cursor.execute('CALL RENTUPDATE()')
    # mysql.connection.commit()
    return render_template('RentStatus.html',rent_status=rent_status)



#---------------------------------------------- TENANT DASHBOARD---------------------------------------------


@app.route('/TenantDashboard')
def TenantDashboard() :
    if 'loggedin' in session:
        return render_template('TenantDashboard.html')
    return render_template('TenantLogin.html')

@app.route('/RentApartment')
def rentApartment() :
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT APT_TITLE, A.ROOM_NO, AREA, RENT_PER_MONTH, APARTMENT_DESC, O.OWNER_NAME FROM APARTMENT AS A, APARTMENT_DETAILS AS AD, OWNER AS O WHERE A.ROOM_NO = AD.ROOM_NO AND A.OWNER_ID = O.OWNER_ID AND A.APT_STATUS = "Unoccupied"')
    mysql.connection.commit()
    apartment=cursor.fetchall()
    cursor.execute('SELECT * FROM APARTMENT_PHOTOS')
    mysql.connection.commit()
    img_url = cursor.fetchall()
    return render_template('RentApartment.html',apartment=apartment, img_url=img_url)

@app.route('/Details', methods=['GET','POST'])
def Details() :
    Error=''
    Uname=''
    Tname=''
    PAddress=''
    aptNo=''
    TFatherName=''
    Date = date.today()
    rentAmt= 0
    Deposit= 0
    #creating variable for connection
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #applying empty validation
    if request.method == 'POST' and 'Username' in request.form and 'aptNo' in request.form and 'TFatherName' in request.form and 'PerAddr' in request.form :
        Uname = request.form['Username']
        aptNo = request.form['aptNo']
        TFatherName = request.form['TFatherName']
        PAddress = request.form['PerAddr']
        cursor.execute('SELECT T_ID FROM TENANT WHERE EMAIL= % s',(Uname,))
        mysql.connection.commit()
        tid_list1 = cursor.fetchone()
        t_id = tid_list1['T_ID']
        cursor.execute('SELECT RENT_PER_MONTH FROM APARTMENT WHERE ROOM_NO = %s AND APT_STATUS = "Unoccupied"',(aptNo,))
        mysql.connection.commit()
        res1 = cursor.fetchone()
        if t_id != None and res1 != None :
            cursor.execute('SELECT FNAME,LNAME FROM TENANT WHERE T_ID = %s',(t_id,))
            mysql.connection.commit()
            res = cursor.fetchone()
            Tname = res['FNAME']+' '+res['LNAME']
            rentAmt=res1['RENT_PER_MONTH']
            Deposit = rentAmt * 2
            return redirect(url_for('Contract', aptNo=aptNo ,Tname=Tname, TFatherName=TFatherName,Uname=Uname, PAddress=PAddress, Date=Date, rentAmt=rentAmt, Deposit=Deposit))
        else :
            Error = 'Invalid Username or Apartment No.!!'
    elif request.method == 'POST' :
        Error= 'Please fill out the form!'
    return render_template('Details.html', Error=Error)



@app.route('/alreadyTenant', methods=['GET','POST'])
def alreadyTenant() :
    Error=''
    Uname=''
    Tname=''
    aptNo=''
    rentAmt= 0
    PhNo=''
    late_fee=0
    #creating variable for connection
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #applying empty validation
    if request.method == 'POST' and 'Username' in request.form and 'aptNo' in request.form :
        Uname = request.form['Username']
        aptNo = request.form['aptNo']
        cursor.execute('SELECT T_ID, PH_NO FROM TENANT WHERE EMAIL = % s',(Uname,))
        mysql.connection.commit()
        tid_list1 = cursor.fetchone()
        t_id = tid_list1['T_ID']
        PhNo = tid_list1['PH_NO']
        cursor.execute('SELECT LATE_FEE FROM RENT WHERE T_ID = % s',(t_id,))
        mysql.connection.commit()
        latefee_list = cursor.fetchone()
        late_fee = latefee_list['LATE_FEE']
        totAmt = int(rentAmt) + int(late_fee)
        # PhNo='9876543212'
        cursor.execute('SELECT RENT_PER_MONTH FROM APARTMENT WHERE ROOM_NO = %s AND APT_STATUS = "Occupied"',(aptNo,))
        mysql.connection.commit()
        res1 = cursor.fetchone()
        if t_id != None and res1 != None :
            cursor.execute('SELECT FNAME,LNAME FROM TENANT WHERE T_ID = %s',(t_id,))
            mysql.connection.commit()
            res = cursor.fetchone()
            Tname = res['FNAME']+' '+res['LNAME']
            rentAmt=res1['RENT_PER_MONTH']
            late_fee = late_fee
            totAmt = int(rentAmt) + int(late_fee)
            return redirect(url_for('Payment1', aptNo=aptNo ,Tname=Tname, Uname=Uname,PhNo=PhNo , rentAmt=rentAmt, late_fee=late_fee, totAmt=totAmt))
        else :
            Error = 'Invalid Username or Apartment No.!!'
    elif request.method == 'POST' :
        Error= 'Please fill out the form!'
    return render_template('alreadyTenant.html', Error=Error)


@app.route('/Contract/<aptNo>/<Tname>/<TFatherName>/<Uname>/<PAddress>/<Date>/<rentAmt>/<Deposit>', methods=['GET','POST'])
def Contract(aptNo,Tname, TFatherName, Uname, PAddress, Date, rentAmt, Deposit) :
    msg7=''
    late_fee=0
    totAmt=0
    #creating variable for connection
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #applying empty validation
    if request.method == 'POST' and 'UserName' in request.form and 'aptno' in request.form and 'rent-amt' in request.form and 'deposit' in request.form and 'start_date' in request.form and 'end_date' in request.form and 'pay_date' in request.form and 'terms' in request.form:
        #passing HTML form data into python variable
        end_date = request.form['end_date']
        # pay_date = request.form['pay_date']
        terms = request.form['terms']
        Username = request.form['UserName']
        Apt_no = request.form['aptno']
        start_date = request.form['start_date']
        Deposit = request.form['deposit']
        rentAmt = request.form['rent-amt']
        #creating variable for connection
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #query to check given data is present in database or no
        cursor.execute('SELECT T_ID FROM TENANT WHERE EMAIL= % s',(Username,))
        mysql.connection.commit()
        tid_list2 = cursor.fetchone()
        T_id = tid_list2['T_ID']
        resDate = datetime.strptime(start_date, '%Y-%m-%d')
        due_date = resDate + relativedelta(months=+2)
        totAmt = int(rentAmt) + int(late_fee)
        #executing query to insert new data into MySQL
        cursor.execute('INSERT INTO CONTRACT VALUES ( NULL , % s, % s, % s , % s , % s , % s)', (T_id, Apt_no, start_date, end_date, Deposit ,terms))
        cursor.execute('INSERT INTO RENT VALUES ( NULL , % s, % s, % s , % s , NULL)', (rentAmt, T_id,due_date, late_fee))
        mysql.connection.commit()
        cursor.execute('SELECT RENT_ID FROM RENT WHERE T_ID = % s',(T_id,))
        mysql.connection.commit()
        rent_id_list = cursor.fetchone()
        rent_id = rent_id_list['RENT_ID']
        cursor.execute('INSERT INTO RENT_STATUS VALUES ( % s, % s)', (rent_id,'Unpaid'))
        cursor.execute('UPDATE TENANT SET ROOM_NO = % s WHERE T_ID = % s',(Apt_no,T_id))
        cursor.execute('UPDATE APARTMENT SET APT_STATUS = "Occupied" WHERE ROOM_NO = % s',(Apt_no,))
        mysql.connection.commit()
        cursor.execute('SELECT PH_NO FROM TENANT WHERE T_ID = % s',(T_id,))
        mysql.connection.commit()
        phone_no = cursor.fetchone()
        PhNo = phone_no['PH_NO']
        #displaying message
        flash('Hope you love gridspace  Apartments... ')
        return redirect(url_for('Payment', aptNo=aptNo ,Tname=Tname, PhNo=PhNo, Uname=Uname, rentAmt=rentAmt, late_fee=late_fee, totAmt=totAmt))
    elif request.method == 'POST' :
        msg7 = 'Please fill out the form !'
    return render_template('contract.html', msg7=msg7, aptNo=aptNo , Date=Date, Tname=Tname, TFatherName=TFatherName, Uname=Uname, PAddress=PAddress, Date1=Date, rentAmt=rentAmt, Deposit=Deposit)


@app.route('/Payment/<aptNo>/<Tname>/<PhNo>/<Uname>/<rentAmt>/<late_fee>/<totAmt>', methods=['GET','POST'])
def Payment(aptNo,Tname,PhNo, Uname, rentAmt, late_fee, totAmt) :
    err=''
    Date = date.today()
    id = uuid.uuid1()
    fields = id.fields
    pay_id = fields[0]
    pay_date = date.today()
    #creating variable for connection
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #applying empty validation
    if request.method == 'POST' and 'email' in request.form and 'roomNo' in request.form and 'acc-no' in request.form and 'cardNo' in request.form and 'cvv' in request.form :
        Uname = request.form['email']
        aptNo = request.form['roomNo']
        Acc_No = request.form['acc-no']
        card_No = request.form['cardNo']
        cvv = request.form['cvv']
        if len(card_No) != 11 and len(cvv) != 3:
            err = 'Invalid Card No or cvv!!'
            return render_template('Payment.html',err=err, aptNo=aptNo ,Tname=Tname, PhNo=PhNo, Uname=Uname, rentAmt=rentAmt, late_fee=late_fee, totAmt=totAmt)
        cursor.execute('SELECT T_ID FROM TENANT WHERE EMAIL= % s',(Uname,))
        mysql.connection.commit()
        tid_list1 = cursor.fetchone()
        t_id = tid_list1['T_ID']
        cursor.execute('SELECT RENT_ID FROM RENT WHERE T_ID= % s',(t_id,))
        mysql.connection.commit()
        rentid_list = cursor.fetchone()
        rent_id = rentid_list['RENT_ID']
        if t_id != None and aptNo != None :
            cursor.execute('INSERT INTO PAYMENT VALUES(% s, % s, % s, % s, % s)',(pay_id,Acc_No,t_id,Date,rentAmt))
            cursor.execute('UPDATE RENT SET PAYMENT_ID = % s WHERE RENT_ID = % s',(pay_id, rent_id))
            cursor.execute('UPDATE RENT_STATUS SET R_STATUS = "Paid" WHERE RENT_ID = % s',(rent_id,))
            mysql.connection.commit()
            pay_amt = rentAmt
            return redirect(url_for('Receipt',Tname=Tname, pay_id=pay_id, pay_date=pay_date ,pay_amt=pay_amt))
    elif request.method == 'POST' :
        err= 'Please fill out the form!'
    return render_template('Payment.html',err=err, aptNo=aptNo ,Tname=Tname, PhNo=PhNo, Uname=Uname, rentAmt=rentAmt, late_fee=late_fee, totAmt=totAmt)


@app.route('/Payment1/<aptNo>/<Tname>/<PhNo>/<Uname>/<rentAmt>/<late_fee>/<totAmt>', methods=['GET','POST'])
def Payment1(aptNo,Tname,PhNo, Uname, rentAmt, late_fee, totAmt) :
    err='Payment Unsuccessfull'
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST' and 'email' in request.form and 'roomNo' in request.form and 'acc-no' in request.form :
        Uname = request.form['email']
        aptNo = request.form['roomNo']
        pay_date = request.form['pay_date']
        Acc_No = request.form['acc-no']
        id = uuid.uuid1()
        fields = id.fields
        pay_id = fields[0]
        Date = date.today()
        cursor.execute('SELECT T_ID FROM TENANT WHERE EMAIL= % s',(Uname,))
        mysql.connection.commit()
        tid_list1 = cursor.fetchone()
        t_id = tid_list1['T_ID']
        cursor.execute('SELECT RENT_ID FROM RENT WHERE T_ID= % s',(t_id,))
        mysql.connection.commit()
        rentid_list = cursor.fetchone()
        rent_id = rentid_list['RENT_ID']
        if t_id != None and aptNo != None :
            cursor.execute('INSERT INTO PAYMENT VALUES(% s, % s, % s, % s, % s)',(pay_id,Acc_No,t_id,Date,rentAmt))
            cursor.execute('UPDATE RENT SET PAYMENT_ID = % s WHERE RENT_ID = % s',(pay_id, rent_id))
            cursor.execute('UPDATE RENT_STATUS SET R_STATUS = "Paid" WHERE RENT_ID = % s',(rent_id,))
            mysql.connection.commit()
            pay_amt = rentAmt
            return redirect(url_for('Receipt',Tname=Tname, pay_id=pay_id, pay_date=pay_date ,pay_amt=pay_amt))
    return render_template('Payment.html', err=err,aptNo=aptNo ,Tname=Tname, PhNo=PhNo, Uname=Uname, rentAmt=rentAmt, late_fee=late_fee, totAmt=totAmt)

 
 
@app.route('/Receipt/<Tname>/<pay_id>/<pay_date>/<pay_amt>', methods=['GET','POST'])
def Receipt(Tname,pay_id,pay_date,pay_amt) :
    return render_template('Reciept.html', Tname=Tname, pay_id=pay_id, pay_date=pay_date ,pay_amt=pay_amt)

@app.route('/filter_apartments', methods=['GET'])
def filter_apartments():
    location = request.args.get('location')
    budget = request.args.get('budget', type=int)
    description = request.args.get('description')  # NEW

    query = """
    SELECT ad.ROOM_NO, ad.APT_TITLE, ad.AREA, ad.APARTMENT_DESC, 
           ab.LOCATION, ab.BLOCK_NAME, a.RENT_PER_MONTH, o.OWNER_NAME
    FROM apartment a
    JOIN apartment_details ad ON a.ROOM_NO = ad.ROOM_NO
    JOIN apartment_block ab ON a.BLOCK_NO = ab.BLOCK_NO
    JOIN owner o ON a.OWNER_ID = o.OWNER_ID
    WHERE 1=1
    """
    params = []

    if location:
        query += " AND LOWER(ab.LOCATION) LIKE LOWER(%s)"
        params.append(f"%{location}%")

    if budget:
        query += " AND a.RENT_PER_MONTH <= %s"
        params.append(budget)

    if description:
        query += " AND ad.APARTMENT_DESC LIKE %s"
        params.append(f"%{description}%")

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, params)
    apartments = cursor.fetchall()

    # Get apartment image data
    cursor.execute("SELECT * FROM apartment_photos")
    img_url = cursor.fetchall()

    return render_template('RentApartment.html', apartment=apartments, img_url=img_url)






if __name__ == '__main__':
    app.run(port=5000,debug=True)
