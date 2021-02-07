import json

a = {
    'tyshxydm': '机构代码',
    'pzslsj': '成立时间',
    'zsd': '联系地址',
    'zsdh': '联系电话',
    'lsswsmc': '机构名称',
    'jj' : '简介'
}
b = {
    'zyzh': '执业证号',
    'xm': '姓名',
    'years': '执业年限',
    'lsswsmc': '机构名称',
    'PIC' : '照片'

}

# print(dept_info_list[0])
# print(len(dept_info_list))

# dept_info_list_ = []
# for dept in dept_info_list:
#     tmp = {}
#     for key in dept:
#         if a.__contains__(key):
#             tmp[a[key]] = dept[key]
#             if key == 'lsswsmc':
#                 print(dept[key])
#     dept_info_list_.append(tmp)

# lawer_list_ = []
# for lawer in lawer_list:
#     tmp = {}
#     for key in lawer:
#         if b.__contains__(key):
#             tmp[b[key]] = lawer[key]
#             if key == 'mc':
#                 print(lawer[key])
#     lawer_list_.append(tmp)
# xxx = {
#     "成立时间": "2013-03-14",
#     "联系地址": "北京市海淀区中关村南大街2号楼A座6层608-610室",
#     "联系电话": "010-57186795",
#     "机构名称": "北京群益律师事务所",
#     "机构代码": "31110000067257265U"
# }
# dept_info_list.append(xxx)
# dept_info_dict = {}
# for dept in dept_info_list:
#     if dept.__contains__('简介'):
#         dept['简介'] = dept['简介'].replace(' ', '')
#     dept_info_dict[dept['机构名称']] = dept

# print(dept_info_dict)
# for lawer in lawer_list:
#     if not dept_info_dict.__contains__(lawer['机构名称']):
#         dept_info_dict[lawer['机构名称']] = {}
#
#     if dept_info_dict[lawer['机构名称']].__contains__('lawers'):
#         try:
#             dept_info_dict[lawer['机构名称']]['lawers'][lawer['姓名']] = lawer
#         except:
#             print(lawer)
#
#     else:
#         try:
#             dept_info_dict[lawer['机构名称']]['lawers'] = {lawer['姓名']: lawer}
#         except:
#             print(lawer)

if __name__ == '__main__':
    # with open('dept_info_list_.txt', 'r', encoding='utf-8') as f:
    #     dept_info_list = eval(f.read())
    with open('lawer_list_.txt', 'r', encoding='utf-8') as f:
        lawer_list = eval(f.read())

    lawer_dcit = {}
    for lawer in lawer_list:
        if lawer.__contains__('姓名'):
            lawer_dcit[lawer['姓名']] = lawer


    # with open('dept_info_list_.txt', 'w', encoding='utf-8') as f:
    #     f.write(str(dept_info_list_))
    with open('lawer_dicts.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(lawer_dcit))