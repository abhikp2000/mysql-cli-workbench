import mysql.connector

class Column:
    def __init__(self,name=None,datatype=None,length=0,options=["N","Y","N"]):
        self.name=name.replace(" ","")
        self.datatype=datatype
        self.length=length
        self.primary=options[0]
        self.null=options[1]
        self.inc=options[2]
        self.__tostring()
    def __tostring(self):
        if self.length == 0:
            self.final=self.name +" "+self.datatype
        else:
            self.final=self.name +" "+self.datatype +" ("+self.length +") "

        if(self.primary=="Y"):
            self.final+=" ,primary key("+self.name+")"
        if(self.null!="N"):
            self.final+=" not null"
        if(self.inc=="Y"):
            self.final+=" auto_increment"
class Workbench:
    def __init__(self,dbname,user="root",host="localhost",password=""):
        self.databaseName=dbname
        self.user=user
        self.host=host
        self.password=password
        self.connectToDB()

    def connectToDB(self):
        self.conn=mysql.connector.connect(user=self.user,host=self.host,password=self.password,database=self.databaseName)
    
    def selectFromTable(self,tablename,attribute):
        if len(attribute)==0:
            users="SELECT * FROM "+tablename
        else:
            users="SELECT "
            for i in range(len(attribute)):
                if(i<len(attribute)-1):
                    users+=attribute[i]
                    users+=','
                else:
                    users+=attribute[i]
            users+=" FROM "+tablename

        cursor = self.conn.cursor()
        cursor.execute(users)
        result=cursor.fetchall()
        for i in result:
            print(i)

    def creatTable(self,tablename,columns):
        query="create table "
        query+=tablename +" ( "
        #create table tablename (
        temp=0
        for i in columns:
            if(temp!=len(columns)-1):
                query+=i.final+","
            else:
                query+=i.final+")"
            temp+=1
        print(query)
        #create table tablename (name varchar(250),addr varchar(250))
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()

    def showTables(self):
        show = "SHOW TABLES"
        cursor = self.conn.cursor()
        cursor.execute(show)
        result = cursor.fetchall()
        return result

    def deleteRecord(self,tablename, where, key):
        delete = "DELETE FROM " + tablename + " where "
        if (len(where) > 0):
            j = 0
            for i in where:
                if (j < len(where) - 1):
                    delete += i
                    delete += "= '"
                    delete += where[i]
                    delete += "' " + key + " "
                else:
                    delete += i
                    delete += " = '"
                    delete += where[i]
                    delete += "' "
                j = j + 1
        print(delete)
        cursor = self.conn.cursor()
        cursor.execute(delete)
        self.conn.commit()

table="abcd"
n=int(input('number of attributes\n'))
column=[]
primary_check=True
for i in range(n):
    name=input('Enter name of col '+str(i)+'\n')
    datatype=input('Enter datatype of col '+str(i)+'\n')
    if(datatype =="varchar" or datatype =="VARCHAR"):
        length=input('Enter size of col '+str(i)+'\n')
    else:
        length=0
    if(primary_check):
        primary=input("primary key?(Y/N)\n")
        if(primary=="Y"):
            primary_check=False
    else:
        primary="N"
    null=input("null(Y/N)\n")
    inc=input("auto increment?(Y/N)\n")

    temp=Column(name,datatype,length,[primary,null,inc])
    column.append(temp)
    
a=Workbench('dbName')
a.creatTable(table,column)
a.showTables()
a.selectFromTable(table,'attribute')
a.deleteRecord(table,'where','key')
