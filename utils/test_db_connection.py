import pymysql

def mysqlconnect():
    # To connect MySQL database
    conn = pymysql.connect(
        host='localhost',
        user='root', 
        password='root',
        database='onboarding',
        )
    return conn


def test_get_otp(email,mobile):
    conn=mysqlconnect()
    
    cur = conn.cursor()
    
    # Select query
    cur.execute(f'select mobile_otp from user_dtls where user_email="{email}" and user_phone="{mobile}";')
    output = cur.fetchone()
    print(output)
    
    otp=output[0]
    
    # To close the connection
    conn.close()
    return otp

# user_otp=test_get_otp(email='simbu@gmail.com',mobile=9876543211)
# print(user_otp)
