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
        url:'/reload_uproll',
        queryParams : function(params) {
				return {
					limit: params.limit,
					offset: params.offset,
	               // userName: $.trim( $('#userName').val() ) ,
	               // age: $.trim( $('#age').val() ) ,
                    Franm_Id:$('#nav_frame_id').val(),
                    Roll_Type:$('#nav_roll_type').val(),
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
        pageList: [5, 10, 20, 50, 100, 200 ,500, 1000], //可供选择的每页的行数（*）
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
            ignoreColumn: [0,7]
        },
		columns: [{
            //#0 选择
                checkbox: true,
                visible: true,
            },{
            //#1 机架号
                title: '机架号',
                field: 'c_frame_id',
                align: 'center',
            },{
            //#2 轧辊类型
                field: 'c_roll_type',
                title: '轧辊类型',
                align: 'center'
            }, {
            //#3 轧辊号
                field: 'c_roll_number',
                title: '轧辊号',
                align: 'center',
            }, {
            //#4 卸辊时间
                field: 'c_down_time',
                title: '卸辊时间',
                align: 'center'
            }, {
            //#5 卸辊班号
                field: 'c_down_cless',
                title: '卸辊班号',
                align: 'center',
            }, {
            //#6 卸辊组号
                field: 'c_down_set',
                title: '卸辊组号',
                align: 'center',
            }, {
            //#7 ID
                field: 'id',
                title: 'ID',
                align: 'center',
                visible: false,
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

    $(function(){
       $('#s_time').val(StartTime())
    });
    $(function(){
       $('#e_time').val(EndTime())
    });