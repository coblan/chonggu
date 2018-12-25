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
    span 一年
已经受理 ： 1812E4465594    
已结案	1812B1955331	
待督办	1812D3275983	
已结案	1812C2407376	

已结案 ：1812B1955331	

在办 ：
qsl
办结：
    """
    sql="""
    SELECT
	COUNT(1) AS shouli_number,
	SUM(CASE WHEN STATUS=9 THEN 0 ELSE 1 END) AS handling,
	SUM(CASE WHEN STATUS=9 THEN 1 ELSE 0 END) AS handle_over
FROM 
	CITYGRID.T_TASKINFO main
WHERE
	1 = 1 
	AND discovertime BETWEEN TO_DATE( '%(start)s 00:00:00', 'yyyy-MM-dd HH24:mi:ss' ) 
	AND TO_DATE( '%(end)s 23:59:59', 'yyyy-MM-dd HH24:mi:ss' ) 
	AND InfoSourceid IN ( 10 )
	AND STATUS <> 10
	AND STREETCODE IN ( '1809' ) 
    """
    now = timezone.now()
    start=now.replace(day=1).strftime('%Y-%m-%d')
    end=now.strftime('%Y-%m-%d')
    sql = sql%{'start':start,'end':end}
    rows = sango_exec_sql(sql)
    
    return rows[0]

@director_view('12345.chuzhi')
def chuzhi():
    """
    """
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
	AND discovertime BETWEEN TO_DATE( '%(start)s 00:00:00', 'yyyy-MM-dd HH24:mi:ss' ) 
	AND TO_DATE( '%(end)s 23:59:59', 'yyyy-MM-dd HH24:mi:ss' ) 
	AND InfoSourceid =10 
        AND STATUS<> 10
	AND STREETCODE IN ( '1809' ) 
    """
    now = timezone.now()
    start=now.replace(day=1).strftime('%Y-%m-%d')
    end=now.strftime('%Y-%m-%d')
    sql = sql%{'start':start,'end':end}
    
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
    """
    
    受理数  结案数  及时结案数
    
    受理数 要去掉 已作废的
    已作废	1812D3736905	监督员上报	2018-12-18 14:50	部件	道路交通	交通信号灯		重固镇	重固镇，北青公路6186号门口...								否	
    已作废	1812D3731953	监督员上报	2
    
    
    红灯  1812D3557565
    字段 ttaskinfo.alllight solvinglight
    
    
    """
    sql ="""
SELECT
	COUNT(1) AS shouli_number,
	SUM(CASE WHEN STATUS=9 THEN 1 ELSE 0 END) AS handle_over,
	SUM(CASE WHEN STATUS=9 AND ALLLIGHT <>'红' THEN 1 ELSE 0 END) AS at_time_handle
FROM 
	CITYGRID.T_TASKINFO main
WHERE
	1 = 1 
	AND discovertime BETWEEN TO_DATE( '%(start)s 00:00:00', 'yyyy-MM-dd HH24:mi:ss' ) 
	AND TO_DATE( '%(end)s 23:59:59', 'yyyy-MM-dd HH24:mi:ss' ) 
	AND InfoSourceid in (1,36,61,9) 
	AND STATUS <> 10
	AND STREETCODE ='1809' 
        """
    now = timezone.now()
    start=now.replace(day=1).strftime('%Y-%m-%d')
    end=now.strftime('%Y-%m-%d')
    sql = sql%{'start':start,'end':end}    
    rows = sango_exec_sql(sql)
    dc = rows[0]
    total = dc['shouli_number'] or 1
    dc['handle_over_ratio']= round(100.0*dc['handle_over']/total,2)
    dc['at_time_handel_ratio']= round(100.0*dc['at_time_handle']/total,2)
    return dc  

@director_view('grid.faxian')
def faxian():
    """
    1:监督员上报
    62:微信上报
    9:其他上报
    
    36:居村采集  // 重固数据中未发现，在赵巷中发现了
    
    提出已作废
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
	AND discovertime BETWEEN TO_DATE( '%(start)s 00:00:00', 'yyyy-MM-dd HH24:mi:ss' ) 
	AND TO_DATE( '%(end)s 23:59:59', 'yyyy-MM-dd HH24:mi:ss' ) 
	AND InfoSourceid IN ( 1, 36, 61, 9 ) 
	AND STREETCODE IN ( '1809' ) 
    """
    now = timezone.now()
    start=now.replace(day=1).strftime('%Y-%m-%d')
    end=now.strftime('%Y-%m-%d')
    sql = sql%{'start':start,'end':end}
    
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
WHERE
    start_time >= to_date('%(start)s', 'YYYY-MM-DD')
    """
    now = timezone.now()
    sp1 = timezone.timedelta(days=1)
    last = now-sp1
    start = last.strftime('%Y-%m-%d')
    sql=sql%{'start':start}
    row=local_exec_sql(sql)[0]
    row['processed'] = row['processed'] or 0
    row['unprocessed']=row['total']-row['processed']
    return row

@director_view('bigscreen.high_happen_case')
def high_happen_case():
    sql="""
 	SELECT
	'总数' AS NAME,
	COUNT(1) AS TOTAL
	FROM
	CITYGRID.T_TASKINFO main
	WHERE
	discovertime BETWEEN TO_DATE( '%(start)s 00:00:00', 'yyyy-MM-dd HH24:mi:ss' ) 
	AND TO_DATE( '%(end)s 23:59:59', 'yyyy-MM-dd HH24:mi:ss' ) 
	AND InfoSourceid in (1,36,61,9) 
	AND STATUS <> 10
	AND STREETCODE ='1809' 
	
	UNION ALL
	
 SELECT
  INFOSCNAME AS name,
 total AS bb
 FROM
 (
 SELECT
 INFOSCNAME,
	COUNT(1) AS TOTAL
	
FROM 
	CITYGRID.T_TASKINFO main
WHERE
	1 = 1 
	AND discovertime BETWEEN TO_DATE( '%(start)s 00:00:00', 'yyyy-MM-dd HH24:mi:ss' ) 
	AND TO_DATE( '%(end)s 23:59:59', 'yyyy-MM-dd HH24:mi:ss' ) 
	AND InfoSourceid in (1,36,61,9) 
	AND STATUS <> 10
	AND STREETCODE ='1809' 
	GROUP BY
	INFOSCNAME
	ORDER BY
	-TOTAL
	)
	WHERE 
	ROWNUM <=5
    """
    now = timezone.now()
    start=now.replace(day=1).strftime('%Y-%m-%d')
    end=now.strftime('%Y-%m-%d')
    sql = sql%{'start':start,'end':end}
    rows = sango_exec_sql(sql,small_key=False)
    #total = JianduCase.objects.count()*1.0
    #query = JianduCase.objects.values('litclass').annotate(number=Count('id')).order_by('-number')
    #rows=[]
    out_rows=[]
    total = rows[0]['TOTAL'] or 1
    for row in rows[1:]:
        out_rows.append({
            'name':row['NAME'],
            'number':row['TOTAL'],
            'percent':'%s%%'% round( row['TOTAL']*100/total,2)
        })
    return out_rows

@director_view('bigscreen.report_case_number_this_month')
def report_case_this_month():
    """
    下面的SQL可以直接在三高里面查询，但是keepername 不完善，所以还是采用本地的数据库
    #---------------------
    SELECT
keeper.KEEPERNAME,
tt.TOTAL
FROM
(SELECT
 KEEPERSN ,
 COUNT(1) AS TOTAL
FROM 
	CITYGRID.T_INFO_MAIN main

WHERE
	discovertime BETWEEN TO_DATE( '2018-12-01 00:00:00', 'yyyy-MM-dd HH24:mi:ss' ) 
	AND TO_DATE( '2018-12-22 23:59:59', 'yyyy-MM-dd HH24:mi:ss' ) 
	AND InfoSourceid in (1,36,61,9) 
	AND STATUS <> 10
	AND STREETCODE ='1809' 
GROUP BY
	KEEPERSN
	ORDER BY 
	-TOTAL
	)tt

 INNER JOIN T_KEEPERSINFO keeper
ON tt.KEEPERSN= keeper.KEEPERSN
#--------------------------
    """
    now_month = timezone.now().strftime('%Y-%m')
    query = JianduCase.objects.filter(subtime__startswith=now_month).values('keepersn').exclude(keepersn__isnull=True).annotate(count=Count('id'),name=F('keepersn__name')).order_by('-count')
    return list(query[:10])
    