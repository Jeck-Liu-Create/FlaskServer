 $("#sel_exportoption").change(function () {
        //刷新参数设置
        $('#tabledata').bootstrapTable('refreshOptions', {
            exportDataType: $(this).val()
        });
    });


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
    //时间初始化
    $(function(){

       $('#s_time').val(StartTime())
    });
    $(function(){

       $('#e_time').val(EndTime())
    });

    function updata() {
        console.log("Search_roll_nm="+$("#Search_roll_nm").val());
        var ROLL_NM = '';
        var str = $("#Search_roll_nm").val();
        if (str === '' || str === undefined || str == null) {
            //return true;
            console.log('空');
            ROLL_NM = 'null';
        } else {
            //return false;
            console.log('非空');
            ROLL_NM = str;
        }
	    $('#tabledata').bootstrapTable({
        url:'/reload_send_data',
        queryParams : function(params) {
				return {
					limit: params.limit,
					offset: params.offset,
	               // userName: $.trim( $('#userName').val() ) ,
	               // age: $.trim( $('#age').val() ) ,
                    ROLL:$('#roll').val(),
                    StartTime:$('#s_time').val(),
                    EndTime:$('#e_time').val(),
                    ROLLNM:ROLL_NM,
				}
			},
		toolbar:'#toolbox',
        fixedColumns: true,
        fixedNumber: 2,
        pagination: true, //前端处理分页
        singleSelect: false, //是否只能单选
        cache: true, //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
        pageNumber: 1, //初始化加载第10页，默认第一页
        pageSize: 10, //每页的记录行数（*）
        pageList: [5, 10, 20, 50, 100], //可供选择的每页的行数（*）
		clickToSelect:true,
		sortName: "create_time",
		sortOrder: "desc",
        showColumns: true, //显示内容列下拉框
        minimumCountColumns: 2, //当列数小于此值时，将隐藏内容列下拉框
        uniqueId: "id", //每一行的唯一标识，一般为主键列
        showToggle: true, //是否显示详细视图和列表视图的切换按钮
        cardView: false, //是否显示详细视图
       // queryParamsType:'limit',
        sidePagination: "server", //分页方式：client客户端分页，server服务端分页（*）
        showExport: true, //导出按钮
        exportDataType: "selected", //导出表格方式（默认basic：只导出当前页的表格数据；all：导出所有数据；selected：导出选中的数据）
        exportTypes: ['json', 'xml', 'csv', 'txt', 'sql', 'excel'], //导出文件类型
        exportOptions: {
            // 导出数据去除第一列出现"on"
            ignoreColumn: [0,1,28,32,33,34]
        },
		columns: [{
            //#0 选择
                checkbox: true,
                visible: true,
            },{
            //#1 序号
                field: 'send_time',
                title: '发送时间',
                align: 'center'
            },{
            //#2 序号
                field: 'number',
                title: '序号',
                align: 'center'
            }, {
            //#3 机架号
                field: 'c_frame_id',
                title: '机架号',
                align: 'center',
            }, {
            //#4 轧辊号
                field: 'c_roll_number',
                title: '辊号',
                align: 'center'
            }, {
            //#6 轧辊位置
                field: 'c_roll_position',
                title: '轧辊位置',
                align: 'center',
            }, {
            //#7 磨前直径
                field: 'c_diameter_before',
                title: '磨前直径',
                align: 'center',
            }, {
            //#8 磨后直径
                field: 'c_diameter',
                title: '磨后直径',
                align: 'center',
            }, {
            //#9 磨削量
                field: 'c_grinding_amount',
                title: '磨削量',
                align: 'center',
                visible: true,
            }, {
            //#10 曲线
                field: 'c_curve',
                title: '曲线',
                align: 'center',
            }, {
            //#11 凸度值 c_crown_value
                field: 'c_crown_value',
                title: '凸度值',
                align: 'center',
            }, {
            //#12 凸度正负标记
                field: 'c_crown_symbol',
                title: '凸度正负标记',
                align: 'center',
            }, {
            //#13 圆度
                field: 'c_roundness',
                title: '圆度',
                align: 'center',
            }, {
            //#14 圆柱度
                field: 'c_cylindricity',
                title: '圆柱度',
                align: 'center',
            }, {
            //#15 同轴度
                field: 'c_coaxiality',
                title: '同轴度',
                align: 'center',
            }, {
            //#16 粗糙度
                field: 'c_roughness',
                title: '粗糙度',
                align: 'center',
            }, {
            //#17 误差
                field: 'c_error',
                title: '误差',
                align: 'center',
            }, {
            //#19 磨削原因
                field: 'c_cause',
                title: '磨削原因',
                align: 'center',
            }, {
            //#20 探伤结果
                field: 'c_result_detection',
                title: '探伤结果',
                align: 'center',
            }, {
            //#5 配对轧辊号
                field: 'c_pairing_roll',
                title: '配对辊号',
                align: 'center'
            }, {
            //#21 日期
                field: 'c_date',
                title: '日期',
                align: 'center',
            }, {
            //#22 操作者
                field: 'c_operator',
                title: '操作者',
                align: 'center',
                visible: true,
            }, {
            //#23 砂轮直径
                field: 'c_wheel_diameter',
                title: '砂轮直径',
                align: 'center',
            }, {
            //#24 轧辊材质
                field: 'c_roll_material',
                title: '轧辊材质',
                align: 'center',
            }, {
            //#25 轧辊类型
                field: 'c_roll_type',
                title: '轧辊类型',
                align: 'center',
            }, {
            //#26 驱动侧轴承号
                field: 'c_drive_bearing',
                title: '驱动侧轴承号',
                align: 'center',
            }, {
            //#27 操作侧轴承号
                field: 'c_side_bearing',
                title: '操作侧轴承号',
                align: 'center',
            }, {
            //#28 开始时间
                field: 'c_start_time',
                title: '开始时间',
                align: 'center',
            }, {
            //#29 结束时间
                field: 'c_end_time',
                title: '结束时间',
                align: 'center',
            }, {
            //#30 磨床
                field: 'c_grinding_machine',
                title: '磨床',
                align: 'center',
                visible: false
            }, {
            //#31 锥形顶端直径
                field: 'c_top_diameter',
                title: '锥形顶端直径',
                align: 'center',
            }, {
            //#32 锥形底端直径
                field: 'c_low_diameter',
                title: '锥形底端直径',
                align: 'center',
            }, {
            //#33 实际凸度 c_actual_convexity
                field: 'c_actual_convexity',
                title: '实际凸度',
                align: 'center',
            }, {
            //#34 班次c_shift
                field: 'c_shift',
                title: '班次',
                align: 'center',
                visible: false
            }, {
            //#35 程序号c_program_number
                field: 'c_shift',
                title: '程序号',
                align: 'center',
                visible: false
            }, {
            //#36
                field: 'c_id',
                title: 'ID',
                visible:false,
                align: 'center',
        },{
            //#38
                field: 'c_woolification',
                title: '是否毛化标记',
                visible:false,
                align: 'center',
        }
        ],

    });

    }

    $(function (){updata()})
    //搜索按钮
    $('#send').click(function(){
        $("#tabledata").bootstrapTable('destroy');
        updata();

    });