#-*- coding:utf-8 -*-
import MySQLdb
import traceback
import random
import operator

review_table = 'yelp_2w_info'
member_table = 'yelp_2w_member'
product_table = 'yelp_2w_product'

def get_member_list(conn, member_list):
    sql = 'select * from ' + member_table
    try:
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(sql)
        rows = cur.fetchall()
        for r in rows:
            member_id = r['member_id']
            member_list.append(member_id)
    except:
        traceback.print_exc()

def get_mean_variance(t_list):
    if not t_list:
        print 'empty project'
        return 0.01, 0.01
    else:
        mean = sum(t_list) / float(len(t_list))
        variance = sum((mean-value)**2 for value in t_list) / float(len(t_list))
        return mean, variance
        
def get_review_list(conn, review_list, member_review_dict, product_review_dict):
    sql = 'select * from ' + review_table
    try:
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(sql)
        rows = cur.fetchall()
        for r in rows:
            review_id = r['id']
            member_id = r['member_id']
            product_id = r['product_id']
            review_list.append(review_id)
            if member_id in member_review_dict:
                member_review_dict[member_id].append(int(review_id))
            else:
                member_review_dict[member_id] = []
                member_review_dict[member_id].append(int(review_id))
            if product_id in product_review_dict:
                product_review_dict[product_id].append(int(review_id))
            else:
                product_review_dict[product_id] = []
                product_review_dict[product_id].append(int(review_id))
    except:
        traceback.print_exc()

def save_file(file_name, content):
    f = open(file_name, 'w')
    f.write(content)
    f.close()
    
if __name__=='__main__':
    conn = MySQLdb.connect(host='seis10', port=3306, user='bshi', passwd='20141031shib', db='bshi', charset='utf8')
    member_list = []
    get_member_list(conn, member_list)
    review_list = []
    member_review_dict = {}
    product_review_dict = {}
    get_review_list(conn, review_list, member_review_dict, product_review_dict)
    review_label_list = [0,]
    for i in xrange(0, len(review_list)):
        t = random.random()
        if t < 0.5:
            review_label_list.append(0)
        else:
            review_label_list.append(1)
    
    n_max = 300
    n_m_non_dict = {}
    n_m_spam_dict = {}
    n_m_count= {}
    r_count = len(review_label_list)-1
    non_count = 0
    spam_count = 0
    non_total_count = 0
    spam_total_count = 0
    total_count = len(review_label_list)-1
    r_DUP_dict = {}
    r_spam_is_DUP_count = 0
    r_non_is_DUP_count = 0
    r_EXT_dict = {}
    r_spam_is_EXT_count = 0
    r_non_is_EXT_count = 0
    r_DEV_dict = {}
    r_spam_is_DEV_count = 0
    r_non_is_DEV_count = 0
    r_ETF_dict = {}
    r_spam_is_ETF_count = 0
    r_non_is_ETF_count = 0
    r_RA_dict = {}
    r_spam_is_RA_count = 0
    r_non_is_RA_count = 0

    r_CS_dict = {}
    pi_CS_non_1 = 0.0
    pi_CS_non_2 = 0.0
    pi_CS_spam_1 = 0.0
    pi_CS_spam_2 = 0.0
    mu_CS_non = 0.0
    mu_CS_spam = 0.0
    gema_CS_non = 0.0
    gema_CS_spam = 0.0
    CS_list_non = []
    CS_list_spam = []

    r_MNR_dict = {}
    pi_MNR_non_1 = 0.0
    pi_MNR_non_2 = 0.0
    pi_MNR_spam_1 = 0.0
    pi_MNR_spam_2 = 0.0
    mu_MNR_non = 0.0
    mu_MNR_spam = 0.0
    gema_MNR_non = 0.0
    gema_MNR_spam = 0.0
    MNR_list_non = []
    MNR_list_spam = []

    r_BST_dict = {}
    pi_BST_non_1 = 0.0
    pi_BST_non_2 = 0.0
    pi_BST_spam_1 = 0.0
    pi_BST_spam_2 = 0.0
    mu_BST_non = 0.0
    mu_BST_spam = 0.0
    gema_BST_non = 0.0
    gema_BST_spam = 0.0
    BST_list_non = []
    BST_list_spam = []
    
    r_RFR_dict = {}
    pi_RFR_non_1 = 0.0
    pi_RFR_non_2 = 0.0
    pi_RFR_spam_1 = 0.0
    pi_RFR_spam_2 = 0.0
    mu_RFR_non = 0.0
    mu_RFR_spam = 0.0
    gema_RFR_non = 0.0
    gema_RFR_spam = 0.0    
    RFR_list_non = []
    RFR_list_spam = []
    
    for member in member_list:
        r_list = member_review_dict[member]
        n_count = len(r_list)
        non_count = 0
        spam_count = 0
        sql2 = 'select * from ' + member_table + ' where member_id=%s'
        cur2 = conn.cursor(MySQLdb.cursors.DictCursor)
        cur2.execute(sql2, (member,))
        r_member=cur2.fetchone()
        CS = r_member['CS']
        if CS == 0:
            CS = 0.001
        if CS == 1:
            CS = 0.999
        MNR = r_member['MNR']
        if MNR == 0:
            MNR = 0.001
        if MNR == 1:
            MNR = 0.999
        BST = r_member['BST']
        if BST == 0:
            BST = 0.001
        if BST == 1:
            BST = 0.999
        RFR = r_member['RFR']
        if RFR == 0:
            RFR = 0.001
        if RFR == 1:
            RFR = 0.999
        for r in r_list:
            sql = 'select * from ' + review_table + ' where id=%s'
            cur =  conn.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(sql, (r,))
            row = cur.fetchone()
            DUP = row['DUP']
            EXT = row['EXT']
            DEV = row['DEV']
            ETF = row['ETF']
            RA = row['RA']
            r_DUP_dict[r] = DUP
            r_EXT_dict[r] = EXT
            r_DEV_dict[r] = DEV
            r_ETF_dict[r] = ETF
            r_RA_dict[r] = RA
            r_CS_dict[r] = CS
            r_MNR_dict[r] = MNR
            r_BST_dict[r] = BST
            r_RFR_dict[r] = RFR
            if review_label_list[r]==1:
                spam_total_count += 1
                spam_count += 1
                if DUP==1:
                    r_spam_is_DUP_count +=1
                if EXT==1:
                    r_spam_is_EXT_count +=1
                if DEV==1:
                    r_spam_is_DEV_count +=1
                if ETF==1:
                    r_spam_is_ETF_count +=1
                if RA==1:
                    r_spam_is_RA_count +=1
                CS_list_spam.append(CS)
                MNR_list_spam.append(MNR)
                BST_list_spam.append(BST)
                RFR_list_spam.append(RFR)
            else:
                non_total_count += 1
                non_count += 1
                if DUP==1:
                    r_non_is_DUP_count +=1
                if EXT==1:
                    r_non_is_EXT_count +=1
                if DEV==1:
                    r_non_is_DEV_count +=1
                if ETF==1:
                    r_non_is_ETF_count +=1
                if RA==1:
                    r_non_is_RA_count +=1
                CS_list_non.append(CS)
                MNR_list_non.append(MNR)
                BST_list_non.append(BST)
                RFR_list_non.append(RFR)
                    
        n_m_non_dict[member] = non_count
        n_m_spam_dict[member] = spam_count
        n_m_count[member] = n_count

    mu_CS_non, gema_CS_non = get_mean_variance(CS_list_non)
    mu_CS_spam, gema_CS_spam = get_mean_variance(CS_list_spam)
    print 'u_CS_non: %f, %f' %(mu_CS_non, gema_CS_non)
    print 'u_CS_spam: %f, %f' %(mu_CS_spam, gema_CS_spam)
    mu_MNR_non, gema_MNR_non = get_mean_variance(MNR_list_non)
    mu_MNR_spam, gema_MNR_spam = get_mean_variance(MNR_list_spam)
    print 'u_MNR_non: %f, %f' %(mu_MNR_non, gema_MNR_non)
    print 'u_MNR_spam: %f, %f' %(mu_MNR_spam, gema_MNR_spam)
    mu_BST_non, gema_BST_non = get_mean_variance(BST_list_non)
    mu_BST_spam, gema_BST_spam = get_mean_variance(BST_list_spam)
    print 'u_BST_non: %f, %f' %(mu_BST_non, gema_BST_non)
    print 'u_BST_spam: %f, %f' %(mu_BST_spam, gema_BST_spam)
    mu_RFR_non, gema_RFR_non = get_mean_variance(RFR_list_non)
    mu_RFR_spam, gema_RFR_spam = get_mean_variance(RFR_list_spam)
    print 'u_RFR_non: %f, %f' %(mu_RFR_non, gema_RFR_non)
    print 'u_RFR_spam: %f, %f' %(mu_RFR_spam, gema_RFR_spam)

    pi_CS_non_1 = mu_CS_non * (mu_CS_non * (1 - mu_CS_non) / gema_CS_non - 1)
    pi_CS_non_2 = (1-mu_CS_non) * (mu_CS_non * (1 - mu_CS_non) / gema_CS_non - 1)
    pi_CS_spam_1 = (mu_CS_spam) * (mu_CS_spam * (1 - mu_CS_spam) / gema_CS_spam - 1)
    pi_CS_spam_2 = (1-mu_CS_spam) * (mu_CS_spam * (1 - mu_CS_spam) / gema_CS_spam - 1)
    #pi_CS_non_1 = 0.5
    #pi_CS_non_2 = 3
    #pi_CS_spam_1 = 3.0
    #pi_CS_spam_2 = 1.0
    print 'non_CS: %f, %f' % (pi_CS_non_1, pi_CS_non_2)
    print 'spam_CS: %f, %f' % (pi_CS_spam_1, pi_CS_spam_2)

    pi_MNR_non_1 = mu_MNR_non * (mu_MNR_non * (1 - mu_MNR_non) / gema_MNR_non - 1)
    pi_MNR_non_2 = (1-mu_MNR_non) * (mu_MNR_non * (1 - mu_MNR_non) / gema_MNR_non - 1)
    pi_MNR_spam_1 = (mu_MNR_spam) * (mu_MNR_spam * (1 - mu_MNR_spam) / gema_MNR_spam - 1)
    pi_MNR_spam_2 = (1-mu_MNR_spam) * (mu_MNR_spam * (1 - mu_MNR_spam) / gema_MNR_spam - 1)
    #pi_MNR_non_1 = 2
    #pi_MNR_non_2 = 20
    #pi_MNR_spam_1 = 2
    #pi_MNR_spam_2 = 2
    print 'non_MNR: %f, %f' % (pi_MNR_non_1, pi_MNR_non_2)
    print 'spam_MNR: %f, %f' % (pi_MNR_spam_1, pi_MNR_spam_2)
    
    pi_BST_non_1 = mu_BST_non * (mu_BST_non * (1 - mu_BST_non) / gema_BST_non - 1)
    pi_BST_non_2 = (1-mu_BST_non) * (mu_BST_non * (1 - mu_BST_non) / gema_BST_non - 1)
    pi_BST_spam_1 = (mu_BST_spam) * (mu_BST_spam * (1 - mu_BST_spam) / gema_BST_spam - 1)
    pi_BST_spam_2 = (1-mu_BST_spam) * (mu_BST_spam * (1 - mu_BST_spam) / gema_BST_spam - 1)
    #pi_BST_non_1 = 0.5
    #pi_BST_non_2 = 3
    #pi_BST_spam_1 = 10
    #pi_BST_spam_2 = 2
    print 'non_BST: %f, %f' % (pi_BST_non_1, pi_BST_non_2)
    print 'spam_BST: %f, %f' % (pi_BST_spam_1, pi_BST_spam_2)
    
    pi_RFR_non_1 = mu_RFR_non * (mu_RFR_non * (1 - mu_RFR_non) / gema_RFR_non - 1)
    pi_RFR_non_2 = (1-mu_RFR_non) * (mu_RFR_non * (1 - mu_RFR_non) / gema_RFR_non - 1)
    pi_RFR_spam_1 = (mu_RFR_spam) * (mu_RFR_spam * (1 - mu_RFR_spam) / gema_RFR_spam - 1)
    pi_RFR_spam_2 = (1-mu_RFR_spam) * (mu_RFR_spam * (1 - mu_RFR_spam) / gema_RFR_spam - 1)
    #pi_RFR_non_1 = 2
    #pi_RFR_non_2 = 5
    #pi_RFR_spam_1 = 0.5
    #pi_RFR_spam_2 = 0.5
    print 'non_RFR: %f, %f' % (pi_RFR_non_1, pi_RFR_non_2)
    print 'spam_RFR: %f, %f' % (pi_RFR_spam_1, pi_RFR_spam_2)
    
    for i in xrange(0, n_max):
        print 'the %dth iteration' %(i,)
        print 'spam_total_count', str(spam_total_count), 'non_total_count', str(non_total_count)        
        CS_list_non = []
        CS_list_spam = []
        MNR_list_non = []
        MNR_list_spam = []
        BST_list_non = []
        BST_list_spam = []
        RFR_list_non = []
        RFR_list_spam = []
        for j in member_list:
            t_non_count = n_m_non_dict[j]
            t_spam_count = n_m_spam_dict[j]
            for k in member_review_dict[j]:
                if review_label_list[k]==0:
                    n_m_non_dict[j] -= 1
                    non_total_count -= 1
                    t_non_count -= 1
                    if r_DUP_dict[k]==1:
                        r_non_is_DUP_count -= 1
                    if r_EXT_dict[k]==1:
                        r_non_is_EXT_count -= 1
                    if r_DEV_dict[k]==1:
                        r_non_is_DEV_count -= 1
                    if r_ETF_dict[k]==1:
                        r_non_is_ETF_count -= 1
                    if r_RA_dict[k]==1:
                        r_non_is_RA_count -= 1
                else:
                    spam_total_count -= 1
                    n_m_spam_dict[j] -=1
                    t_spam_count -= 1
                    if r_DUP_dict[k]==1:
                        r_spam_is_DUP_count -= 1
                    if r_EXT_dict[k]==1:
                        r_spam_is_EXT_count -= 1
                    if r_DEV_dict[k]==1:
                        r_spam_is_DEV_count -= 1
                    if r_ETF_dict[k]==1:
                        r_spam_is_ETF_count -= 1
                    if r_RA_dict[k]==1:
                        r_spam_is_RA_count -= 1
                first_factor_non= (n_m_non_dict[j] + 50) / float(n_m_count[j] -1 + 100)
                first_factor_spam = (n_m_spam_dict[j] + 50) / float(n_m_count[j] - 1 + 100)
                if review_label_list[k] == 0:
                    t_non_count += 1
                else:
                    t_spam_count += 1
                #print first_factor_non, first_factor_spam, t_non_count, t_spam_count, n_m_count[j]
                sf_DUP_non=0.0
                if r_DUP_dict[k]==1:
                    sf_DUP_non = (r_non_is_DUP_count + 1) / float(non_total_count + 2)
                else:
                    sf_DUP_non = (non_total_count - r_non_is_DUP_count + 1) / float(non_total_count + 2)
                sf_DUP_spam=0.0
                if r_DUP_dict[k]==1:
                    sf_DUP_spam = (r_spam_is_DUP_count + 1) / float(spam_total_count + 2)
                else:
                    sf_DUP_spam = (spam_total_count - r_spam_is_DUP_count + 1) / float(spam_total_count + 2)
                    
                sf_EXT_non=0.0
                if r_EXT_dict[k]==1:
                    sf_EXT_non = (r_non_is_EXT_count + 1) / float(non_total_count + 2)
                else:
                    sf_EXT_non = (non_total_count - r_non_is_EXT_count + 1) / float(non_total_count + 2)
                sf_EXT_spam=0.0
                if r_EXT_dict[k]==1:
                    sf_EXT_spam = (r_spam_is_EXT_count + 1) / float(spam_total_count + 2)
                else:
                    sf_EXT_spam = (spam_total_count - r_spam_is_EXT_count + 1) / float(spam_total_count + 2)
                    
                sf_DEV_non=0.0
                if r_DEV_dict[k]==1:
                    sf_DEV_non = (r_non_is_DEV_count + 1) / float(non_total_count + 2)
                else:
                    sf_DEV_non = (non_total_count - r_non_is_DEV_count + 1) / float(non_total_count + 2)
                sf_DEV_spam=0.0
                if r_DEV_dict[k]==1:
                    sf_DEV_spam = (r_spam_is_DEV_count + 1) / float(spam_total_count + 2)
                else:
                    sf_DEV_spam = (spam_total_count - r_spam_is_DEV_count + 1) / float(spam_total_count + 2)

                sf_ETF_non=0.0
                if r_ETF_dict[k]==1:
                    sf_ETF_non = (r_non_is_ETF_count + 1) / float(non_total_count + 2)
                else:
                    sf_ETF_non = (non_total_count - r_non_is_ETF_count + 1) / float(non_total_count + 2)
                sf_ETF_spam=0.0
                if r_ETF_dict[k]==1:
                    sf_ETF_spam = (r_spam_is_ETF_count + 1) / float(spam_total_count + 2)
                else:
                    sf_ETF_spam = (spam_total_count - r_spam_is_ETF_count + 1) / float(spam_total_count + 2)

                sf_RA_non=0.0
                if r_RA_dict[k]==1:
                    sf_RA_non = (r_non_is_RA_count + 1) / float(non_total_count + 2)
                else:
                    sf_RA_non = (non_total_count - r_non_is_RA_count + 1) / float(non_total_count + 2)
                sf_RA_spam=0.0
                if r_RA_dict[k]==1:
                    sf_RA_spam = (r_spam_is_RA_count + 1) / float(spam_total_count + 2)
                else:
                    sf_RA_spam = (spam_total_count - r_spam_is_RA_count + 1) / float(spam_total_count + 2)

                td_CS_non = pow(r_CS_dict[k], pi_CS_non_1-1) * pow(1-r_CS_dict[k], pi_CS_non_2-1)
                td_CS_spam = pow(r_CS_dict[k], pi_CS_spam_1-1) * pow(1-r_CS_dict[k], pi_CS_spam_2-1)
                td_MNR_non = pow(r_MNR_dict[k], pi_MNR_non_1-1) * pow(1-r_MNR_dict[k], pi_MNR_non_2-1)
                td_MNR_spam = pow(r_MNR_dict[k], pi_MNR_spam_1-1) * pow(1-r_MNR_dict[k], pi_MNR_spam_2-1)
                td_BST_non = pow(r_BST_dict[k], pi_BST_non_1-1) * pow(1-r_BST_dict[k], pi_BST_non_2-1)
                td_BST_spam = pow(r_BST_dict[k], pi_BST_spam_1-1) * pow(1-r_BST_dict[k], pi_CS_spam_2-1)
                td_RFR_non = pow(r_RFR_dict[k], pi_RFR_non_1-1) * pow(1-r_RFR_dict[k], pi_RFR_non_2-1)
                td_RFR_spam = pow(r_RFR_dict[k], pi_RFR_spam_1-1) * pow(1-r_RFR_dict[k], pi_RFR_spam_2-1)
                #prob_non = first_factor_non *  sf_DUP_non * sf_EXT_non * sf_DEV_non * sf_ETF_non * sf_RA_non * td_CS_non * td_MNR_non * td_BST_non * td_RFR_non
                prob_non = first_factor_non * sf_DUP_non * sf_EXT_non * sf_DEV_non * sf_ETF_non * sf_RA_non * td_CS_non * td_MNR_non
                #print first_factor_non, sf_DUP_non, sf_EXT_non, sf_DEV_non, sf_ETF_non, sf_RA_non, td_CS_non, td_MNR_non, td_BST_non, td_RFR_non
                #prob_spam = first_factor_spam * sf_DUP_spam * sf_EXT_spam * sf_DEV_spam * sf_ETF_spam * sf_RA_spam * td_CS_spam * td_MNR_spam *  td_BST_spam * td_RFR_spam
                prob_spam = first_factor_spam * sf_DUP_spam * sf_EXT_spam * sf_DEV_spam * sf_ETF_spam * sf_RA_spam * td_CS_spam * td_MNR_spam
                #print first_factor_spam, sf_DUP_spam, sf_EXT_spam, sf_DEV_spam, sf_ETF_spam, sf_RA_spam, td_CS_spam, td_MNR_spam, td_BST_spam, td_RFR_spam
                if prob_non > prob_spam:
                    review_label_list[k] = 0
                    non_total_count += 1
                    n_m_non_dict[j] += 1
                    if r_DUP_dict[k]==1:
                        r_non_is_DUP_count += 1
                    if r_EXT_dict[k]==1:
                        r_non_is_EXT_count += 1
                    if r_DEV_dict[k]==1:
                        r_non_is_DEV_count += 1
                    if r_ETF_dict[k]==1:
                        r_non_is_ETF_count += 1
                    if r_RA_dict[k]==1:
                        r_non_is_RA_count += 1
                    CS_list_non.append(r_CS_dict[k])
                    MNR_list_non.append(r_MNR_dict[k])
                    BST_list_non.append(r_BST_dict[k])
                    RFR_list_non.append(r_RFR_dict[k])
                else:
                    review_label_list[k] = 1
                    n_m_spam_dict[j] += 1
                    spam_total_count += 1
                    if r_DUP_dict[k]==1:
                        r_spam_is_DUP_count += 1
                    if r_EXT_dict[k]==1:
                        r_spam_is_EXT_count += 1
                    if r_DEV_dict[k]==1:
                        r_spam_is_DEV_count += 1
                    if r_ETF_dict[k]==1:
                        r_spam_is_ETF_count += 1
                    if r_RA_dict[k]==1:
                        r_spam_is_RA_count += 1
                    CS_list_spam.append(r_CS_dict[k])
                    MNR_list_spam.append(r_MNR_dict[k])
                    BST_list_spam.append(r_BST_dict[k])
                    RFR_list_spam.append(r_RFR_dict[k])

        if i > 250:
            mu_CS_non, gema_CS_non = get_mean_variance(CS_list_non)
            mu_CS_spam, gema_CS_spam = get_mean_variance(CS_list_spam)
            print 'u_CS_non: %f, %f' %(mu_CS_non, gema_CS_non)
            print 'u_CS_spam: %f, %f' %(mu_CS_spam, gema_CS_spam)
            mu_MNR_non, gema_MNR_non = get_mean_variance(MNR_list_non)
            mu_MNR_spam, gema_MNR_spam = get_mean_variance(MNR_list_spam)
            print 'u_MNR_non: %f, %f' %(mu_MNR_non, gema_MNR_non)
            print 'u_MNR_spam: %f, %f' %(mu_MNR_spam, gema_MNR_spam)
            mu_BST_non, gema_BST_non = get_mean_variance(BST_list_non)
            mu_BST_spam, gema_BST_spam = get_mean_variance(BST_list_spam)
            print 'u_BST_non: %f, %f' %(mu_BST_non, gema_BST_non)
            print 'u_BST_spam: %f, %f' %(mu_BST_spam, gema_BST_spam)
            mu_RFR_non, gema_RFR_non = get_mean_variance(RFR_list_non)
            mu_RFR_spam, gema_RFR_spam = get_mean_variance(RFR_list_spam)
            print 'u_RFR_non: %f, %f' %(mu_RFR_non, gema_RFR_non)
            print 'u_RFR_spam: %f, %f' %(mu_RFR_spam, gema_RFR_spam)
            
            if (mu_CS_non * (1 - mu_CS_non) / gema_CS_non - 1) < 10:
                pi_CS_non_1 = mu_CS_non * (mu_CS_non * (1 - mu_CS_non) / gema_CS_non - 1)
                pi_CS_non_2 = (1-mu_CS_non) * (mu_CS_non * (1 - mu_CS_non) / gema_CS_non - 1)
            if (mu_CS_spam * (1 - mu_CS_spam) / gema_CS_spam - 1) < 10:
                pi_CS_spam_1 = (mu_CS_spam) * (mu_CS_spam * (1 - mu_CS_spam) / gema_CS_spam - 1)
                pi_CS_spam_2 = (1-mu_CS_spam) * (mu_CS_spam * (1 - mu_CS_spam) / gema_CS_spam - 1)
                
            if (mu_MNR_non * (1 - mu_MNR_non) / gema_MNR_non - 1) < 10:
                pi_MNR_non_1 = mu_MNR_non * (mu_MNR_non * (1 - mu_MNR_non) / gema_MNR_non - 1)
                pi_MNR_non_2 = (1-mu_MNR_non) * (mu_MNR_non * (1 - mu_MNR_non) / gema_MNR_non - 1)
                
            if (mu_MNR_spam * (1 - mu_MNR_spam) / gema_MNR_spam - 1) < 10:
                pi_MNR_spam_1 = (mu_MNR_spam) * (mu_MNR_spam * (1 - mu_MNR_spam) / gema_MNR_spam - 1)
                pi_MNR_spam_2 = (1-mu_MNR_spam) * (mu_MNR_spam * (1 - mu_MNR_spam) / gema_MNR_spam - 1)

            if (mu_BST_non * (1 - mu_BST_non) / gema_BST_non - 1) < 10:
                pi_BST_non_1 = mu_BST_non * (mu_BST_non * (1 - mu_BST_non) / gema_BST_non - 1)
                pi_BST_non_2 = (1-mu_BST_non) * (mu_BST_non * (1 - mu_BST_non) / gema_BST_non - 1)
            if (mu_BST_spam * (1 - mu_BST_spam) / gema_BST_spam - 1) < 10:
                pi_BST_spam_1 = (mu_BST_spam) * (mu_BST_spam * (1 - mu_BST_spam) / gema_BST_spam - 1)
                pi_BST_spam_2 = (1-mu_BST_spam) * (mu_BST_spam * (1 - mu_BST_spam) / gema_BST_spam - 1)

            if (mu_RFR_non * (1 - mu_RFR_non) / gema_RFR_non - 1) < 10:
                pi_RFR_non_1 = mu_RFR_non * (mu_RFR_non * (1 - mu_RFR_non) / gema_RFR_non - 1)
                pi_RFR_non_2 = (1-mu_RFR_non) * (mu_RFR_non * (1 - mu_RFR_non) / gema_RFR_non - 1)
            if (mu_RFR_spam * (1 - mu_RFR_spam) / gema_RFR_spam - 1) < 10:
                pi_RFR_spam_1 = (mu_RFR_spam) * (mu_RFR_spam * (1 - mu_RFR_spam) / gema_RFR_spam - 1)
                pi_RFR_spam_2 = (1-mu_RFR_spam) * (mu_RFR_spam * (1 - mu_RFR_spam) / gema_RFR_spam - 1)

            print 'non_CS: %f, %f' % (pi_CS_non_1, pi_CS_non_2)
            print 'spam_CS: %f, %f' % (pi_CS_spam_1, pi_CS_spam_2)
            print 'non_MNR: %f, %f' % (pi_MNR_non_1, pi_MNR_non_2)
            print 'spam_MNR: %f, %f' % (pi_MNR_spam_1, pi_MNR_spam_2)
            print 'non_BST: %f, %f' % (pi_BST_non_1, pi_BST_non_2)
            print 'spam_BST: %f, %f' % (pi_BST_spam_1, pi_BST_spam_2)
            print 'non_RFR: %f, %f' % (pi_RFR_non_1, pi_RFR_non_2)
            print 'spam_RFR: %f, %f' % (pi_RFR_spam_1, pi_RFR_spam_2)
            
    r_spam_score_dict = {}
    member_content = ''
    member_score_dict = {}
    product_score_dict = {}
    for member in member_list:
        r_list = member_review_dict[member]
        r_count = len(r_list)
        spam_count = n_m_spam_dict[member]
        spam_score = float(spam_count) / float(r_count)
        member_score_dict[member] = spam_score
        for r in r_list:
            r_spam_score_dict[r] = spam_score
    
    product_content = ''
    for product in product_review_dict.keys():
        r_list = product_review_dict[product]
        r_count = len(r_list)
        spam_count = 0
        for r in r_list:
            if review_label_list[r]==1:
                spam_count += 1
        spam_score = float(spam_count) / float(r_count)
        product_score_dict[product] = spam_score

        
    sorted_member_list = sorted(member_score_dict.items(), key=operator.itemgetter(1), reverse=True)
    sorted_product_list = sorted(product_score_dict.items(), key=operator.itemgetter(1), reverse=True)
    for item in sorted_member_list:
        member = item[0]
        r_list = member_review_dict[member]
        r_count = len(r_list)
        spam_count = n_m_spam_dict[member]
        spam_score = float(spam_count) / float(r_count)
        member_list = [member, str(spam_score), str(r_count)]
        member_content += '\t'.join(member_list) +'\t' +' '.join([str(x-1) for x in r_list]) + '\n'
        
    for item in sorted_product_list:
        product = item[0]
        r_list = product_review_dict[product]
        r_count = len(r_list)
        spam_count = 0
        product_list = [product, str(item[1]), str(r_count)]
        product_content += '\t'.join(product_list) +'\t' +' '.join([str(x-1) for x in r_list]) + '\n'
        
    sorted_r_spam_score = sorted(r_spam_score_dict.items(), key=operator.itemgetter(1), reverse=True)
    for i in xrange(0, 3):
        percent = 5.0 * (i+1) / 100.0
        t_len = len(sorted_r_spam_score) * percent
        start_list = sorted_r_spam_score[0:int(t_len)]
        end_list = sorted_r_spam_score[int(-1 * t_len):]
        start_t_list = [str(x[0]-1) + ' ' + str(x[1]) for x in start_list]
        end_t_list = [str(x[0]-1) + ' ' + str(x[1]) for x in end_list]
        start_content = '\n'.join(start_t_list)
        end_content = '\n'.join(end_t_list)
        save_file(str(i) + '_1.txt', start_content)
        save_file(str(i) + '_0.txt', end_content)

    save_file('user_spam.txt', member_content)
    save_file('product_spam.txt', product_content)