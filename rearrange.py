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
