def grid_arrange(main_frame, list_of_elements):

    pos_x=0
    pos_y=0

    main_frame.update()
    max_width = main_frame.winfo_width()
    max_height= main_frame.winfo_height()

    print("max height :", max_height)
    print("max width  :", max_width)

    print("list of elements len:", len(list_of_elements))
    for element in list_of_elements:

        element.place(x=pos_x, y=pos_y)
        main_frame.update()
        pos_x += element.winfo_width()
        if(pos_x > max_width):
            pos_x = 0
            pos_y += element.winfo_height()
            element.place(x = pos_x, y = pos_y)


def ribbon_style(main_frame, list_of_elements):

    pos_x =0
    pos_y =0
    rel_x =0
    #print("After: ",len(list_of_elements))
    for element in list_of_elements:

     #   print("w:",element.winfo_width())
        if (element.winfo_width() == 2):
            print("got a frame seprators")
            element.place(x = pos_x + rel_x, y = pos_y)
            pos_x = pos_x + rel_x + 2
            pos_y = 0
            continue
            
        element.place(x = pos_x, y = pos_y)
        pos_y += element.winfo_height()

        if (rel_x < element.winfo_width()):
            rel_x = element.winfo_width()


def basic_frame_v_pack(frame, list_of_elements):

    for element in list_of_elements:
        element.pack(side="top", fil="x")

    
def basic_frame_h_pack(frame, list_of_elements):

    for element in list_of_elements:
        element.pack(side="left", fil="x")

def basic_frame_hv_pack(frame, list_of_list_elements):

    c_row = 0
    c_col = 0
    
    for l in list_of_list_elements:
        c_col = 0
            
        for element in l:
            element.grid(row=c_row, column=c_col)
            c_col = c_col + 1

        c_row = c_row + 1    
        
