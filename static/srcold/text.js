//返回开始时间
     function StartTime()
    {
        var now = new Date();

        var year = now.getFullYear();       //年
        var month = now.getMonth() + 1;     //月
        var day = now.getDate();            //日


        var clock = year + "-";

        if(month < 10)
            clock += "0";

        clock += month + "-";

        if(day < 10)
            clock += "0";

        clock += day + "T";

        clock += "00:00:00";
        return(clock);
    }
//返回结束日期
         function EndTime()
    {
        var now = new Date();

        var year = now.getFullYear();       //年
        var month = now.getMonth() + 1;     //月
        var day = now.getDate();            //日

        var hh = now.getHours();            //时
        var mm = now.getMinutes();          //分
        var ss = now.getSeconds() ;         //秒


        var clock = year + "-";

        if(month < 10)
            clock += "0";

        clock += month + "-";

        if(day < 10)
            clock += "0";

        clock += day + "T";

        if(hh < 10)
            clock += "0";

        clock += hh + ":";

        if (mm < 10)
            clock += '0';

        clock += mm + ":";

        if (ss < 10)
            clock += '0';

        clock += ss ;

        return(clock);
    }

    $(function(){

       $('#s_time').val(StartTime())
    });
    $(function(){

       $('#e_time').val(EndTime())
    });
    $(function () {
        $('#tabledata').bootstrapTable({
            url: '/jsondata',  // 请求数据源的路由
            dataType: "json",
            queryParams: function (params){
                return{
                    offset: params.offset, //页码
                    limit: params.limit,//页面大小
                    ROLL:$('#roll').val(), //磨床编号
                    StartTime:$('#s_time').val(), //开始时间
                    EndTime:$('#e_time').val(),//结束时间

                };
            },
            pagination: true, //前端处理分页
            singleSelect: false,//是否只能单选
            search: true, //显示搜索框，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            toolbar: '#toolbar', //工具按钮用哪个容器
            striped: true, //是否显示行间隔色
            cache: true, //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pageNumber: 1, //初始化加载第10页，默认第一页
            pageSize: 10, //每页的记录行数（*）
            pageList: [10, 20, 50, 100], //可供选择的每页的行数（*）
            // strictSearch: true,//设置为 true启用 全匹配搜索，false为模糊搜索
            showColumns: true, //显示内容列下拉框
            showRefresh: true, //显示刷新按钮
            minimumCountColumns: 2, //当列数小于此值时，将隐藏内容列下拉框
            // clickToSelect: true, //设置true， 将在点击某行时，自动勾选rediobox 和 checkbox
            height: 500, //表格高度，如果没有设置height属性，表格自动根据记录条数决定表格高度#}
            uniqueId: "id", //每一行的唯一标识，一般为主键列
            showToggle: true, //是否显示详细视图和列表视图的切换按钮
            cardView: false, //是否显示详细视图
// <!--            detailView: true, //是否显示父子表，设置为 true 可以显示详细页面模式,在每行最前边显示+号#}-->
            sidePagination: "server", //分页方式：client客户端分页，server服务端分页（*）
            showExport: true, //导出按钮
            exportDataType: "all", //导出表格方式（默认basic：只导出当前页的表格数据；all：导出所有数据；selected：导出选中的数据）
            exportTypes: ['json', 'xml', 'csv', 'txt', 'sql', 'excel'], //导出文件类型
            // {
            //     checkbox: true,
            //     visible: true,
            // },
            columns: [{
                checkbox: true,
                visible: true,
            },{
                field: 'c_id',
                title: '序号',
                align: 'center',  //对齐方式，居中
            }, {
                field: 'c_roll_number',
                title: '辊号',
                align: 'center'
            }, {
                field: 'c_program_number',
                title: '程序号',
                align: 'center',
            }, {
                field: 'c_operator',
                title: '操作者',
                align: 'center',
            }, {
                field: 'c_shift',
                title: '班次',
                align: 'center',
            }, {
                field: 'c_curve',
                title: '曲线',
                align: 'center',
            }, {
                field: 'c_diameter',
                title: '直径',
                align: 'center',
            }, {
                field: 'c_diameter_before',
                title: '磨前直径',
                align: 'center',
            }, {
                field: 'c_error',
                title: '误差',
                align: 'center',
            }, {
                field: 'c_coaxiality',
                title: '同轴度',
                align: 'center',
            }, {
                field: 'c_cylindricity',
                title: '圆柱度',
                align: 'center',
            }, {
                field: 'c_roundness',
                title: '圆度',
                align: 'center',
            }, {
                field: 'c_wheel_diameter',
                title: '砂轮直径',
                align: 'center',
            }, {
                field: 'c_actual_convexity',
                title: '实际凸度',
                align: 'center',
            }, {
                field: 'c_start_time',
                title: '开始时间',
                align: 'center',
            }, {
                field: 'c_end_time',
                title: '结束时间',
                align: 'center',
            }, {
                field: 'c_grinding_machine',
                title: '磨床',
                align: 'center',
            }, {
                field: 'c_date',
                title: '日期',
                align: 'center',
            }, {
                title: '操作',
                field: 'id',
                align: 'center',
                formatter: function (value, row) {
                    var e = '<a href="#" mce_href="#" onclick="edit(\'' + row.id + '\')">编辑</a> ';  //row.id为每行的id
                    var d = '<a href="#" mce_href="#" onclick="del(\'' + row.id + '\')">删除</a> ';
                    return e + d;
                }
            }
            ],
        });
    });


//返回刷新后的数据
     $('#send').click(function(){
         $.ajax({
             type: "GET",
             url: "/reload",
             data: {ROLL:$('#roll').val(), StartTime:$('#s_time').val(), EndTime:$('#e_time').val()},
             dataType: "json",
             success: function(data){
                 alert(JSON.stringify(data))
                console.log(JSON.stringify(data));
                 jsondata = JSON.stringify(data);
                // $("#table").bootstrapTable('refresh');
                $("#tabledata").bootstrapTable('load',data);
                             /*if (data={'data':'未搜索到数据'}){
                                 window.alert("未搜索到数据");
                             }
                             else {

                             }*/
                      }
         });
    });