require('./scss/banli_status.scss')

Vue.component('com-banli-status',{
    template:`<div class="com-banli-status">
        <div class="scien-text head2">办理情况</div>
        <div style="padding: 10px 15px;">
            <div class="item">
              <div class="scien-text">受理数</div>
              <div class="number">22</div>
            </div>

             <div class="item">
                  <div class="scien-text">在办数</div>
                  <div class="number">22</div>
            </div>

             <div class="item">
                  <div class="scien-text">办结数</div>
                  <div class="number">22</div>
            </div>

        </div>
    </div>`
})