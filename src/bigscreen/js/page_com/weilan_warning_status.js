require('./scss/weilan_warning_status.scss')

Vue.component('com-weilan-warning',{
    template:`<div class="com-weilan-warning">
     <div class="scien-text head2">围栏告警情况</div>
     <div class="item"  v-for="head in heads">
         <span v-text="row[head.name]" :class="head.name"></span><br>
         <span v-text="head.label"></span>
     </div>

    </div>`,
    data:function(){
        return {
            heads:[
                {name:'total',label:'告警数'},
                {name:'processed',label:'处理数'},
                {name:'unprocessed',label:'未处理数'},
            ],
            row:{
                total:0,
                processed:0,
                unprocessed:0,
            }
        }
    },
    mounted:function(){
        var self=this
        ex.director_call('warning_number',{},function(resp){
            ex.assign(self.row,resp)
        })
    }
})