import sys
from repository import repo, _Repository
import repository
from DTO import Vaccine, Supplier, Clinic, Logistic
from repository import _Repository


def split_first_line(line):
    line = line.split(',')
    a = line[3].split('\n')
    line[3] = a[0]
    return line


def insert_into_table(file, firstLine):
    a = int(firstLine[0])
    b = int(firstLine[1]) + a
    c = int(firstLine[2]) + b
    d = int(firstLine[3]) + c

    linesOfVac = []
    linesOfSup = []
    linesOfClin = []
    linesOfLog = []
    for i in range(0, a):
        linesOfVac.append(file[i])
    for i in range(a, b):
        linesOfSup.append(file[i])
    for i in range(b, c):
        linesOfClin.append(file[i])
    for i in range(c, d):
        linesOfLog.append(file[i])
    insert_into_vaccines(linesOfVac)
    insert_into_suppliers(linesOfSup)
    insert_into_clinics(linesOfClin)
    insert_into_logistics(linesOfLog)


def insert_into_vaccines(linesOfVac):
    for i in range(0, len(linesOfVac)):
        line = linesOfVac[i].split(',')
        a = line[3].split('\n')
        line[3] = a[0]
        line[0] = int(line[0])
        line[2] = int(line[2])
        line[3] = int(line[3])
        repo.vaccines.insert(Vaccine(line[0], line[1], line[2], line[3]))


def insert_into_suppliers(linesOfSup):
    for i in range(0, len(linesOfSup)):
        line = linesOfSup[i].split(',')
        a = line[2].split('\n')
        line[2] = a[0]
        line[0] = int(line[0])
        line[2] = int(line[2])
        repo.suppliers.insert(Supplier(line[0], line[1], line[2]))


def insert_into_clinics(linesOfClin):
    for i in range(0, len(linesOfClin)):
        line = linesOfClin[i].split(',')
        a = line[3].split('\n')
        line[3] = a[0]
        line[0] = int(line[0])
        line[2] = int(line[2])
        line[3] = int(line[3])
        repo.clinics.insert(Clinic(line[0], line[1], line[2], line[3]))


def insert_into_logistics(linesOfLog):
    for i in range(0, len(linesOfLog)):
        line = linesOfLog[i].split(',')
        a = line[3].split('\n')
        line[3] = a[0]
        line[0] = int(line[0])
        line[2] = int(line[2])
        line[3] = int(line[3])
        repo.logistics.insert(Logistic(line[0], line[1], line[2], line[3]))


def Orders(file2,file3):
    for i in range(0, len(file2)):
        line = file2[i].split(',')
        if len(line) == 3:
            Receive_Shipment(line)
        else:
            Send_Shipment(line)
        a = total_inventory()
        b = total_demand()
        c = total_received()
        d = total_sent()
        file3.write(str(a[0]) + ',' + str(b[0]) + ',' + str(c[0]) + ',' + str(d[0]) + "\n")


def Receive_Shipment(line):
    a = line[2].split('\n')
    line[2] = a[0]
    b = max_id_in_vaccines()
    k = int(b[0]) + 1
    c = get_id_supplier(line[0])
    update_count_received(line[1], int(c[0]))
    repo.vaccines.insert(Vaccine(k, line[2], int(c[0]), int(line[1])))


def Send_Shipment(line):
    a = line[1].split('\n')
    line[1] = a[0]
    b = get_clinics_logistic(line[0])
    c = get_vaccines()
    if len(c) > 0:
        update_demand(line[0], line[1])
        update_count_sent(line[1], b[0])
        amount = int(line[1])
        for i in range(0, len(c)):
            d = int(c[i][3])
            if d == amount:
                remove_vaccine(c[i][1],c[i][0])
                break
            elif d < amount:
                remove_vaccine(c[i][1],c[i][0])
                amount = amount - d
            else:
                update_vaccine_quantity(amount, c[i][0])
                break


def get_clinics_logistic(location):
    return repo.get_clinics_logistic(location)


def update_count_received(amount, id):
    repo.update_count_received(amount, id)


def get_vaccines():
    return repo.get_vaccines()


def update_demand(location, demand):
    repo.update_demand(location, demand)


def update_vaccine_quantity(amount, id):
    repo.update_vaccine_quantity(amount, id)


def update_count_sent(amount, id):
    repo.update_count_sent(amount, id)


def total_inventory():
    return repo.get_total_inventory()


def remove_vaccine(date,id):
    repo.remove_vaccine(date,id)


def total_demand():
    return repo.get_total_demand()


def total_received():
    return repo.get_total_received()


def total_sent():
    return repo.get_total_sent()


def max_id_in_vaccines():
    return repo.get_max_id_vaccines()


def get_id_supplier(supplier):
    return repo.get_id_supplier(supplier)


def main(argv):

    repo.crate_tables()

    file1 = open(argv[1], "r")
    file1 = file1.readlines()
    firstLine = split_first_line(file1[0])
    file1.remove(file1[0])
    insert_into_table(file1, firstLine)

    file2 = open(argv[2], "r")
    file2 = file2.readlines()
    file3 = open(argv[3], "w")
    Orders(file2 , file3)
    repo.close_db()


if __name__ == '__main__':
    main(sys.argv)

#repo.crate_tables()
#file1 = open(argv[1], "r")
#file1 = file1.readlines()
#firstLine = split_first_line(file1[0])
#file1.remove(file1[0])
#insert_into_table(file1, firstLine)
# file2 = open('/home/spl211/Desktop/mission4/orders.txt', "r")
#file2 = open(argv[2], "r")
#file2 = file2.readlines()
#file3 = open(argv[3], "w")
#Orders(file2, file3)
#repo.close_db()