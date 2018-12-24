Vue.component('com-chuzhi',{
    data:function(){
        return {
            row:{
                first_contact_ratio:0,
                real_solve_ratio:0,
                man_yi_ratio:0,
                AnShiBanJie_ratio:100
            }
        }
    },
    template:`<div>
    <div class="scien-text head2">处置绩效</div>
        <com-can-circle-percent :percent="row.first_contact_ratio" color="red" title="先行联系率"></com-can-circle-percent>
        <com-can-circle-percent :percent="row.real_solve_ratio" color="blue" title="市民满意率"></com-can-circle-percent>
        <com-can-circle-percent :percent="row.man_yi_ratio" color="yellow" title="实际解决率"></com-can-circle-percent>
        <com-can-circle-percent :percent="row.AnShiBanJie_ratio" color="red" title="按时办结率"></com-can-circle-percent>
    </div>`,
    mounted:function(){
        var self=this
        ex.director_call('12345.chuzhi',{}).then(
            function(resp){
                ex.assign(self.row,resp)
            }
        )
    }
})