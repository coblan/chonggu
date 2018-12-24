Vue.component('com-can-circle-percent',{
    props:['percent','color','title'],
    template:`<div class="com-can-circle-percent" style="display: inline-block">
    <canvas height="150" width="150" style="width: 100px;height: 100px"></canvas>
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


function toCanvas(canvas ,progress,color,title){
    //canvas进度条
    //var canvas = document.getElementById(id),
    var   ctx = canvas.getContext("2d")
     var percent = progress  //最终百分比
    var circleX = canvas.width / 2  //中心x坐标
    var circleY = canvas.height / 2 //  中心y坐标
    var radius = 70 // 圆环半径
    var lineWidth = 8 // 圆形线条的宽度
    var fontSize = 22; //字体大小
    //两端圆点
    function smallcircle1(cx, cy, r) {
        ctx.beginPath();
        //ctx.moveTo(cx + r, cy);
        ctx.lineWidth = 1;
        ctx.fillStyle = '#06a8f3';
        ctx.arc(cx, cy, r,0,Math.PI*2);
        ctx.fill();
    }
    function smallcircle2(cx, cy, r) {
        ctx.beginPath();
        //ctx.moveTo(cx + r, cy);
        ctx.lineWidth = 1;
        ctx.fillStyle = '#00f8bb';
        ctx.arc(cx, cy, r,0,Math.PI*2);
        ctx.fill();
    }

    //画圆
    function circle(cx, cy, r) {
        ctx.beginPath();
        //ctx.moveTo(cx + r, cy);
        ctx.lineWidth = lineWidth;
        ctx.strokeStyle = '#222';
        //ctx.arc(cx, cy, r, Math.PI*2/3, Math.PI * 1/3);
        ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.stroke();
    }

    //画弧线
    function sector(cx, cy, r, startAngle, endAngle, anti) {
        ctx.beginPath();
        //ctx.moveTo(cx, cy + r); // 从圆形底部开始画
        ctx.lineWidth = lineWidth;

        // 渐变色 - 可自定义
        var linGrad = ctx.createLinearGradient(
            circleX-radius-lineWidth, circleY, circleX+radius+lineWidth, circleY
        );
        linGrad.addColorStop(0.0, '#06a8f3');
        //linGrad.addColorStop(0.5, '#9bc4eb');
        linGrad.addColorStop(1.0, '#00f8bb');
        ctx.strokeStyle =  color //linGrad;

       // 圆弧两端的样式
        ctx.lineCap = 'round';

        //圆弧
        ctx.arc(
            cx, cy, r,
            -Math.PI/2,
            -Math.PI/2 - endAngle/100 * (Math.PI*2),
            true
        );
        //ctx.arc(
        //    cx, cy, r,
        //    (Math.PI*2/3),
        //    (Math.PI*2/3) + endAngle/100 * (Math.PI*5/3),
        //    false
        //);
        ctx.stroke();
    }

    //刷新
    function loading() {
        if (process >= percent) {
            clearInterval(circleLoading);
        }

        //清除canvas内容
        ctx.clearRect(0, 0, circleX * 2, circleY * 2);

       // 中间的字
        ctx.font = (fontSize+10) + 'px SimHei bolder'//'px April';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = color//'#999';
        //ctx.fillText(parseFloat(process).toFixed(0) + '%', circleX, circleY);
        ctx.fillText(parseFloat(process).toFixed(0) + '%', circleX, circleY-20);

        ctx.font = fontSize + 'px SimHei'//'px April';
        ctx.fillStyle='#668393'
        ctx.fillText(title, circleX, circleY+20);

       // 圆形
        circle(circleX, circleY, radius);

       // 圆弧
        sector(circleX, circleY, radius, Math.PI*2/3, process);
       // 两端圆点
        smallcircle1(150+Math.cos(2*Math.PI/360*120)*100, 150+Math.sin(2*Math.PI/360*120)*100, 5);
        //smallcircle2(150+Math.cos(2*Math.PI/360*(120+process*3))*100, 150+Math.sin(2*Math.PI/360*(120+process*3))*100, 5);
       // 控制结束时动画的速度
        if (process / percent > 0.90) {
            process += 0.30;
        } else if (process / percent > 0.80) {
            process += 0.55;
        } else if (process / percent > 0.70) {
            process += 0.75;
        } else {
            process += 1.0;
        }
    }

    var process = 0.0;  //进度
    var circleLoading = window.setInterval(function () {
        loading();
    }, 20);

}