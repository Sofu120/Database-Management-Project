# main.py
import eel
from views.models.employee import showallrecords, save_newemployee, show_selectedEmployee, update_newemployee, \
    show_deleteEmployee
import pyautogui  # https://pypi.org/project/PyAutoGUI/

eel.init('views')


@eel.expose
def fetchalldata():
    select_reg = showallrecords()
    eel.action_out(select_reg)


@eel.expose
def btn_save(name, position, office):
    msg = save_newemployee(name, position, office)
    eel.save_return(str(msg))


@eel.expose
def get_employee(id):
    select_employee = show_selectedEmployee(id)
    eel.action_edit(select_employee)


@eel.expose
def btn_update(name, position, office, id):
    msg = update_newemployee(name, position, office, id)
    eel.update_return(str(msg))


@eel.expose
def get_delete_employee(id):
    select_del_employee = show_deleteEmployee(id)
    eel.delete_return(select_del_employee)


eel.start(
    'templates/employee.html',
    size=pyautogui.size()
)