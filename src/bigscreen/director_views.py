from shanghai_grid.sangao.db_bridge import exec_sql as sango_exec_sql
from helpers.func.sql import exec_sql as local_exec_sql
from helpers.director.shortcut import director_view
from helpers.director.kv import get_value
from shanghai_grid.dianzi_weilan.models import OutBlockWarning
from django.utils import timezone
from django.db.models import Count,Sum,F
from shanghai_grid.case_cmp.models import JianduCase

@director_view('12345.banli')
def banli_12345():
    """
    InfoSourceid = 10  // 12345
    
    """
    sql="""
    SELECT
	COUNT(1) AS shouli_number,
	SUM(CASE WHEN STATUS=9 THEN 1 ELSE 0 END) AS handle_over
FROM 
	CITYGRID.T_TASKINFO main
WHERE
	1 = 1 
	AND discovertime BETWEEN TO_DATE( '2018-12-14 00:00:00', 'yyyy-MM-dd HH24:mi:ss' ) 
	AND TO_DATE( '2018-12-22 23:59:59', 'yyyy-MM-dd HH24:mi:ss' ) 
	AND InfoSourceid IN ( 10 ) 
	AND STREETCODE IN ( '1809' ) 

    """
    rows = sango_exec_sql(sql)
    
    return rows[0]

@director_view('12345.chuzhi')
def chuzhi():
    sql="""
    SELECT 
	SUM (
		CASE
		WHEN ISFIRSTCONTACT = 1 THEN
			1
		ELSE
			0
		END
	) AS FIRST_YES,
	SUM (
		CASE
		WHEN ISFIRSTCONTACT = 0 THEN
			1
		ELSE
			0
		END 
	) AS FIRST_NO,
	SUM (
	CASE
	WHEN ALLMANYINAME_BF = '满意' THEN
		1
	WHEN ALLMANYINAME_BF = '基本满意' THEN
		0.8
	WHEN ALLMANYINAME_BF = '一般' THEN
		0.6
	ELSE
		0
	END
) AS MAN_YI,
 SUM (
	CASE
	WHEN ALLMANYINAME_BF IN (
		'满意',
		'不满意',
		'基本满意',
		'一般'
	) THEN
		1
	ELSE
		0
	END
) AS MAN_YI_TOTAL,
 SUM (
	CASE
	WHEN CASEVALUATIONNAME = '实际解决' THEN
		1
	ELSE
		0
	END
) AS "REAL_SOLVE",
 SUM (
	CASE
	WHEN CASEVALUATIONNAME = '解释说明' THEN
		1
	ELSE
		0
	END
) AS "JIE_SOLVE"

FROM 
	T_TASKINFO main
WHERE
	1 = 1 
	AND discovertime BETWEEN TO_DATE( '2018-12-01 00:00:00', 'yyyy-MM-dd HH24:mi:ss' ) 
	AND TO_DATE( '2018-12-22 23:59:59', 'yyyy-MM-dd HH24:mi:ss' ) 
	AND InfoSourceid =10 
	AND STREETCODE IN ( '1809' ) 
    """
    rows = sango_exec_sql(sql,small_key=False)
    row=rows[0]
    first_contact_ratio = row.get('FIRST_YES')/(row.get('FIRST_YES')+row.get('FIRST_NO') )
    real_solve=row.get('REAL_SOLVE')
    jie_solve=row.get('JIE_SOLVE')
    solve_total =( real_solve + jie_solve  or 1) * 1.0 
    real_solve_ratio = real_solve/solve_total
    
    manyi_total =( row.get('MAN_YI_TOTAL') or 1)* 1.0 
    man_yi_ratio = float( row.get('MAN_YI', 0) )/ manyi_total
    
    dc={
        'first_contact_ratio': round(first_contact_ratio*100,2),
        'AnShiBanJie_ratio':100,
        'real_solve_ratio':round(real_solve_ratio*100,2) ,
        'man_yi_ratio':  round(man_yi_ratio*100,2)
    }
    return dc

@director_view('hotline_complain')
def hotline_complain():
    return {
        'hotline_complain_last':get_value('hotline_complain_last','').split(','),
        'hotline_complain_this':get_value('hotline_complain_this','').split(',')
    }

@director_view('bigscreen.grid_banli')
def grid_banli():
    sql ="""
        SELECT
	COUNT(1) AS shouli_number,
	SUM(CASE WHEN STATUS=9 THEN 1 ELSE 0 END) AS handle_over
FROM 
	CITYGRID.T_TASKINFO main
WHERE
	1 = 1 
	AND discovertime BETWEEN TO_DATE( '2018-12-14 00:00:00', 'yyyy-MM-dd HH24:mi:ss' ) 
	AND TO_DATE( '2018-12-22 23:59:59', 'yyyy-MM-dd HH24:mi:ss' ) 
	AND InfoSourceid in (1,36,61,9) 
	AND STREETCODE ='1809' 
        """
    rows = sango_exec_sql(sql)
    
    return rows[0]    

@director_view('grid.faxian')
def faxian():
    """
    1:监督员上报
    62:微信上报
    9:其他上报
    
    36:居村采集  // 重固数据中未发现，在赵巷中发现了
    """
    
    sql="""
    SELECT
	SUM(CASE WHEN INFOSOURCEID=1 THEN 1 ELSE 0 END) AS JIANDU,
	SUM(CASE WHEN INFOSOURCEID=36 THEN 1 ELSE 0 END) AS CUNJU,
	SUM(CASE WHEN INFOSOURCEID=61 THEN 1 ELSE 0 END) AS WEIXIN,
	SUM(CASE WHEN INFOSOURCEID=9 THEN 1 ELSE 0 END) AS OTHER
FROM
	CITYGRID.T_TASKINFO main 
WHERE
	1 = 1 
	AND discovertime BETWEEN TO_DATE( '2018-12-01 00:00:00', 'yyyy-MM-dd HH24:mi:ss' ) 
	AND TO_DATE( '2018-12-15 23:59:59', 'yyyy-MM-dd HH24:mi:ss' ) 
	AND InfoSourceid IN ( 1, 36, 61, 9 ) 
	AND STREETCODE IN ( '1809' ) 
    """
    rows = sango_exec_sql(sql)
    
    return rows[0]     
    
@director_view('get_duty_info')
def get_duty_info():
    return {
        'yinji_duty':get_value('yinji_duty',''),
        'director_duty':get_value('director_duty',''),
        'infoer_duty':get_value('infoer_duty','')
    }

@director_view('warning_number')
def warning_number():
    sp1 = timezone.timedelta(days=1)
    last_day = timezone.now()-sp1
    last_day=last_day.replace(hour=0,minute=0)
    sql = """
    SELECT 
 COUNT(id) AS TOTAL,
SUM(CASE WHEN proc_status = 'processed' THEN 1 ELSE 0 END) AS processed
FROM
 dianzi_weilan_outblockwarning
    """
    row=local_exec_sql(sql)[0]
    row['unprocessed']=row['total']-row['processed']
    return row

@director_view('bigscreen.high_happen_case')
def high_happen_case():
    total = JianduCase.objects.count()*1.0
    query = JianduCase.objects.values('litclass').annotate(number=Count('id')).order_by('-number')
    rows=[]
    for row in query[:5]:
        rows.append({
            'name':row['litclass'],
            'number':row['number'],
            'percent':'%s%%'% round( row['number']*100/total,2)
        })
    return rows

@director_view('bigscreen.report_case_number_this_month')
def report_case_this_month():
    query = JianduCase.objects.values('keepersn').exclude(keepersn__isnull=True).annotate(count=Count('id'),name=F('keepersn__name')).order_by('-count')
    return list(query[:10])
    