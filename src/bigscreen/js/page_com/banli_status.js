require('./scss/banli_status.scss')

Vue.component('com-banli-status',{
    data:function(){
        return {
            row :{
                shouli_number:0,
                handling:0,
                handle_over:0,
            }
        }
    },
    template:`<div class="com-banli-status">
        <div class="scien-text head2">办理情况</div>
        <div style="padding: 40px 30px;">
            <div class="item">
              <div class="scien-text">受理数</div>
              <div class="number" v-text="row.shouli_number">22</div>
            </div>

             <div class="item">
                  <div class="scien-text">在办数</div>
                  <div class="number" v-text="row.handling">22</div>
            </div>

             <div class="item">
                  <div class="scien-text">办结数</div>
                  <div class="number" v-text="row.handle_over">22</div>
            </div>

        </div>
    </div>`,
    mounted:function(){
        var self=this
        ex.director_call('12345.banli',{},function(resp){
            ex.assign(self.row,resp)
        })
    }
})