#-*- coding:utf-8 -*-
import MySQLdb
import json
import traceback

review_table = 'amazon_audio_3w_info'
member_table = 'amazon_audio_3w_member'
product_table = 'amazon_audio_3w_product'
output_name = 'amazon_audio_3w_raw_profile.txt'

def read_file(file_name):
    f = open(file_name)
    lines = f.readlines()
    return lines

def read_member_product_info(all_member_info, all_product_info):
    lines = read_file('/misc/projdata4/info_fil/bshi/Data/review/bing_liu/amazon-memberinfo-locations.txt')
    for line in lines:
        content = line.strip()
        t_lines = [l.strip() for l in line.split('\t')]
        if len(t_lines) > 6:
            username = t_lines[0]
            member_rank = t_lines[1]
            birthday = t_lines[2]
            location = t_lines[3]
            name = t_lines[4]
            member_id = t_lines[5]
            state = t_lines[6]
            content = 'usename:' + username + '\t' + 'member_rank:' + member_rank + '\t' + 'birthday:' + birthday + '\t' + 'location:' + location + '\t' + 'name:' + name + '\t' + 'member_id:' + member_id + '\t' + 'state:' + state
            all_member_info[str(member_id)] = content

    lines = read_file('/misc/projdata4/info_fil/bshi/Data/review/bing_liu/productInfoXML-reviewed-AudioCDs.txt')
    t_content = ''
    product_id = ''
    for line in lines:
        t_lines = [l.strip() for l in line.split('\t')]
        if len(t_lines)==4:
            product_id = t_lines[0]
            sales_rank = t_lines[1]
            label = t_lines[2]
            sales_price = t_lines[3]
            t_content += 'product_id:' + product_id + '\t' + 'sales_rank:' + sales_rank + '\t' + 'label:' + label + '\t' + 'sales_price:' + sales_price
        elif len(t_lines)==1:
            t_content = ''
        else:
            t_content += '\t' + line.strip()
            if product_id:
                all_product_info[product_id] = t_content
                t_content = ''
                product_id = ''
        
def output_txt(conn, file_name, all_member_info, all_product_info):
    raw_f = open(file_name, 'w')
    raw_f.close()
    raw_f = open(file_name, 'a')
    try:
        sql = 'select * from ' + review_table
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(sql)
        rows = cur.fetchall()
        i = 0
        for r in rows:
            i += 1
            if i % 100==0:
                print i
            sql2 = 'select * from ' + member_table +' where member_id=%s'
            sql3 = 'select * from ' + product_table + ' where product_id=%s'
            member_id = r['member_id'].encode('utf-8')
            product_id = r['product_id'].encode('utf-8')
            id = r['id']
            raw_body = r['body'].replace('\n', ' ').replace('\r', '')
            post_body= r['post_body'].replace('\n', ' ').replace('\r', '')
            DUP = r['DUP']
            EXT = r['EXT']
            DEV = r['DEV']
            ETF = r['ETF']
            RA = r['RA']
            is_J = r['is_J']
            is_burst = r['is_burst']
            helpful_score = r['helpful_score']
            rating = r['rating']
            cur.execute(sql2, (member_id,))
            r_member = cur.fetchone()
            CS = r_member['CS']
            MNR = r_member['MNR']
            BST = r_member['BST']
            RFR = r_member['RFR']
            cur.execute(sql3, (product_id,))
            r_product = cur.fetchone()
            p_CS = r_product['p_CS']
            p_MNR = r_product['p_MNR']
            p_BST = r_product['p_BST']
            p_RFR = r_product['p_RFR']
            t_list = [member_id, product_id, rating, helpful_score, DUP, EXT, DEV, ETF, RA, CS, MNR, BST, RFR, is_J, is_burst, p_CS, p_MNR, p_BST, p_RFR]
            content_raw = '\t'.join(str(x) for x in t_list) + '\n'
            content_raw += raw_body.strip() + '\n'
            if member_id in all_member_info:
                try:
                    content_raw += all_member_info[member_id].strip() + '\n'
                except UnicodeDecodeError:
                    content_raw += member_id + '\tDecode Error!' + '\n'
            else:
                content_raw += member_id + ' No Contents\n'
            if product_id in all_product_info:
                try:
                    content_raw += all_product_info[product_id].strip() + '\n'
                except UnicodeDecodeError:
                    content_raw += product_id + '\tDecode Error!' + '\n'
            else:
                content_raw += product_id + ' No Contents\n'
            if type(content_raw) == unicode:
                content_raw = content_raw.encode('utf-8')
            else:
                content_raw = content_raw.decode('ascii').encode('utf-8')
            raw_f.write(content_raw)
            content_raw = ''
    except:
        traceback.print_exc()
    raw_f.close()

if __name__=='__main__':
    conn = MySQLdb.connect(host='seis10.se.cuhk.edu.hk', port=3306, user='bshi', passwd='20141031shib', db='bshi', charset='utf8')
    all_member_info = {}
    all_product_info = {}
    read_member_product_info(all_member_info, all_product_info)
    output_txt(conn, output_name, all_member_info, all_product_info)