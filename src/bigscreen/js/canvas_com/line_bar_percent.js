Vue.component('com-can-line-bar-percent',{
    props:['percent','color','title'],
    template:`<div class="com-can-line-bar-percent" style="display: inline-block">
    <canvas height="120" width="40" style="width: 25px;height: 100px"></canvas>
    </div>`,
    mounted:function(){
        var canvas = $(this.$el).find('canvas')[0];
        //var ctx = canvas.getContext("2d");
        //ctx.strokeStyle = "#FFFFFF";
        //ctx.beginPath();
        //ctx.arc(100,75,50,0,2*Math.PI);
        //ctx.stroke();
        toCanvas(canvas,this.percent,this.color,this.title)
    },
    watch:{
        percent:function(){
            var canvas = $(this.$el).find('canvas')[0];
            toCanvas(canvas,this.percent,this.color,this.title)
        }

    }
})

function  toCanvas(canvas,percent,color){
    var ctx = canvas.getContext("2d");
    ctx.strokeStyle=color;
    ctx.lineWidth=1
    for (var i=0;i<=100;i=i+3){
        if(i>percent){
            ctx.strokeStyle='grey';
        }
        var y = 110 -i
        ctx.beginPath();
        ctx.moveTo(0,y)
        ctx.lineTo(50,y)
        ctx.stroke();
        ctx.closePath();
    }


}