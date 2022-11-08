from operator import itemgetter

def main():
    file = open('/home/petersjg/windows_directory/fimoDifferences.txt', 'r')
    echo_list = []
    non_echo_list = []
    for line in file:
        if 'ECO' in line:
            echo_list.append(line)
        else:
            non_echo_list.append(line)
            
    new_eco_list = []
    for eco in echo_list:
        split_eco = eco.split()
        new_eco_list.append((split_eco[0], int(split_eco[1]), split_eco[2]))

    new_neco_list = []
    for neco in non_echo_list:
        split_eco = neco.split()
        new_neco_list.append((split_eco[0], int(split_eco[1]), split_eco[2]))
    
    new_eco_list.sort(key=itemgetter(1))
    new_neco_list.sort(key=itemgetter(1))
    
    outstr = ""
    for eco in new_eco_list:
        outstr += str(eco[0]) + ' ' + str(eco[1]) + ' ' + str(eco[2]) + '\n'
    print(outstr)
    outstr = ""
    for neco in new_neco_list:
        outstr += str(neco[0]) + ' ' + str(neco[1]) + ' ' + str(neco[2]) + '\n'
    print(outstr)
    
    return
    
main()