require('./scss/grid_banli.scss')

Vue.component('com-grid-banli',{
    data:function(){
        return {
            amount_heads:[
                {name:'shouli_number',label:'受理数'},
                {name:'handle_over',label:'结案数'},
                {name:'at_time_handle',label:'及时结案数'},
            ],
            row:{
                shouli_number:0,
                handle_over:0,
                at_time_handle:0,
                handle_over_ratio:0,
                at_time_handel_ratio:0,
            },

        }
    },
    template:`<div class="com-grid-banli">
        <div class="scien-text head2">办理情况</div>
        <div class="icontent">
             <div class="amount-info" v-for="head in amount_heads">
                  <span class="head-label" v-text="head.label"></span>
                  <span class="number" v-text="row[head.name]"></span>
             </div>
        </div>
        <div class="icontent">
            <div class="ratio">
                <com-can-line-bar-percent :percent="row.handle_over_ratio" color="red"></com-can-line-bar-percent>
                <br><span>结案率</span><br>
                <span class="number"><span v-text="row.handle_over_ratio"></span>%</span>
            </div>

            <div class="ratio">
                <com-can-line-bar-percent :percent="row.at_time_handel_ratio" color="green"></com-can-line-bar-percent>
                <br><span>及时结案率</span><br>
                <span class="number"><span v-text="row.at_time_handel_ratio"></span>%</span>
            </div>

        </div>

    </div>`,
    mounted:function(){
        var self=this
        ex.director_call('bigscreen.grid_banli',{},function(resp){
            ex.assign(self.row,resp)
        })
    }
})