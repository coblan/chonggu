from helpers.director.shortcut import FieldsPage,Fields,page_dc,director
from helpers.director.kv import get_value,set_value

class BigScreenPage(FieldsPage):
    def get_template(self, prefer=None):
        return 'jb_admin/fields.html'
    
    class fieldsCls(Fields):
        def get_heads(self):
            return [
                {'name':'hotline_complain_last','label':'热线投诉年度<br>环比（去年）','editor':'linetext'},
                {'name':'hotline_complain_this','label':'热线投诉年度<br>环比（今年）','editor':'linetext'},
                {'name':'yinji_duty','label':'应急值班','editor':'linetext'},
                {'name':'director_duty','label':'网格指挥长','editor':'linetext'},
                {'name':'infoer_duty','label':'信息员','editor':'linetext'},
                
            ]
        
        def save_form(self):
            set_value('hotline_complain_last', self.kw.get('hotline_complain_last'))
            set_value('hotline_complain_this',self.kw.get('hotline_complain_this'))
            set_value('yinji_duty',self.kw.get('yinji_duty'))
            set_value('director_duty',self.kw.get('director_duty'))
            set_value('infoer_duty',self.kw.get('infoer_duty'))
            
        def get_row(self):
            return {
                '_director_name':self.get_director_name(),
                'hotline_complain_last':get_value('hotline_complain_last'),
                'hotline_complain_this':get_value('hotline_complain_this'),
                'yinji_duty':get_value('yinji_duty'),
                'director_duty':get_value('director_duty'),
                'infoer_duty':get_value('infoer_duty')
            }
    
director.update({
    'bigscreen.setting':BigScreenPage.fieldsCls
})

page_dc.update({
    'bigscreen.setting':BigScreenPage,
    
})