# Procare Productivity Tool
# Started 7/13/16 by Thomas Calhoun

import csv

print("////////////////////   PROCARE PRODUCTIVITY TOOL   \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\".center(80))
print("APP VER. 0.2b (alpha) ......................... 7/18/2016 *TJC".center(80))

changelog = """
# -=CHANGELOG=- ########################################################################################################
# 0.3b (7/xx/16) CSV Save capabilities !!FUTURE RELEASE!! Note
# 0.2b (7/18/16) Application functional, no longer in Alpha phase as UI and data iteration seems to works smoothly.
# 0.1a (7/13/16) Alpha - First Build. Formula for percentage calculations implemented. No data input on this version.
########################################################################################################################
"""

# ---/// Variables \\\---

# Efficiency Goals in Minutes
goal_beds = 35
goal_o2_w_portable = 45
goal_o2_no_portable = 25
goal_hospice_sm = 15
goal_hospice_lg = 30
goal_hospital_dc = 20

goal_details = {
    goal_beds: "Hospital Bed Setup",
    goal_o2_w_portable: "Home Oxygen, with Portable System",
    goal_o2_no_portable: "Home Oxygen, without Portable",
    goal_hospice_sm: "Hospice Delivery, Small",
    goal_hospice_lg: "Hospice Delivery, Large",
    goal_hospital_dc: "Hospital Discharge"
}

# Local value variables
setup = False
rte_date = "6-1-1999"
driver_id = "Test Driver"
stop_num = 1
driver_num_stops = 3
route_detail_ex = {  # Detail Example only, meant to help redesign the format for recording information.
    1: ["19255", goal_o2_no_portable, 32, goal_details.get(goal_o2_no_portable)],
    2: ["10329", goal_hospital_dc, 14, goal_details.get(goal_hospital_dc)],
    3: ["21299", goal_beds, 55, goal_details.get(goal_beds)],
}
route_detail = {}

# Text Variables defined ahead of time, for cleaner functions.

menuTitle = "=*= Main Menu =*="
menuDataPreview = "Data Available for {} Driver(s). Total of {} deliveries, averaging {}% efficiency."  # .format()
menuTxt = """   Please choose from the following:
    1 -------------------- Input Data (Drivers and Stops)
    2 -------------------- View Current Data (Details)
    3 -------------------- Save Current Data (CSV File, Excel Compatible)
    4 -------------------- Application Info

    0 -------------------- Exit

    Selection >>> """


def app_info():
    print("This program is designed to serve as a tool to help".center(80))
    print("determine productivity in a DME Distribution environment.".center(80))
    print()
    print("Efficiency Standards are set for various types of".center(80))
    print("deliveries, from a full Oxygen setup to a resupply delivery.".center(80), "\n\n")

    print("""Planned features coming soon:
Near - Data file iteration. Hope to use .CSV excel-compatible documents to automate data handling.
Distant - GUI Interface. Lets face it, command prompt programs don't make the big bucks. (Close as ver 2.0)
Far, Far Away - Re-work in another programming language and compile to a universal .exe file. (Close as ver 3.0)
    The reason, is that this program is coded in the Python Language - one that requires a local
    interpreter to be installed (similar to Java, just less widespread and implemented.
    I hope to redevelop in either C++ or Java.

        """)
    print(changelog)
    print("Developed By:".center(80), "\n\n", "Thomas J Calhoun".center(80), "\n", "thomas@procarehm.com".center(80),
          "\n", "john.fullmetaljacket@gmail.com".center(80))


def user_input():
    global rte_date, driver_id, driver_num_stops, route_detail, setup
    """
    Function to establish values for performance comparison.
    :return:
    """
    print("\nPlease enter data in the fields below.\n")
    rte_date = str(input("Route Date: "))
    driver_id = input("Driver Name: ")
    driver_num_stops = int(input("Number of Stops on this route: "))  # going to use this later

    print("\n\n\n")

    def route_builder():
        global stop_num, driver_num_stops, route_detail
        print("\n\n", "^" * 80)
        print("=*= Route Detail Entry =*=".center(80), "\n\n")
        print("Driver: {}".format(driver_id))

        while True:
            print("\n", "Driver Stop input".center(80), "\n")
            print("""A - Hospital Bed
B - Oxygen, with Portable System
C - Oxygen, without Portable
D - Hospice, Small (DME items, Nebulizers, etc...)
E - Hospice, Large (Hosp Bed, Full O2 setup)
F - Hospital Discharge

X - (Exit This Menu)
                """)
            stop_type_d = None
            stop_type_r = None
            stop_type = input("Stop Type: ").lower()
            stop_ord = int(input("Order # Reference: "))
            stop_dur = int(input("Stop Duration: "))

            if stop_type == "a":
                stop_type_r = goal_beds
                stop_type_d = goal_details.get(goal_beds)
            elif stop_type == "b":
                stop_type_r = goal_o2_w_portable
                stop_type_d = goal_details.get(goal_o2_w_portable)
            elif stop_type == "c":
                stop_type_r = goal_o2_no_portable
                stop_type_d = goal_details.get(goal_o2_no_portable)
            elif stop_type == "d":
                stop_type_r = goal_hospice_sm
                stop_type_d = goal_details.get(goal_hospice_sm)
            elif stop_type == "e":
                stop_type_r = goal_hospice_lg
                stop_type_d = goal_details.get(goal_hospice_lg)
            elif stop_type == "f":
                stop_type_r = goal_hospital_dc
                stop_type_d = goal_details.get(goal_hospital_dc)
            elif stop_type == "x": break
            else: route_builder()

            route_detail[stop_num] = [stop_ord, stop_type_r, stop_dur, stop_type_d]

            driver_num_stops -= 1
            stop_num += 1

            if driver_num_stops == 0: break

    route_builder()
    setup = True


def calculation():
    all_stops_perc = []
    print("\n\n")
    for stop in route_detail.values():
        ord = stop[0]
        goal = stop[1]
        actual = stop[2]
        description = stop[3]
        performance = 100 * float(goal) / float(actual)
        print("{}'s stop time performance on {} is:\n"
              ">>    {}% ({} in {} minutes.)\n".format(driver_id, ord, int(performance), description, actual))
        all_stops_perc.append(performance)
        #route_detail[stop].insert(description)

    all_stops_avg = sum(all_stops_perc) / len(all_stops_perc)
    print("\n\nFor Driver: {}         Date: {}".format(driver_id, rte_date))
    print("Route Performance Average:    {}% in {} stops.".format(int(all_stops_avg), len(all_stops_perc)), "\n")
    input("Press enter to continue...".center(80))


def save_data():
    with open("ProCareHM_Driver_productivity{}.csv".format(rte_date), "w") as f:
        w = csv.writer(f, dialect='excel', delimiter=" ")
        w.writerows([driver_id])
        w.writerows([rte_date])
        w.writerows(["Stop#/Order# TimeGoal TimeActual Description Goal%"])
        w.writerows(route_detail.items())
    f.close()


def menu():  # Initializes functions defined above

    def start_input():  # Nested Starters for better error handling, to prevent a force restart of the program.
        try:
            user_input()
        except Exception as err:
            print("\n\nOh No! The following error was encountered:\n{}\nCheck your input and try again\n\n".format(err))
            start_input()

    def start_calculation():
        try:
            calculation()  # !!! Test values for arguments at the moment.
        except Exception as err:
            print("\n\nOh No! The following error was encountered:\n{}\nCheck your input and try again\n\n".format(err))
            start_calculation()

    def start_save_file():
        try:
            save_data()
        except Exception as err:
            print("\n\nOh No! The following error was encountered:\n{}\nCheck your input and try again\n\n".format(err))
            start_save_file()

    while True:
        print("\n\n", menuTitle.center(80), "\n\n")
        menu_selection = int(input(menuTxt))
        if menu_selection == 1:
            start_input()
        elif menu_selection == 2:
            if setup == True: start_calculation()
            else: print("\n\nWoa! You need to setup some data first!\n\n")
        elif menu_selection == 3:
            start_save_file()
            print("\n\nSave Complete!\n\n")
        elif menu_selection == 4:
            app_info()
        elif menu_selection == 9:
            global route_detail, setup
            print("\n\n\n", "///// PRESET DATA PREVIEW - TESTING ONLY!!! \\\\\\\\\\".center(80), "\n")
            route_detail = route_detail_ex
            setup = True
            start_calculation()
        elif menu_selection == 0:
            break
        else:
            print("\n\n", "Error! Selection not recognized, please try again!".center(80), "\n\n")


def start():  # error handling for main menu

    try:
        menu()
    except Exception as err:
        print("\n\nOh No! The following error was encountered:\n{}\nCheck your input and try again\n\n".format(err))
        start()

start()
