var toushu_year_compare = {
    data:function(){
        return {
            hotline_complain_last:[],
            hotline_complain_this:[],
        }
    },
    template:`<div>
    <div class="scien-text head2">热线投诉年度环比</div>
    <div class="draw-panel" style="width: 450px;height: 200px"></div>
    </div>`,
    mounted:function(){
        var self=this
        ex.director_call('hotline_complain',{},function(resp){
            ex.assign(self,resp)
            self.draw_chart()
        })

    },
    methods:{
        draw_chart:function(){
            var self=this
            var myChart = echarts.init($(this.$el).find('.draw-panel')[0]);
            // 指定图表的配置项和数据
            var option = {
                legend: {
                    orient: 'horizontal', // 'vertical'
                    x: 'right', // 'center' | 'left' | {number},
                    y: 'top', // 'center' | 'bottom' | {number}
                    //backgroundColor: '#eee',
                    //borderColor: 'rgba(178,34,34,0.8)',
                    //borderWidth: 4,
                    //padding: 10,    // [5, 10, 15, 20]
                    //itemGap: 20,
                    textStyle: {color: '#668393'},
                    //selected: {
                    //    '降水量': false
                    //},
                },
                xAxis: {
                    type: 'category',
                    data: ['1', '2', '3', '4', '5', '6', '7','8','9','10','11','12'],
                    axisLabel:{
                        color:'#668393',
                    }
                },
                yAxis: {
                    type: 'value',
                    axisLabel:{
                        color:'#668393',
                    },
                    splitLine: {
                        show: false
                    }
                },
                series: [{
                    name:'去年',
                    data: self.hotline_complain_last,//[520, 332, 401, 234, 1290, 1330, 820,834,834,112,213,955],
                    type: 'line',
                    color:'yellow'
                },
                    {
                        name:'今年',
                        data: self.hotline_complain_this ,//[820, 932, 901, 934, 1290, 1330, 1320,1234,1234,1512,213,1255],
                        type: 'line',
                    },
                ]
            };


            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        }
    }
}

Vue.component('com-toushu-year-compare', function (resolve, reject) {
    ex.load_js('https://cdn.bootcss.com/echarts/4.1.0-release/echarts.min.js')
    .then(function(){
        resolve(toushu_year_compare)
    })

})


