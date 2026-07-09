def group_list(initial_list,group_size=4):
    grouped_list=[]
    group_range=range(0,len(initial_list),group_size)
    for i in group_range:
        grouped_list.append(initial_list[i:i+group_size])
    return grouped_list