from flask import Flask, render_template, json, request
import sqlalchemy, re
from sqlalchemy import create_engine, Column, String, Integer, func
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

Base = declarative_base()


# SQLAlchemy 
e = sqlalchemy.create_engine( 'mysql://root:a@localhost/Employee' )
session = sessionmaker()
session.configure(bind=e)
Base.metadata.create_all(e) 



#Table Base Class
class account(Base):
    __tablename__ = 'Account'
    acc_id = Column(Integer,primary_key=True)
    user_no = Column(Integer)
    fname = Column(String(45))
    lname = Column(String(45))
    mname = Column(String(45))
    email = Column(String(50))
    cell_no = Column(Integer)
    address = Column(String(400))

    def jdump(self):
        return {'acc_id' : int(self.acc_id), 'user_no' : int(self.user_no), 'fname' : self.fname, 'lname' : self.lname,'mname' : self.mname, 'email' : self.email, 'cell_no' : int(self.cell_no), 'adress' : self.address}



@app.route('/')
def main():
    return render_template('index.html')

			
	
@app.route('/save',methods=['POST'])
def save():
    # read the posted values from the UI
    _fname = str(request.form['fname'])
    _lname = str(request.form['lname'])
    _mname = str(request.form['mname'])
    _email = str(request.form['email'])
    _cell_no = str(request.form['cell_no'])
    _address = str(request.form['address'])


    if re.match('^([\+]?\d{1,3})?\d{10}$', _cell_no) :
        _user_no = int(_cell_no[-6:])
    else:
        return json.dumps([{'status' : 'false','msg':'please enter valid entry'}])    

    # validate the received values
    if not _user_no and not _fname and not _lname and not _mname and not _email and not _cell_no and not _address :
        return json.dumps({'status' : 'false','msg':'Enter the required fields'})    


    d = account(user_no = _user_no, fname = _fname, lname = _lname, mname = _mname, email = _email, cell_no = _cell_no, address = _address)
    s = session()
    s.add(d)
    s.commit()
    return json.dumps({ 'status' : 'true', 'msg':'data commited' })


@app.route('/get',methods=['GET'])
def get():

    # read values from the Table
    s = session()
    return json.dumps(map(lambda x: x.jdump(), s.query(account).all()))    

		
if __name__ == "__main__":
    app.run('0.0.0.0')		
