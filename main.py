import mysql.connector
import nicparser
import check_value
import matplotlib.pyplot as plt
import numpy as np

con = mysql.connector.connect(host="localhost", user="root", password="", database="election_vote")
cursor = con.cursor()

party = ("kaputa", "yatura", "aliya", "maduwa", "makara")


class Citizen:
    def __init__(self, name, nic, age, province):
        self.name = name
        self.nic = nic
        self.age = age
        self.province = province

    def store_data(self):
        sql = "INSERT INTO citizen (name, nic, age, province) VALUES (%s, %s, %s, %s)"
        val = (self.name, self.nic, self.age, self.province)
        cursor.execute(sql, val)

        con.commit()

        print(cursor.rowcount, "record inserted.")

    def get_nic(self):
        cursor.execute("SELECT nic FROM citizen")
        self.citizen_nic = cursor.fetchall()
        for i in range(len(self.citizen_nic)):
            return self.citizen_nic[i][0]


class Candidate:
    def __init__(self, name, number, age, nic, edu_qualif, province, party, votes):
        self.name = name
        self.number = number
        self.age = age
        self.nic = nic
        self.edu_qualif = edu_qualif
        self.province = province
        self.party = party
        self.votes = votes

    def store_data(self):
        cursor.execute("use election_vote")
        sql = "INSERT INTO candidate (name, number, nic, age, edu_qualif, province, party,votes) VALUES (%s, %s, %s, %s," \
              " %s, %s, %s, %s)"
        val = (self.name, self.number, self.nic, self.age, self.edu_qualif, self.province, self.party, self.votes)
        cursor.execute(sql, val)

        con.commit()
        print(cursor.rowcount, "record inserted.")

    def display_all_candidate(self):
        for p in party:
            print("____________________________________________________________")
            print(p)
            print("____________________________________________________________")
            cursor.execute(f"SELECT name, number, edu_qualif, province FROM candidate WHERE party = '{p}'")
            candidate_details = cursor.fetchall()
            for i in range(len(candidate_details)):
                print("number: " + str(candidate_details[i][1]))
                print("name: " + candidate_details[i][0] + " |  educational qualification: " + candidate_details[i][
                    2] + " |  province:" + candidate_details[i][3])

# -----------------------------------------------------------------------------------------------------------------------
class User_register:
    def candidate_register(self):
        candidate_province = ""
        candidate_name = input("Enter candidate name: ")
        candidate_number = int(input("Enter the number you are competing with: "))
        candidate_age = int(input("Enter candidate age: "))
        candidate_party = input("Enter your party: ")
        candidate_edu_qualif = input("Enter candidate education qualification: ")
        candidate_nic = input("Enter candidate nic: ")

        passnic = bool(nicparser.NICParser(candidate_nic))
        if passnic:
            print("Yes.. valid nic")

            candidate_citizen = input("Are you citizen y/n: ")
            if candidate_citizen == "y":
                candidate_province = input("Enter candidate province: ")

                candi2 = Candidate(candidate_name, candidate_number, candidate_age, candidate_nic, candidate_edu_qualif,
                                   candidate_province,
                                   candidate_party, 0)
                candi2.store_data()
                c = input("You want to add next (Y/N): ")
                if c.lower() == "y":
                    User_register.citizen_register()
                else:
                    exit()

            else:
                print("Sorry, Cannot complete this....")
                exit(0)

        else:
            print("Invalid NIC number.. Please try again..")
            c = input("You want try to again (Y/N): ")
            if c.lower() == "y":
                User_register.citizen_register()
            else:
                exit()

    def citizen_register(self):
        citizen_nic = ""
        cursor.execute("SELECT nic FROM citizen")
        nic = cursor.fetchall()
        citizen_name = input("Enter citizen name: ")
        citizen_age = int(input("Enter citizen age: "))
        citizen_province = input("Enter citizen province: ")

        if citizen_age >= 18:
            print("woow.. ok..")

            citizen_nic = input("Enter candidate nic: ")
            if nicparser.NICParser(citizen_nic):
                if check_value.nic_available(nic, citizen_nic):
                    citizen1 = Citizen(citizen_name, citizen_nic, citizen_age, citizen_province)
                    citizen1.store_data()
                else:
                    print("This NIC used previously...")
                    print(check_value.nic_available(nic, citizen_nic))
                    exit(0)
            else:
                print("Invalid NIC number.  Try Again...\n")
                c = input("You want try to again (Y/N): ")
                if c.lower() == "y":
                    User_register.citizen_register()
                else:
                    exit()
        else:
            print("Only citizens above the age of 18 can place a vote....")

        c = input("You want to add next (Y/N): ")
        if c.lower() == "y":
            User_register.candidate_register()
        else:
            exit()

    def citizen_delete(self):
        nic = ""
        print("\n\t\t1 - delete using NIC number\n"
              "\t\t2 - delete all registered citizen")

        ans1 = int(input("Enter your choice: "))

        if ans1 == 1:
            nic = input("Enter NIC number you want to delete citizen: ")
            cursor.execute(f"SELECT * FROM citizen WHERE nic = '{nic}'")

            reg_citizen_details = cursor.fetchall()
            for n in range(len(reg_citizen_details)):
                for i in range(len(reg_citizen_details[n])):
                    print(reg_citizen_details[n][i])
                print("\n\n")

            ans = input("Are you sure delete this citizen (Y/N): ")
            if ans.lower() == "y":
                cursor.execute(f"DELETE FROM citizen WHERE  nic = '{nic}'")
                con.commit()
                print("deleted this record(s) !")
            else:
                print("Not deleted.")
                main_interface()

        if ans1 == 2:
            ans = input("Are you sure delete this citizen (Y/N): ")
            if ans.lower() == "y":
                cursor.execute(f"DELETE FROM citizen WHERE  1")
                con.commit()
                print("deleted records !")
                main_interface()
            else:
                print("Not deleted.")
                main_interface()

    def candidate_delete(self):
        nic = ""
        print("\n\t\t1 - delete using NIC number\n"
              "\t\t2 - delete all registered candidate")

        ans1 = int(input("Enter your choice: "))

        if ans1 == 1:
            nic = input("Enter NIC number you want to delete candidate: ")
            cursor.execute(f"SELECT * FROM candidate WHERE nic = '{nic}'")

            reg_candidate_details = cursor.fetchall()
            for n in range(len(reg_candidate_details)):
                for i in range(len(reg_candidate_details[n])):
                    print(reg_candidate_details[n][i])
                print("\n\n")

            ans = input("Are you sure delete this candidate (Y/N): ")
            if ans.lower() == "y":
                cursor.execute(f"DELETE FROM candidate WHERE  nic = '{nic}'")
                con.commit()
                print("deleted this record(s) !")
            else:
                print("Not deleted.")
                main_interface()

        if ans1 == 2:
            ans = input("Are you sure delete this candidate (Y/N): ")
            if ans.lower() == "y":
                cursor.execute(f"DELETE FROM candidate WHERE 1")
                con.commit()
                print("deleted records !")
                main_interface()
            else:
                print("Not deleted.")
                main_interface()



candi2 = Candidate("", "", "", "", "", "", "", "")


def vote():
    candi2.display_all_candidate()

    cursor.execute("SELECT province FROM citizen")
    citizen_province = cursor.fetchall()

    last_citizen_province = citizen_province[len(citizen_province) - 1]

    try:
        vote1 = int(input("Enter your first vote using competing number: "))
        vote2 = int(input("Enter your second vote using competing number: "))
        vote3 = int(input("Enter your third vote using competing number: "))

        cursor.execute(f"SELECT province, votes FROM candidate WHERE number = '{vote1}'")
        candidate_detail = cursor.fetchall()
        vote1_province = candidate_detail[0][0]
        vote1_votes = candidate_detail[0][1]

        cursor.execute(f"SELECT province, votes FROM candidate WHERE number = '{vote2}'")
        candidate_detail = cursor.fetchall()
        vote2_province = candidate_detail[0][0]
        vote2_votes = candidate_detail[0][1]

        cursor.execute(f"SELECT province, votes FROM candidate WHERE number = '{vote3}'")
        candidate_detail = cursor.fetchall()
        vote3_province = candidate_detail[0][0]
        vote3_votes = candidate_detail[0][1]

        vote_province_array = (vote1_province, vote2_province, vote3_province)

        if (vote1 == vote2) | (vote3 == vote1) | (vote3 == vote2):
            print("you cannot same votes more than one")
            vote()
        else:
            if check_value.check_same_value(last_citizen_province, vote_province_array):
                vote1_votes = vote1_votes + 1
                vote2_votes = vote2_votes + 1
                vote3_votes = vote3_votes + 1

                cursor.execute(f"UPDATE candidate SET votes = {vote1_votes} WHERE number = '{vote1}'")
                con.commit()
                cursor.execute(f"UPDATE candidate SET votes = {vote2_votes} WHERE number = '{vote2}'")
                con.commit()
                cursor.execute(f"UPDATE candidate SET votes = {vote3_votes} WHERE number = '{vote3}'")
                con.commit()
                print(cursor.rowcount, " votes are successfully")

            else:
                print("citizen can vote only once in his state/province")
                vote()
    except:
        print("enter correct numbers")
        vote()


def check_reg_nic(usr_nic):
    cursor.execute("SELECT nic FROM citizen")
    nic = cursor.fetchall()
    reg_nic = nic
    for n in range(len(reg_nic)):
        if usr_nic == reg_nic[n][0]:
            return True


class view_result:
    def __init__(self):
        cursor.execute("SELECT name, votes, party FROM candidate")
        self.result = cursor.fetchall()

    def candidate_result(self):

        names = []
        votes = []
        for n in range(len(self.result)):
            names.append(self.result[n][0])
            votes.append(self.result[n][1])

        x = np.array(names)
        y = np.array(votes)

        plt.bar(x, y, width=0.1)
        plt.show()

    def party_result(self):
        sum_vote = 0
        party_votes = []
        for i in range(len(party)):
            for n in range(len(self.result)):
                if party[i] == self.result[n][2]:
                    sum_vote += self.result[n][1]
            party_votes.append(sum_vote)
            sum_vote = 0

        x = np.array(party)
        y = np.array(party_votes)

        plt.bar(x, y, width=0.1)
        plt.show()


def main_interface():
    print("\t\t\t\t+++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("\t\t\t\t\t\t\t\tELECTION VOTING SYSTEM")
    print("\t\t\t\t+++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("\t\t\t0 - View party\n"
          "\t\t\t1 - Citizen register/delete\n"
          "\t\t\t2 - Candidate register/delete\n"
          "\t\t\t3 - View election results\n\n"
          "\t\t\t4 - Voting\n"
          "\t\t\t5 - exit\n\n")

    usr_in = int(input("Enter your choice: "))
    if usr_in == 0:
        for p in range(len(party)):
            print(party[p])

    if usr_in == 1:
        print("\n\t\t1 - Register\n"
              "\t\t2 - Delete\n")
        usr_in = int(input("Enter your choice: "))
        usr_reg = User_register()
        if usr_in == 1:
            usr_reg.citizen_register()
        if usr_in == 2:
            usr_reg.citizen_delete()

    if usr_in == 2:
        print("\n\t\t1 - Register\n"
              "\t\t2 - Delete\n")
        usr_in = int(input("Enter your choice: "))
        usr_reg1 = User_register()
        if usr_in == 1:
            usr_reg1.candidate_register()
        if usr_in == 2:
            usr_reg1.candidate_delete()

    if usr_in == 3:
        usr_nic = input("Enter your nic number: ")
        if check_reg_nic(usr_nic):
            vote()
        else:
            print("Not registered")

    if usr_in == 3:
        print("\n\t\t1 - Election results of candidates\n"
              "\t\t2 - Election results of parties\n")
        usr_in = int(input("Enter your choice: "))
        result = view_result()

        if usr_in == 1:
            result.candidate_result()

        if usr_in == 2:
            result.party_result()
    if usr_in == 5:
        exit(1)


main_interface()
