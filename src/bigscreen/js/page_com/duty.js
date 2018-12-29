Vue.component('com-duty',{
    template:`<div style="padding-bottom: 20px">
     <div class="scien-text head2">平台值班</div>
     <table style="margin: 10px">
       <tr v-for="head in heads">
            <td v-text="head.label" style="width: 200px;text-align: right;color: #00a7d0;padding: 8px 20px"></td>
             <td v-text="row[head.name]"></td>
        </tr>
     </table>
    </div>`,
    data:function(){
        return {
            heads:[
                {name:'yinji_duty',label:'应急值班'},
                {name:'director_duty',label:'网格指挥长'},
                {name:'infoer_duty',label:'信息员'},
            ],
            row:{
                'yinji_duty':'',
                director_duty:'',
                infoer_duty:''
            }
        }
    },
    mounted:function(){
        var self=this
        ex.director_call('get_duty_info',{},function(resp){
            ex.assign(self.row,resp)
        })
    }
})