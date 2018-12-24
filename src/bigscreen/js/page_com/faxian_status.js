var faxian_status={
    template:`<div>
    <div class="scien-text head2">发现情况</div>
     <div class="draw-panel" style="width: 450px;height: 180px"></div>
    </div>`,
    mounted:function(){
        var self=this
        ex.director_call('grid.faxian',{},function(resp){
            self.draw_chart(resp)
        })
    },
    methods:{
        draw_chart:function(back_data){
            var myChart = echarts.init($(this.$el).find('.draw-panel')[0]);

            // 指定图表的配置项和数据
            var option = {
                //tooltip: {
                //    trigger: 'item',
                //    formatter: "{a} <br/>{b}: {c} ({d}%)"
                //},
                legend: {
                    orient: 'vertical',
                    right:20,
                    top:30,
                    data:['监督员上报','微信上报','村居采集','其他上报'],
                    textStyle:{
                        color:'white'
                    },
                    formatter: function(name) {
                        var data = option.series[0].data;
                        var total = 0;
                        var tarValue;
                        for (var i = 0, l = data.length; i < l; i++) {
                            total += data[i].value;
                            if (data[i].name == name) {
                                tarValue = data[i].value;
                            }
                        }
                        var p = (tarValue / total * 100).toFixed(2);
                        return name + ' ' + ' ' + '(' + p + '%)';
                    },
                },

                series: [
                    {
                        name:'访问来源',
                        type:'pie',
                        center : ['35%', '50%'],
                        radius: ['50%', '70%'],
                        avoidLabelOverlap: false,
                        label: {
                            normal: {
                                show: false,
                                position: 'center'
                            },
                            //emphasis: {
                            //    show: true,
                            //    textStyle: {
                            //        fontSize: '30',
                            //        fontWeight: 'bold'
                            //    }
                            //}
                        },
                        labelLine: {
                            normal: {
                                show: false
                            }
                        },
                        data:[
                            {value:back_data.jiandu, name:'监督员上报'},
                            {value:back_data.weixin, name:'微信上报'},
                            {value:back_data.cunju, name:'村居采集'},
                            {value:back_data.other, name:'其他上报'},
                        ]
                    }
                ]
            };



            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        }
    }
}

Vue.component('com-faxian-status', function (resolve, reject) {
    ex.load_js('https://cdn.bootcss.com/echarts/4.1.0-release/echarts.min.js')
        .then(function(){
            resolve(faxian_status)
        })

})