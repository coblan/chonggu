require('./scss/gaofa_case.scss')

Vue.component('com-gaofa-case',{
    template:`<div class="com-gaofa-case">
    <div class="scien-text head2">高发问题</div>
    <table>
        <tr>
            <th v-for="head in heads" v-text="head.label" :style="{width:head.width}"></th>
        </tr>
        <tr v-for="row in rows">
            <td v-for="head in heads" v-text="row[head.name]"></td>
        </tr>
    </table>
    </div>`,
    data:function(){
        return {
            heads:[
                {name:'name',label:'名称',width:'200px'},
                {name:'number',label:'数量',width:'100px'},
                {name:'percent',label:'占比',width:'100px'},
            ],
            rows:[
                //{name:'xxx',number:'123',percent:'124'},
                //{name:'xxx',number:'123',percent:'124'},
                //{name:'xxx',number:'123',percent:'124'},

            ]
        }
    },
    mounted:function(){
        var self=this
        ex.director_call('bigscreen.high_happen_case',{},function(resp){
            self.rows = resp
        })
    }
})