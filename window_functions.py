import tkinter as tk


global _str_cmd_out 

def get_cmd_string(status, msg):
    global _str_cmd_out 

    _str_cmd_out = ""
    
    print("the ",status.get(), ":\n message", msg)

    # str_cmd_out = f'DISPLAY=:0 zenity --{status.get()} --text="{msg}"'

    
    cmd = f'''GUI_USER=$(loginctl list-sessions --no-legend | awk '$4=="seat0" && $6=="active" {{print $3; exit}}'); \
    [ -n "$GUI_USER" ] && sudo -u "$GUI_USER" DISPLAY=:0 XAUTHORITY=/home/$GUI_USER/.Xauthority zenity --info --text="{msg}" || echo "No active GUI session"'''
    

    print(cmd)
        
    print("final command: ", str_cmd_out)
    
    
def pop_up_question_for_send_msg(main_frame):

    global  _str_cmd_out

    pop_up_window = tk.Toplevel(main_frame)
    pop_up_window.geometry("300x300")
    pop_up_window.resizable(False, False)
    pop_up_window.grab_set()
    
    selected_status = tk.StringVar(value="info")
    options   = ["info", "warning", "error", "progress"]
    
    text_area = tk.Text(pop_up_window)
    dropmenu  = tk.OptionMenu(pop_up_window, selected_status, *options)
    ok_btn    = tk.Button(pop_up_window, text = "OK", command= lambda: get_cmd_string(selected_status, text_area.get("1.0", "end"))) 
        

    
    dropmenu.pack(side= "top", fill = "x")
    ok_btn.pack(side="bottom")
    text_area.pack(fill= "x")

    pop_up_window.focus_set()
    
    main_frame.wait_window(pop_up_window)
    return _str_cmd_out 




# main_frame = tk.Tk()
# main_frame.geometry("300x300")
# 
# 
# open_pop_up = tk.Button(main_frame, text= "open", command = lambda:pop_up_question_for_send_msg(main_frame))
# open_pop_up.pack()
# 
# 
# main_frame.mainloop()



cmd = f'''GUI_USER=$(loginctl list-sessions --no-legend | awk '$4=="seat0" && $6=="active" {{print $3; exit}}'); \
[ -n "$GUI_USER" ] && sudo -u "$GUI_USER" DISPLAY=:0 XAUTHORITY=/home/$GUI_USER/.Xauthority zenity --info --text="hello" || echo "No active GUI session"'''


print(cmd)
    
