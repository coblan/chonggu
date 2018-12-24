require('./scss/case_number_this_month.scss')

Vue.component('com-case-number-this-month',{
    template:`<div class="com-case-number-this-month">
     <div class="scien-text head2">本月案件上报情况</div>
     <table>
        <tr>
            <th style="width: 20px"></th> <th v-for="head in heads" v-text="head.label" :style="{width:head.width}"></th>
        </tr>
        <tr v-for="(row,index) in rows1">
            <td v-text="index+1"></td> <td v-for="head in heads" v-text="row[head.name]"></td>
        </tr>
     </table>

         <table>
            <tr>
                <th style="width: 20px"></th> <th v-for="head in heads" v-text="head.label" :style="{width:head.width}"></th>
            </tr>
            <tr v-for="(row,index) in rows2">
                <td v-text="index+5"></td> <td v-for="head in heads" v-text="row[head.name]"></td>
            </tr>
     </table>
    </div>`,
    data:function(){
        return {
            heads:[
                {name:'name',label:'IOPS',width:'100px'},
                {name:'count',label:'（件）',width:'30px'},
            ],
            rows:[
                //{name:'v胜算',count:'213'},
                //{name:'v胜算',count:'213'},
                //{name:'v胜算',count:'213'},
                //{name:'v胜算',count:'213'},
                //{name:'v胜算',count:'213'},
                //{name:'v胜算',count:'213'},
                //{name:'v胜算',count:'213'},
                //{name:'v胜算',count:'213'},
                //{name:'v胜算',count:'213'},
                //{name:'v胜算',count:'213'},
            ]
        }
    },
    mounted:function(){
        var self=this
        ex.director_call('bigscreen.report_case_number_this_month',{},function(resp){
            self.rows=resp
        })
    },
    computed:{
        rows1:function(){
            return this.rows.slice(0,5)
        },
        rows2:function(){
            return this.rows.slice(5)
        }
    }
})